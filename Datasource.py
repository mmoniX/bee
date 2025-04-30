from project import df
import mariadb



class Datasource:

    def __init__(self):
        try:
            """
                initialize connection strings to the Maria db
            """
            self.conn = mariadb.connect(
                user="bee_user",  
                password="password",  
                host="localhost",  
                port=3306,  
                database="bee_db"   
                )
            
        except mariadb.Error as ex:
            print(f"Error Using The credentials to DB : {ex}")



    def connect_db(self):
        try:
            """
                WillEstablish connection to the database and then , 
                then push the required data.
                work on-progress
            """
        except  mariadb.Error as ex:
            print(f'Error connecting to Database : {ex}')