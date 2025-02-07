# utils.py
import os
from datetime import datetime
import calendar

def create_folders():
    base_path = 'data'
    states = [
        "andhra-pradesh", "arunachal-pradesh", "assam", "bihar", 
        "chhattisgarh", "goa", "gujarat", "haryana", "himachal-pradesh", 
        "jharkhand", "karnataka", "kerala", "madhya-pradesh", "maharashtra", 
        "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab", 
        "rajasthan", "sikkim", "tamil-nadu", "telangana", "tripura", 
        "uttar-pradesh", "uttarakhand", "west-bengal"
    ]
    union_territories = [
        "andaman-and-nicobar-islands", "chandigarh", 
        "dadra-and-nagar-haveli-and-daman-and-diu", "lakshadweep", "delhi", 
        "puducherry", "jammu-and-kashmir", "ladakh"
    ]
    
    climate_events = ["Monsoon", "Heatwave", "Disasters"]
    year = datetime.now().year

    # Create subfolders for each state/UT, event, year, month, day
    for state in states:
        for event in climate_events:
            for month in range(1, 13):
                days_in_month = calendar.monthrange(year, month)[1]
                for day in range(1, days_in_month + 1):
                    os.makedirs(f"{base_path}/states/{state}/{event}/{year}/{month:02d}/{day:02d}", exist_ok=True)

    for ut in union_territories:
        for event in climate_events:
            for month in range(1, 13):
                days_in_month = calendar.monthrange(year, month)[1]
                for day in range(1, days_in_month + 1):
                    os.makedirs(f"{base_path}/union-territories/{ut}/{event}/{year}/{month:02d}/{day:02d}", exist_ok=True)

if __name__ == "__main__":
    create_folders()
