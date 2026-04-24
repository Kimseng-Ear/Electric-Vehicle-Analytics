-- 1. Yearly EV Growth Trend
SELECT ModelYear, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY ModelYear
ORDER BY ModelYear;

-- 2. Top 10 Brands
SELECT TOP 10 Make, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY Make
ORDER BY TotalVehicles DESC;

-- 3. Top Models
SELECT TOP 10 Model, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY Model
ORDER BY TotalVehicles DESC;

-- 4. Geographic Analysis
SELECT State, County, City, PostalCode, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY State, County, City, PostalCode
ORDER BY TotalVehicles DESC;

-- 5. Vehicle Type Comparison
SELECT VehicleType, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY VehicleType
ORDER BY TotalVehicles DESC;

-- 6. Average Electric Range
SELECT Make, Model, AVG(ElectricRange) AS AvgRange
FROM dbo.EV_Population
WHERE ElectricRange > 0
GROUP BY Make, Model
ORDER BY AvgRange DESC;

-- 7. CAFV Eligibility
SELECT CAFVEligibility, COUNT(*) AS TotalVehicles,
       CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS Percentage
FROM dbo.EV_Population
GROUP BY CAFVEligibility;

-- 8. Utility Provider Analysis
SELECT ElectricUtility, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY ElectricUtility
ORDER BY TotalVehicles DESC;

-- 9. Legislative District Insights
SELECT LegislativeDistrict, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY LegislativeDistrict
ORDER BY TotalVehicles DESC;

-- 10. Year-over-Year Growth Rate
WITH YearlyStats AS (
    SELECT ModelYear, COUNT(*) AS TotalVehicles
    FROM dbo.EV_Population
    GROUP BY ModelYear
)
SELECT ModelYear, TotalVehicles,
       LAG(TotalVehicles) OVER (ORDER BY ModelYear) AS PrevYearVehicles,
       CASE WHEN LAG(TotalVehicles) OVER (ORDER BY ModelYear) IS NULL THEN 0
            ELSE CAST((TotalVehicles - LAG(TotalVehicles) OVER (ORDER BY ModelYear)) * 100.0 / LAG(TotalVehicles) OVER (ORDER BY ModelYear) AS DECIMAL(10,2))
       END AS YoYGrowthRate
FROM YearlyStats
ORDER BY ModelYear;
