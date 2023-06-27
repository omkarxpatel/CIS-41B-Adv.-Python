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

    # Skip the header rows and read the data into a DataFrame
    df = pd.read_csv(io.StringIO(data), skiprows=51, delim_whitespace=True,
                     names=["year", "month", "decimal_date", "average", "de_season", "days", "st_dev", "unc_mean"])

    # Print the DataFrame
    print(df)
else:
    print("Failed to download the file.")
