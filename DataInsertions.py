from df_to_pg import Datasource as ds


class DataInsertion:

    def __init__(self):
        try:
            pass
        except  Exception as e:
            print(f"Error initialing query : {e}")
    

    def insert(self, insert_query, data):
        try:
            c = ds.connectPSQL()
            if len(insert_query) == 0:
                raise ValueError("Query cannot be Empty")
            # saved = c.execute(insert_query, data)

            # saved.commit()
        except Exception as e:
            print(f"Error Inserting into sensor_type_tbl : {e}")