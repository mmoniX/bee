import psycopg2
from dotenv import load_dotenv
import os

class Datasource:
    def __init__(self):
        load_dotenv()
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        try:
            self.conn = psycopg2.connect(
                user=DB_USER, 
                password=DB_PASSWORD, #empty for now
                host=DB_HOST, # use localhost if db not work
                port=DB_PORT, 
                database=DB_NAME
                )
            
            self.cursor = self.conn.cursor()
            print("Connection established")
        except psycopg2.Error as ex:
            print(f"Connection to database failed: {ex}")

    def insert_data(self): #TODO
        try:
            print(f"cursor : { self.cursor}")
        except Exception as ex:
            print(f"Error Conneting to Database : {ex}")
    
    def close_connection(self):
        if self.cursor:
            self.cursor.close() 
        if self.conn:
            self.conn.close()
        print("Connection to PostgreSQL database closed.")

ds = Datasource()
ds.insert_data()