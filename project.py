import os
import requests
import json
import pandas as pd
import datetime
from dotenv import load_dotenv

load_dotenv()
web = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup"
apikey = os.getenv("API_KEY")
query = f"/entityId?page=0&x-apikey={apikey}"

hives = [
    "digital_bee_hive_42-s2120",
    "digital_bee_hive_42_dragino-s31lb",
    "digital_bee_hive_42_dragino-d23-lb"
]
url1, url2, url3 = [f"{web}/{hive}{query}" for hive in hives]

sources = [
    ("hive_s2120", url1),
    ("hive_s31lb", url2),
    ("hive_d23-lb", url3),
]

def fetch_data(sources):
  for name, url in sources:
    try:
      response = requests.get(url)
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

columns = ["timestamp", "ID", "Name", "Type", "Location",
       "lightIntensity", "rainGauge", "relativeHumidity", "temperature", "pressure", "windDirection",
       "uvIndex", "windSpeed", "tempC1", "tempC2", "tempC3"]
df = pd.DataFrame(columns=columns)

def process_data(json_data, df):
  for entity in json_data.get("entities", []):
    row = {}
    try:
      ts = entity["SERVER_ATTRIBUTE"]["location"].get("ts") #which TS to extract
      if ts is None:
        continue
      ts = datetime.datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
      row["timestamp"] = ts
      row["ID"] = entity.get("entityId", {}).get("id", None)
      row["Name"] = entity.get("ENTITY_FIELD", {}).get("name", None)
      row["Type"] = entity.get("ENTITY_FIELD", {}).get("type", None)
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

#for temporary, will change it after complete everything
for name, json_data in fetch_data(sources):
  if json_data:
    df = process_data(json_data, df)

df = df.astype({
  'lightIntensity' : 'float',
  'rainGauge' : 'float',
  'relativeHumidity' : 'float',
  'temperature' : 'float',
  'pressure' : 'float',
  'windDirection' : 'float',
  'uvIndex' : 'float',
  'windSpeed' : 'float',
  'tempC1' : 'float',
  'tempC2' : 'float',
  'tempC3' : 'float'})

print(df.head(50))
