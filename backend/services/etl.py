import pandas as pd
import numpy as np
import pyodbc
import re
import os

def clean_data(input_path: str, output_path: str) -> pd.DataFrame:
    print(f"Reading data from {input_path}...")
    df = pd.read_csv(input_path)

    print("Cleaning columns...")
    # Standardize column names
    df.columns = [re.sub(r'[^a-zA-Z0-9]', '', col) for col in df.columns]
    
    print("Removing duplicates...")
    df = df.drop_duplicates()
    
    print("Handling missing values...")
    df.fillna({
        'County': 'Unknown',
        'City': 'Unknown',
        'State': 'Unknown',
        'PostalCode': '00000',
        'Make': 'Unknown',
        'Model': 'Unknown',
        'VehicleType': 'Unknown',
        'CAFVEligibility': 'Unknown',
        'ElectricUtility': 'Unknown',
        'LegislativeDistrict': -1,
        'CensusTract': 'Unknown',
        'ElectricRange': 0.0,
        'ModelYear': 0,
        'VehicleLocation': 'POINT(0 0)'
    }, inplace=True)
    
    print("Cleaning Data Types...")
    df['PostalCode'] = df['PostalCode'].astype(str).str.replace(r'\.0$', '', regex=True)
    df['ModelYear'] = df['ModelYear'].astype(int)
    df['ElectricRange'] = df['ElectricRange'].astype(float)
    
    print("Extracting Latitude and Longitude...")
    def extract_lat_lon(loc):
        if pd.isna(loc) or 'POINT' not in str(loc):
            return 0.0, 0.0
        match = re.search(r'POINT \(([-\d\.]+) ([-\d\.]+)\)', str(loc))
        if match:
            return float(match.group(2)), float(match.group(1)) # lat, lon
        return 0.0, 0.0

    df[['Latitude', 'Longitude']] = df.apply(lambda row: pd.Series(extract_lat_lon(row['VehicleLocation'])), axis=1)
    df = df.drop(columns=['VehicleLocation'], errors='ignore')
    
    print("Filtering invalid records...")
    df = df[(df['ModelYear'] > 1900) & (df['ModelYear'] <= 2100)]
    
    print(f"Saving cleaned data to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    return df

def load_to_sql_server(df: pd.DataFrame, connection_string: str):
    print("Connecting to SQL Server...")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    print("Loading data into EV_Population table...")
    insert_query = """
    INSERT INTO dbo.EV_Population (
        VIN, County, City, State, PostalCode, ModelYear, Make, Model, 
        VehicleType, CAFVEligibility, ElectricRange, LegislativeDistrict, 
        Latitude, Longitude, ElectricUtility, CensusTract
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    batch_size = 1000
    records = []
    
    for index, row in df.iterrows():
        records.append((
            str(row.get('VIN110', row.get('VIN', ''))),
            str(row['County'])[:100],
            str(row['City'])[:100],
            str(row['State'])[:50],
            str(row['PostalCode'])[:20],
            int(row['ModelYear']),
            str(row['Make'])[:100],
            str(row['Model'])[:100],
            str(row['VehicleType'])[:100],
            str(row['CAFVEligibility'])[:255],
            float(row['ElectricRange']),
            int(row['LegislativeDistrict']),
            float(row['Latitude']),
            float(row['Longitude']),
            str(row['ElectricUtility'])[:255],
            str(row['CensusTract'])[:50]
        ))
        
        if len(records) >= batch_size:
            cursor.executemany(insert_query, records)
            conn.commit()
            records = []
            
    if records:
        cursor.executemany(insert_query, records)
        conn.commit()
        
    print("Data loaded successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    raw_path = "../../data/raw/Electric_Vehicle_Population_Data.csv"
    processed_path = "../../data/processed/cleaned_ev_data.csv"
    # Set to SQL Authentication if needed: 'Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=EVAnalyticsDB;UID=user;PWD=password;'
    conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=EVAnalyticsDB;Trusted_Connection=yes;"
    
    try:
        if os.path.exists(raw_path):
            cleaned_df = clean_data(raw_path, processed_path)
            load_to_sql_server(cleaned_df, conn_str)
        else:
            print(f"File not found: {raw_path}")
            print("Please place the Electric_Vehicle_Population_Data.csv file in the data/raw/ directory.")
    except Exception as e:
        print(f"ETL process failed: {e}")
