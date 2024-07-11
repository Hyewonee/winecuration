from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import random
import pandas as pd

# Path to your ChromeDriver
chrome_driver_path = 'C:/winecuration/chromedriver-win64/chromedriver.exe'  # Update this path

# Read URLs from CSV file
wineUrls = pd.read_csv('C:/winecuration/vivinocrawler/wine_links_complete.csv')['Wine URL'].tolist()

# Function to get the details from a Vivino page
def getWineDetails(url):
    try:
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        
        # Increase wait time
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > section > div.inner > div.clear > div.wine-top-right > dl > dt')))

        # Initialize a dictionary to store the details
        wineDetails = {}

        # Extracting Name
        wineNameKr = driver.find_element(By.CSS_SELECTOR, 'body > section > div.inner > div.clear > div.wine-top-right > dl > dt')
        wineNameEn = driver.find_element(By.CSS_SELECTOR, 'body > section > div.inner > div.clear > div.wine-top-right > dl > dd')

        if wineNameKr and wineNameEn:
            wineDetails['Name Kr'] = wineNameKr.text.strip()
            wineDetails['Name En'] = wineNameEn.text.strip()
        else:
            wineDetails['Name Kr'] = "N/A"
            wineDetails['Name En'] = "N/A"

        #kind of wine, region, nation
        wineTag = driver.find_element(By.CSS_SELECTOR, "body > section > div.inner > div.clear > div.wine-top-right > div.bagde-box > p")
        if wineTag:
            wineDetails['Tag'] = [tag.text for tag in wineTag.find_elements(By.TAG_NAME, 'span')]
        else:
            wineDetails['Tag'] = "N/A"

        sentAndPair = driver.find_elements(By.CLASS_NAME, "view-wine-matching")
        if sentAndPair:
            for sentAndPairElemnt in sentAndPair :
                if sentAndPairElemnt.find_element(By.TAG_NAME, 'span').text == '아로마':
                    wineDetails['Sent'] = [tag.text for tag in sentAndPairElemnt.find_elements(By.TAG_NAME, 'p')]
                if sentAndPairElemnt.find_element(By.TAG_NAME, 'span').text == '음식매칭':
                    wineDetails['Pair'] = [tag.text for tag in sentAndPairElemnt.find_elements(By.TAG_NAME, 'p')]
        # if wineSent:
        #     wineDetails['Sent'] = [tag.text for tag in wineSent.find_elements(By.TAG_NAME, 'p')]
        # else:
        #     wineDetails['Sent'] = "N/A"
        # #body > section > div.inner > div.clear > div.wine-top-right > div.wine-top-right-inner > div.view-wine-matching > div.wine-matching-list.swiper-container.swiper-container-initialized.swiper-container-horizontal > ul
        # #body > section > div.inner > div.clear > div.wine-top-right > div.wine-top-right-inner > div.view-wine-matching > div.wine-matching-list.swiper-container.swiper-container-initialized.swiper-container-horizontal > ul
        # winePair = driver.find_element(By.CSS_SELECTOR, "body > section > div.inner > div.clear > div.wine-top-right > div.wine-top-right-inner > div:nth-child(2) > div.wine-matching-list.swiper-container.swiper-container-initialized.swiper-container-horizontal > ul")
        # if winePair:
        #     wineDetails['Pair'] = [tag.text for tag in winePair.find_elements(By.TAG_NAME, 'p')]
        # else:
        #     wineDetails['Pair'] = "N/A"

        wineInfo = driver.find_element(By.CSS_SELECTOR, ".wine-d-box-info-list")
        
        # Extract text from each <dt> and <dd> inside the parent element
        text_data = []
        for dl in wineInfo.find_elements(By.TAG_NAME, "dl"):
            dt_text = dl.find_element(By.TAG_NAME, "dt").text
            dd_elements = dl.find_elements(By.TAG_NAME, "dd")
            dd_texts = []
            for dd_element in dd_elements:
                # Extract text including any text from child elements like <a>
                dd_text = " ".join([element.text for element in dd_element.find_elements(By.XPATH, ".//*")])
                dd_texts.append(dd_text if dd_text else dd_element.text)
            dd_text_combined = " ".join(dd_texts)
            text_data.append(f"{dt_text} : {dd_text_combined}")
        
        if text_data:
            wineDetails["Info"] = text_data
        else:
            wineDetails['Info'] = "N/A"

        wineNote = driver.find_element(By.CSS_SELECTOR, "#tasting > div > div.makersnote-list1 > div.board-list.board-list-makers > div > div.makers-item-tt > div")
        if wineNote:
            wineDetails['Note'] = wineNote.text
        else:
            wineDetails['Note'] = "N/A"

        # 당도 산미 탄닌 바디
        sweetness = driver.find_element(By.CSS_SELECTOR, "body > section > div.inner > div.clear > div.wine-top-right > div.wine-components > ul > li:nth-child(1) > div")
        sourness = driver.find_element(By.CSS_SELECTOR, "body > section > div.inner > div.clear > div.wine-top-right > div.wine-components > ul > li:nth-child(2) > div")
        bodytaste = driver.find_element(By.CSS_SELECTOR, "body > section > div.inner > div.clear > div.wine-top-right > div.wine-components > ul > li:nth-child(3) > div")
        tannin = driver.find_element(By.CSS_SELECTOR, "body > section > div.inner > div.clear > div.wine-top-right > div.wine-components > ul > li:nth-child(4) > div")
        
        if sweetness and sourness and bodytaste and tannin :
            wineDetails['Sweet'] = len(sweetness.find_elements(By.CLASS_NAME, 'on'))
            wineDetails['Sourness'] = len(sourness.find_elements(By.CLASS_NAME, 'on'))
            wineDetails['Body'] = len(bodytaste.find_elements(By.CLASS_NAME, 'on'))
            wineDetails['Tannin'] = len(tannin.find_elements(By.CLASS_NAME, 'on'))
        else : 
            wineDetails['Sweet'] = "N/A"
            wineDetails['Sourness'] = "N/A"
            wineDetails['Body'] = "N/A"
            wineDetails['Tannin'] = "N/A"
        driver.quit()
        return wineDetails
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        driver.quit()
        return None

# Collecting all details
wine_data = []
retry_attempts = 5
for url in wineUrls:
    attempts = 0
    while attempts < retry_attempts:
        wine_details = getWineDetails(url)
        if wine_details:
            wine_data.append(wine_details)
            break
        else:
            attempts += 1
            sleep_time = random.uniform(30, 60)  # Random sleep time between 30 and 60 seconds
            print(f"Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
    if attempts == retry_attempts:
        print(f"Failed to fetch data for {url} after {retry_attempts} attempts.")
    time.sleep(random.uniform(1, 5))  # Random delay between 1 and 5 seconds between requests

# Writing data to a pickle file
if wine_data:
    with open('wine_data.pkl', 'wb') as output_file:
        pickle.dump(wine_data, output_file)

    print("Data has been successfully written to wine_data.pkl")
else:
    print("No data to write.")
