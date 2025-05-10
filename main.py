from project import BeeData
from df_to_pg import DataSource
import time

def program():
    ds = None
    try:
        feature = BeeData()
        df = feature.run()

        ds = DataSource()
        ds.insert_data(df)        
    except Exception as ex:
        print(f"Error due to {ex}")
    finally:
        if ds:
            ds.close_connection()
        print("Connection closed")

if __name__ == '__main__':
    while True:
        program()
        print("Waiting for the next 30 minutes...")
        time.sleep(30 * 60)
