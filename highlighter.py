from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl, QRegularExpression
from PyQt5.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt5.QtWidgets import QMessageBox
import os
import sys

class ColorSyntaxHTML(QSyntaxHighlighter):
 
	#========================================================================
	def __init__(self, parent=None, mistakes_words=[]):
		super(ColorSyntaxHTML, self).__init__(parent)
 
		# List of rules : [[regex, format], [regex, format], ...]
		self.regles = []
		#--------------------------------------------------------------------		
		# KEYWORDS FORMAT :	
		keyword_format = QTextCharFormat()
		keyword_format.setForeground(QColor('#FF5300')) # mots clés en bleu
		keyword_format.setFontWeight(QFont.Bold) # pour mise en gras
		# ATTRIBUTS FORMAT :
		attribute_format = QTextCharFormat()
		attribute_format.setForeground(QColor('#0289A2')) # mots clés en bleu
		attribute_format.setFontWeight(QFont.Bold)		
		# ATTRIBUTES VALUES FORMAT :
		value_format = QTextCharFormat()
		value_format.setForeground(QColor('#600492')) # mots clés en bleu
		value_format.setFontWeight(QFont.Bold)
		# FORBIDDEN FORMAT :
		forbidden_format = QTextCharFormat()
		forbidden_format.setForeground(QtCore.Qt.red) # mots clés en bleu
		forbidden_format.setFontWeight(QFont.Bold)
		#--------------------------------------------------------------------
		# COMENTS :
		coment_format = QTextCharFormat()
		coment_format.setForeground(QtCore.Qt.green) # mots clés en bleu		
		#--------------------------------------------------------------------
		# VERIFICATION :
		verif_format = QTextCharFormat()
		verif_format.setForeground(QColor('#4169e1')) # mots clés en bleu
		verif_format.setFontWeight(QFont.Bold)
		#--------------------------------------------------------------------	

		# NUMBER :
		nombre_format = QTextCharFormat()
		nombre_format.setForeground(QtCore.Qt.darkGreen)
		nombre_motif =  r"\\b[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\\b"
		nombre_regex = QRegularExpression(nombre_motif)		
		self.regles.append([nombre_regex, nombre_format])
		# --------------------------------------------------------------------
		# spellcheck :
		mistake_format = QTextCharFormat()
		mistake_format.setForeground(QColor('#ff2222'))		

		# --------------------------------------------------------------------
		keyword_motifs = ['HTML', 'abbr', 'acronym', 'address', 'a', 'applet', 'area', 'b', 
		'base', 'basefont', 'bdo', 'bgsound', 'big', 'blink', 'blockquote', 'body', 'br', 'button', 
		'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'commment', 'dd', 'del', 'dfn', 'dir', 
		'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'font', 'form', 'frame', 'frameset', 'h1', 'h2', 
		'h3', 'h4', 'h5', 'h6', 'head', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 
		'kbd', 'label', 'layer', 'legend', 'li', 'link', 'map', 'marquee', 'menu', 'meta', 'nextid', 
		'nobr', 'noembed', 'noframes', 'noscript', 'object', 'ol', 'option', 'p', 'param', 'pre', 'q', 
		's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'style', 'sub', 'sup', 
		'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'title', 'tr', 'tt', 'u', 'ul', 
		'var', 'wbr', 'xmp']
		# Save setting to the rules :
		for keyword_motif in keyword_motifs:
			keyword_regex = QRegularExpression(r'<' + keyword_motif, QRegularExpression.CaseInsensitiveOption)
			self.regles.append([keyword_regex, keyword_format])
		# for keyword_motif in keyword_motifs:
		# 	keyword_regex = QRegularExpression(keyword_motif + r'.*?([/"\']>)', QRegularExpression.CaseInsensitiveOption)
		# 	self.regles.append([keyword_regex, keyword_format])		
		# for keyword_motif in keyword_motifs:
		# 	keyword_regex = QRegularExpression(keyword_motif + r'>', QRegularExpression.CaseInsensitiveOption)
		# 	self.regles.append([keyword_regex, keyword_format])		
		for keyword_motif in keyword_motifs:
			keyword_regex = QRegularExpression(r'(</' + keyword_motif + r'\s*?>)', QRegularExpression.CaseInsensitiveOption)
			self.regles.append([keyword_regex, keyword_format])		
		# --------------------------------------------------------------------


		# --------------------------------------------------------------------
		attribute_motifs = ['accept', 'accept-charset', 'accesskey', 'action', 'align', 'alt', 'async', 
		'autocapitalize', 'autofocus', 'autocomplete', 'autoplay', 'bgcolor', 'border', 'buffered', 'challenge', 
		'charset', 'checked', 'cite', 'class', 'code', 'codebase', 'color', 'cols', 'colspan', 'content', 
		'contenteditable', 'contextmenu', 'controls', 'coords', 'crossorigin', 'data', 'data-*', 'datetime', 'default', 
		'defer', 'dir', 'dirname', 'disabled', 'download', 'draggable', 'dropzone', 'enctype', 'for', 'form', 
		'formaction', 'headers', 'height', 'hidden', 'high', 'href', 'hreflang', 'http-equiv', 'icon', 'id', 
		'integrity', 'ismap', 'itemprop', 'keytype', 'kind', 'label', 'lang', 'language', 'list', 'loop', 'low', 
		'manifest', 'max', 'maxlength', 'media', 'method', 'min', 'minlength', 'multiple', 'muted', 'name', 'novalidate', 
		'open', 'optimum', 'pattern', 'ping', 'placeholder', 'played', 'poster', 'preload', 'radiogroup', 'readonly', 
		'rel', 'required', 'reversed', 'rows', 'rowspan', 'sandbox', 'scope', 'scoped', 'selected', 'shape', 
		'size', 'sizes', 'slot', 'span', 'spellcheck', 'src', 'srcdoc', 'srclang', 'srcset', 'start', 'step', 
		'style', 'summary', 'tabindex', 'target', 'title', 'translate', 'type', 'usemap', 'value', 'width', 'wrap',
		'cellpadding', 'cellspacing', 'face', 'valign']
		# Save the rules :
		for attr_motif in attribute_motifs:
			r = attr_motif + r'=([\'"]{1}.*?[\'"]){1}'			
			value_regex = QRegularExpression(r, QRegularExpression.CaseInsensitiveOption)
			self.regles.append([value_regex, value_format])
		# ---------------------------------------------------------------------------------	
		# Save the rules :
		for attribute_motif in attribute_motifs:
			attribute_regex = QRegularExpression('(%s)=' % attribute_motif, QRegularExpression.CaseInsensitiveOption)
			self.regles.append([attribute_regex, attribute_format])	
		# --------------------------------------------------------------------				
		coment_regex = QRegularExpression(r'<!--.*-->', QRegularExpression.CaseInsensitiveOption | QRegularExpression.MultilineOption)
		self.regles.append([coment_regex, coment_format])
		# --------------------------------------------------------------------
		self.verif_motifs = ['*[subscriber_firstname_capitalized]*', '*[subscriber_lastname_capitalized]*', '*[subscriber_attribute_zipcode]*',
		'*[subscriber_attribute_civility]*', '*[subscriber_email]*', 'images.promoenexclu.eu', 'ls.promoenexclu.eu', 'images.enviedbonsplans.eu', 
		'ls.enviedbonsplans.eu', 'images.lagendadesventesprivees.eu', 'ls.lagendadesventesprivees.eu']
		for verif_motif in self.verif_motifs:
			verif_regex = QRegularExpression(QRegularExpression.escape(verif_motif), QRegularExpression.CaseInsensitiveOption)
			self.regles.append([verif_regex, verif_format])	
		# --------------------------------------------------------------------
		mistake_motifs = ['courrir', 'nourir']
		print('Mistakes motifs :', list(mistake_motifs))
		for mistake_motif in mistake_motifs:
			mistake_regex = QRegularExpression(r'\b' + mistake_motif + r'\b')
			self.regles.append([mistake_regex, mistake_format])	
	#========================================================================

	def highlightBlock(self, text):
		"""analyse chaque ligne et applique les règles""" 		
		# analyse des lignes avec les règles		
		for expression, tformat in self.regles:
			match_iterator = expression.globalMatch(text)
			while match_iterator.hasNext():
				match = match_iterator.next()
				self.setFormat(match.capturedStart(), match.capturedLength(), tformat)			
		self.setCurrentBlockState(0)