import tkinter as tk
import sqlite3
from sqlite3 import Error
import os
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from DB_Helper.pySelector import ListType, MateTypes
import DB_Helper.pySelector as Selector


def get_header():
    sql_headers = 'SELECT header FROM tbl_header;'
    pwd = os.path.abspath(os.path.dirname(__file__))
    database = pwd + '\\metrics_database.db'
    db = sqlite3.connect(database)
    head = pd.read_sql(sql_headers, con=db)
    db.close()
    return head


def main():
    db = os.path.abspath(os.path.dirname(__file__)) + '\\metrics_database.db'
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db))
    Session = sessionmaker(bind=engine)
    session = Session()
    header = get_header()
    h_list = header['header'].tolist()
    create = {'calcs': ListType.CALCULATOR,
              'intermediates': ListType.SELECTOR,
              'attributes': ListType.SELECTOR,
              'expenses': ListType.SELECTOR}
    app = Selector.ListApp(create_list=create, session=session)
    app.mainloop()
    print('done')


if __name__ == "__main__":
    main()
