import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Specify the path to your downloaded ChromeDriver executable
chrome_driver_path = 'C:/winecuration/chromedriver-win64/chromedriver.exe'  # Update this path

# Set up the Selenium WebDriver
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

# Open the Vivino explore page
url = "https://www.wine21.com/13_search/wine_list.html"
driver.get(url)
time.sleep(5)  # Wait for the page to load

# Scroll down the page to load more wines
last_height = driver.execute_script("return document.body.scrollHeight")
while True :
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for new content to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract wine elements and get their links
wine_links = []
wine_elements = driver.find_elements(By.CSS_SELECTOR, ".wineCard__wineCard--2dj2T a.anchor_anchor__m8Qi-")

for element in wine_elements:
    wine_link = element.get_attribute('href')
    wine_links.append(wine_link)

# Save the links to a CSV file
df = pd.DataFrame(wine_links, columns=["Wine URL"])
df.to_csv("wine_links.csv", index=False)

# Close the WebDriver
driver.quit()