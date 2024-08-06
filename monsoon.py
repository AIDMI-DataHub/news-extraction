from datetime import datetime, timedelta
import pygooglenews
import pytz
import csv
import os

def run_monsoon_script():
    gn = pygooglenews.GoogleNews(lang='en', country='India')

    # Get today's and yesterday's date
    today = datetime.utcnow()
    yesterday = today - timedelta(1)

    # Format dates as strings
    from_date = yesterday.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')
    from_time = "00:00:00"
    to_time = "23:59:59"

    # Combine date and time for the range
    from_datetime = f"{from_date} {from_time} GMT"
    to_datetime = f"{to_date} {to_time} GMT"

    states = ["andhra-pradesh", "arunachal-pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat", "haryana", "himachal-pradesh", "jharkhand", "karnataka", "kerala", "madhya-pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil-nadu", "telangana", "tripura", "uttar-pradesh", "uttarakhand", "west-bengal"]
    union_territories = ["andaman-and-nicobar-islands", "chandigarh", "dadra-and-nagar-haveli-and-daman-and-diu", "lakshadweep", "delhi", "puducherry", "jammu-and-kashmir", "ladakh"]

    for region in states + union_territories:
        query = f"Monsoon or rainfall in {region.replace('-', ' ')} 2024"
        print("query", query)
        try:
            results = gn.search(query=query, from_=from_date, to_=to_date)
            save_results(results, 'states' if region in states else 'union-territories', region, datetime.now(), from_datetime, to_datetime)
        except Exception as e:
            print(f"Error searching for {region}: {e}")

def save_results(results, region_type, region_name, current_date, from_datetime, to_datetime):
    year = current_date.year
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")
    path = f"data/{region_type}/{region_name}/Monsoon/{year}/{month}/{day}"
    os.makedirs(path, exist_ok=True)  # Ensuring the date folder exists
    file_path = os.path.join(path, 'results.csv')
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Date", "Source", "Summary", "Place"])

        for entry in results['entries']:
            if is_within_date_range(entry.published, from_datetime, to_datetime):
                title = entry.title
                link = entry.link
                date = convert_gmt_to_ist(entry.published)
                source = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else ""
                summary = entry.summary if hasattr(entry, 'summary') else ""
                place = ""  # Empty column for Place
                
                writer.writerow([title, link, date, source, summary, place])

    print(f"CSV file created successfully for {region_name}.")

def is_within_date_range(published_date, from_datetime, to_datetime):
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    pub_date = datetime.strptime(published_date, date_format)
    from_dt = datetime.strptime(from_datetime, "%Y-%m-%d %H:%M:%S %Z")
    to_dt = datetime.strptime(to_datetime, "%Y-%m-%d %H:%M:%S %Z")
    return from_dt <= pub_date <= to_dt

def convert_gmt_to_ist(gmt_datetime):
    gmt_format = "%a, %d %b %Y %H:%M:%S %Z"
    gmt_dt = datetime.strptime(gmt_datetime, gmt_format)
    gmt = pytz.timezone('GMT')
    ist = pytz.timezone('Asia/Kolkata')
    gmt_dt = gmt.localize(gmt_dt)
    ist_dt = gmt_dt.astimezone(ist)
    return ist_dt.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    run_monsoon_script()
