from config import Config
import MySQLProxy

class DatabaseSetup:
    def __init__(self):
        Config.ReadConfig()

    def ProceeAction(self):
        with MySQLProxy.MySQLProxy(host=Config.host, user=Config.user, password=Config.password,
                                   charset=Config.charset) as (conn, cursor):
            self.ExecuteSQLFile('DatabaseSetup.sql', cursor)

    def ExecuteSQLFile(self, filepath, cursor):
        with open(filepath, encoding='utf-8', mode='r') as f:
            # 读取整个sql文件，以分号切割。[:-1]删除最后一个元素，也就是空字符串
            sql_list = f.read().split(';')[:-1]
            for x in sql_list:
                # 判断包含空行的
                if '\n' in x:
                    # 替换空行为1个空格
                    x = x.replace('\n', ' ')

                # 判断多个空格时
                if '    ' in x:
                    # 替换为空
                    x = x.replace('    ', '')

                # sql语句添加分号结尾
                sql_item = x + ';'
                # print(sql_item)
                cursor.execute(sql_item)
                print("执行成功sql: %s" % sql_item)






