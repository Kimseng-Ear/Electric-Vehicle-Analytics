from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib

# Using pyodbc driver with Trusted Connection
server = 'localhost'
database = 'EVAnalyticsDB'
driver = 'ODBC Driver 17 for SQL Server'

# SQL Authentication Option (uncomment if needed)
# uid = 'your_username'
# pwd = 'your_password'
# params = urllib.parse.quote_plus(f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={uid};PWD={pwd};")

# Trusted Connection Option
params = urllib.parse.quote_plus(f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;")

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
