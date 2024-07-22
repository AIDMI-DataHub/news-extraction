import pygooglenews
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import pytz

# Initialize GoogleNews object
gn = pygooglenews.GoogleNews()

# Define the date range
from_date = "2024-07-18"
to_date = "2024-07-19"
from_time = "07:00:00"
to_time = "07:00:00"

# Combine date and time for the range
from_datetime = f"{from_date} {from_time} GMT"
to_datetime = f"{to_date} {to_time} GMT"

# Search for articles related to "Monsoon India" within a date range
results_date_range = gn.search(query="Monsoon India", from_=from_date, to_=to_date)

# Function to check if the published date is within the specified date range
def is_within_date_range(published_date, from_datetime, to_datetime):
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    pub_date = datetime.strptime(published_date, date_format)
    from_dt = datetime.strptime(from_datetime, "%Y-%m-%d %H:%M:%S %Z")
    to_dt = datetime.strptime(to_datetime, "%Y-%m-%d %H:%M:%S %Z")
    print(f"Checking article published on {pub_date} against range {from_dt} to {to_dt}")
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

# Create the root XML element
root = ET.Element("articles")

# Add filtered articles to the XML
for entry in results_date_range['entries']:
    print(f"Article published on {entry.published}")
    if is_within_date_range(entry.published, from_datetime, to_datetime):
        article = ET.SubElement(root, "article")
        
        title = ET.SubElement(article, "title")
        title.text = entry.title
        
        link = ET.SubElement(article, "link")
        link.text = entry.link
        
        date = ET.SubElement(article, "date")
        date.text = convert_gmt_to_ist(entry.published)
        
        if 'source' in entry:
            source = ET.SubElement(article, "source")
            source.text = entry.source.title
    else:
        print(f"Article {entry.title} not within date range.")

# Write the XML to a file
tree = ET.ElementTree(root)
with open("articles.xml", "wb") as xml_file:
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

print("XML file created successfully.")
