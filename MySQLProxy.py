import pymysql

# 1,支持with语句，封装数据库操作
# 2，暂时只需要实现每次调用创建链接
#   后续需要考虑数据库连接复用问题，提高效率
#   实现参考：DBUtils.PooledDB 或者自己按照功能实现一个
# 3,数据库的索引优化，需要通过sql文件或者python代码实现
class MySQLProxy:
    def __init__(self, host, user, password, database="", charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    def __enter__(self):
        if self.database == "":
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                charset=self.charset)
        else:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset)
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def __exit__(self, exc_type, exc_value, exc_trackback):
        if exc_trackback is None:
            print("[Exit]: MySQL Exited without exception.")
            self.cursor.close()
            self.conn.close()
        else:
            print("[Exit]: MySQl Exited with exception raised.")
        return False  # 可以省略，缺省的None也是被看做是False

