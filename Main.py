import tushare as ts

pro = ts.pro_api('2b69f227d5927d200cafdf1f448671c79b57a5dcc6e086681de05f08')

df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001',
                   fields='exchange,cal_date,is_open,pretrade_date', is_open='0')

print(df)

