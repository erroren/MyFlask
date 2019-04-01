import pymysql


class MySqlHelper():
    def __init__(self, _database="goods", _host="localhost", _port=3306,
                 _user="root", _password="123456", _charset="utf8"):
        self.con = None
        self.cur = None
        try:
            self.con = pymysql.Connect(host=_host, user=_user, password=_password,
                                       database=_database, port=_port, charset=_charset)
            self.cur = self.con.cursor()
        except Exception as e:
            print(e)

    def select_db(self, db_name):
        self.con.select_db(db_name)

    def select_one(self, sql, args=None):
        try:
            self.cur.execute(sql, args)
            return self.cur.fetchone()
        except Exception as e:
            print("+++++")
            print(e)
        finally:
            self.close()

    def select_many(self, sql, args=None, n=0):
        try:
            self.cur.execute(sql, args)
            if n != 0:
                return self.cur.fetchmany(n)
            else:
                return self.cur.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.close()

    def update(self, sql, args=None):
        try:
            self.cur.execute(sql, args)
            self.con.commit()
            # return res
        except Exception as e:
            self.con.rollback()
            print(e)
        finally:
            self.close()

    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.con is not None:
            self.con.close()
