from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from database.database import get_db

app = FastAPI(
    title="EV Market Intelligence API",
    description="Enterprise-grade API for querying Electric Vehicle population data and market trends.",
    version="1.1.0",
    contact={
        "name": "Data Analytics Team",
        "email": "analytics@example.com",
    },
)

# --- Response Models for Documentation ---
class VehicleRecord(BaseModel):
    VIN: str
    Make: str
    Model: str
    ModelYear: int
    City: str
    ElectricRange: float
    # Add other fields as needed based on DB schema

class AnalyticsResponse(BaseModel):
    data: List[Dict[str, Any]]

@app.get("/vehicles", response_model=AnalyticsResponse, tags=["Data Exploration"])
def get_vehicles(
    db: Session = Depends(get_db), 
    skip: int = Query(0, description="Number of records to skip", ge=0), 
    limit: int = Query(100, description="Max number of records to return", ge=1, le=1000),
    make: Optional[str] = Query(None, description="Filter by vehicle manufacturer")
):
    """
    Retrieve a paginated list of vehicles from the database.
    Useful for raw data exploration and filtering.
    """
    try:
        query = "SELECT * FROM dbo.EV_Population"
        if make:
            query += f" WHERE Make = '{make}'"
        query += f" ORDER BY VehicleID OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY"
        
        result = db.execute(text(query)).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Query Error: {str(e)}")

@app.get("/analytics/trends", response_model=AnalyticsResponse, tags=["Market Intelligence"])
def get_trends(db: Session = Depends(get_db)):
    """
    Returns yearly adoption trends, showing the total number of vehicles registered per year.
    Used to visualize the growth trajectory of the EV market.
    """
    try:
        result = db.execute(text("SELECT ModelYear, TotalVehicles FROM vw_YearlyTrend ORDER BY ModelYear")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/brands", response_model=AnalyticsResponse, tags=["Market Intelligence"])
def get_brands(db: Session = Depends(get_db), limit: int = Query(10, description="Number of top brands to return")):
    """
    Retrieves the top N EV brands by registration volume.
    Helps identify market leaders and brand dominance.
    """
    try:
        result = db.execute(text(f"EXEC sp_GetTopBrands @TopN={limit}")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/models", response_model=AnalyticsResponse, tags=["Market Intelligence"])
def get_models(db: Session = Depends(get_db)):
    """
    Returns the top 10 EV models across all manufacturers.
    Provides insight into which specific vehicle models are most popular.
    """
    try:
        query = """
        SELECT TOP 10 Model, COUNT(*) AS TotalVehicles 
        FROM dbo.EV_Population 
        GROUP BY Model 
        ORDER BY TotalVehicles DESC
        """
        result = db.execute(text(query)).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/cities", response_model=AnalyticsResponse, tags=["Geographic Insights"])
def get_cities(db: Session = Depends(get_db)):
    """
    Aggregates vehicle registration counts by city.
    Useful for identifying geographic hotspots for EV adoption.
    """
    try:
        result = db.execute(text("EXEC sp_GetCityAnalytics")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/range", response_model=AnalyticsResponse, tags=["Technical Specs"])
def get_range(db: Session = Depends(get_db)):
    """
    Calculates the average electric range for each manufacturer.
    Used to compare technical performance across brands.
    """
    try:
        result = db.execute(text("EXEC sp_GetRangeByMake")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/cafv", response_model=AnalyticsResponse, tags=["Policy Insights"])
def get_cafv(db: Session = Depends(get_db)):
    """
    Returns counts of vehicles based on their Clean Alternative Fuel Vehicle (CAFV) eligibility.
    Highlights the impact of government incentives on the vehicle population.
    """
    try:
        query = """
        SELECT CAFVEligibility, COUNT(*) AS TotalVehicles
        FROM dbo.EV_Population
        GROUP BY CAFVEligibility
        """
        result = db.execute(text(query)).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
