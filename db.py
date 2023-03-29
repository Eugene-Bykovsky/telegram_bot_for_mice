import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def connect_to_db():
    mydb = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        passwd=os.getenv('PASSWD'),
        database=os.getenv('DATABASE')
    )
    mycursor = mydb.cursor()
    return mydb, mycursor
