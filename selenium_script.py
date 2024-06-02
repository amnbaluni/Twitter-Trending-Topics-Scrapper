from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import datetime
import uuid
import requests

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trends']

for record in collection.find():
    print(record)

def fetch_trending_topics():
    proxy_user = "amanbaluni" 
    proxy_pass = "__"  # Hiding proxymesh password
    proxy_host = "us-ca.proxymesh.com"      
    proxy_port = 31280                     
    
    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    
    # Setup Selenium with proxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Login to Twitter
    driver.get("https://twitter.com/login")
    username = driver.find_element(By.NAME, "session[amanbaluni]")
    password = driver.find_element(By.NAME, "session[__]")  #hiding the password
    username.send_keys("amanbaluni")
    password.send_keys("__")  #hiding the password
    password.send_keys(Keys.RETURN)
    
    # Wait for login and redirection
    driver.implicitly_wait(10)
    
    # Fetch trending topics
    driver.get("https://twitter.com/explore")
    trending_section = driver.find_element(By.XPATH, '//section[@aria-labelledby="accessible-list-0"]')
    trends = trending_section.find_elements(By.XPATH, './/span[contains(text(), "#")]')[:5]
    
    trend_names = [trend.text for trend in trends]
    
    # Get current IP address used for the request
    ip_address = requests.get('https://api.ipify.org').text
    
    # Create a unique ID for this run
    unique_id = str(uuid.uuid4())
    
    # Store results in MongoDB
    record = {
        "_id": unique_id,
        "trend1": trend_names[0] if len(trend_names) > 0 else "",
        "trend2": trend_names[1] if len(trend_names) > 1 else "",
        "trend3": trend_names[2] if len(trend_names) > 2 else "",
        "trend4": trend_names[3] if len(trend_names) > 3 else "",
        "trend5": trend_names[4] if len(trend_names) > 4 else "",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_address
    }
    
    collection.insert_one(record)
    
    driver.quit()
    
    return record

if __name__ == "__main__":
    result = fetch_trending_topics()
    print(result)
