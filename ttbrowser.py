import sys, os, re
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QApplication, 
    QPushButton, QLabel, QLineEdit, QTextEdit, QTreeView, QFileSystemModel, QGridLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import design

class TeamtoolBrowser(QWidget, design.Ui_Form):
    def __init__(self, parent=None):
        super(TeamtoolBrowser, self).__init__(parent)
        self.setupUi(self)
        self.browser = QWebEngineView()
        self.loadPage()
        self.initUI()
        self.eventUI()

    def eventUI(self):
        self.btnRefresh.clicked.connect(lambda: self.browse(refresh=True))
        self.btnGo.clicked.connect(lambda: self.browse())
        self.codeEdit.textChanged.connect(lambda: self.browse(offline=True))
        self.fileView.doubleClicked.connect(self.selectFile)
        self.searchBar.returnPressed.connect(lambda: self.browse())
        self.browser.loadStarted.connect(lambda: self.startLoading())
        self.browser.loadFinished.connect(lambda: self.onLoadingFinished())
        self.btnPrev.clicked.connect(lambda: self.prev())
        self.btnNext.clicked.connect(lambda: self.next())

    def startLoading(self):
        self.loadingAnimation.start()
        self.labelLoading.setVisible(True)

    def prev(self):
        self.browser.page().triggerAction(QWebEnginePage.Back)
        self.searchBar.setText(self.browser.url().toString())

    def next(self):
        self.browser.page().triggerAction(QWebEnginePage.Forward)
        self.searchBar.setText(self.browser.url().toString())

    def onLoadingFinished(self):
        self.loadingAnimation.stop()
        self.labelLoading.setVisible(False)

    def browse(self, refresh=False, offline=False):
        if offline:
            self.browser.setHtml(self.codeEdit.toPlainText())
            return
        if refresh:
            url = self.browser.url()
        else:
            url = self.searchBar.text()
            if not re.match('http://|https://', url, re.I):
                url = f'http://{url}'
        print(f'Browse to this URL: {url}')
        if isinstance(url, str) and url != '':
            if refresh:
                self.browser.setUrl(url)
            else:
                self.browser.setUrl(QtCore.QUrl(url))

    def selectFile(self, index):        
        if not self.fileModel.isDir(index) and index.data().lower().endswith(('.html', '.txt')):
            with open(self.fileModel.fileInfo(index).absoluteFilePath(), 'r', encoding='utf-8') as f:
                self.browser.setHtml(f.read())
        else:
            print('Can not read this file...')


    def initUI(self):
        self.browser = QWebEngineView()        
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

        self.searchBar.setPlaceholderText('Tapez ici votre URL')
        self.loadPage()        

        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('QWebEngineView')
        self.show()

    def loadPage(self):
        with open('home.html', 'r') as f:
            html = f.read()
            self.browser.setHtml(html)    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bro = TeamtoolBrowser()    
    sys.exit(app.exec_())