from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")  
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://exclusivecarregistry.com/profile-list")

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20) # Tempo para carregar os demais dados, tive que aumentar,
    # pois estava deixando valores para trás.

    pagination = driver.find_elements("css selector", "div.simplepagination")
    
    if not pagination:
        break
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break
    last_height = new_height

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
driver.quit()
profiles = []
profile_items = soup.select("main#profilelist div.userlist.wrapperfull div.profile_item")

for profile in profile_items:
    name = profile.select_one("div.text span").text.strip() if profile.select_one("div.text span") else ""
    tags = [tag.text.strip() for tag in profile.select("div.tag_cloud span")]
    flag = profile.select_one("img.flag")["alt"] if profile.select_one("img.flag") else ""
    verified = profile.select_one("img.verified")["alt"] if profile.select_one("img.verified") else ""
    
    profiles.append({"name": name, "tags": ", ".join(tags), "country": flag, "verified": verified})

df = pd.DataFrame(profiles) #Save em CSV
df.to_csv("profiles.csv", index=False)
