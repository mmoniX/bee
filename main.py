from project import BeeData
from df_to_pg import DataSource
import time

def program():
    try:
        feature = BeeData()
        df = feature.run()
        if df.empty:
            print("No data to insert.")
            return
        with DataSource() as ds:
            ds.insert_data(df)       
    except Exception as ex:
        print(f"Error due to {ex}")

if __name__ == '__main__':
    while True:
        program()
        print("Waiting for the next 10 minutes...")
        time.sleep(10 * 60)
