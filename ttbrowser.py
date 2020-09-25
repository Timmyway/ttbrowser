import sys, os, re
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QApplication, 
    QPushButton, QLabel, QLineEdit, QTextEdit, QTreeView, QFileSystemModel, QGridLayout,
    QPlainTextEdit
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
import design
from custom_editor import TxtInput, CustomTextEditor

class TeamtoolBrowser(QWidget, design.Ui_Form):
    def __init__(self, parent=None):
        super(TeamtoolBrowser, self).__init__(parent)
        self.setupUi(self)
        self.browser = QWebEngineView()
        self.profile = QWebEngineProfile("somestorage", self.browser)
        self.webpage = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.webpage)
        self.initUI()
        self.eventUI()

    def eventUI(self):
        self.btnRefresh.clicked.connect(lambda: self.browse(refresh=True))
        self.codeEdit.textChanged.connect(lambda: self.browse(offline=True))
        self.fileView.doubleClicked.connect(self.selectFile)
        self.urlBar.returnPressed.connect(lambda: self.browse())
        self.webpage.loadStarted.connect(lambda: self.startLoading())
        self.webpage.loadFinished.connect(lambda: self.onLoadFinished())
        self.btnPrev.clicked.connect(lambda: self.prev())
        self.btnNext.clicked.connect(lambda: self.next())    

    def prev(self):
        ''' History: go back '''
        self.webpage.page().triggerAction(QWebEnginePage.Back)
        self.urlBar.setText(self.webpage.url().toString())

    def next(self):
        ''' History: move forward '''
        self.webpage.page().triggerAction(QWebEnginePage.Forward)
        self.urlBar.setText(self.webpage.url().toString())

    def startLoading(self):
        ''' When page starts to load '''
        self.loadingAnimation.start()
        self.labelLoading.setVisible(True)

    def onLoadFinished(self):
        ''' When page has finished to load '''
        self.loadingAnimation.stop()
        self.labelLoading.setVisible(False)

        if self.webpage.history().canGoBack():
            self.btnPrev.setEnabled(True)
        else:
            self.btnPrev.setEnabled(False)

        if self.webpage.history().canGoForward():
            self.btnNext.setEnabled(True)
        else:
            self.btnNext.setEnabled(False)
        self.urlBar.setText(self.webpage.url().toString())

    def browse(self, refresh=False, offline=False):
        ''' Browse to urlBar URL or render a text/html string '''

        # Offline mode, load plaintext html code
        if offline:
            self.webpage.setHtml(self.codeEdit.toPlainText())
            return
        # Online mode
        if refresh:
            url = self.browser.reload()
            return        
        url = self.urlBar.text()
        if not re.match('http://|https://', url, re.I):
            url = f'http://{url}'
        # print('===============>', os.path.join('statics/button', 'lock-ssl.png'), QUrl(url).scheme())
        if QUrl(url).scheme() == 'https':
            print('HTTPS')
            self.httpsicon.setPixmap(self.pixmap_ssl)                
        else:
            print('HTTP')
            self.httpsicon.setPixmap(self.pixmap_nossl)
        print(f'Browse to this URL: {url}')
        if isinstance(url, str) and url != '':            
            self.webpage.setUrl(QUrl(url))            

    def selectFile(self, index):
        ''' Select a file in file system '''
        if not self.fileModel.isDir(index) and index.data().lower().endswith(('.html', '.txt')):
            with open(self.fileModel.fileInfo(index).absoluteFilePath(), 'r', encoding='utf-8') as f:
                self.webpage.setHtml(f.read())
        else:
            print('Can not read this file...')


    def initUI(self):
        ''' Configuration of widgets '''
        self.gLayoutBrowser.addWidget(self.browser)        
        self.loadingAnimation = QMovie('loading.gif')
        self.loadingAnimation.setScaledSize(QtCore.QSize(24, 24))
        self.labelLoading.setMovie(self.loadingAnimation)
        self.labelLoading.setVisible(False)

        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(QtCore.QDir.currentPath())        
        self.fileView.setModel(self.fileModel)
        self.fileModel.setNameFilters(('.html', '.txt'))
        self.fileView.setColumnWidth(0, 170)
        self.fileView.setColumnWidth(1, 50)
        self.fileView.setColumnWidth(2, 50)

        self.splitterMain.setStretchFactor(1, 3)
        self.splitterSidebar.setStretchFactor(0, 1)

        self.urlBar.setPlaceholderText('Tapez ici votre URL')
        self.loadPage(online=True)
        self.pixmap_ssl = QPixmap(os.path.join('static/button', 'lock-ssl.png'))
        self.pixmap_nossl = QPixmap(os.path.join('static/button', 'lock-nossl.png'))        
        print(f'w: {self.pixmap_ssl.width()} | h: {self.pixmap_ssl.height()}')        
        self.httpsicon.setPixmap(self.pixmap_nossl)        

        self.setGeometry(300, 300, 1280, 720)
        self.updateTitle()

        # self.codeEdit = TxtInput([QPushButton('Hello'), QPushButton('World')])
        # self.editor = CustomTextEditor(txtInput=self.codeEdit)
        self.codeEdit = QPlainTextEdit()
        self.splitterSidebar.addWidget(self.codeEdit)

        self.show()        


    def loadPage(self, online=True):
        ''' Load home page '''
        if online:
            self.browser.setUrl( QUrl("https://www.google.com") )
            return
        with open('home.html', 'r') as f:
            html = f.read()
            self.browser.setHtml(html)

    def updateTitle(self):
        title = self.browser.page().title()
        self.setWindowTitle(f'{title}')


class WebView(QWebEngineView):
    """docstring for WebView"""
    def __init__(self, arg):
        super(WebView, self).__init__()
        self.arg = arg
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bro = TeamtoolBrowser()
    sys.exit(app.exec_())