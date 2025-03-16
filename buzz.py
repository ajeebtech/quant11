from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import time
from utils import *
import ollama
import json
from bs4 import BeautifulSoup
options = Options()
# options.add_experimental_option("prefs", {
#     "profile.managed_default_content_settings.images": 2,
#     "profile.managed_default_content_settings.javascript": 2
# })
# options.add_argument("--disable-gpu --log-level=3 --disable-extensions --blink-settings=imagesEnabled=false --disable-blink-features=AutomationControlled")

file_path = 'news.google.com_cookies.txt'

driver = webdriver.Chrome(options=options)
driver.get('https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en')
load_cookies_from_file(driver, file_path)

search_box = driver.find_element(By.CLASS_NAME, "Ax4B8")
search_box.click()  
subject = 'Technology'
search_box.send_keys(subject) 
search_box.send_keys(Keys.RETURN) 
base_url = driver.current_url
driver.get(base_url)
article_links = driver.find_elements(By.XPATH, "//article//a[@href]")
hrefs = [link.get_attribute("href") for link in article_links][:5]
articles = {'subject':hrefs}
with open('articles.json', 'w') as f:
    json.dump(articles,f,indent=4)
# save to json
for href in hrefs:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(href)  # Replace with your target URL

    # Extract all text from the <body> tag
    text = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()
    response = ollama.chat(
                model='granite3.1-dense',
                messages=[{
                    'role': 'user',
                    'content': f"{text} \n summarise this article, but don't return anything if the article isn't about {subject}",
                }]
            )
    response = response['message']['content'].strip()
    [score,sentimnt] = sentiment(document=response)
    print(f"Sentiment: {sentimnt} | Score: {score:.4f}")
    driver.quit()
    break

