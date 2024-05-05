#############################################
## CLASS Project
## Course: cmps3500
## Date: 4.12.2024                         
## Orgn: CSUB - CMPS 3500                  
## File: project.py                        
## Student 1: Gustavo Jimenez
## Student 2: David Ayeni
## Student 3: Brian Ruiz
## Student 4: 
## DESCRIPTION: Implementation Basic Data Analysis Routine
#############################################

import time
import pandas as pd

def loadData(filePath):
    #Function to load the dataset from a CSV file
    print("Loading and cleaning input data set:")
    print("************************************")
    
    start_time = time.time()

    # Read CSV file
    print(f"[{time.strftime('%H:%M:%S')}] Starting Script")
    print(f"[{time.strftime('%H:%M:%S')}] Loading {filePath}")
    data = pd.read_csv(filePath)
    
    total_columns = len(data.columns)
    print(f"[{time.strftime('%H:%M:%S')}] Total Columns Read: {total_columns}")
    # Total rows read
    total_rows = len(data)
    print(f"[{time.strftime('%H:%M:%S')}] Total Rows Read: {total_rows}")

    end_time = time.time()
    load_time = end_time - start_time
    print(f"\nTime to load is: {load_time:.2f} seconds")

    return data

def cleanData(data):
    print("Processing input data set:")
    print("**************************")

    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Performing Data Clean Up")

    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    data = data.dropna()
    checkColumns = ['ID', 'Severity', 'Zipcode', 'Start_Time', 'End_Time', 'Visibility(mi)', 'Weather_Condition', 'Country']
    data = data.dropna(subset=checkColumns)
    data = data.dropna(thresh=5)
    data = data[data['Distance(mi)'] != 0]
    data['Zipcode'] = data['Zipcode'].astype(str).str[:5]
    data['Start_Time'] = pd.to_datetime(data['Start_Time'])
    data['End_Time'] = pd.to_datetime(data['End_Time'])
    data = data[data['End_Time'] != data['Start_Time']]

    total_rows = len(data)
    print(f"[{time.strftime('%H:%M:%S')}] Total Rows Read after cleaning is: {total_rows}")
    
    end_time = time.time()
    process_time = end_time - start_time
    print(f"\nTime to process is: {process_time:.2f} seconds")


    return data


def display_menu():
    print("Menu:")
    print("1. Load data")
    print("2. Process data")
    print("3. Print Answers")
    print("4. Search Accidents (Use City, State, and Zip Code)")
    print("5. Search Accidents (Year, Month and Day)")
    print("6. Search Accidents (Temperature Range and Visibility Range)")
    print("7. Quit")

#Question 1 - 10
def Question1(data):
    print("\n\t1. What are the 3 months with the highest amount accidents reported?")
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    accidents_per_month = data['Start_Time'].dt.month.value_counts().sort_values(ascending=False)
    for month_num, count in accidents_per_month.head(3).items():
        month_name = month_names[month_num]
        print(f"{month_name}: {count} accidents")
    print("")

def Question2(data):
    print("\t2. What is the year with the highest amount of accidents reported?")
    accidents_per_year = data['Start_Time'].dt.year.value_counts()
    max_year = accidents_per_year.idxmax()
    print(f"Year with the most accidents: {max_year}\n")

def Question3(data):
    print("\t3. What is the state that had the most accidents of severity 2?, display the data per year.")
    severity_2_data = data[data['Severity'] == 2]
    accidents_per_state = severity_2_data['State'].value_counts()
    max_state = accidents_per_state.idxmax()
    print(f"The state that had the most accidents of severity 2: {max_state}")
    state_data = severity_2_data[severity_2_data['State'] == max_state]
    accidents_per_year = state_data['Start_Time'].dt.year.value_counts().sort_index()
    print("Accidents per year:")
    for year, count in accidents_per_year.items():
        print(f"Year {year}: {count} accidents")
    print("")

def Question4(data):
    print("\t4. What severity is the most common in Virginia, California and Florida?")
    states = ['VA', 'CA', 'FL']
    for state in states:
        state_data = data[data['State'] == state]
        severity_counts = state_data['Severity'].value_counts()
        most_common_severity = severity_counts.idxmax()
        print(f"Most common severity in {state}: Severity {most_common_severity}")
    print("")

def Question5(data):
    print("\t5. What are the 5 cities that had the most accidents in in California? display the data per year.")
    california_data = data[data['State'] == 'CA']
    accidents_per_city = california_data.groupby([california_data['City'], california_data['Start_Time'].dt.year]).size().reset_index(name='Accident Count')
    for year, year_data in accidents_per_city.groupby('Start_Time'):
        print(f"Year {year}:")
        top_5 = year_data.nlargest(5, 'Accident Count')
        for index, row in top_5.iterrows():
            print(f"{row['City']}: {row['Accident Count']} accidents")
        print("")

