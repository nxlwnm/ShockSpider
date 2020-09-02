<<<<<<< HEAD
import akshare as ak
import DatabaseSetup
import DatabaseUpdate
from config import Config
import MySQLProxy

# 数据库的初始化 一般只需要跑一次
# 需要考虑如何自动判定
# 数据库的常态内容需要支持自动更新，比如每7天自动获取并加入到数据库
# DS = DatabaseSetup.DatabaseSetup()
# DS.Setup()

# 净值数据需要每天23:以后更新
Config.ReadConfig()
with MySQLProxy.MySQLProxy(host=Config.host, user=Config.user, password=Config.password,
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
    if int(item[0]) in IDs:
        print(" ".join(resultsDict[int(item[0])]))
    else:
        pass


# if __name__ == '__main__':
#    pass
=======
import tushare as ts

pro = ts.pro_api('2b69f227d5927d200cafdf1f448671c79b57a5dcc6e086681de05f08')

df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001',
                   fields='exchange,cal_date,is_open,pretrade_date', is_open='0')

print(df)

>>>>>>> 7a54d061dab6cc27a0d8d02797094011b14807a6
