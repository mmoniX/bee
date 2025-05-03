import psycopg2

class Datasource:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                user="postgres", 
                password="admin", 
                host="db", # use localhost if db not work
                port=5432, 
                database="bee_pgdb")
            self.cursor = self.conn.cursor()
            print("Connection established")
        except psycopg2.Error as ex:
            print(f"Connection to database failed: {ex}")

    # def insert_data(): #TODO

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection to PostgreSQL database closed.")
