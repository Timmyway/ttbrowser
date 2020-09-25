import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont, QKeySequence, QTextCursor, QTextDocument, QTextOption, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QGridLayout, QHBoxLayout, QPushButton, QLineEdit, \
QSplitter, QListWidget, QSizePolicy, QCheckBox, QLabel
import re
import random
from string import hexdigits
# CUSTOM IMPORT :
from highlighter import ColorSyntaxHTML # pour coloration syntaxique SQL
 
#############################################################################
class CustomTextEditor(QWidget):
 
	def __init__(self, parent=None, txtInput=None):
		super(CustomTextEditor, self).__init__(parent)        
		# met en place la coloration syntaxique
		if txtInput is None:
			self.txtInput = QTextEdit()
		else:
			self.txtInput = txtInput
		self.txtOutput = QTextEdit()
		# Search/Replace buttons :
		self.btnSearch = QPushButton('Search')
		self.btnReplaceAll = QPushButton('Replace all')
		self.btnQuickSearchImages = QPushButton('I')
		self.btnQuickSearchLinks = QPushButton('L')
		# self.btnClear = QPushButton('Clear')
		self.chkCaseSensitivity = QCheckBox('Case sensitive')
		# Line edit to search and replace :
		self.formSearch = QLineEdit()
		self.formReplace = QLineEdit()
		# Labels :
		self.labelCount = QLabel()
		self.labNotif = QLabel('')
		# List widget :
		self.listFound = QListWidget()
		# --------------------------------------
		self.mainLayout = QGridLayout()
		self.splitVLayout = QSplitter(QtCore.Qt.Vertical)
		self.layoutCommand = QGridLayout()
		# Syntax highlighting :
		self.colorSyntaxHtml = ColorSyntaxHTML(self.txtInput.document())        
		self.hotkey = {}
		self.bind_key('actionSearch', 'Ctrl+F', lambda: self.on_ctrl_f_pushed(self.formSearch, self.txtInput))
		self.bind_key('actionSearchOnReturnPress', 'Return', lambda: self.search_and_replace(), widget=self.formSearch)
		self.bind_key('actionSearchOnEnterPress', 'Enter', lambda: self.search_and_replace(), widget=self.formSearch)
		self.config()

	def set_size_policy(self, widget, hpolicy=QSizePolicy.Expanding, vpolicy=QSizePolicy.Expanding):
		policy = QSizePolicy(hpolicy, vpolicy)
		policy.setHorizontalStretch(0)
		policy.setVerticalStretch(0)
		widget.setSizePolicy(policy)

	def config(self):		
		# ---------- SET STYLES ----------------------------------------
		self.setAutoFillBackground(True)
		pal = self.palette()
		pal.setColor(self.backgroundRole(), QColor('#7FD1B9'))
		self.setPalette(pal)
		self.setStyleSheet('''QTextEdit {
			margin-right: 5px;
			background: #ffffff; color: black;
			border-radius: 4px; border: 0px solid #CBC9D2;
			selection-background-color: #ffa500;
		}
		QTextEdit:hover {
			background: #ffffff;
		}
		QListWidget {
			background: #ffffff; color: black;
		}
		QCheckBox, QLabel {
			color: #000000;
			font-size: 14px;
		}
		QPushButton {
			background: #333333; color: #ffffff;
			border-width: 2px; border-radius: 4px;
			width: 100px;
			padding: 4px;
			font-size: 13px;
		}
		QSplitter {
			background: transparent;
		}
		QPushButton:hover {
			border: 2px solid #FFFFFF;
		}
		''')
		style_btn_mini = ''' width: 20px; height: 20px; 
		border-radius: 8px;
		background-color: {bgcolor}; color: {color};		
		'''
		self.btnQuickSearchImages.setStyleSheet(style_btn_mini.format(bgcolor='#1e90ff', 
			color='#ffffff'))
		self.btnQuickSearchLinks.setStyleSheet(style_btn_mini.format(bgcolor='#ff4500', 
			color='#ffffff'))
		# ----------------------------------------------------------------		
		self.setLayout(self.mainLayout)
		self.layoutCommand.addWidget(self.btnSearch, 0, 0)
		self.layoutCommand.addWidget(self.btnQuickSearchImages, 0, 1)		
		self.layoutCommand.addWidget(self.btnReplaceAll, 1, 0)
		self.layoutCommand.addWidget(self.btnQuickSearchLinks, 1, 1)
		self.layoutCommand.addWidget(self.formSearch, 0, 2)
		self.layoutCommand.addWidget(self.formReplace, 1, 2)
		# self.layoutCommand.addWidget(self.btnClear, 0, 2)
		self.layoutCommand.addWidget(self.labelCount, 0, 3)
		self.layoutCommand.addWidget(self.labNotif, 1, 4)
		self.layoutCommand.addWidget(self.chkCaseSensitivity, 1, 3)
		self.mainLayout.addLayout(self.layoutCommand, 0, 0)
		self.splitVLayout.addWidget(self.txtInput)		
		self.splitVLayout.addWidget(self.listFound)
		self.mainLayout.addWidget(self.splitVLayout, 2, 0, 1, 3)		
		self.splitVLayout.setHandleWidth(6)
		self.splitVLayout.setSizes([200, 40])
		# TEXT WIDGET CONFIG :
		# Set fonts :
		font = QFont()
		font.setFamily("DejaVu Sans Mono")
		font.setStyleHint(QFont.Courier)
		font.setPointSize(10)
		self.txtInput.setFont(font)
		self.txtInput.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
		# ---------- SIGNAL CONNECTION ----------------------------------------
		self.btnSearch.clicked.connect(lambda: self.search_and_replace())
		# self.btnClear.clicked.connect(lambda: self.wash(self.txtInput))        
		self.btnReplaceAll.clicked.connect(lambda: self.search_and_replace(replace=True))
		self.listFound.itemDoubleClicked.connect(lambda: self.find_on_text(self.listFound.currentItem().text()))
		self.btnQuickSearchImages.clicked.connect(lambda: self.search_and_replace(pattern='src'))
		self.btnQuickSearchLinks.clicked.connect(lambda: self.search_and_replace(pattern='href'))
		# ---------- SET POLICY ----------------------------------------
		self.set_size_policy(self.formSearch, QSizePolicy.Expanding, QSizePolicy.Maximum)
		self.set_size_policy(self.formReplace, QSizePolicy.Expanding, QSizePolicy.Maximum)
		self.set_size_policy(self.btnSearch, QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.set_size_policy(self.btnReplaceAll, QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.set_size_policy(self.btnQuickSearchImages, QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.set_size_policy(self.btnQuickSearchLinks, QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.set_size_policy(self.txtInput, QSizePolicy.Expanding, QSizePolicy.Expanding)
		# Set listWidget cursor shape :
		self.listFound.setCursor(QtCore.Qt.IBeamCursor)

	def wash(self, text_edit):		
		text_edit.clear()		
		self.labelCount.setText('')
		self.listFound.clear()

	def on_ctrl_f_pushed(self, source_form, text_edit):
		text = self.current_selection(text_edit)
		source_form.clear()
		source_form.setText(text)

	def current_selection(self, text_edit):
		cursor = text_edit.textCursor()
		return cursor.selectedText()

	def bind_key(self, key_name, key_combo, func, widget=None):
		if not widget:
			widget = self
		self.hotkey[key_name] = QtWidgets.QShortcut(QKeySequence(key_combo), widget)
		self.hotkey[key_name].activated.connect(func)	
	 
	def search_and_replace(self, replace=False, pattern=None):
		print('Search and replace function activated')
		to_search = self.formSearch.text()
		if pattern:
			to_search = pattern
		replace_with = self.formReplace.text()
		text = self.txtInput.toPlainText()
		pattern = re.escape(to_search)
		if to_search == '':
			return
		# REPLACE BLOCK ----------------------------------------------------------
		if replace:
			print('Replace now :')			
			self.txtInput.clear()
			if self.chkCaseSensitivity.isChecked():
				text = re.sub(pattern, replace_with, text)
			else:
				text = re.sub(pattern, replace_with, text, flags=re.IGNORECASE)
			self.txtInput.insertPlainText(text)
			print('Updating label value')
			self.update_label(self.labNotif, '')
		# SEARCH ONLY ------------------------------------------------------------
		else:
			print('Search only :')
			if self.chkCaseSensitivity.isChecked(): # Check if case sensitive checkbox is checked
				matches = re.findall(pattern + r'.*', text)
			else:
				matches = re.findall(pattern + r'.*', text, re.IGNORECASE)
			if matches:
				# If there is any item matches :
				self.listFound.clear() # Clear the found listWidget
				[self.listFound.addItem(match) for match in matches]
				self.labelCount.setText('<span style="color: #64ca77;">%s items found</span>' % len(matches))
				print('Updating label value')
				self.update_label(self.labNotif, '')
			else:
				# If no matches :				
				self.labelCount.setText('<span style="color: red;">No item found</span>')
				self.listFound.clear()
				self.listFound.addItem('No item found...')
				return None 

	def detect_bads(self):
		fr = re.findall(r'\.fr', self.txtInput.toPlainText())
		com = re.findall(r'\.com', self.txtInput.toPlainText())
		pixel = re.findall(r'<img.*?width="1".*?>{1}|<img.*?height="1".*?>{1}', self.txtInput.toPlainText())
		bads = [x for x in (fr + com + pixel) if x is not None]
		print('Bads :', bads)

	def find_on_text(self, pattern):
		print('Find on text')
		# self.txtInput.moveCursor(QTextCursor.Start)                
		found = self.txtInput.find(pattern)
		if not found:
			found = self.txtInput.find(self.listFound.currentItem().text(), QTextDocument.FindBackward)		
		# self.txtInput.moveCursor(QTextCursor.Start)

	def update_label(self, label, text=''):
		if isinstance(label, QLabel):
			old_color = label.palette().color(QPalette.Background).name()
			print(old_color)			
			pick = '#%s' % ''.join([random.choice(hexdigits) for i in range(6)])			
			while pick.lower() == old_color.lower():
				pick = '#%s' % ''.join([random.choice(hexdigits) for i in range(6)])				
			label.clear()
			label.setText(text)
			label.setFixedWidth(15)
			label.setFixedHeight(15)
			label.setStyleSheet('background: %s' % pick)

class TxtInput(QTextEdit):
	"""docstring for CustomTextEditor"""
	def __init__(self, widgets, parent=None):
		super(TxtInput, self).__init__()
		self.widgets = widgets
		self.parent = parent
		self.LineWrapMode(QTextEdit.WidgetWidth)

	def focusInEvent(self, event):        
		self.hide_widgets_around()
		QTextEdit.focusInEvent(self, event)

	def dropEvent(self, event):		
		if event.mimeData().hasText():
			# Strip the file:/// from the beginning. We want a path--not URL
			file_path = event.mimeData().text()
			print(file_path)
			with open(file_path.lstrip("file:///"), encoding='utf-8') as f:
				self.insertPlainText(f.read())

	def insertFromMimeData(self, source):
		if source.hasText():
			self.insertPlainText(source.text())
		else:
			QTextEdit().insertFromMimeData(source)

	# def focusOutEvent(self, event):
	#     self.show_widgets_around()
	#     QTextEdit.focusOutEvent(self, event)

	# def keyPressEvent(self, event):
	#     if event.key() == QtCore.Qt.Key_Escape:
	#         print('Escape pressed !')            
	#     else:
	#         QTextEdit.keyPressEvent(self, event)

	def hide_widgets_around(self):
		[widget.hide() for widget in self.widgets]

	def show_widgets_around(self):
		[widget.show() for widget in self.widgets]
		

 
#############################################################################
if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = QWidget()
	editor = TxtInput([QPushButton('Hello'), QPushButton('World')])
	txt = CustomTextEditor(txtInput=editor)
	layout = QHBoxLayout()
	layout.addWidget(txt)
	w.setLayout(layout)    
	w.show()
	sys.exit(app.exec_())