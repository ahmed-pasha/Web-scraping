from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pymongo import MongoClient
from datetime import datetime
import uuid
import random
import requests

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "twitter_data"
MONGO_COLLECTION = "trending_topics"
PROXY_LIST = [
    "http://username:userpassword@us.proxymesh.com:port"
]

USERNAME = "user_name"  
PASSWORD = "user_pass"

def get_new_proxy():
    """Selects a new proxy for each request."""
    return random.choice(PROXY_LIST)

def configure_driver_with_proxy(proxy_address):
    """Configures the WebDriver with a given proxy."""
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy.ssl_proxy = proxy_address

    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-notifications")
    edge_options.proxy = proxy

    return webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

def login_to_twitter(driver):
    """Logs into Twitter."""
    try:
        driver.get("https://twitter.com/login")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        username_field = driver.find_element(By.XPATH, "//input[@name='text']")
        username_field.send_keys(USERNAME)
        username_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password_field = driver.find_element(By.XPATH, "//input[@name='password']")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Timeline: Trending now')]")))
        print("Login successful.")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def get_external_ip(proxy_address):
    """Fetches the external IP address using the proxy."""
    try:
        proxies = {"http": proxy_address, "https": proxy_address}
        response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=30)
        response.raise_for_status()
        return response.json().get("ip")
    except Exception as e:
        print(f"Error fetching IP address: {e}")
        return "Unavailable"

def store_results_in_mongodb(trends, unique_id, end_time, ip_address):
    """Stores results in MongoDB."""
    try:
        with MongoClient(MONGO_URI) as client:
            db = client[MONGO_DB]
            collection = db[MONGO_COLLECTION]
            document = {
                "unique_id": unique_id,
                "trends": trends,
                "end_time": end_time,
                "ip_address": ip_address,
            }
            collection.insert_one(document)
            print("Results stored in MongoDB:", document)
    except Exception as e:
        print(f"Error storing in MongoDB: {e}")

def fetch_trending_topics():
    """Fetches trending topics and stores them in MongoDB."""
    proxy_address = get_new_proxy()
    driver = configure_driver_with_proxy(proxy_address)
    unique_id = str(uuid.uuid4())

    try:
        if not login_to_twitter(driver):
            raise Exception("Twitter login failed.")

        trending_section = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Timeline: Trending now')]"))
        )
        trending_topics = trending_section.find_elements(By.XPATH, ".//span[contains(@dir, 'ltr')]")
        top_trends = [topic.text for topic in trending_topics if topic.text][:5]

        print("Top 5 Trending Topics:", top_trends)

        ip_address = get_external_ip(proxy_address)
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        store_results_in_mongodb(top_trends, unique_id, end_time, ip_address)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_trending_topics()
