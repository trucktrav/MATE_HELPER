import sqlite3
from sqlite3 import Error
import os
import pandas as pd

sql_headers = 'SELECT DISTINCT header FROM Intermediates;'
pwd = os.path.abspath(os.path.dirname(__file__))
# database = pwd + '\\data\\mission\\test1\\metrics_database.db'
database = pwd + '\\metrics_database.db'
print(database)
db = sqlite3.connect(database)

inters = pd.read_sql(sql_headers, db)
head = inters.loc[:, 'header']

cur = db.cursor()
sql_c_header = 'CREATE table if not exists ' \
             'tbl_header(' \
             ' _id integer primary key,' \
             'header text ' \
             ');'

cur.execute(sql_c_header)
sql_getheaders = "select * from tbl_header;"
try:
    cur.execute(sql_getheaders)
except ValueError:
    pass
except Error as e:
    print(e)

rows = cur.fetchall()
if len(rows) == 0:
    print('create the header table')
    # need to populate the header table
    header = pd.read_sql(sql_headers, db)
    header.to_sql('tbl_header', db, if_exists='append', index_label='_id')

heads = pd.read_sql(sql_getheaders, db)