import requests
import json
import csv
from datetime import datetime

# API endpoint
url = "https://api.apartmentdevelopments.com.au/developments/bundled"

# Parameters for the API request
params = {
    "address": "true",  # Required to get address details
    "slugs": "true",    # Required if you need unique slugs for developments
    "bci": "true",      # Optional, keep it only if you need building information
    "status": "published",  # Only fetch published data
    "classifications": "apartments,townhouses,new-land-estates,penthouses,prestige-homes,villas,terraces",  # Filter by these categories
    "page": 1,          # Start at page 1
    "limit": 500,       # Fetch up to 500 results per request
    "details": "true",  # Include detailed data
    "galleries": "false",  # Don't need gallery images
    "stateSearch": "true",  # Required for state-specific filtering
    "radius": 120000,   # Adjust radius as needed (in meters)
    "state": "new-south-wales",  # Only fetch data from Victoria
    "postalCode": "2000"  # Focus on postal code 3000
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
    # Parse the JSON response
    data = response.json()

    # Extract 'nearbyOnly' developments
    developments = data.get("data", {}).get("developments", {}).get("nearbyOnly", [])

    # List to store extracted data
    results = []
    # Source site
    source = "a-d"
    # Date Scraped
    date = datetime.today().strftime('%Y-%m-%d')

    for development in developments:
        title = development.get("title", "")
        url = development.get("url", "").replace("\\", "")  # Clean URL slashes
        address = development.get("address", {})
        thoroughfare = address.get("thoroughfare", "")
        thoroughfare_number = address.get("thoroughfareNumber", "")
        full_thoroughfare = f"{thoroughfare_number} {thoroughfare}" if thoroughfare_number else thoroughfare
        area = address.get("area", "")
        state = address.get("state", "")
        postal_code = address.get("postalCode", "")

        # Append the extracted data as a dictionary
        results.append({
            "Address": full_thoroughfare,
            "Suburb": area,
            "State": state,
            "PostCode": postal_code,
            "Date Scraped": date,
            "Source Site": source,
            "Url": "https://a-d.com.au" + url,
            "Name": title
        })

    # Print the results
    print(json.dumps(results, indent=4))

    # Define the CSV file name
    csv_file = f"{date}_{source}_ProjectListings.csv"

    # Save the results to a CSV file
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Address", "Suburb", "State", "PostCode", "Date Scraped", "Source Site", "Url", "Name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row
        writer.writerows(results)  # Write all rows

    print(f"Data successfully saved to {csv_file}")

else:
    # Print error message if request fails
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(response.text)
