import pandas as pd
import csv
import numpy as np

# Initialize an empty list to store rows
data = []

# Open the CSV file and read up to one million rows
with open('US_Accidents_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i >= 1000000:
            break
        data.append(row[:20])  # Append only the first 18 columns

# Convert the list of rows into a NumPy array
array = np.array(data)

x = None

for row in array:
    if (row[1] is None or row[2] is None or row[3] is None or row[4] is None or row[10] is None or row[11] is None or row[17] is None or row[19] is None ):
        del array[row]
        print("-------------------------------->")
        print(row)

    print(row)
