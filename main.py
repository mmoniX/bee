from project import BeeData
from DataInsertions import DataInsertion

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
        query = "INSERT INTO sensor_type_tbl (columns) values (%s, %f ...)"
        data = df['column_name']
        DataInsertion.insert(query, data=data)
        
    except Exception as ex:
        print(f"Error due to {ex}")