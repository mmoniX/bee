import psycopg2
import uuid
import datetime
from dotenv import load_dotenv
import os
import pandas as pd

class DataSource:
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
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT, 
                database="bee_pgdb_3"
            )
            self.cursor = self.conn.cursor()
            print("Connection established")
        except psycopg2.Error as ex:
            print(f"Connection to database failed: {ex}")

    def insert_data(self, df):
        created_at = datetime.datetime(2025, 4, 14, 10, 0, 0)

        # Insert Sensor_type
        unique_sensor_types = df["Sensor_Type"].dropna().unique()
        sensor_type_query = """
            INSERT INTO sensor_type_tbl (id, sensor_type_name, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (sensor_type_name) DO NOTHING;
        """
        sensor_type_map = {}
        for st in unique_sensor_types:
            sensor_id = str(uuid.uuid4())
            self.cursor.execute(sensor_type_query, (sensor_id, st, created_at))
            sensor_type_map[st] = sensor_id
        print("sensor_type_ok")
        
        # Insert Measurement_unit
        measurement_units = {
            "lightIntensity": "lux",
            "rainGauge": "mm",
            "relativeHumidity": "%",
            "temperature": "°C",
            "pressure": "hPa",
            "windDirection": "°",
            "uvIndex": "index",
            "windSpeed": "m/s",
            "tempC1": "°C",
            "tempC2": "°C",
            "tempC3": "°C"
        }
        unit_query = """
            INSERT INTO measurement_unit_tbl (id, measurement_unit, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (measurement_unit) DO NOTHING;
        """
        unit_map = {}
        for unit in set(measurement_units.values()):
            unit_id = str(uuid.uuid4())
            self.cursor.execute(unit_query, (unit_id, unit, created_at))
            unit_map[unit] = unit_id
        print("measurement_unit_ok")

        # Insert Locations
        unique_locations = df["Location"].dropna().unique()
        location_query = """
            INSERT INTO location_tbl (id, location_name, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (location_name) DO NOTHING;
        """
        location_map = {}
        for loc in unique_locations:
            loc_id = str(uuid.uuid4())
            self.cursor.execute(location_query, (loc_id, loc, created_at))
            location_map[loc] = loc_id
        print("location_ok")

        # Insert Sensor
        sensor_query = """
            INSERT INTO sensors_tbl (
                id, sensor_type_id, sensor_name, location_id, installation_date,
                measurement_unit_id, last_seen, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sensor_name) DO NOTHING;
        """
        sensor_map = {}
        for _, row in df.iterrows():
            sensor_name = row["Sensor_Name"]
            if sensor_name in sensor_map:
                continue
            sensor_id = str(uuid.uuid4())
            sensor_type = sensor_type_map.get(row["Sensor_Type"])
            location_id = location_map.get(row["Location"])
            installation_date = created_at
            measurement_unit_id = unit_map.get("°C")  # use temperature's unit as a placeholder
            self.cursor.execute(sensor_query, (
                sensor_id, sensor_type, sensor_name, location_id, installation_date,
                measurement_unit_id, created_at, True, created_at
            ))
            sensor_map[sensor_name] = sensor_id
        print("sensor_ok")

        # Insert Beehives
        draft_hive_name = {
            "hive_1": ["LoRa-2CF7F1C0613005BC", "LoRa-A840411F645AE815"],
            "hive_2": ["LoRa-2CF7F1C0613005BC", "LoRa-A8404138A188669C", "LoRa-A84041892E5A7A68"],
            "hive_3": ["LoRa-2CF7F1C0613005BC", "LoRa-A840419521864618", "LoRa-A84041CC625AE81E"]
        }
        beehive_query = """
            INSERT INTO beehive_tbl (id, beehive_name, sensor_id, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (beehive_name, sensor_id) DO NOTHING;
        """
        beehive_map = {}
        for hive_name, sensor_list in draft_hive_name.items():
            for sensor_name in sensor_list:
                sensor_id = sensor_map.get(sensor_name)
                if sensor_id:
                    hive_id = str(uuid.uuid4())
                    self.cursor.execute(beehive_query, (hive_id, hive_name, sensor_id, created_at))
                    beehive_map[hive_name, sensor_name] = hive_id
        print("beehive_ok")

        # Insert Reading
        reading_query = """
            INSERT INTO reading_tbl (id, beehive_id, ts, feature_name, reading_value, measurement_unit_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in df.iterrows():
            sensor_name = row["Sensor_Name"]
            timestamp = row["timestamp"]
            hives_for_sensor = [hive_name for hive_name, sensors in draft_hive_name.items()
                                if sensor_name in sensors]
            for hive_name in hives_for_sensor:
                beehive_id = beehive_map.get((hive_name, sensor_name))
                if not beehive_id:
                    continue
                for feature, unit in measurement_units.items():
                    reading_value = row.get(feature)
                    if pd.notna(reading_value):
                        self.cursor.execute(reading_query, (
                            str(uuid.uuid4()), beehive_id, timestamp, feature,
                            reading_value, unit_map[unit], created_at
                        ))
        print("reading_ok")
    
        self.conn.commit()
        print("Data inserted.")
   
    def close_connection(self):
        if self.cursor:
            self.cursor.close() 
        if self.conn:
            self.conn.close()
        print("Connection to PostgreSQL database closed.")
