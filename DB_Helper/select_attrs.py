import tkinter as tk
import sqlite3
from sqlite3 import Error
import os
import pandas as pd
import pySelector


def get_header():
    sql_headers = 'SELECT header FROM tbl_header;'
    pwd = os.path.abspath(os.path.dirname(__file__))
    database = pwd + '\\metrics_database.db'
    db = sqlite3.connect(database)
    head = pd.read_sql(sql_headers, con=db)
    return head


def main():
    header = get_header()
    h_list = header['header'].tolist()
    app = pySelector.ListApp()
    data = {'intermediates': h_list, 'attributes': h_list, 'calcs': h_list}
    app.set_data(list_data=data)
    app.mainloop()
    print('done')


if __name__ == "__main__":
    main()
