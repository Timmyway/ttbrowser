import sqlalchemy
from sqlalchemy import (create_engine, MetaData, 
	Table, String, Column, Text, DateTime, Integer, 
	select, Index, asc
)

print(sqlalchemy.__version__)

# Create engine
# engine = create_engine('sqlite:///model/cp.db')
engine = create_engine('sqlite:///model/bookmark.db')

metadata = MetaData()

bookmark = Table('bookmark', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255)),
	Column('url', Text()),
	Column('folder', String(2000)),
)

metadata.create_all(engine)

def store_bookmark(name, url, folder=''):
	print('Store bookmark with name: ', name)
	ins = bookmark.insert().values(
		name=name, 
		url=url, 
		folder=folder
	)
	print(ins)
	conn = engine.connect()
	return conn.execute(ins)

def get_bookmark(name, url=None):	
	sel = select([bookmark]
		).where(
			bookmark.c.name == name
		).distinct()
	print(sel)
	conn = engine.connect()
	try:
		return conn.execute(sel).fetchall()
	except sqlalchemy.exc.InterfaceError as e:
		print(e)
		return -1

def delete_bookmark(name):
	d = delete(bookmark
		).where(
			bookmark.c.name == name
		)
	print(sel)
	conn = engine.connect()
	return conn.execute(d).fetchall()