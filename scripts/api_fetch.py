import requests
import pandas as pd
from datetime import datetime

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

start_year = datetime.now().year - 5
current_year = datetime.now().year
current_month = datetime.now().month


all_records = []
seen_ids = set()

for year in range(start_year, current_year + 1):
    for month in range(1, 13):

        if year == current_year and month > current_month:
            continue

        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 3
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Failed for {start_date} → {end_date}")
            continue

        data = response.json()
        events = data.get("features", [])

        print(start_date, "→", end_date, ":", len(events), "events")

        for earthquake in events:
            eq_id = earthquake["id"]

            if eq_id in seen_ids:
                continue
            seen_ids.add(eq_id)

            properties = earthquake["properties"]
            geometry = earthquake["geometry"]
            coordinates = geometry["coordinates"]
            record = {
    "id": eq_id,
    "time": properties.get("time"),
    "updated": properties.get("updated"),
    
    "latitude": coordinates[1],
    "longitude": coordinates[0],
    "depth_km": coordinates[2],
    
    "mag": properties.get("mag"),
    "magType": properties.get("magType"),
    "place": properties.get("place"),
    "status": properties.get("status"),
    "tsunami": properties.get("tsunami"),
    "alert": properties.get("alert"),
    "felt": properties.get("felt"),
    "cdi": properties.get("cdi"),
    "mmi": properties.get("mmi"),
    "sig": properties.get("sig"),
    
    "net": properties.get("net"),
    "code": properties.get("code"),
    "ids": properties.get("ids"),
    "sources": properties.get("sources"),
    "types": properties.get("types"),
    
    "nst": properties.get("nst"),
    "dmin": properties.get("dmin"),
    "rms": properties.get("rms"),
    "gap": properties.get("gap"),
    "magError": properties.get("magError"),
    "depthError": properties.get("depthError"),
    "magNst": properties.get("magNst"),
    
    "locationSource": properties.get("locationSource"),
    "magSource": properties.get("magSource"),
    
    "type": properties.get("type")
}

           


            all_records.append(record)


df = pd.DataFrame(all_records)

df.to_csv("../data/raw/earthquakes_raw.csv", index=False)

print("Saved to data/raw/earthquakes_raw.csv")
