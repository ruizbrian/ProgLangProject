#############################################
## NAME: GUSTAVO JIMENEZ                   ##
## DATE: 4.12.2024                         ##
## ORGN: CSUB - CMPS 3500                  ##
## FILE: project.py                        ##
#############################################


import pandas as pd

def loadData(filePath):
    """
    Function to load the dataset from a CSV file
    """
    # Read CSV file
    data = pd.read_csv(filePath)

    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    return data

def cleanData(data):

    data = data.dropna()
    checkColumns = ['ID', 'Severity', 'Zipcode', 'Start_Time', 'End_Time', 'Visibility(mi)', 'Weather_Condition', 'Country']
    data = data.dropna(subset=checkColumns)

    data = data.dropna(thresh=5)

    data = data[data['Distance(mi)'] != 0]

    data['Zipcode'] = data['Zipcode'].astype(str).str[:5]

    data['Start_Time'] = pd.to_datetime(data['Start_Time'])
    data['End_Time'] = pd.to_datetime(data['End_Time'])
    data = data[data['End_Time'] != data['Start_Time']]

    return data

def main():
    filePath = "/home/stu/gjimenez3/3500/ProgLangProject/data/US_Accidents_data.csv"
    #filePath = "/home/stu/gjimenez3/3500/project/InputDataSample.csv"

    data = loadData(filePath)

    cleanedData = cleanData(data)

    print(data)
    print(cleanedData)

if __name__ == "__main__":
    main()
