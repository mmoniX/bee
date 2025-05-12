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
                database="final"
            )
            self.cursor = self.conn.cursor()
            print("Connection established")
        except psycopg2.Error as ex:
            print(f"Connection to database failed: {ex}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Connection to PostgreSQL database closed.")

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
        self.cursor.execute("SELECT id, measurement_unit FROM measurement_unit_tbl")
        existing_units = self.cursor.fetchall()
        unit_map = {unit: unit_id for unit_id, unit in existing_units}

        # unit_map = {}
        for unit in set(measurement_units.values()):
            if unit not in unit_map:
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

        # Insert Beehives
        unique_hive = df["Hive_Name"].dropna().unique()
        beehive_query = """
            INSERT INTO beehive_tbl (id, beehive_name, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (beehive_name) DO NOTHING;
        """
        for hive in unique_hive:
            hive_id = str(uuid.uuid4())
            self.cursor.execute(beehive_query, (hive_id, hive, created_at))
        self.cursor.execute("SELECT id, beehive_name FROM beehive_tbl")
        beehive_map = {name: id_ for id_, name in self.cursor.fetchall()}
        print("beehive_ok")

        # Insert Sensor
        sensor_query = """
            INSERT INTO sensors_tbl (
                id, sensor_name, sensor_type_id, location_id, installation_date,
                last_seen, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sensor_name) DO NOTHING;
        """
        sensor_map = {}
        self.cursor.execute("SELECT id, sensor_name FROM sensors_tbl")
        existing_sensors = {name: id_ for id_, name in self.cursor.fetchall()}
        sensor_map = existing_sensors.copy()  # <-- FIXED HERE
        for _, row in df.iterrows():
            sensor_name = row["Sensor_Name"]
            if sensor_name in sensor_map:
                continue
            sensor_id = str(uuid.uuid4())
            sensor_type_id = sensor_type_map.get(row["Sensor_Type"])
            location_id = location_map.get(row["Location"])
            if sensor_type_id and location_id:
                self.cursor.execute(sensor_query, (
                    sensor_id, sensor_name, sensor_type_id, location_id,
                    created_at, created_at, True, created_at
                ))
                sensor_map[sensor_name] = sensor_id
        print("sensor_ok")

        # Insert Beehive-Sensor              ON CONFLICT (beehive_id, sensor_id) DO NOTHING;
        beehive_sensor_query = """
            INSERT INTO beehive_sensor_tbl (id, beehive_id, sensor_id, created_at)
            VALUES (%s, %s, %s, %s)
        """
        beehive_sensor_map = {}
        for _, row in df.iterrows():
            hive_name = row["Hive_Name"]
            sensor_name = row["Sensor_Name"]
            beehive_id = beehive_map.get(hive_name)
            sensor_id = sensor_map.get(sensor_name)
            if beehive_id and sensor_id:
                beehive_sensor_id = str(uuid.uuid4())
                self.cursor.execute(beehive_sensor_query, (
                    beehive_sensor_id, beehive_id, sensor_id, created_at
                ))
                beehive_sensor_map[(beehive_id, sensor_id)] = beehive_sensor_id
        print("beehive_sensor_ok")

        # Insert Reading
        reading_query = """
            INSERT INTO reading_tbl (id, beehive_sensor_id, ts, feature_name, reading_value, 
                measurement_unit_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in df.iterrows():
            sensor_name = row["Sensor_Name"]
            hive_name = row["Hive_Name"]
            timestamp = row["timestamp"]
            beehive_id = beehive_map.get(hive_name)
            sensor_id = sensor_map.get(sensor_name)
            if not (beehive_id and sensor_id):
                continue
            beehive_sensor_id = beehive_sensor_map.get((beehive_id, sensor_id))
            if not beehive_sensor_id:
                continue
            for feature, unit in measurement_units.items():
                reading_value = row.get(feature)
                if pd.notna(reading_value):
                    reading_id = str(uuid.uuid4())
                    self.cursor.execute(reading_query, (
                        reading_id, beehive_sensor_id, timestamp, feature, 
                        reading_value, unit_map[unit], created_at
                    ))
        print("reading_ok")

        if not sensor_map:
            print("No sensors inserted or matched existing records.")
        if not beehive_sensor_map:
            print("No beehive-sensor relations created.")

        self.conn.commit()
        print("Data inserted.")
