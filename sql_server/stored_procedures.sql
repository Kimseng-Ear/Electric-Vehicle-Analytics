USE EVAnalyticsDB;
GO

CREATE OR ALTER PROCEDURE sp_GetTopBrands
    @TopN INT = 10
AS
BEGIN
    SET NOCOUNT ON;
    SELECT TOP (@TopN) Make, COUNT(*) AS TotalVehicles
    FROM dbo.EV_Population
    GROUP BY Make
    ORDER BY TotalVehicles DESC;
END;
GO

CREATE OR ALTER PROCEDURE sp_GetTrendByYear
AS
BEGIN
    SET NOCOUNT ON;
    SELECT ModelYear, COUNT(*) AS TotalVehicles
    FROM dbo.EV_Population
    GROUP BY ModelYear
    ORDER BY ModelYear;
END;
GO

CREATE OR ALTER PROCEDURE sp_GetCityAnalytics
AS
BEGIN
    SET NOCOUNT ON;
    SELECT City, COUNT(*) AS TotalVehicles
    FROM dbo.EV_Population
    GROUP BY City
    ORDER BY TotalVehicles DESC;
END;
GO

CREATE OR ALTER PROCEDURE sp_GetRangeByMake
AS
BEGIN
    SET NOCOUNT ON;
    SELECT Make, AVG(ElectricRange) AS AvgRange
    FROM dbo.EV_Population
    WHERE ElectricRange > 0
    GROUP BY Make
    ORDER BY AvgRange DESC;
END;
GO
