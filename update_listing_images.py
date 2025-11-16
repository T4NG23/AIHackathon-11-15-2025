"""
Script to add free stock images to marketplace listings using Unsplash API
Images are fetched as public URLs (no API key needed for basic access)
"""

import json
import os

# Mapping of items to free image URLs from Unsplash (high-res, royalty-free)
# Using direct Unsplash URLs that don't require authentication
IMAGE_MAPPING = {
    "listing_20251115_001": "https://images.unsplash.com/photo-1507842217343-583f20270319?w=500&h=500&fit=crop",  # Python textbook
    "listing_20251115_002": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=500&h=500&fit=crop",  # Biology textbook
    "listing_20251115_003": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=500&h=500&fit=crop",  # Chemistry textbook
    "listing_20251115_004": "https://images.unsplash.com/photo-1507842217343-583f20270319?w=500&h=500&fit=crop",  # Calculus textbook
    "listing_20251115_005": "https://images.unsplash.com/photo-1507842217343-583f20270319?w=500&h=500&fit=crop",  # Python PDF
    "listing_20251115_006": "https://images.unsplash.com/photo-1507842217343-583f20270319?w=500&h=500&fit=crop",  # Algorithms textbook
    "listing_20251115_007": "https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=500&h=500&fit=crop",  # TI-84 Calculator
    "listing_20251115_008": "https://images.unsplash.com/photo-1576091160550-112173f7f869?w=500&h=500&fit=crop",  # Lab Goggles
    "listing_20251115_009": "https://images.unsplash.com/photo-1550355291-bbee04a92027?w=500&h=500&fit=crop",  # iClicker
    "listing_20251115_010": "https://images.unsplash.com/photo-1507842217343-583f20270319?w=500&h=500&fit=crop",  # Notebooks
    "listing_20251115_011": "https://images.unsplash.com/photo-1569163139394-de4798aa62b3?w=500&h=500&fit=crop",  # 3-Ring Binders
    "listing_20251115_012": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&h=500&fit=crop",  # MacBook Air M1
    "listing_20251115_013": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&h=500&fit=crop",  # iPad Air
    "listing_20251115_014": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop",  # Sony Headphones
    "listing_20251115_015": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=500&h=500&fit=crop",  # USB-C Charger
    "listing_20251115_016": "https://images.unsplash.com/photo-1587829191301-c8450a4b2fa6?w=500&h=500&fit=crop",  # Mechanical Keyboard
    "listing_20251115_017": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&h=500&fit=crop",  # USB Flash Drive
    "listing_20251115_018": "https://images.unsplash.com/photo-1576091160550-112173f7f869?w=500&h=500&fit=crop",  # Lab Coat
    "listing_20251115_019": "https://images.unsplash.com/photo-1631217314831-c6227db76b6e?w=500&h=500&fit=crop",  # Medical Scrubs
    "listing_20251115_020": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=500&h=500&fit=crop",  # Engineering Drawing Kit
    "listing_20251115_021": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500&h=500&fit=crop",  # Art Supplies
    "listing_20251115_022": "https://images.unsplash.com/photo-1584568694244-14fbbc50d688?w=500&h=500&fit=crop",  # Mini Fridge
    "listing_20251115_023": "https://images.unsplash.com/photo-1586985289688-cacf32ca6e87?w=500&h=500&fit=crop",  # Microwave
    "listing_20251115_024": "https://images.unsplash.com/photo-1565636192335-14bfc9b06b5a?w=500&h=500&fit=crop",  # Desk Lamp
    "listing_20251115_025": "https://images.unsplash.com/photo-1550355291-bbee04a92027?w=500&h=500&fit=crop",  # Tower Fan
    "listing_20251115_026": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=500&fit=crop",  # Bike Lock
    "listing_20251115_027": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&h=500&fit=crop",  # Study Desk
}

def update_listings_with_images():
    """Update listings.json with image URLs"""
    listings_file = 'data/listings.json'
    
    # Load current listings
    with open(listings_file, 'r') as f:
        listings = json.load(f)
    
    # Update each listing with image URL
    updated_count = 0
    for listing in listings:
        listing_id = listing.get('id')
        if listing_id in IMAGE_MAPPING:
            listing['image_url'] = IMAGE_MAPPING[listing_id]
            updated_count += 1
            print(f"✓ Updated {listing.get('title')} with image")
        else:
            print(f"⚠ No image found for {listing.get('id')}")
    
    # Save updated listings
    with open(listings_file, 'w') as f:
        json.dump(listings, f, indent=2)
    
    print(f"\n✓ Successfully updated {updated_count} listings with images")
    print(f"Images saved to: {listings_file}")

if __name__ == '__main__':
    update_listings_with_images()
