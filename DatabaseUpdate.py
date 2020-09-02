import akshare as ak
from config import Config
import MySQLProxy
import DatabaseSetup
import time
from datetime import datetime

#DS = DatabaseSetup.DatabaseSetup()
#DS.Setup()

class DatabaseUpdate:
    def __init__(self):
        self.fund_em_fund_name_df = ak.fund_em_fund_name()
        Config.ReadConfig()

    def ProceeAction(self):
        with MySQLProxy.MySQLProxy(host=Config.host, user=Config.user, password=Config.password,
                                   database=Config.database, charset=Config.charset) as (conn, cursor):
            self.ProcessAllFundNameTableUpdate(conn, cursor)

    def ProcessAllFundNameTableUpdate(self, conn, cursor):
        # query if need update
        sqlSelect: str = '''SELECT * FROM Table_Update_Time WHERE TableName = "All_Fund_Name";'''
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        deltaDay = 0
        for row in results:
            if row[0] == "All_Fund_Name":
                deltaDay = (datetime.now() - row[1]).days

        if deltaDay >= Config.AllFundNameTableUpdateInternal:
            # update All_Fund_Name
            self.UpdateAllFundName(conn, cursor)
            # update Table_Update_Time
            self.UpdateTimeTable(conn, cursor)
        else:
            print("no need to update All_Fund_Name table")

    def UpdateTimeTable(self, conn, cursor):
        sqlSelect: str = '''SELECT TableName FROM Table_Update_Time WHERE TableName = "All_Fund_Name";'''
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        results = [item[0] for item in results]

        localtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(localtime)
        if "All_Fund_Name" in results:
            sql = '''
            UPDATE Table_Update_Time 
            SET LastUpdateTime = str_to_date('%s', '%%Y-%%m-%%d %%H:%%i:%%S');
            ''' % localtime
            cursor.execute(sql)
        else:
            sql = '''
                    INSERT INTO Table_Update_Time 
                    (TableName, LastUpdateTime)
                    VALUES
                    ('All_Fund_Name', str_to_date('%s', '%%Y-%%m-%%d %%H:%%i:%%S'));
                    ''' % localtime
            cursor.execute(sql)
        conn.commit()

    def UpdateAllFundName(self, conn, cursor):
        sqlSelect: str = ''' SELECT ID FROM All_Fund_Name;'''
        cursor.execute(sqlSelect)
        results = cursor.fetchall()
        results = [item[0] for item in results]

        for row in self.fund_em_fund_name_df.values:
            if int(row[0]) in results:
                print("update %s" % row[0])
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
                print("INSERT %s" % row[0])
                sql = '''INSERT INTO All_Fund_Name 
                (ID, PinYin, Name, Type, WholeName )
                VALUES
                (%s, '%s', '%s', '%s', '%s');
                ''' % (row[0], row[1], row[2], row[3], row[4])
                cursor.execute(sql)
        conn.commit()


DU = DatabaseUpdate()
DU.ProceeAction()




