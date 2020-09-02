import akshare as ak
from DatabaseSetup import DatabaseSetup
from config import Config
from MySQLProxy import MySQLProxy
from DatabaseUpdate import DatabaseUpdate

def main():
    Config.ReadConfig()

    # 数据库的初始化 一般只需要跑一次
    # 跑过Setup都需要补一个Update重新更新数据，所以尽量避免更改数据库结构
    DS = DatabaseSetup()
    DS.ProceeAction()

    DU = DatabaseUpdate()
    DU.ProceeAction()

    """    with MySQLProxy(host=Config.host, user=Config.user, password=Config.password,
                               database=Config.database, charset=Config.charset) as (conn, cursor):
        sql : str = '''SELECT * FROM  All_fund_name'''
        cursor.execute(sql)
        result: [] = cursor.fetchall()
        IDs = [item[0] for item in result]
        result: [] = [[str(InnerItem) for InnerItem in item] for item in result]
        resultsDict = {IDs[i]: result[i] for i in range(len(IDs))}

    fund_em_open_fund_daily_df = ak.fund_em_open_fund_daily()
    print(" ".join(fund_em_open_fund_daily_df.columns))
    for item in fund_em_open_fund_daily_df.values:
        print(" ".join(item))"""

    """    for item in fund_em_open_fund_daily_df.values:
        if int(item[0]) in IDs:
            print(" ".join(resultsDict[int(item[0])]))
        else:
            pass"""


if __name__ == '__main__':
    main()
