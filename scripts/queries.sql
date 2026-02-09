

-- CREATE DATABASE AND USE
CREATE DATABASE IF NOT EXISTS earthquake_db;
USE earthquake_db;

-- Preview data
SELECT * FROM earthquakes LIMIT 5;

-- ================================================
-- 1. Top 10 strongest earthquakes (mag)
SELECT id, place, mag, depth_km, time, country
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;

-- 2. Top 10 deepest earthquakes (depth_km)
SELECT id, place, mag, depth_km, time, country
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;

-- 3. Shallow earthquakes < 50 km and mag > 7.5
SELECT id, place, mag, depth_km, time, country
FROM earthquakes
WHERE depth_km < 50 AND mag > 7.5
ORDER BY mag DESC;

-- 4. Average depth per country
SELECT country, AVG(depth_km) AS avg_depth
FROM earthquakes
GROUP BY country
ORDER BY avg_depth DESC;

-- 5. Average magnitude per magnitude type (magType)
SELECT magtype, AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY magtype
ORDER BY avg_magnitude DESC;

-- 6. Year with most earthquakes
SELECT year, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY year
ORDER BY quake_count DESC
LIMIT 1;

-- 7. Month with highest number of earthquakes
SELECT month, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY month
ORDER BY quake_count DESC
LIMIT 1;

-- 8. Day of week with most earthquakes
SELECT day_of_week, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY day_of_week
ORDER BY quake_count DESC
LIMIT 1;

-- 9. Count of earthquakes per hour of day
SELECT HOUR(time) AS quake_hour, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY quake_hour
ORDER BY quake_hour;

-- 10. Most active reporting network (net)
SELECT net, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY net
ORDER BY quake_count DESC
LIMIT 1;

-- 11. Top 5 places with highest casualties
SELECT place, SUM(cdi) AS total_casualties
FROM earthquakes
GROUP BY place
ORDER BY total_casualties DESC
LIMIT 5;

-- 12. Average economic loss by alert level
SELECT alert, AVG(sig) AS avg_economic_loss
FROM earthquakes
GROUP BY alert
ORDER BY avg_economic_loss DESC;

-- 13. Count of reviewed vs automatic earthquakes (status)
SELECT status, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY status
ORDER BY total_earthquakes DESC;

-- 14. Count by earthquake type (type)
SELECT type, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY type
ORDER BY total_earthquakes DESC;

-- 15. Number of earthquakes by data type (types)
SELECT types, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY types
ORDER BY total_earthquakes DESC;

-- 16. Average RMS and GAP per continent
SELECT country AS continent, AVG(rms) AS avg_rms, AVG(gap) AS avg_gap
FROM earthquakes
GROUP BY country
ORDER BY country;

-- 17. Events with high station coverage (nst > 50)
SELECT *
FROM earthquakes
WHERE nst > 50
ORDER BY nst DESC;

-- 18. Number of tsunamis triggered per year
SELECT year, SUM(tsunami) AS tsunamis_triggered
FROM earthquakes
GROUP BY year
ORDER BY tsunamis_triggered DESC;

-- 19. Count earthquakes by alert levels
SELECT alert, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY alert
ORDER BY total_earthquakes DESC;

-- 20. Top 5 countries with highest average magnitude in past 10 years
SELECT country, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY avg_mag DESC
LIMIT 5;

-- 21. Countries that experienced both shallow & deep earthquakes within same month
SELECT country, month
FROM earthquakes
WHERE quake_depth_flag IN ('shallow','deep')
GROUP BY country, month
HAVING COUNT(DISTINCT quake_depth_flag) = 2;

-- 22. Year-over-year growth rate in total number of earthquakes globally
SELECT year, quake_count,
LAG(quake_count) OVER (ORDER BY year) AS previous_year,
((quake_count - LAG(quake_count) OVER (ORDER BY year)) /
 LAG(quake_count) OVER (ORDER BY year)) * 100 AS growth_rate
FROM (
  SELECT year, COUNT(*) AS quake_count
  FROM earthquakes
  GROUP BY year
) AS yearly_cnt
ORDER BY year;

-- 23. 3 most seismically active regions (frequency + avg magnitude)
SELECT country, COUNT(*) AS frequency, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY frequency DESC, avg_mag DESC
LIMIT 3;

-- 24. Average depth of earthquakes within ±5° latitude range of equator per country
SELECT country, AVG(depth_km)
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country;

-- 25. Countries with highest ratio of shallow to deep earthquakes
SELECT country,
COUNT(CASE WHEN quake_depth_flag = 'shallow' THEN 1 END) AS shallow_cnt,
COUNT(CASE WHEN quake_depth_flag = 'deep' THEN 1 END) AS deep_cnt,
COUNT(CASE WHEN quake_depth_flag = 'shallow' THEN 1 END) /
COUNT(CASE WHEN quake_depth_flag = 'deep' THEN 1 END) AS ratio_cnt
FROM earthquakes
GROUP BY country
ORDER BY ratio_cnt DESC;

-- 26. Average magnitude difference between earthquakes with tsunami alerts vs without
SELECT avg_mag - avg_mag_tsunami AS mag_diff, avg_mag, avg_mag_tsunami
FROM (
  SELECT
    AVG(CASE WHEN tsunami = 0 THEN mag END) AS avg_mag,
    AVG(CASE WHEN tsunami = 1 THEN mag END) AS avg_mag_tsunami
  FROM earthquakes
) t;

-- 27. Events with lowest data reliability (highest avg error margins)
SELECT id, gap, rms, (gap + rms)/2 AS avg_error
FROM earthquakes
ORDER BY avg_error DESC
LIMIT 10;

-- 28. Regions with highest frequency of deep-focus earthquakes (depth > 300 km)
SELECT country, COUNT(*) AS deep_quakes
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_quakes DESC;

-- 29. Pairs of consecutive earthquakes within 50 km & 1 hour
-- Note: Requires self join or advanced spatial/time calculations
-- Placeholder: logic can be implemented in Python or MySQL spatial extensions

-- 30. Top 3 regions by frequency + avg magnitude (combined)
SELECT country, COUNT(*) AS frequency, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY frequency DESC, avg_mag DESC
LIMIT 3;
