import json
import requests
from typing import Optional

# Pixabay API key - you'll need to get one from https://pixabay.com/api/docs/
PIXABAY_API_KEY = "53267698-c01f2790dff42aed080dadb01"  # Get free key from pixabay.com/api/

# Mapping of listing IDs to specific Pixabay search queries for better matches
PIXABAY_SEARCH_QUERIES = {
    "listing_20251115_001": "python programming textbook",
    "listing_20251115_002": "biology textbook book",
    "listing_20251115_003": "chemistry textbook science",
    "listing_20251115_004": "calculus math textbook",
    "listing_20251115_005": "python programming pdf digital",
    "listing_20251115_006": "algorithms computer science book",
    "listing_20251115_007": "graphing calculator ti-84",
    "listing_20251115_008": "lab safety goggles",
    "listing_20251115_009": "iclicker classroom remote",
    "listing_20251115_010": "notebooks college ruled",
    "listing_20251115_011": "binders office supplies",
    "listing_20251115_012": "macbook air laptop",
    "listing_20251115_013": "ipad tablet apple pencil",
    "listing_20251115_014": "sony headphones wireless",
    "listing_20251115_015": "usb-c charging cable",
    "listing_20251115_016": "mechanical keyboard rgb",
    "listing_20251115_017": "usb flash drive storage",
    "listing_20251115_018": "lab coat white",
    "listing_20251115_019": "medical scrubs nurse",
    "listing_20251115_020": "engineering drawing kit tools",
    "listing_20251115_021": "art supplies paint brushes",
    "listing_20251115_022": "mini fridge dorm",
    "listing_20251115_023": "microwave oven compact",
    "listing_20251115_024": "desk lamp led usb",
    "listing_20251115_025": "tower fan oscillating",
    "listing_20251115_026": "bike lock u-lock",
    "listing_20251115_027": "study desk computer",
}


def get_pixabay_image(query: str) -> Optional[str]:
    """
    Fetch an image URL from Pixabay based on search query.
    Returns the URL of the best matching image.
    """
    try:
        params = {
            "key": PIXABAY_API_KEY,
            "q": query,
            "image_type": "photo",
            "per_page": 3,
            "order": "popular",
            "min_width": 500,
            "min_height": 500,
        }
        
        response = requests.get("https://pixabay.com/api/", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data["hits"]:
            # Get the first result (most popular)
            image_url = data["hits"][0]["largeImageURL"]
            return image_url
        else:
            print(f"  ⚠️  No results found for: {query}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error fetching from Pixabay for '{query}': {e}")
        return None


def update_listings_with_pixabay_images():
    """Read listings.json and update image_urls with Pixabay images."""
    
    # Read current listings
    try:
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
    except FileNotFoundError:
        print("❌ listings.json not found!")
        return
    
    print(f"🖼️  Fetching images from Pixabay for {len(listings)} listings...\n")
    
    updated_count = 0
    failed_count = 0
    
    for listing in listings:
        listing_id = listing.get("id")
        title = listing.get("title", "Unknown")
        
        # Get search query for this listing
        search_query = PIXABAY_SEARCH_QUERIES.get(listing_id, title)
        
        print(f"📍 {listing_id}: {title}")
        print(f"   Searching: '{search_query}'", end="")
        
        # Fetch image from Pixabay
        image_url = get_pixabay_image(search_query)
        
        if image_url:
            listing["image_url"] = image_url
            print(f" ✅")
            updated_count += 1
        else:
            print(f" ⚠️  Using fallback")
            # Try fallback with just the title
            image_url = get_pixabay_image(title)
            if image_url:
                listing["image_url"] = image_url
                updated_count += 1
            else:
                failed_count += 1
    
    # Save updated listings
    try:
        with open("data/listings.json", "w") as f:
            json.dump(listings, f, indent=2)
        print(f"\n✅ Updated listings.json")
        print(f"📊 Summary:")
        print(f"   Total listings: {len(listings)}")
        print(f"   Updated: {updated_count}")
        print(f"   Failed: {failed_count}")
    except Exception as e:
        print(f"❌ Error saving listings.json: {e}")


if __name__ == "__main__":
    if PIXABAY_API_KEY == "your_pixabay_api_key_here":
        print("❌ ERROR: You need to set your Pixabay API key!")
        print("\n📝 Steps to get a free Pixabay API key:")
        print("   1. Go to https://pixabay.com/api/")
        print("   2. Sign up for a free account")
        print("   3. Copy your API key")
        print("   4. Replace 'your_pixabay_api_key_here' in this script with your key")
        print("   5. Run the script again")
    else:
        update_listings_with_pixabay_images()
