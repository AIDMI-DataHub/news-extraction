# heatwave.py
from datetime import datetime, timedelta
import pytz
import os
import pandas as pd
import time
import pygooglenews

from language_map import get_language_for_region  # <-- import your helper

def run_heatwave_script():
    today = datetime.utcnow()
    yesterday = today - timedelta(1)

    from_date = yesterday.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    current_year = datetime.now().year

    # Define multiple search terms for heat/heatwave
    heat_terms = [
        "heat", 
        "heatwave", 
        "heatstroke", 
        "humidity", 
        "heat exhaustion", 
        "hot weather"
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
        "dadra-and-nagar-haveli-and-daman-and-diu",
        "lakshadweep", "delhi", "puducherry", 
        "jammu-and-kashmir", "ladakh"
    ]

    for region in states + union_territories:
        region_lang = get_language_for_region(region)

        # We'll do a 2-pass search: once in local language, once in English
        for lang_code in [region_lang, "en"]:
            gn = pygooglenews.GoogleNews(lang=lang_code, country='IN')

            # Build the query using OR for multiple heat terms
            # e.g. "(heat OR heatwave OR heatstroke OR ... ) in {region}"
            query_string = ' OR '.join(heat_terms)
            query = f"({query_string}) in {region.replace('-', ' ')}"
            
            print("🔍 Query:", query, "| Language:", lang_code)

            all_entries = []
            try:
                results = gn.search(query=query, from_=from_date, to_=to_date)
                print(f"🛠 Debug: Raw results for '{query}' in [{lang_code}]: {results}")

                if not results or 'entries' not in results or not results['entries']:
                    print(f"⚠ No results found for {query} in [{lang_code}].")
                    continue

                print(f"✅ Found {len(results['entries'])} articles for {region} in [{lang_code}]")
                all_entries.extend(extract_results(results, "Heatwave", lang_code))

            except Exception as e:
                print(f"❌ Error searching for {region} in [{lang_code}]: {e}")

            if all_entries:
                save_results(all_entries, 
                             'states' if region in states else 'union-territories', 
                             region, 
                             datetime.now())
            else:
                print(f"⚠ No articles saved for {region} in [{lang_code}].")

            time.sleep(2)  # Adjust as needed to reduce blocking

def extract_results(results, term, lang_code):
    extracted_entries = []
    for entry in results.get('entries', []):
        title = entry.title
        link = entry.link
        date = convert_gmt_to_ist(entry.published)

        source = ""
        if hasattr(entry, 'source') and hasattr(entry.source, 'title'):
            source = entry.source.title

        summary = entry.summary if hasattr(entry, 'summary') else ""

        extracted_entries.append([
            title,         # Title
            link,          # Link
            date,          # Date (converted to IST)
            source,        # Source
            summary,       # Summary
            term,          # e.g. "Heatwave"
            lang_code      # LanguageQueried
        ])
    
    return extracted_entries

def save_results(all_entries, region_type, region_name, current_date):
    if not all_entries:
        return

    year = current_date.year
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")

    path = f"data/{region_type}/{region_name}/Heatwave/{year}/{month}/{day}"
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, 'results.csv')

    columns = ["Title", "Link", "Date", "Source", "Summary", "Term", "LanguageQueried"]
    df = pd.DataFrame(all_entries, columns=columns)

    # Append to the CSV; write header only if the file doesn't exist
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

    print(f"✅ CSV file updated for Heatwave in {region_name}.")

def convert_gmt_to_ist(gmt_datetime):
    gmt_format = "%a, %d %b %Y %H:%M:%S %Z"
    gmt = pytz.timezone('GMT')
    ist = pytz.timezone('Asia/Kolkata')

    try:
        gmt_dt = datetime.strptime(gmt_datetime, gmt_format)
        gmt_dt = gmt.localize(gmt_dt)  # attach GMT tz
        ist_dt = gmt_dt.astimezone(ist)
        return ist_dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return gmt_datetime

if __name__ == "__main__":
    run_heatwave_script()
    