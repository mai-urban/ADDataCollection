import requests
import json
import csv
from datetime import datetime

# API endpoint
url = "https://api.apartmentdevelopments.com.au/developments/bundled"

# States to fetch data for
states = ["victoria", "new-south-wales"]

# Source site and date
source = "a-d"
date = datetime.today().strftime('%Y-%m-%d')

# Define the CSV file name
csv_file = f"{date}_{source}_ProjectListings.csv"

# List to store all results
all_results = []

# Loop through each state
for state in states:
    page = 1
    print(f"Fetching data for state: {state}")
    while True:
        # Parameters for the API request
        params = {
            "address": "true",
            "slugs": "true",
            "bci": "true",
            "status": "published",
            "classifications": "apartments,townhouses,new-land-estates,penthouses,prestige-homes,villas,terraces",
            "page": page,
            "limit": 500,
            "details": "true",
            "galleries": "false",
            "stateSearch": "true",
            "radius": 120000,
            "state": state,
            "postalCode": "2000" if state == "new-south-wales" else "3000"
        }

        # Headers for the API request
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://a-d.com.au",
            "referer": "https://a-d.com.au/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                # Parse the JSON response
                data = response.json()

                # Extract 'nearbyOnly' developments
                developments = data.get("data", {}).get("developments", {}).get("nearbyOnly", [])

                # Stop if no more data is returned
                if not developments:
                    print(f"No more developments found for {state}.")
                    break

                for development in developments:
                    title = development.get("title", "")
                    dev_url = development.get("url", "").replace("\\", "")  # Clean URL slashes
                    address = development.get("address", {})
                    thoroughfare = address.get("thoroughfare", "")
                    thoroughfare_number = address.get("thoroughfareNumber", "")
                    full_thoroughfare = f"{thoroughfare_number} {thoroughfare}".strip() if thoroughfare_number else thoroughfare
                    area = address.get("area", "")
                    state_name = address.get("state", "")
                    postal_code = address.get("postalCode", "")

                    # Append the extracted data as a dictionary
                    all_results.append({
                        "Address": full_thoroughfare,
                        "Suburb": area,
                        "State": state_name,
                        "PostCode": postal_code,
                        "Date Scraped": date,
                        "Source Site": source,
                        "Url": "https://a-d.com.au" + dev_url,
                        "Name": title
                    })

                print(f"State: {state}, Page {page} processed with {len(developments)} records.")
                page += 1  # Move to the next page

            except json.JSONDecodeError:
                print(f"Failed to decode JSON for {state} on page {page}.")
                print(f"Response Text: {response.text}")
                break

        else:
            print(f"Failed to fetch data for {state} on page {page}. Status code: {response.status_code}")
            print(response.text)
            break

# Save all results to a single CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Address", "Suburb", "State", "PostCode", "Date Scraped", "Source Site", "Url", "Name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the header row
    writer.writerows(all_results)  # Write all rows

print(f"Data successfully saved to {csv_file}")