def Question6(data):
    print("\t6. What was the average humidity and average temperature of all accidents of severity 4 that occurred in the city of Boston? display the data per month.")
    boston_data = data[(data['Severity'] == 4) & (data['City'] == 'Boston')]
    boston_data = boston_data.copy()
    boston_data['Month'] = boston_data['Start_Time'].dt.month
    monthly_average = boston_data.groupby('Month').agg({'Humidity(%)': 'mean', 'Temperature(F)': 'mean'}).reset_index()
    monthly_average['Month'] = monthly_average['Month'].map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    print("Average Humidity and Temperature for Severity 4 Accidents in Boston:")
    print(monthly_average)
    print("")

def Question7(data):
    print("\t7. What are the 3 most common weather conditions (weather_conditions) when accidents occurred in New York city? display the data per month.")
    nyc_data = data[(data['City'] == 'New York') & (data['State'] == 'NY')]
    nyc_data = nyc_data.copy()
    nyc_data['Month'] = nyc_data['Start_Time'].dt.month
    weather_counts = nyc_data.groupby(['Month', 'Weather_Condition']).size().reset_index(name='Count')
    weather_counts['Month'] = weather_counts['Month'].map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    for month in weather_counts['Month'].unique():
        month_data = weather_counts[weather_counts['Month'] == month]
        top_3_weather_conditions = month_data.nlargest(3, 'Count').reset_index(drop=True)
        print(f"Top 3 weather conditions for {month}:")
        print(top_3_weather_conditions[['Weather_Condition', 'Count']].to_string(index=False))  
    print("\n")

def Question8(data):
    print("\t8. What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire?")
    nh_data = data[(data['State'] == 'NH') & (data['Severity'] == 2)]
    
    if nh_data.empty:
        print("No accidents with severity 2 found in the state of New Hampshire.")
    else:
        max_visibility = nh_data['Visibility(mi)'].max()
        print(f"The maximum visibility of accidents with severity 2 in New Hampshire is: {max_visibility} miles.")
    print("")

def Question9(data):
    print("\t9. How many accidents of each severity were recorded in Bakersfield? Display the data per year.")
    bakersfield_data = data[data['City'] == 'Bakersfield']
    
    if bakersfield_data.empty:
        print("No accidents recorded in Bakersfield.")
    else:
        bakersfield_data = bakersfield_data.copy()
        bakersfield_data['Year'] = bakersfield_data['Start_Time'].dt.year
        severity_counts = bakersfield_data.groupby(['Year', 'Severity']).size().reset_index(name='Count')
        for year in severity_counts['Year'].unique():
            year_data = severity_counts[severity_counts['Year'] == year]
            print(f"Year: {year}")
            print(year_data[['Severity', 'Count']].to_string(index=False))
    print("")

def Question10(data):
    print("\t10. What was the longest accident (in hours) recorded in Las Vegas in the Spring (March, April, and May)? Display the data per year.")
    lv_data = data[(data['City'] == 'Las Vegas') & (data['Start_Time'].dt.month.isin([3, 4, 5]))]
    
    if lv_data.empty:
        print("No accidents recorded in Las Vegas during Spring (March, April, May).")
    else:
        lv_data = lv_data.copy()
        lv_data['Duration'] = (lv_data['End_Time'] - lv_data['Start_Time']).dt.total_seconds() / 3600
        longest_accidents_per_year = lv_data.groupby(lv_data['Start_Time'].dt.year)['Duration'].max()
        print("Longest accident (in hours) recorded in Las Vegas in the Spring (March, April, and May) per year:")
        for year, duration in longest_accidents_per_year.items():
            print(f"Year: {year}, Duration: {duration:.2f} hours")
    print("\n")



def search_accidents_by_state_city_zip(data, state=None, city=None, zipcode=None):
    start_time = time.time()
    
    # Filter data based on input values
    filtered_data = data.copy()
    if state:
        filtered_data = filtered_data[filtered_data['State'] == state]
    if city:
        filtered_data = filtered_data[filtered_data['City'] == city]
    if zipcode:
        filtered_data = filtered_data[filtered_data['Zipcode'] == zipcode]
    
    # Count the number of accidents
    num_accidents = len(filtered_data)
    
    print(f"Number of accidents in {state if state else 'all states'}, {city if city else 'all cities'}, {zipcode if zipcode else 'all zip codes'}: {num_accidents}")
    
    end_time = time.time()  # Record end time
    search_time = end_time - start_time
    print(f"Time to perform serach: {search_time:.2f} seconds")

