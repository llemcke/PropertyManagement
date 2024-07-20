import os
import MySQLdb
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

mydb = MySQLdb.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USERNAME"),
    passwd=os.getenv("PASSWORD"),
    db=os.getenv("DATABASE"),
    autocommit=True,
    ssl_mode="REQUIRED"
)

class System():
    def checkLogin (self, username:str,password:str)->int:
        cursor=mydb.cursor()
        try:
            cursor.execute(userStr)
            userExists=cursor.fetchone()
        except:
            userExists=None
        if userExists==None:
            userExists=-1
        try:
            cursor.execute(passStr)
            pass=cursor.fetchone()
        except:
            userExists=None
        if userExists==None:
            userExists=-1
        mydb.commit()
        cursor.close()
