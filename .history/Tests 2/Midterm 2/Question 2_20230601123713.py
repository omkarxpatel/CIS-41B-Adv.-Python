import pandas as pd
import requests
import io

# URL of the text file
url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"

# Send a GET request to download the file
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Read the text content of the response
    data = response.text

    # Skip the header rows
    rows = data.split('\n')[51:]

    # Initialize an empty list to store the valid rows
    valid_rows = []

    # Process each row, skipping any problematic lines
    for row in rows:
        try:
            # Split the row by whitespace and append to the valid_rows list
            valid_rows.append(row.split())
        except:
            pass

    # Convert the list of valid rows into a DataFrame
    df = pd.DataFrame(valid_rows, columns=["year", "month", "decimal_date", "average", "de_season", "days", "st_dev", "unc_mean"])

    # Print the DataFrame
    print(df)
else:
    print("Failed to download the file.")
