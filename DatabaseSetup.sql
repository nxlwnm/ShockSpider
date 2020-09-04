create database if not exists ShockSpider;
use ShockSpider;
DROP TABLE IF EXISTS All_Fund_Name;
CREATE TABLE IF NOT EXISTS All_Fund_Name (    
    ID INT,
    PinYin VARCHAR(20) NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Type VARCHAR(20) NOT NULL,
    WholeName VARCHAR(100) NOT NULL,
    PRIMARY KEY (ID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS Table_Update_Time;
CREATE TABLE IF NOT EXISTS Table_Update_Time (
    TableName VARCHAR(20) ,
    LastUpdateTime DATETIME NOT NULL,
    PRIMARY KEY (TableName)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS Open_Fund_Daily;
CREATE TABLE IF NOT EXISTS Open_Fund_Daily (
    ID INT,
    Name VARCHAR(100) NOT NULL,
    UnitMoney FLOAT NOT NULL DEFAULT 0,
    AccuMoney FLOAT NOT NULL DEFAULT 0,
    PrevUnitMoney FLOAT NOT NULL DEFAULT 0,
    PrevAccuMoney FLOAT NOT NULL DEFAULT 0,
    DailyGrowthValue FLOAT NOT NULL DEFAULT 0,
    DailyGrowthRate FLOAT NOT NULL DEFAULT 0,
    SubscriptionStatus VARCHAR(20) NOT NULL,
    RedemptionStatus VARCHAR(20) NOT NULL,
    Charge VARCHAR(10) NOT NULL,
    PRIMARY KEY (ID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS Open_Fund_Info;
CREATE TABLE IF NOT EXISTS Open_Fund_Info (
    SN INT auto_increment,
    ID INT,
    Indicator VARCHAR(20),
    Date DATETIME,
    EquityReturn FLOAT,
    UnitMoney FLOAT,
    PRIMARY KEY (SN)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE UNIQUE INDEX Open_Fund_Info_Index ON Open_Fund_Info(ID, Indicator, Date);