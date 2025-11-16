import json

with open('data/listings.json', 'r') as f:
    listings = json.load(f)

missing = [l for l in listings if not l.get('image_url')]
has_images = len([l for l in listings if l.get('image_url')])

print(f'Total listings: {len(listings)}')
print(f'With images: {has_images}')
print(f'Missing images: {len(missing)}')

if missing:
    print('\nMissing images:')
    for item in missing:
        print(f'  - {item["id"]}: {item["title"]}')
