CREATE DATABASE EVAnalyticsDB;
GO

USE EVAnalyticsDB;
GO

CREATE TABLE dbo.EV_Population (
    VehicleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    VIN NVARCHAR(20) NOT NULL,
    County NVARCHAR(100),
    City NVARCHAR(100),
    State NVARCHAR(50),
    PostalCode NVARCHAR(20),
    ModelYear INT CHECK (ModelYear >= 1990 AND ModelYear <= 2100),
    Make NVARCHAR(100),
    Model NVARCHAR(100),
    VehicleType NVARCHAR(100),
    CAFVEligibility NVARCHAR(255),
    ElectricRange FLOAT CHECK (ElectricRange >= 0),
    LegislativeDistrict INT,
    Latitude FLOAT,
    Longitude FLOAT,
    ElectricUtility NVARCHAR(255),
    CensusTract NVARCHAR(50)
);
GO

-- Create indexes for performance optimization
CREATE CLUSTERED INDEX CIX_EV_Population_ModelYear ON dbo.EV_Population(ModelYear) 
WITH (DROP_EXISTING = OFF);
GO

CREATE NONCLUSTERED INDEX NCIX_EV_Population_Make ON dbo.EV_Population(Make);
CREATE NONCLUSTERED INDEX NCIX_EV_Population_City ON dbo.EV_Population(City);
CREATE NONCLUSTERED INDEX NCIX_EV_Population_VehicleType ON dbo.EV_Population(VehicleType);
GO
