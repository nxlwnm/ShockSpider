import akshare as ak
from config import Config
from MySQLProxy import MySQLProxy
import DatabaseSetup
import time
from datetime import datetime

#DS = DatabaseSetup.DatabaseSetup()
#DS.Setup()

class DatabaseUpdate:
    def __init__(self):
        Config.ReadConfig()

    def ProceeAction(self):
        with MySQLProxy() as (conn, cursor):
            self.ProcessAllFundNameTableUpdate(conn, cursor)
            self.ProcessOpenFundDailyTableUpdate(conn, cursor)

    def ProcessOpenFundDailyTableUpdate(self, conn, cursor):
        # query if need update
        sqlSelect: str = '''SELECT * FROM Table_Update_Time WHERE TableName = "Open_Fund_Daily";'''
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        lastUpdateTime = datetime.min
        for row in results:
            if row[0] == "Open_Fund_Daily":
                lastUpdateTime = row[1]

        # 23点前未更新，或超过一天未更新(忽略周末的情况0
        if lastUpdateTime.hour < 23 < datetime.now().hour or (datetime.now()- lastUpdateTime).day >= 1:
            self.UpdateOpenFundDailyTable(conn, cursor)
            self.UpdateTimeTableForOpenFundDailyTable(conn, cursor)
        else:
            print("no need to update Open_Fund_Daily table")

    def ProcessAllFundNameTableUpdate(self, conn, cursor):
        # query if need update
        sqlSelect: str = '''SELECT * FROM Table_Update_Time WHERE TableName = "All_Fund_Name";'''
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        deltaDay = 1000
        for row in results:
            if row[0] == "All_Fund_Name":
                deltaDay = (datetime.now() - row[1]).days

        if deltaDay >= Config.AllFundNameTableUpdateInternal:
            # update All_Fund_Name
            self.UpdateAllFundName(conn, cursor)
            # update Table_Update_Time
            self.UpdateTimeTableForAllFundTable(conn, cursor)
        else:
            print("no need to update All_Fund_Name table")

    def UpdateAllFundName(self, conn, cursor):
        sqlSelect: str = ''' SELECT ID FROM All_Fund_Name;'''
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        results = [item[0] for item in results]

        fund_em_fund_name_df = ak.fund_em_fund_name()
        for row in fund_em_fund_name_df.values:
            if int(row[0]) in results:
                print("update AllFundName %s" % row[0])
                sql = '''UPDATE All_Fund_Name 
                        SET 
                        ID = %s,
                        PinYin = '%s',
                        Name = '%s',
                        Type = '%s',
                        WholeName = '%s'
                        WHERE ID = %s;''' % (row[0], row[1], row[2], row[3], row[4], row[0])
                cursor.execute(sql)
            else:
                print("INSERT AllFundName %s" % row[0])
                sql = '''INSERT INTO All_Fund_Name 
                (ID, PinYin, Name, Type, WholeName )
                VALUES
                (%s, '%s', '%s', '%s', '%s');
                ''' % (row[0], row[1], row[2], row[3], row[4])
                cursor.execute(sql)
        conn.commit()

    def UpdateOpenFundDailyTable(self, conn, cursor):
        sqlSelect: str = ''' SELECT ID FROM Open_Fund_Daily;'''
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        results = [item[0] for item in results]

        fund_em_open_fund_daily_df = ak.fund_em_open_fund_daily()
        for row in fund_em_open_fund_daily_df.values:
            for index in range(len(row)):
                if row[index] == '':
                    row[index] = "0"
            if int(row[0]) in results:
                print("update Open_Fund_Daily %s" % row[0])
                sql = '''UPDATE Open_Fund_Daily 
                        SET 
                        ID = %s,
                        Name = '%s',
                        UnitMoney = %s,
                        AccuMoney = %s,
                        PrevUnitMoney = %s,
                        PrevAccuMoney = %s,
                        DailyGrowthValue = %s,
                        DailyGrowthRate = %s,
                        SubscriptionStatus = '%s',
                        RedemptionStatus = '%s',
                        Charge = '%s'
                        WHERE ID = %s;
                        ''' % (row[0], row[1], row[2], row[3], row[4], row[5],
                               row[6], row[7], row[8], row[9], row[10], row[0])
                cursor.execute(sql)
            else:
                print("INSERT Open_Fund_Daily %s" % row[0])
                sql = '''INSERT INTO Open_Fund_Daily 
                (ID, Name, UnitMoney, AccuMoney, 
                PrevUnitMoney, PrevAccuMoney, DailyGrowthValue, DailyGrowthRate,
                SubscriptionStatus, RedemptionStatus, Charge)
                VALUES
                (%s, '%s', %s, %s, %s, %s, %s, %s,'%s', '%s', '%s');
                ''' % (row[0], row[1], row[2], row[3], row[4], row[5],
                       row[6], row[7], row[8], row[9], row[10])
                cursor.execute(sql)
        conn.commit()

    def UpdateTimeTable(self, conn, cursor, table_name: str):
        sqlSelect: str = '''SELECT TableName FROM Table_Update_Time WHERE TableName = "%s";''' % table_name
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        results = [item[0] for item in results]

        localtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if table_name in results:
            sql = '''
                    UPDATE Table_Update_Time 
                    SET LastUpdateTime = str_to_date('%s', '%%Y-%%m-%%d %%H:%%i:%%S');
                    WHERE TableName = '%s';
                    ''' % (localtime, table_name)
            cursor.execute(sql)
        else:
            sql = '''
                INSERT INTO Table_Update_Time 
                (TableName, LastUpdateTime)
                VALUES
                ('%s', str_to_date('%s', '%%Y-%%m-%%d %%H:%%i:%%S'));
                ''' % (table_name, localtime)
            cursor.execute(sql)
        conn.commit()

    def UpdateTimeTableForAllFundTable(self, conn, cursor):
        self.UpdateTimeTable(conn, cursor, "All_Fund_Name")

    def UpdateTimeTableForOpenFundDailyTable(self, conn, cursor):
        self.UpdateTimeTable(conn, cursor, "Open_Fund_Daily")