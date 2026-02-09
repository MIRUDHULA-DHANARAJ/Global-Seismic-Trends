import pandas as pd
import re
import numpy as np


df = pd.read_csv("../data/raw/earthquakes_raw.csv")

# ------------------------------

def extract_country(place):
    if pd.isna(place):
        return "other_regions"

    match = re.search(r',\s*([^,]+)$', place)
    if match:
        return match.group(1).strip().lower()

    return "other_regions"

df['country'] = df['place'].apply(extract_country)
# -------------------


df['alert'] = (df['alert'].astype(str).str.strip().str.lower().replace('nan', pd.NA))



# ------------------------------
text_cols = ['magType', 'status', 'type', 'net', 'sources', 'types']

for col in text_cols:
    df[col] = (df[col].astype(str).str.strip().str.lower().replace('nan', pd.NA))


df['sources'] = df['sources'].str.strip(',')
df['types'] = df['types'].str.strip(',')

# ------------------------------

num_col = ['mag', 'depth_km', 'nst', 'dmin', 'rms', 'gap',
           'magError', 'depthError', 'magNst', 'sig']

df[num_col] = df[num_col].apply(pd.to_numeric, errors='coerce')

quality_cols = ['nst', 'dmin', 'rms', 'gap', 'magError', 'depthError', 'magNst','mag','depth_km']
for col in quality_cols:
    df[col] = df[col].fillna(df[col].median())

df['sig'] = df['sig'].fillna(0)



# ------------------------------

df.to_csv("../data/cleaned/earthquakes_cleaned.csv", index=False)
print("Cleaned data saved successfully")
