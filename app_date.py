import pygooglenews_date
gn = pygooglenews_date.GoogleNews_date()

# Search for articles related to "Heatwave" with a specific date
results_specific_date = gn.search(query="Heatwave", from_="2023-07-11", to_="2023-07-11")

# Search for articles related to "Heatwave" within a date range
results_date_range = gn.search(query="Heatwave", from_="2023-07-01", to_="2023-07-11")

# Search for articles related to "Heatwave" without date filtering
results_no_date = gn.search(query="Heatwave")

# Print results
for entry in results_specific_date['entries']:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Summary: {entry.summary}")
    print(f"Date: {entry.published}")
    if 'source' in entry:
        print(f"Source: {entry.source.title}")
    print("\n")
