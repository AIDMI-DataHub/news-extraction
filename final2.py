import pygooglenews
from datetime import datetime, timedelta
import pytz
import csv

# Initialize GoogleNews object
gn = pygooglenews.GoogleNews()

# Define search parameters
search_query = "Assam Floods"

# Define date range
use_specific_date = True  # Set to False if you want to use a date range

# If using specific date, set specific_date and ensure from_date and to_date are None
specific_date = "2024-07-19" if use_specific_date else None
from_date = None
to_date = None

# If using a date range, set from_date and to_date and ensure specific_date is None
# Example for date range:
# from_date = "2024-07-18"
# to_date = "2024-07-19"
# specific_date = None

# Search for articles within the date range
if use_specific_date:
    results = gn.search(query=search_query, from_=specific_date, to_=specific_date)
else:
    results = gn.search(query=search_query, from_=from_date, to_=to_date)

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
        title = entry.title
        link = entry.link
        date = convert_gmt_to_ist(entry.published)
        source = entry.source.title if 'source' in entry else ""
        summary = ""  # Empty column for Summary
        place = ""  # Empty column for Place
        
        # Write the article details to the CSV
        writer.writerow([title, link, date, source, summary, place])

print("CSV file created successfully.")
