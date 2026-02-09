import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqlconnector://root:12345@localhost:3306/earthquake_db')


st.title("🌏Earthquake Analytics Dashboard")


queries = {
    "-- 1. Top 10 strongest earthquakes (mag)": """
        select id, place, mag, depth_km, time, country
        from earthquakes
        order by mag desc
        limit 10;
    """,

    "-- 2. Top 10 deepest earthquakes (depth_km)": """
        select id, place, mag, depth_km, time, country
        from earthquakes
        order by depth_km desc
        limit 10;
    """,

    "-- 3. Shallow earthquakes < 50 km and mag > 7.5": """
        select id, place, mag, depth_km, time, country
        from earthquakes
        where depth_km < 50 and mag > 7.5
        order by mag desc;
    """,

    "-- 4. Average depth per country": """
        select country, avg(depth_km) as avg_depth
        from earthquakes
        group by country
        order by avg_depth desc;
    """,

    "-- 5. Average magnitude per magnitude type (magType)": """
        select magtype, avg(mag) as avg_magnitude
        from earthquakes
        group by magtype
        order by avg_magnitude desc;
    """,

    "-- 6. Year with most earthquakes": """
        select year, count(*) as quake_count
        from earthquakes
        group by year
        order by quake_count desc
        limit 1;
    """,

    "-- 7. Month with highest number of earthquakes": """
        select month, count(*) as quake_count
        from earthquakes
        group by month
        order by quake_count desc
        limit 1;
    """,

    "-- 8. Day of week with most earthquakes": """
        select day_of_week, count(*) as quake_count
        from earthquakes
        group by day_of_week
        order by quake_count desc
        limit 1;
    """,

    "-- 9. Count of earthquakes per hour of day": """
        select hour(time) as quake_hour, count(*) as quake_count
        from earthquakes
        group by quake_hour
        order by quake_hour;
    """,

    "-- 10. Most active reporting network (net)": """
        select net, count(*) as quake_count
        from earthquakes
        group by net
        order by quake_count desc
        limit 1;
    """,

    "-- 11. Top 5 places with highest casualties": """
        select place, sum(cdi) as total_casualties
        from earthquakes
        group by place
        order by total_casualties desc
        limit 5;
    """,

    "-- 12. Average economic loss by alert level": """
        select alert, avg(sig) as avg_economic_loss
        from earthquakes
        group by alert
        order by avg_economic_loss desc;
    """,

    "-- 13. Count of reviewed vs automatic earthquakes (status)": """
        select status, count(*) as total_earthquakes
        from earthquakes
        group by status
        order by total_earthquakes desc;
    """,

    "-- 14. Count by earthquake type (type)": """
        select type, count(*) as total_earthquakes
        from earthquakes
        group by type
        order by total_earthquakes desc;
    """,

    "-- 15. Number of earthquakes by data type (types)": """
        select types, count(*) as total_earthquakes
        from earthquakes
        group by types
        order by total_earthquakes desc;
    """,

    "-- 16. Average RMS and gap per continent": """
        select country as continent, avg(rms) as avg_rms, avg(gap) as avg_gap
        from earthquakes
        group by country
        order by country;
    """,

    "-- 17. Events with high station coverage (nst > 50)": """
        select *
        from earthquakes
        where nst > 50
        order by nst desc;
    """,

    "-- 18. Number of tsunamis triggered per year": """
        select year, sum(tsunami) as tsunamis_triggered
        from earthquakes
        group by year
        order by tsunamis_triggered desc;
    """,

    "-- 19. Count earthquakes by alert levels (red, orange, etc.)": """
        select alert, count(*) as total_earthquakes
        from earthquakes
        group by alert
        order by total_earthquakes desc;
    """,

    "-- 20. Top 5 countries with highest average magnitude (last 10 years)": """
        select country, avg(mag)
        from earthquakes
        group by country
        order by avg(mag) desc
        limit 5;
    """,

    "-- 21. Countries with both shallow and deep earthquakes in same month": """
        select country, month
        from earthquakes
        where quake_depth_flag in ('shallow','deep')
        group by country, month
        having count(distinct quake_depth_flag) = 2;
    """,

    "-- 22. Year-over-year growth rate of earthquakes globally": """
        select year, quake_count,
        lag(quake_count) over(order by year) as previous_year,
        (quake_count - lag(quake_count) over(order by year)) /
        lag(quake_count) over(order by year) * 100 as growth_rate
        from (
            select year, count(*) as quake_count
            from earthquakes
            group by year
        ) as yearly_cnt
        order by year;
    """,

    "-- 23. Top 3 most seismically active regions by frequency & magnitude": """
        select country, count(*) as frequency, avg(mag) as avg_mag
        from earthquakes
        group by country
        order by frequency desc, avg_mag desc
        limit 3;
    """,

    "-- 24. Average depth within ±5° latitude of equator per country": """
        select country, avg(depth_km)
        from earthquakes
        where latitude between -5 and 5
        group by country;
    """,

    "-- 25. Countries with highest ratio of shallow to deep earthquakes": """
        select country,
        count(case when quake_depth_flag='shallow' then 1 end) as shallow_cnt,
        count(case when quake_depth_flag='deep' then 1 end) as deep_cnt,
        count(case when quake_depth_flag='shallow' then 1 end) /
        count(case when quake_depth_flag='deep' then 1 end) as ratio_cnt
        from earthquakes
        group by country
        order by ratio_cnt desc;
    """,

    "-- 26. Average magnitude difference between earthquakes with and without tsunami alerts": """
        select avg_mag-avg_mag_tsunami as mag_diff, avg_mag, avg_mag_tsunami
        from (
            select
            avg(case when tsunami=0 then mag end) as avg_mag,
            avg(case when tsunami=1 then mag end) as avg_mag_tsunami
            from earthquakes
        ) t;
    """,

    "-- 27. Lowest data reliability events (highest avg error of gap & rms)": """
        select id, gap, rms, (gap+rms)/2 as avg_error
        from earthquakes
        order by avg_error desc
        limit 10;
    """,

    "-- 28. Regions with highest frequency of deep-focus earthquakes (depth > 300 km)": """
        select country, count(*) as deep_quakes
        from earthquakes
        where depth_km > 300
        group by country
        order by deep_quakes desc;
    """,

    "-- 29. Pairs of consecutive earthquakes within 50 km & 1 hour": """
        select a.id as quake1_id, b.id as quake2_id, a.time as time1, b.time as time2,
        a.latitude as lat1, a.longitude as lon1, b.latitude as lat2, b.longitude as lon2
        from earthquakes a
        join earthquakes b on a.time < b.time
        where abs(timestampdiff(HOUR, a.time, b.time)) <= 1
        and (6371*acos(cos(radians(a.latitude))*cos(radians(b.latitude))*cos(radians(b.longitude)-radians(a.longitude))
            + sin(radians(a.latitude))*sin(radians(b.latitude)))) <= 50
        order by a.time;
    """,

    "-- 30. Select all data sample (first 5 rows)": """
        SELECT * FROM earthquakes LIMIT 5;
    """
}



selected_query = st.sidebar.selectbox("Select a question", list(queries.keys()))

if st.button("Run Query"):
    df = pd.read_sql(queries[selected_query], engine)
    st.dataframe(df)
    
   
    
