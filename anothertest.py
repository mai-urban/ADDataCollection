from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime

# Define the website and path to chromedriver
website = "https://a-d.com.au/new-apartments-developments/vic"
path = "/Users/maimizuno/Documents/AutomationWithPython/chromedriver-mac-arm64/chromedriver"

# Configure headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Initialize WebDriver
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)

# Wait object
wait = WebDriverWait(driver, 60)

names = []
addresses = []
links = []

# Locate and extract data
name_elements = wait.until(
    lambda d: d.find_elements(By.XPATH, "//span[@class='search-page ng-tns-c211-1']")
)
address_elements = wait.until(
    lambda d: d.find_elements(By.XPATH, "//div[@class='location ng-tns-c211-1']")
)

# Ensure both lists match
if len(name_elements) == len(address_elements):
    for name_element, address_element in zip(name_elements, address_elements):
        # Extract name and address
        names.append(name_element.text)
        addresses.append(address_element.text)

        # Extract the link (find the parent <a> tag of the name element)
        try:
            link_element = name_element.find_element(By.XPATH, "./ancestor::a")
            link = link_element.get_attribute("href")
        except Exception:
            link = None  # Handle cases where no link is found
        links.append(link)
else:
    print("Warning: Mismatched number of names and addresses!")

# Add today's date
today_date = datetime.today().strftime('%Y-%m-%d')
dates = [today_date] * len(names)

# Create DataFrame
ad_dict = {'name': names, 'address': addresses, 'date': dates, 'link': links}
ad_properties = pd.DataFrame(ad_dict)
print(ad_properties)

# Save to CSV
# ad_properties.to_csv('properties.csv', index=False)

# Quit the browser
driver.quit()
