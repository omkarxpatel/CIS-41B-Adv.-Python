import pandas as pd
import requests


response = requests.get("https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt")

if response.status_code == 200:
    data = response.text

    rows = data.split('\n')[51:]
    valid = []

    for row in rows:
        try:
            row_data = row.split()

            if len(row_data) == 8:
                valid.append(row_data)
        except:
            pass

    num_columns = len(valid[0])

    df = pd.DataFrame(valid,columns=["column_" + str(x) for x in range(1, col+1)])

    print(df)
else:
    print("Failed to download the file.")
