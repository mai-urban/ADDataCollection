from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

# Define the website and path to chromedriver
website = "https://a-d.com.au/new-apartments-developments/vic"
path = "/Users/maimizuno/Documents/AutomationWithPython/chromedriver-mac-arm64/chromedriver"

# Configure headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920x1080")  # Set screen size for headless mode

# Initialize WebDriver with headless options
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)

# Wait object to ensure elements are loaded
wait = WebDriverWait(driver, 60)  # Timeout after 60 seconds

addresses = []
names = []

'''
# Click "Show More" until all data is loaded
while True:
    try:
        # Wait for "Show More" button to appear and scroll into view
        show_more_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'load-more')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)

        # Click the button
        show_more_button.click()
        print("Clicked 'Show More' button.")
        time.sleep(2)  # Wait briefly to allow new content to load
    except Exception:
        print("No more 'Show More' button found.")
        # Exit the loop when the "Show More" button is no longer available
        break
'''

# Locate all address elements
address_elements = driver.find_elements(By.XPATH, "//div[@class='location ng-tns-c211-1']")
# Locate all name elements
name_elements = driver.find_elements(By.XPATH, "//span[@class='search-page ng-tns-c211-1']")
# Locate all links
link_elements = driver.find_elements(By.XPATH, "//a[@class='ng-tns-c211-19']")
# Extract the href attributes from the elements
links = [link.get_attribute("href") for link in link_elements]

# Ensure both lists have the same length (pairing names and addresses)
if len(name_elements) == len(address_elements):
    for address_element, name_element in zip(address_elements, name_elements):
        addresses.append(address_element.text)
        names.append(name_element.text)
else:
    print("Warning: Mismatched number of names and addresses!")

# Add today's date to each entry
today_date = datetime.today().strftime('%Y-%m-%d')
dates = [today_date] * len(names)  # Create a list with today's date for all rows

# Create DataFrame and add the date column
ad_dict = {'address': addresses, 'name': names, 'date': dates, 'link': links}
ad_properties = pd.DataFrame(ad_dict)

# Print the DataFrame
print(ad_properties)

# Save the data to a CSV file (uncomment if needed)
# ad_properties.to_csv('properties.csv', index=False)

# Quit the browser
driver.quit()
