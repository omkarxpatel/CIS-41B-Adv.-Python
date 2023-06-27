import pandas as pd
import requests
import io

url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"

response = requests.get(url)

if response.status_code == 200:
    data = response.text

    rows = data.split('\n')[51:]

    valid_rows = []

    for row in rows:
        try:
            row_data = row.split()

            if len(row_data) == 8:
                valid_rows.append(row_data)
        except:
            pass

    num_columns = len(valid_rows[0])

    df = pd.DataFrame(valid_rows, columns=["column_" + str(i) for i in range(1, num_columns+1)])

    print(df)
else:
    print("Failed to download the file.")
