import requests
from bs4 import BeautifulSoup
import json
import os
from PIL import Image
from io import BytesIO

URL = "https://www.discogs.com/lists/1001-albums-you-must-hear-before-you-die/18222?limit=250"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

# Create images directory if it doesn't exist
if not os.path.exists('imgs'):
    os.makedirs('imgs')
index=0


try:
    with open('db.json', 'r') as file:
        recup_data = json.load(file)
    final_db = recup_data['list']
    page_start = recup_data['page']
    index_lim = recup_data['index']
    print("FOUND BACKUP")
    if index_lim == 0:
        raise Exception("INDEX 0 ERROR")
except FileNotFoundError:
    print("NO ERROR DATA FOUND")
    final_db = []
    index_lim = -1
    page_start = 1

for page in range(page_start, 5):
    response = requests.get(URL + f"&page={page}", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    list_items = soup.select("ol#listitems > li.listitem")

    for index, item in enumerate(list_items, start=1):
        if index < index_lim:
            print(f"skipped p{page} | {index}")
            continue

        info_dict = {}

        img = item.select_one("img")
        img_src = img['src']
        entry_name = img['alt'].replace('/', '|')

        # Save image
        img_response = requests.get(img_src, headers=headers)
        img_data = Image.open(BytesIO(img_response.content))
        filename = f"imgs/{entry_name}.jpeg"
        img_data.save(filename)

        artist, album = img['alt'].split(" - ", 1)
        info_dict['Index'] = index
        info_dict['Album'] = album
        info_dict['Artist'] = artist

        # Now get link
        link = item.select_one("a.thumbnail_link")['href']

        # Fetch album details page
        album_response = requests.get(link, headers=headers)
        album_soup = BeautifulSoup(album_response.content, 'html.parser')

        # Extract album details
        table = album_soup.select_one(".table_1fWaB")
        tracklist = [row.select_one('span').text for row in album_soup.select("//*[starts-with(@class, 'tracklist_')] tr") if row.select_one('span')]

        # Populate info dictionary
        for row in table.select("tr"):
            key = row.select_one("th").text.replace(":", "").strip()
            values = [a.text for a in row.select("td a")]
            if key == 'Year':
                info_dict[key] = int(values[0])
            else:
                info_dict[key] = values

        notes = album_soup.select_one(".notes_1LXvZ").text if album_soup.select_one(".notes_1LXvZ") else ''
        info_dict['Tracklist'] = tracklist
        info_dict['Notes'] = notes

        final_db.append(info_dict)
    index_lim = -1

# Save the final database to a JSON file
#with open('db.json', 'w') as file:
#json.dump({'list': final_db, 'page': page, 'index': index}, file)

