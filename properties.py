from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import pandas as pd

# Define the website and path to chromedriver
website = "https://a-d.com.au/new-apartments-developments/vic"
path = "/Users/maimizuno/Documents/AutomationWithPython/chromedriver-mac-arm64/chromedriver"

# Initialize WebDriver
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)

# Wait object to ensure elements are loaded
wait = WebDriverWait(driver, 30)  # Timeout after 30 seconds

# Locate all container elements
containers = driver.find_elements(by="xpath", value="//div[@class='property-item']")  # Adjusted XPath to match containers

names = []
addresses = []

# Iterate over each container to extract name and address
for container in containers:
    name = container.find_element(by="xpath", value=".//span[@class ='search-page ng-tns-c211-1']").text
    address = container.find_element(by="xpath", value=".//div[@class ='location ng-tns-c211-1']").text

    names.append(name)
    addresses.append(address)

# Create DataFrame and print it
ad_dict = {'name': names, 'address': addresses}
ad_properties = pd.DataFrame(ad_dict)
print(ad_properties)

# Save the data to a CSV file (uncomment if needed)
# ad_properties.to_csv('properties.csv', index=False)

# Quit the browser
driver.quit()
