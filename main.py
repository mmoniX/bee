from project import BeeData
from DataInsertions import DataInsertion
from df_to_pg import Datasource


if __name__ == '__main__':
    try:
        feature = BeeData()
        df = feature.run()
        df.to_csv('readings.csv', sep=',', index=False)
        # print(df.head())
        # print(df.describe())
        """
             Notice that we read from API into Dataframe
             we can not tetch from dataframe series  as the data_to_be_inserted
        """
        # Connections to the Database
        
    except Exception as ex:
        print(f"Error due to {ex}")