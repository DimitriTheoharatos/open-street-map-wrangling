import sqlite3
import csv
from pprint import pprint

#store database into a variable
db_file = "phoenix_az.db"


#connect to the database
db = sqlite3.connect(db_file)

#create a cursor object in order to interact with the database
c = db.cursor()

#if recreating the table, remove first if it currently exists 
c.execute('''DROP TABLE IF EXISTS node''')
c.execute('''DROP TABLE IF EXISTS node_tags''')
c.execute('''DROP TABLE IF EXISTS way''')
c.execute('''DROP TABLE IF EXISTS way_tags''')
c.execute('''DROP TABLE IF EXISTS way_nodes''')
db.commit()


### Create the framework for each of the tables to be inputted into the database

#---
#create node table
c.execute('''
    CREATE TABLE node(id INTEGER, lat NUMERIC, lon NUMERIC, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT)
''')
db.commit()

#create node_tags table
c.execute('''
    CREATE TABLE node_tags(id INTEGER, key TEXT, value TEXT, type TEXT)
''')
db.commit()

#create way table
c.execute('''
    CREATE TABLE way(id INTEGER, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT)
''')
db.commit()

#create way_tags table
c.execute('''
    CREATE TABLE way_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
db.commit()

#create way_nodes table
c.execute('''
    CREATE TABLE way_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
db.commit()

#---

# Read in the csv file as a dictionary, format the
# data as a list of tuples:

with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['lat'], i['lon'], i['user'].decode("utf-8"), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]
# insert the formatted data
c.executemany("INSERT INTO node(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?,?,?);", to_db)
# commit the changes
db.commit()

with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type']) for i in dr]
# insert the formatted data
c.executemany("INSERT INTO node_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
db.commit()

with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['user'].decode("utf-8"), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]
# insert the formatted data
c.executemany("INSERT INTO way(id, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?);", to_db)
# commit the changes
db.commit()

with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type']) for i in dr]
# insert the formatted data
c.executemany("INSERT INTO way_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
db.commit()

with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['node_id'],i['position']) for i in dr]

# insert the formatted data
c.executemany("INSERT INTO way_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)
# commit the changes
db.commit()



#c.execute('SELECT * FROM nodes_tags')
#all_rows = c.fetchall()
#print('1):')
#pprint(all_rows)

db.close()