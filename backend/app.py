from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from database.database import get_db

app = FastAPI(title="EV Analytics API", version="1.0")

@app.get("/vehicles")
def get_vehicles(
    db: Session = Depends(get_db), 
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000),
    make: Optional[str] = None
):
    try:
        query = "SELECT * FROM dbo.EV_Population"
        if make:
            query += f" WHERE Make = '{make}'"
        query += f" ORDER BY VehicleID OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY"
        
        result = db.execute(text(query)).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/trends")
def get_trends(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT ModelYear, TotalVehicles FROM vw_YearlyTrend ORDER BY ModelYear")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/brands")
def get_brands(db: Session = Depends(get_db), limit: int = 10):
    try:
        result = db.execute(text(f"EXEC sp_GetTopBrands @TopN={limit}")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/models")
def get_models(db: Session = Depends(get_db)):
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

@app.get("/analytics/cities")
def get_cities(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("EXEC sp_GetCityAnalytics")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/range")
def get_range(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("EXEC sp_GetRangeByMake")).fetchall()
        return {"data": [dict(row._mapping) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/cafv")
def get_cafv(db: Session = Depends(get_db)):
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
