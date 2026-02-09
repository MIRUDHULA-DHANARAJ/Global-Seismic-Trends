import pandas as pd
from sqlalchemy import create_engine


df = pd.read_csv(r"D:\Global-Seismic-Trends\data\cleaned\earthquakes_final.csv")


engine = create_engine('mysql+mysqlconnector://root:12345@localhost:3306/earthquake_db')

df.to_sql(
    name='earthquakes', 
    con=engine, 
    if_exists='replace',  
    index=False
)

print("Data inserted into MySQL successfully!")
