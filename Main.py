import gevent
from gevent import monkey
monkey.patch_all()
import akshare as ak
from DatabaseSetup import DatabaseSetup
from config import Config
from MySQLProxy import MySQLProxy
from DatabaseUpdate import DatabaseUpdate

def PrintInfo(**args):
    fund_em_info_df = ak.fund_em_open_fund_info(**args)
    print(len(fund_em_info_df.values))

# fund_em_open_fund_info这种需要大量并发的api，需要想办法使其异步化，否则查询速度是无法接受的
# 封装异步api，使外部看起来是同步的
# 数据库操作的pool化
def main():
    Config.ReadConfig()

    # 数据库的初始化 一般只需要跑一次
    # 跑过Setup都需要补一个Update重新更新数据，所以尽量避免更改数据库结构
    """    DS = DatabaseSetup()
    DS.ProceeAction()

    DU = DatabaseUpdate()
    DU.ProceeAction()"""
    #fund_em_info_df = ak.fund_em_open_fund_info(fund="000001", indicator="单位净值走势")
    #print(fund_em_info_df)
    with MySQLProxy() as (conn, cursor):
        sql = '''SELECT ID FROM Open_Fund_Daily'''
        cursor.execute(sql)
        result: [] = cursor.fetchall()
        result = ["%06d" % item[0] for item in result]

    requests = []
    for fundId in result:
        requests.append(gevent.spawn(PrintInfo, fund=fundId, indicator="单位净值走势"))
    gevent.joinall(requests)

if __name__ == '__main__':
    main()
