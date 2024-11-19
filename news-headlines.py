from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

website = "https://a-d.com.au/new-apartments-developments/vic"
path = "C:/Users/UniMa/chromedriver-win64/chromedriver-win64/chromedriver.exe"

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)

containers = driver.find_elements(by="xpath", value="//span[@class ='m-3 block relative dark:text-white']")

property_names = []
addresses = []

for container in containers:
    property_name = container.find_element(by="xpath", value="./a/b").text
    address = container.find_element(by="xpath", value="./a/span").text
    link = container.find_element(by="xpath", value="./a").get_attribute("href")

    property_names.append(property_name)
    addresses.append(address)
    links.append(link)

my_dict = {'property name': property_names, 'address': addresses, 'link': links }
df_properties = pd.DataFrame(my_dict)
df_properties.to_csv('properties.csv', index=True)

driver.quit()