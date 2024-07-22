import pygooglenews
from datetime import datetime, timedelta
import pytz
import csv

# Initialize GoogleNews object
gn = pygooglenews.GoogleNews()

# Define search parameters
search_query = "Assam Floods"

# Set to False if you want to use a date range
use_specific_date = False  

# If using a specific date, set specific_date and ensure from_date and to_date are None
specific_date = None

from_date = "2024-07-18"  # Previous day for GMT time conversion
to_date = "2024-07-19"
from_time = "18:30:00"  # 00:00 IST on July 19 in GMT
to_time = "06:30:00"  # 12:00 IST on July 19 in GMT

# Combine date and time for the range
from_datetime = f"{from_date} {from_time} GMT"
to_datetime = f"{to_date} {to_time} GMT"

# Search for articles within the date range
results = gn.search(query=search_query, from_=from_date, to_=to_date)

# Function to check if the published date is within the specified date range
def is_within_date_range(published_date, from_datetime, to_datetime):
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    pub_date = datetime.strptime(published_date, date_format)
    from_dt = datetime.strptime(from_datetime, "%Y-%m-%d %H:%M:%S %Z")
    to_dt = datetime.strptime(to_datetime, "%Y-%m-%d %H:%M:%S %Z")
    return from_dt <= pub_date <= to_dt

# Function to convert GMT to IST in "YYYY-MM-DD HH:MM:SS" format
def convert_gmt_to_ist(gmt_datetime):
    gmt_format = "%a, %d %b %Y %H:%M:%S %Z"
    gmt_dt = datetime.strptime(gmt_datetime, gmt_format)
    gmt = pytz.timezone('GMT')
    ist = pytz.timezone('Asia/Kolkata')
    gmt_dt = gmt.localize(gmt_dt)
    ist_dt = gmt_dt.astimezone(ist)
    return ist_dt.strftime("%Y-%m-%d %H:%M:%S")

# Define the CSV file name
csv_file_name = "articles.csv"

# Write the filtered articles to the CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Title", "Link", "Date", "Source", "Summary", "Place"])

    for entry in results['entries']:
        if is_within_date_range(entry.published, from_datetime, to_datetime):
            title = entry.title
            link = entry.link
            date = convert_gmt_to_ist(entry.published)
            source = entry.source.title if 'source' in entry else ""
            summary = ""  # Empty column for Summary
            place = ""  # Empty column for Place
            
            # Write the article details to the CSV
            writer.writerow([title, link, date, source, summary, place])

print("CSV file created successfully.")
