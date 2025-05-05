from project import BeeData  #is there any use of it?
import  psycopg2


class Datasource:

    def __init__(self):
        try:
            """
                initialize connection strings to the Maria db
            """
            self.conn = psycopg2.connect(
                user="bee_user",  
                password="admin",  
                host="localhost",  
                port=5432,  
                database="beedb"   
                )
            
        except psycopg2.Error as ex:
            print(f"Error Using The credentials to DB : {ex}")



    def connect_db(self):
        try:
            """
                WillEstablish connection to the database and then , 
                then push the required data.
                work on-progress
            """
            query = "uinsert into db() values()"

        except  mariadb.Error as ex:
            print(f'Error connecting to Database : {ex}')