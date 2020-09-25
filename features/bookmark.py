from model.db import store_bookmark, get_bookmark, delete_bookmark

class Bookmark(object):
	"""docstring for Bookmark"""
	def __init__(self, url, name='New bookmark'):
		super(Bookmark, self).__init__()		
		self.name = name
		self.url = url


	def store(self):
		store_bookmark(self.name, self.url)

	def get(self):
		get_bookmark(self.name)

	def delete(self):
		delete_bookmark(self.id)


if __name__ == '__main__':
	qt = Bookmark('Overiq', 'https://overiq.com/sqlalchemy-101/crud-using-sqlalchemy-core/')