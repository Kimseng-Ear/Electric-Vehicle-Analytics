import pandas as pd
import numpy as np
import random

num_records = 500

makes_models = {
    'Tesla': ['Model 3', 'Model Y', 'Model S', 'Model X'],
    'Nissan': ['Leaf', 'Ariya'],
    'Chevrolet': ['Bolt EV', 'Volt'],
    'Ford': ['Mustang Mach-E', 'F-150 Lightning'],
    'Audi': ['e-tron', 'Q4 e-tron']
}

cities_counties = {
    'Seattle': 'King',
    'Bellevue': 'King',
    'Portland': 'Multnomah',
    'San Francisco': 'San Francisco',
    'Los Angeles': 'Los Angeles'
}

data = {
    'VIN (1-10)': ['1N4AZ1CP' + str(i) for i in range(num_records)],
    'County': [],
    'City': [],
    'State': ['WA'] * num_records,
    'Postal Code': [str(random.randint(90000, 99999)) for _ in range(num_records)],
    'Model Year': [random.randint(2015, 2024) for _ in range(num_records)],
    'Make': [],
    'Model': [],
    'Vehicle Type': [random.choice(['Battery Electric Vehicle (BEV)', 'Plug-in Hybrid Electric Vehicle (PHEV)']) for _ in range(num_records)],
    'CAFV Eligibility': ['Clean Alternative Fuel Vehicle Eligible'] * num_records,
    'Electric Range': [random.randint(50, 300) for _ in range(num_records)],
    'Base MSRP': [0] * num_records,
    'Legislative District': [random.randint(1, 49) for _ in range(num_records)],
    'DOL Vehicle ID': [random.randint(100000000, 999999999) for _ in range(num_records)],
    'Vehicle Location': [f"POINT ({-122.0 + random.uniform(-1, 1)} {47.0 + random.uniform(-1, 1)})" for _ in range(num_records)],
    'Electric Utility': ['CITY OF SEATTLE - (WA)|CITY OF TACOMA - (WA)'] * num_records,
    'Census Tract': ['53033000000'] * num_records
}

for _ in range(num_records):
    city = random.choice(list(cities_counties.keys()))
    county = cities_counties[city]
    data['City'].append(city)
    data['County'].append(county)
    
    make = random.choice(list(makes_models.keys()))
    model = random.choice(makes_models[make])
    data['Make'].append(make)
    data['Model'].append(model)

df = pd.DataFrame(data)
df.to_csv('Electric_Vehicle_Population_Data.csv', index=False)
print("Dummy data generated.")
