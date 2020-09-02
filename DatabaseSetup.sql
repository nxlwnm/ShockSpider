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