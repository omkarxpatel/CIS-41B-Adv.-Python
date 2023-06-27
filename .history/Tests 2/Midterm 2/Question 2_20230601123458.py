import pandas as pd
import requests
import io

url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"

response = requests.get(url)

if response.status_code == 200:
    data = response.text

    df = pd.read_csv(io.StringIO(data), skiprows=51, delim_whitespace=True,
                     names=["year", "month", "decimal_date", "average", "de_season", "days", "st_dev", "unc_mean"])

    print(df)
else:
    print("Failed to download the file.")
