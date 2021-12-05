import discogs_client
import csv
import pathlib

user = "XX"

user_token = "XX"

client = discogs_client.Client('get_user_library/0.1', user_token=user_token)

fetch_user = client.user(user)

collection = fetch_user.collection_folders[0]

fieldnames = ["Artist(s)", "Album", "Year", "Format(s)", "Date added", "Rating", "Release URL"]

rows = []

item_count = 0

for item in collection.releases:
    new_value = {
        "Artist(s)": ", ".join(artist.name for artist in item.release.artists),
        "Album": item.release.title,
        "Year": item.release.year,
        "Format(s)": ", ".join(format["name"] for format in item.release.formats),
        "Date added": item.date_added.isoformat(),
        "Rating": item.rating,
        "Release URL": item.release.url,
        #"Lowest price": str(item.release.marketplace_stats.lowest_price.value) + item.release.marketplace_stats.lowest_price.currency
    }
    rows.append(new_value)
    item_count+=1
    print(f"Item {item_count}/{collection.releases.count}")


with open(pathlib.Path.home().joinpath("test", user+".csv"), 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)