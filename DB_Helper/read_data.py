import sqlite3
from sqlite3 import Error
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pandas as pd
from DB_Helper.py_eval_helper import EvalHelp
from DB_Helper.pySelector import MateTypes
DEBUG_CREATE_EVAL = False


def create_eval_table(conn):
    """create the eval table, drops it first and deletes all the data

    Args:
        conn: connection to database

    Returns:
        nothing
    """
    sqld = 'DROP TABLE IF EXISTS tbl_eval;'
    sql = "CREATE TABLE IF NOT EXISTS tbl_eval " \
          "(_id INTEGER PRIMARY KEY NOT NULL," \
          " str_name TEXT NOT NULL," \
          " str_function TEXT," \
          " str_lst_header TEXT," \
          " str_display TEXT," \
          " int_type INTEGER);"
    sql_index = "CREATE UNIQUE INDEX idx_eval ON tbl_eval (_id, int_type);"

    cur = conn.cursor()
    cur.execute(sqld)
    conn.commit()
    conn.execute(sql)
    conn.commit()
    cur.execute(sql_index)
    conn.commit()


def get_atter(strname: str, db: sqlite3.connect):
    """gets the attribute from the database by selecting any rows from intermediates table
    that match strname,

    Args:
        strname - name of the attribute to retrieve

    Returns:
        dataframe: columns: engage_id, strname
    """
    sql = 'SELECT engagement_id, value as temp FROM Intermediates WHERE header = "{0}" ' \
          'order by engagement_id;'.format(strname)
    print("Read the {0} data".format(strname))
    ret = pd.read_sql(sql, db)
    # SQL wont allow the column name be the same as the filter, so rename the value column from temp to the right name
    ret = ret.rename(columns={"temp": strname})
    return ret


pwd = os.path.abspath(os.path.dirname(__file__))
file = pwd + '\\metrics_database.db'
con = sqlite3.connect(database=file)

engine = sqlalchemy.create_engine('sqlite:///{0}'.format(file))
Session = sessionmaker(bind=engine)
session = Session()

if DEBUG_CREATE_EVAL:
    print('drop and create eval table')
    create_eval_table(conn=con)
    sql = 'INSERT INTO tbl_eval (str_name, str_display, str_function, str_lst_header, int_type)' \
          ' SELECT header, header, "run_data[" || quote(header) || "]", header, {0}' \
          ' FROM tbl_header;'.format(MateTypes.HEADER.value)
    # sql = 'UPDATE tbl_eval SET str_type = "header"  WHERE _id >= 20';

    cur = con.cursor()
    cur.execute(sql)
    con.commit()
else:
    list = [MateTypes.INTERMEDIATE, MateTypes.ATTRIBUTE, MateTypes.EXPENSE]
    data = {MateTypes.INTERMEDIATE: None, MateTypes.ATTRIBUTE: None, MateTypes.EXPENSE: None}
    for elem in list:
        query = session.query(EvalHelp).filter_by(type=elem.value)
        for row in query:
            names = iter(row.header.split(sep=','))
            name = next(names)
            df = get_atter(strname=name, db=con)
            for name in names:
                df = df.merge(get_atter(strname=name, db=con), on=['engagement_id'])

            if data[elem] is None:
                data[elem] = df[['engagement_id']]

            data[elem][row.name] = eval(row.function, {'run_data': df})

    # query = session.query(EvalHelp).filter_by(type='intermediates')
    # for row in query:
    #     print('inter', row.function, row.header)
    #
    # query = session.query(EvalHelp).filter_by(type='attributes')
    # for row in query:
    #     print('attrs', row.function, row.header)

con.close()
session.close()
