USE EVAnalyticsDB;
GO

CREATE OR ALTER VIEW vw_YearlyTrend AS
SELECT ModelYear, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY ModelYear;
GO

CREATE OR ALTER VIEW vw_TopBrands AS
SELECT Make, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY Make;
GO

CREATE OR ALTER VIEW vw_CityDistribution AS
SELECT City, County, State, COUNT(*) AS TotalVehicles
FROM dbo.EV_Population
GROUP BY City, County, State;
GO

CREATE OR ALTER VIEW vw_RangeAnalytics AS
SELECT Make, Model, AVG(ElectricRange) AS AvgElectricRange, MAX(ElectricRange) AS MaxElectricRange
FROM dbo.EV_Population
GROUP BY Make, Model;
GO
