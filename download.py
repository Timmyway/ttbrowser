from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem

class DownloadManager(QWebEngineDownloadItem):
	"""docstring for DownloadManager"""
	def __init__(self, browser):
		super(DownloadManager, self).__init__()
		self.browser = browser
		self.config()

	def config(self):
		self.setDownloadDirectory('download')
		