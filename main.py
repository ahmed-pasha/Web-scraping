from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

def log_result(results, step, status, message=""):
    results.append({"Step": step, "Status": status, "Message": message})

def login_to_twitter(driver, username, password, results):
    try:
        driver.get("https://twitter.com/login")
        print("Navigating to Twitter login page...")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
        )

        username_field = driver.find_element(By.XPATH, "//input[@name='text']")
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        print("Entered username")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        password_field = driver.find_element(By.XPATH, "//input[@name='password']")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        print("Entered password")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']"))
        )
        log_result(results, "Login", "Success")
        print("Login successful")

    except Exception as e:
        log_result(results, "Login", "Failure", str(e))
        print(f"Login failed: {str(e)}")

def fetch_trending_topics():
    
    edge_options = Options()
    edge_options.add_argument("--start-maximized")  
    edge_options.add_argument("--disable-notifications")  
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

    results = []

    try:
        username = "user_id" 
        password = "user_pass"

        login_to_twitter(driver, username, password, results)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Timeline: Trending now')]"))
            )
            trending_section = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Timeline: Trending now')]")
            trending_topics = trending_section.find_elements(By.XPATH, ".//div[@dir='ltr']")

            top_trends = [topic.text for topic in trending_topics[:5]]

            print("Top 5 Trending Topics:")
            for idx, trend in enumerate(top_trends, start=1):
                print(f"{idx}. {trend}")

            log_result(results, "Fetch Trending Topics", "Success")
        except NoSuchElementException as e:
            log_result(results, "Fetch Trending Topics", "Failure", "Trending section not found")
            print("Trending section not found")

    except Exception as e:
        log_result(results, "Test Execution", "Failure", str(e))
        print(f"Test execution failed: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_trending_topics()