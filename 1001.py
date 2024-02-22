from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import requests
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
import time
import json


URL = "https://www.discogs.com/lists/1001-albums-you-must-hear-before-you-die/18222?limit=250"


options = webdriver.ChromeOptions()

#options.add_argument('--disable-extensions')
#options.headless = True
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
# Disable images
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

#options.add_argument("--headless")
index = 0
page=0
final_db=[]
def save():
    if index ==0 or final_db==[] or page==0:
        print("NO SAVE")
        return
    file = open('db.json','w')
    file.write(json.dumps({'list':final_db, 'page':page,'index':index}))
    file.close()

# Initialize the Chrome driver with the specified options
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# For some reason discogs doesn't stop loading
try:
    file = open('db.json', 'r')
    recup_data = json.load(file)
    file.close()
    final_db = recup_data['list']
    page_start = recup_data['page']

    index_lim = recup_data['index']

    print("FOUND BACKUP")
    if index_lim ==0:
        raise Exception("INDEX 0 ERROR")
except FileNotFoundError:
    print("NO ERROR DATA FOUND")
    final_db = []
    index_lim = -1
    page_start = 1

for page in range(page_start,5):
    driver.set_page_load_timeout(10)
    try:
        driver.get(URL + f"&page={page}")
    except TimeoutException:
        pass
    print("loaded main page")
    driver.set_page_load_timeout(60)

    list_items = driver.find_elements("css selector", "ol#listitems > li.listitem")

    for index, item in enumerate(list_items, start=1):
        print(f"p{page} | {index}")
        if index < index_lim:
            print(f"skiped p{page} | {index}")
            continue
        
        info_dict = {}

        img = item.find_element("css selector", "img")
        img_src = img.get_attribute('src')
        entry_name = img.get_attribute('alt').replace('/', '|')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = requests.get(img_src, headers=headers)
        img_data = Image.open(BytesIO(response.content))
        filename = f"imgs/{entry_name}.jpeg"
        img_data.save(filename)
       
        info_dict['Index'] = index
        
        #extract artist and album from image from image alt atrribute
        img_alt_att = img.get_attribute('alt')
        # Treat exceptions
        exceptions = {'Missy ': "Missy Misdemeanor Elliott* - Supa Dupa Fly"}
        if img_alt_att in exceptions.keys():
            img_alt_att = exceptions[img_alt_att]
        artist, album = img_alt_att.split(" - ",1)
        info_dict['Album'] = album
        info_dict['Artist'] = artist

        # Now get link
        link = item.find_element(By.CSS_SELECTOR, "a.thumbnail_link").get_attribute('href')
        try:
            driver.execute_script(f"window.open('{link}','_blank');")
        except TimeoutException:
            pass
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])


        # Find the table by its class name
        table = driver.find_element(By.CLASS_NAME, "table_1fWaB")

        # Iterate through each row in the table
        for row in table.find_elements(By.TAG_NAME, "tr"):
            # Extract the header (key) and data (value)
            key = row.find_element(By.TAG_NAME, "th").text.replace(":", "").strip()
            values = [a.text for a in row.find_elements(By.TAG_NAME, "a")]
            
            # Special handling for 'Year' to convert it into an integer
            if key == 'Year' and values:
                info_dict[key] = int(values[0])
            else:
                info_dict[key] = values

        # Get tracklist
        tracklist = []
        table = driver.find_element(By.XPATH, "//*[starts-with(@class, 'tracklist_')]")

        for row in table.find_elements(By.TAG_NAME, "tr"):
            try:
                tracklist.append(row.find_element(By.TAG_NAME, 'span').text)
            except:
                pass

        info_dict['Tracklist'] = tracklist
        try:
            notes = driver.find_element(By.CLASS_NAME, "notes_1LXvZ").text
        except:
            notes = ''
        info_dict['Notes'] = notes
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        final_db.append(info_dict)
    index_lim=-1


#save_all()
