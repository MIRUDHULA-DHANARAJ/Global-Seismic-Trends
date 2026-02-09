import pandas as pd
import numpy as np

df = pd.read_csv(r"D:\Global-Seismic-Trends\data\cleaned\earthquakes_cleaned.csv")

# ----------

df['time'] = pd.to_datetime(df['time'], unit='ms')
df['updated'] = pd.to_datetime(df['updated'], unit='ms')

# -------------

df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month
df['day'] = df['time'].dt.day
df['day_of_week'] = df['time'].dt.day_name()

# Depth flag
df['quake_depth_flag'] = np.where(df['depth_km'] < 70, 'shallow', 'deep')

# --------------
df['quake_strength_flag'] = np.where(df['mag'] >= 4, 'strong', 'moderate')

# Save
df.to_csv("data/cleaned/earthquakes_final.csv", index=False)
print("Feature engineered data saved successfully!")
