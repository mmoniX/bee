import os
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv

class BeeData:
    def __init__(self):
        load_dotenv()
        self.web = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup"
        self.apikey = os.getenv("API_KEY")
        self.query = f"/entityId?page=0&x-apikey={self.apikey}"
        self.hives = [
           "digital_bee_hive_42-s2120",
           "digital_bee_hive_42_dragino-s31lb",
           "digital_bee_hive_42_dragino-d23-lb"
        ]
        url1, url2, url3 = [f"{self.web}/{hive}{self.query}" for hive in self.hives]
        self.sources = [
           ("hive_s2120", url1),
           ("hive_s31lb", url2),
           ("hive_d23-lb", url3)
        ]
        self.columns = ["timestamp", "ID", "Sensor_Name", "Sensor_Type", "Hive_Name", "Location", 
                        "lightIntensity", "rainGauge", "relativeHumidity", "temperature", "pressure", 
                        "windDirection", "uvIndex", "windSpeed", "tempC1", "tempC2", "tempC3"
        ]
        self.hive_sensor_map = {
            "W42": ["LoRa-2CF7F1C0613005BC"],
            "Hive_1": ["LoRa-A840411F645AE815", "LoRa-A84041892E5A7A68"],
            "Hive_2": ["LoRa-A8404138A188669C", "LoRa-A840419521864618"],
            "Hive_3": ["LoRa-A84041CC625AE81E", "LoRa-A8404160C85A7A7B"],
        }

    def fetch_data(self, sources):
        for name, url in sources:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    json_data = response.json()
                    print(f"{name} fetched successfully!")
                    yield name, json_data
                else:
                    print(f"Failed to get data from {name}: {response.status_code}")
                    yield name, None
            except Exception as e:
                print(f"An error occurred while fetching data from {name}: {e}")
                yield name, None

    def process_data(self, json_data, df):
        for entity in json_data.get("entities", []):
            row = {}
            try:
                ts = entity.get("SERVER_ATTRIBUTE", {}).get("location", {}).get("ts")
                if ts is None:
                    continue
                row["timestamp"] = datetime.datetime.fromtimestamp(ts / 1000, tz=datetime.timezone.utc)
                row["ID"] = entity.get("entityId", {}).get("id", None)
                row["Sensor_Name"] = entity.get("ENTITY_FIELD", {}).get("name", None)
                row["Sensor_Type"] = entity.get("ENTITY_FIELD", {}).get("type", None)
                row["Location"] = entity.get("SERVER_ATTRIBUTE", {}).get("location", {}).get("value", None)
                row["lightIntensity"] = entity.get("TIME_SERIES", {}).get("lightIntensity", {}).get("value", None)
                row["rainGauge"] = entity.get("TIME_SERIES", {}).get("rainGauge", {}).get("value", None)
                row["relativeHumidity"] = entity.get("TIME_SERIES", {}).get("relativeHumidity", {}).get("value", None)
                row["temperature"] = entity.get("TIME_SERIES", {}).get("temperature", {}).get("value", None)
                row["pressure"] = entity.get("TIME_SERIES", {}).get("pressure", {}).get("value", None)
                row["windDirection"] = entity.get("TIME_SERIES", {}).get("windDirection", {}).get("value", None)
                row["uvIndex"] = entity.get("TIME_SERIES", {}).get("uvIndex", {}).get("value", None)
                row["windSpeed"] = entity.get("TIME_SERIES", {}).get("windSpeed", {}).get("value", None)
                row["tempC1"] = entity.get("TIME_SERIES", {}).get("tempC1", {}).get("value", None)
                row["tempC2"] = entity.get("TIME_SERIES", {}).get("tempC2", {}).get("value", None)
                row["tempC3"] = entity.get("TIME_SERIES", {}).get("tempC3", {}).get("value", None)

                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            except Exception as e:
                print(f"Missing field {e}, skipping entity.")
        return df

    def get_dataframe(self, sources, columns):
        df = pd.DataFrame(columns=columns)
        for name, json_data in self.fetch_data(sources):
            if json_data:
                df = self.process_data(json_data, df)
        numeric_cols = self.columns[6:]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return (df)
    
    def expand_by_hive(self, df):
        expanded_rows = []
        for _, row in df.iterrows():
            sensor_name = row["Sensor_Name"]
            for hive, sensors in self.hive_sensor_map.items():
                if sensor_name in sensors:
                    new_row = row.copy()
                    new_row["Hive_Name"] = hive
                    expanded_rows.append(new_row)
        return pd.DataFrame(expanded_rows)
            
    def run(self):
        base_df = self.get_dataframe(self.sources, self.columns)
        expanded_df = self.expand_by_hive(base_df)
        return expanded_df