def search_accidents_by_year_month_day(data, year=None, month=None, day=None):
    start_time = time.time()
  
    datacopy = data.copy()
    datacopy['Start_Time'] = datacopy['Start_Time'].astype(str)
    filtered_data = datacopy.copy()
    if year:
        filtered_data = filtered_data[filtered_data['Start_Time'].str.startswith(str(year))]
    if month:
        filtered_data = filtered_data[filtered_data['Start_Time'].str[5:7] == str(month).zfill(2)]
    if day:
        filtered_data = filtered_data[filtered_data['Start_Time'].str[8:10] == str(day).zfill(2)]
       
    # Count the number of accidents
    num_accidents = len(filtered_data)
    
    print(f"Number of accidents in {year if year else 'all years'}-{month if month else 'all months'}-{day if day else 'all days'}: {num_accidents}")
    
    end_time = time.time()  # Record end time
    search_time = end_time - start_time
    print(f"Time to perform serach: {search_time:.2f} seconds")

def search_accidents_by_temperature_visibility(data, min_temp=None, max_temp=None, min_visibility=None, max_visibility=None):  
    start_time = time.time()
    
    #Convert input values to float if they are not None
    if min_temp:
        min_temp = float(min_temp)
    if max_temp:
        max_temp = float(max_temp)
    if min_visibility:
        min_visibility = float(min_visibility)
    if max_visibility:
        max_visibility = float(max_visibility)
    
    # Filter data based on input values
    filtered_data = data.copy()
    if min_temp and max_temp:
        filtered_data = filtered_data[(filtered_data['Temperature(F)'] >= min_temp) & (filtered_data['Temperature(F)'] <= max_temp)]
    if min_visibility and max_visibility:
        filtered_data = filtered_data[(filtered_data['Visibility(mi)'] >= min_visibility) & (filtered_data['Visibility(mi)'] <= max_visibility)]
    
    # Count the number of accidents
    num_accidents = len(filtered_data)
    
    print(f"Number of accidents with temperature between {min_temp if min_temp else 'any'} and {max_temp if max_temp else 'any'} Fahrenheit, and visibility between {min_visibility if min_visibility else 'any'} and {max_visibility if max_visibility else 'any'} miles: {num_accidents}")

    end_time = time.time()  # Record end time
    search_time = end_time - start_time
    print(f"Time to perform serach: {search_time:.2f} seconds")

def main():
    start_time = time.time()

    filePath = "US_Accidents_data.csv"
    data = None
    data_loaded = False  # Flag to track whether data has been loaded

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            if data is None:
                data = loadData(filePath)
                data_loaded = True  # Set data_loaded flag to True
                print("Data loaded successfully.\n\n\n")
            else:
                print("Data is already loaded.\n\n\n")
        elif choice == "2":
            if data_loaded:  # Check if data is loaded before processing
                data = cleanData(data)
                print("Data processed successfully.\n\n\n")
            else:
                print("Please load data first.\n\n\n")
        elif choice == "3":
            if data is not None:
                
                print("Answering questions:\n")
                Question1(data)
                Question2(data)
                Question3(data)
                Question4(data)
                Question5(data)
                Question6(data)
                Question7(data)
                Question8(data)
                Question9(data)
                Question10(data)

                print("\n\n\n")
            else:
                print("Please load data first.\n\n\n")
        elif choice == "4":
            state = input("Enter a State(e.g CA): ")
            city = input("Enter a city: ")
            zipcode = input("Enter a zipcode: ")
            search_accidents_by_state_city_zip(data, state, city, zipcode)

            print("\n\n\n")
            pass
        elif choice == "5":
            year = input("Enter a year: ")
            month = input("Enter a month: ")
            day = input("Enter a day: ")
            search_accidents_by_year_month_day(data, year, month, day)

            print("\n\n\n")
            pass
        elif choice == "6":
            min_t = input("Enter a minimum temperature (F): ")
            max_t = input("Enter a maximum temperature (F): ")
            min_v = input("Enter a minimum visibility (mi): ")
            max_v = input("Enter a maximum visibility (mi): ")
            search_accidents_by_temperature_visibility(data, min_t, max_t, min_v, max_v)

            print("\n\n\n")
            pass
        elif choice == "7":
            print("Quitting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

    end_time = time.time()  # Record end time
    total_running_time = end_time - start_time
    print(f"Total running time: {total_running_time:.2f} seconds")



if __name__ == "__main__":
    main()

