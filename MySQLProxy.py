import pymysql
from DBUtils.PooledDB import PooledDB
from config import Config

# 1,支持with语句，封装数据库操作
# 2，暂时只需要实现每次调用创建链接
#   后续需要考虑数据库连接复用问题，提高效率
#   实现参考：DBUtils.PooledDB 或者自己按照功能实现一个
# 3,数据库的索引优化，需要通过sql文件或者python代码实现
# 暂时只会有一个连接可能，所以不考虑扩展性了
class MySQLProxy:
    def __enter__(self):
        if not hasattr(MySQLProxy, "pool"):
            Config.ReadConfig()
            MySQLProxy.pool = PooledDB(pymysql, 0, 5, blocking=True,
                                       host=Config.host,
                                       user=Config.user,
                                       password=Config.password,
                                       database=Config.database,
                                       charset=Config.charset)
        MySQLProxy.conn = MySQLProxy.pool.connection()
        MySQLProxy.cursor = MySQLProxy.conn.cursor()
        return MySQLProxy.conn, MySQLProxy.cursor

    def __exit__(self, exc_type, exc_value, exc_trackback):
        if exc_trackback is None:
            print("[Exit]: MySQL Exited without exception.")
            MySQLProxy.cursor.close()
            MySQLProxy.conn.close()
        else:
            print("[Exit]: MySQl Exited with exception raised.")
        return False  # 可以省略，缺省的None也是被看做是False

