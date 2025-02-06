# disasters.py
from datetime import datetime, timedelta
import pytz
import os
import pandas as pd
import time
import pygooglenews

from language_map import get_language_for_region  # Import helper function

def run_disaster_script():
    today = datetime.utcnow()
    yesterday = today - timedelta(1)

    from_date = yesterday.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    # Multiple search terms for disaster-related news
    disaster_terms = [
        "Cyclone", "Typhoon", "Flood", "Earthquake", 
        "Wildfire", "Hurricane", "Landslide", "Tsunami", 
        "Drought", "Severe Storm"
    ]

    states = [
        "andhra-pradesh", "arunachal-pradesh", "assam", "bihar", "chhattisgarh", 
        "goa", "gujarat", "haryana", "himachal-pradesh", "jharkhand", "karnataka", 
        "kerala", "madhya-pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", 
        "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil-nadu", 
        "telangana", "tripura", "uttar-pradesh", "uttarakhand", "west-bengal"
    ]
    union_territories = [
        "andaman-and-nicobar-islands", "chandigarh", 
        "dadra-and-nagar-haveli-and-daman-and-diu", "lakshadweep", "delhi", 
        "puducherry", "jammu-and-kashmir", "ladakh"
    ]

    for region in states + union_territories:
        region_lang = get_language_for_region(region)

        for lang_code in [region_lang, "en"]:
            gn = pygooglenews.GoogleNews(lang=lang_code, country='IN')

            query_string = ' OR '.join(disaster_terms)
            query = f"({query_string}) in {region.replace('-', ' ')}"
            
            print(f"🔍 Query: {query} | Language: {lang_code}")

            all_entries = []
            try:
                results = gn.search(query=query, from_=from_date, to_=to_date)

                if not results or 'entries' not in results or not results['entries']:
                    print(f"⚠ No results found for {query} in [{lang_code}].")
                    continue

                entries = extract_results(results, "Disaster", lang_code)
                all_entries.extend(entries)

            except Exception as e:
                print(f"❌ Error searching for {region} in [{lang_code}]: {e}")

            if all_entries:
                save_results(all_entries, 'states' if region in states else 'union-territories', region, datetime.now())

            time.sleep(2)

def extract_results(results, term, lang_code):
    extracted_entries = []
    for entry in results.get('entries', []):
        title = entry.title
        link = entry.link
        date = convert_gmt_to_ist(entry.published)

        source = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else ""
        summary = entry.summary if hasattr(entry, 'summary') else ""

        extracted_entries.append([title, link, date, source, summary, term, lang_code])
    
    return extracted_entries

def save_results(all_entries, region_type, region_name, current_date):
    if not all_entries:
        return

    path = f"data/{region_type}/{region_name}/Heatwave/{current_date.year}/{current_date.strftime('%m')}/{current_date.strftime('%d')}"
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, 'results.csv')

    columns = ["Title", "Link", "Date", "Source", "Summary", "Term", "LanguageQueried"]
    df = pd.DataFrame(all_entries, columns=columns)

    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
    print(f"✅ CSV updated for Heatwave in {region_name}.")

def convert_gmt_to_ist(gmt_datetime):
    try:
        gmt_format = "%a, %d %b %Y %H:%M:%S %Z"
        gmt = pytz.timezone('GMT')
        ist = pytz.timezone('Asia/Kolkata')
        gmt_dt = datetime.strptime(gmt_datetime, gmt_format)
        gmt_dt = gmt.localize(gmt_dt)
        return gmt_dt.astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return gmt_datetime

if __name__ == "__main__":
    run_heatwave_script()
