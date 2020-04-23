import sqlite3
import pandas as pd


class SafeEval(object):
    """"""

    def __init__(self, database, eval_type):
        """Constructor for SafeEval
        @type database: str
        """
        self._database = database
        # self.conn = sqlite3.connect(database=database)
        # self.cur = self.conn.cursor()
        self._eval_type = eval_type
        self._lst_eval = pd.DataFrame
        self.load_data(database, eval_type)

    def load_data(self, database: str, eval_type: str) -> bool:
        """loads the SafeEval data from the connection provided

        Args:
            database - location of the db to read
            eval_type - type of evaluations to load

        Returns:
            success
        """
        success = True
        sql = "CREATE TABLE IF NOT EXISTS tbl_eval " \
              "(_id INTEGER PRIMARY KEY NOT NULL," \
              " str_name TEXT NOT NULL," \
              " str_function TEXT," \
              " str_display TEXT," \
              " str_type TEXT);"
        sql_index = "CREATE UNIQUE INDEX idx_eval ON tbl_eval (_id, str_type);"

        if database != self._database:
            self._database = database
        conn = sqlite3.connect(database=database)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        sql = 'SELECT * FROM sqlite_master WHERE tbl_name = "{0}" AND type = "{1}";'.format('tbl_eval', 'index')
        # if len(cur.execute(sql).fetchall()) <= 0:
        #     cur.execute(sql_index)
        #     conn.commit()

        sql = "SELECT * FROM tbl_eval WHERE str_type = '{0}';".format(eval_type)
        self._lst_eval = pd.read_sql(sql=sql, con=conn)

        conn.close()

        return success

    def save_data(self):
        """save the current data to the associated database

        Args:none


        Returns:
            success
        """
        x, y = self._lst_eval.shape
        if x == 0 or y == 0:
            return False

        success = True
        conn = sqlite3.connect(database=self._database)
        cur = conn.cursor()
        r, c = self._lst_eval.shape
        for i in range(r):
            temp = self._lst_eval.iloc[[i], :]
            try:
                sql = "UPDATE tbl_eval SET " \
                      "_id = {4}, str_name = '{0}', str_function = '{1}', str_display = '{2}', str_type = '{3}'" \
                      " WHERE _id = {4} AND str_type = '{3}';".format(temp['str_name'][0],
                                                                      temp['str_function'][0],
                                                                      temp['str_display'][0],
                                                                      temp['str_type'][0],
                                                                      temp['_id'][0])
                print(sql)
                cur.execute(sql)
            except sqlite3.OperationalError:
                print('error')
                temp.to_sql(name='tbl_eval', con=conn, if_exists='append',
                            index=False)
                            # , index_label=['_id', 'str_type'])
# print('update {0}'.format(sql))
            else:
                print('error')
                pass
            finally:
                pass
        # self._lst_eval.to_sql(name='tbl_eval', con=conn, if_exists='fail',
        #                       index=True, index_label=['_id', 'str_type'])
        conn.close()

        return success

    def add_eval(self, name: str, function: str = "", display: str = "", set_id: int = 0):
        """adds an eval item to the list

        Args:

        Returns:
            success
            @param set_id:
            @type name: str
            @param function: str
            @param display:
        """
        success = True
        # TODO add safe add check before the append
        if function == "":
            function = name
        if display == "":
            display = name
        temp = {'str_name': name, 'str_function': function, 'str_display': display}
        temp = pd.DataFrame(temp, index=[0])
        temp['str_type'] = self._eval_type
        temp['_id'] = len(self._lst_eval.index) if set_id == 0 else set_id

        self._lst_eval = self._lst_eval.append(other=temp, ignore_index=True)
        return success

    def get_list(self, column='none'):
        """get the _lst_eval

        Args:
            column='none'

        Returns:
            return the dataframe if no column, otherwise return the column
        """
        if column == 'none':
            return self._lst_eval
        else:
            return self._lst_eval[column]
