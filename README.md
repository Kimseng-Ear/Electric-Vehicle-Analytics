# Electric Vehicle Population Analytics & Market Intelligence Dashboard

## Project Overview
This project is a complete, enterprise-grade, production-ready full-stack Data Analytics platform that analyzes Electric Vehicle (EV) Population Data. It includes a Python ETL pipeline, Microsoft SQL Server database design, advanced SQL analytics, a FastAPI backend, and an interactive Streamlit dashboard. 

Perfect for Data Analysts, BI Analysts, Data Engineers, and Full Stack Developers.

## Architecture
- **Data Ingestion & ETL**: Python (Pandas) scripts to clean and transform raw CSV data, validating data types and handling missing values, before loading it directly into Microsoft SQL Server using `pyodbc`.
- **Database**: Microsoft SQL Server (`EVAnalyticsDB`) utilizing normalized tables, views, stored procedures, CTEs, window functions, and optimized clustered/non-clustered indexes.
- **Backend API**: FastAPI serving endpoints to the frontend, abstracting SQL complexity and providing scalable data access.
- **Frontend Dashboard**: Streamlit web application providing dynamic data visualization and filtering (KPI cards, bar charts, area charts, pies) powered by Plotly.

## Folder Structure
```
ev-analytics-dashboard/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── database/
│
├── sql_server/
│   ├── schema.sql
│   ├── stored_procedures.sql
│   ├── views.sql
│   ├── analytics_queries.sql
│
├── dashboard/
│   ├── main.py
│   ├── pages/
│
├── notebooks/
│   ├── exploratory_analysis.ipynb
│
├── reports/
│
├── requirements.txt
├── README.md
```

## SQL Server Setup
1. Ensure Microsoft SQL Server and SSMS are installed.
2. Connect to your SQL Server instance via SSMS.
3. Run `sql_server/schema.sql` to generate `EVAnalyticsDB` and the core tables/indexes.
4. Run `sql_server/views.sql` and `sql_server/stored_procedures.sql` to install the data objects.
5. `sql_server/analytics_queries.sql` contains business intelligence queries (e.g., Year-over-Year Growth Rate, CAFV Eligibility) using CTEs and window functions.

## Python ETL Workflow
1. Place the `Electric_Vehicle_Population_Data.csv` file inside the `data/raw/` directory.
2. Make sure your Python environment has the necessary dependencies (`pip install -r requirements.txt`).
3. Run the ETL pipeline script to clean data and import it to SQL Server:
   ```bash
   cd backend/services
   python etl.py
   ```
   *Note: Modify `conn_str` inside `etl.py` if your SQL Server instance uses SQL Authentication or a different server name.*

## Running the Application
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Backend API (FastAPI):
   ```bash
   cd backend
   python app.py
   # API will run on http://localhost:8000
   ```
3. Start the Dashboard (Streamlit):
   ```bash
   cd dashboard
   streamlit run main.py
   # Dashboard will open at http://localhost:8501
   ```

## Business Insights Provided
- **Yearly EV Growth Trend**: Tracking total adoption and calculating Year-over-Year Growth.
- **Brand & Model Performance**: Identifying top manufacturers and market share breakdowns.
- **Geographic Distribution**: Pinpointing high-adoption cities and zip clustering.
- **CAFV Eligibility**: Visualizing clean alternative fuel eligibility.

## Power BI Integration (Bonus Step)
This project is designed to easily integrate with **Power BI**. 
1. Open Power BI Desktop and select **Get Data -> SQL Server**.
2. Enter your server credentials and connect to `EVAnalyticsDB`.
3. Select `vw_YearlyTrend`, `vw_TopBrands`, and `vw_CityDistribution`.
4. Build interactive reports with native DAX measures and Slicers.

## Future Improvements
- Deploy the database on Azure SQL.
- Containerize the backend and dashboard using Docker.
- Create automated scheduled runs for the ETL process using Apache Airflow.
