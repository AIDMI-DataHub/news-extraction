# language_map.py

def get_language_for_region(region_name: str) -> str:
    """
    Returns the local language code for a given Indian state/UT.
    We'll also use 'en' for states or UTs that do not have a well-supported code in Google News.
    """
    language_mapping = {
        "andhra-pradesh": "te",    # Telugu
        "arunachal-pradesh": "en", # fallback to English
        "assam": "as",
        "bihar": "hi",
        "chhattisgarh": "hi",
        "goa": "en",              # 'gom' is not well supported
        "gujarat": "gu",
        "haryana": "hi",
        "himachal-pradesh": "hi",
        "jharkhand": "hi",
        "karnataka": "kn",
        "kerala": "ml",
        "madhya-pradesh": "hi",
        "maharashtra": "mr",
        "manipur": "en",
        "meghalaya": "en",
        "mizoram": "en",
        "nagaland": "en",
        "odisha": "or",
        "punjab": "pa",
        "rajasthan": "hi",
        "sikkim": "en",
        "tamil-nadu": "ta",
        "telangana": "te",
        "tripura": "en",
        "uttar-pradesh": "hi",
        "uttarakhand": "hi",
        "west-bengal": "bn",
        "andaman-and-nicobar-islands": "en",
        "chandigarh": "hi",
        "dadra-and-nagar-haveli-and-daman-and-diu": "gu",
        "lakshadweep": "en",
        "delhi": "hi",
        "puducherry": "ta",
        "jammu-and-kashmir": "en",
        "ladakh": "en",
    }
    return language_mapping.get(region_name, "en")