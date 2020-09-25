from model.db import store_bookmark, get_bookmark, delete_bookmark

class Bookmark(object):
	"""docstring for Bookmark"""
	def __init__(self, name=None, url=None):
		super(Bookmark, self).__init__()
		if name is not None:		
			self.name = name
		if url is not None:
			self.url = url


	def store(self):
		if self.name is None and self.url is None:
			return
		store_bookmark(self.name, self.url)

	@staticmethod
	def get_url_by_name(name):		
		url_record = get_bookmark(name)
		if isinstance(url_record, list) and len(url_record) > 0:
			return url_record[0].url
		return -1

if __name__ == '__main__':
	qt = Bookmark('Overiq', 'https://overiq.com/sqlalchemy-101/crud-using-sqlalchemy-core/')
	# qt.store()	
	print(Bookmark.get_url_by_name('Overiq'))