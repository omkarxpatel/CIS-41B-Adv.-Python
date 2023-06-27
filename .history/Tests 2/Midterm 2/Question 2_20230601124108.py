import pandas as pd
import requests


response = requests.get("https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt")

if response.status_code == 200:
    data = response.text

    rows = data.split('\n')[51:]
    valid = []

    for row in rows:
        try:
            data = row.split()

            if len(data) == 8:
                valid.append(data)
        except:
            pass

    col = len(valid[0])

    df = pd.DataFrame(valid,columns=["column_" + str(x) for x in range(1, col+1)])

    print(df)
else:
    print("Cannot download the file.")
