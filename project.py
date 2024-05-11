#############################################
## CLASS Project
## Course: cmps3500
## Date: 4.12.2024                         
## Orgn: CSUB - CMPS 3500                  
## File: project.py                        
## Student 1: Gustavo Jimenez
## Student 2: David Ayeni
## Student 3: Brian Ruiz
## Student 4: Russell Barreyro
## DESCRIPTION: Implementation Basic Data Analysis Routine
#############################################

import time # Importing the time module for time-related functionality
import pandas as pd # Importing pandas library for data manipulation
import os

def load_data(filePath=None):
    # Function to load the dataset from a CSV file
    print("Loading and cleaning input data set:")
    print("************************************")

    start_time = time.time() # Record start time

    data = None

    if filePath is None:
        # List all CSV files in the current directory
        files = [f for f in os.listdir() if f.endswith('.csv')]
        if not files:
            print("No CSV files found in the current directory.")
            return None
        else:
            print("Available CSV files in the current directory:")
            for idx, file in enumerate(files, 1):
                print(f"{idx}. {file}")
            choice = input("Enter the number corresponding to the file you want to load: ")
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(files):
                    print("Invalid choice.")
                    return None
                filePath = files[idx]
            except ValueError:
                print("Invalid choice. Please enter a number.")
                return None

   
    data = None

    # Read CSV file
    print(f"[{time.strftime('%H:%M:%S')}] Starting Script")
    print(f"[{time.strftime('%H:%M:%S')}] Loading {filePath}")
    data = pd.read_csv(filePath)
    if data is not None:
        total_columns = len(data.columns)
        print(f"[{time.strftime('%H:%M:%S')}] Total Columns Read: {total_columns}")
        # Total rows read
        total_rows = len(data)
        print(f"[{time.strftime('%H:%M:%S')}] Total Rows Read: {total_rows}")

    data.columns = map(str.lower, data.columns)

    end_time = time.time() # Record end time
    load_time = end_time - start_time # Calculate load time
    print(f"\nTime to load is: {load_time:.2f} seconds")

    return data


def clean_data(data):
    # Function to clean the loaded dataset
    print("Processing input data set:")
    print("**************************")

    start_time = time.time() # Record start time
    print(f"[{time.strftime('%H:%M:%S')}] Performing Data Clean Up")
    
    # Convert column names to lowercase
    data.columns = map(str.lower, data.columns)

    # Check if all required columns exist
    required_columns = ['id', 'severity', 'zipcode', 'start_time', 'end_time','visibility(mi)', 'weather_condition', 'country']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        print(f"Error: Missing columns: {', '.join(missing_columns)}")
        return None

    # Data cleaning operations...
    # Remove columns with 'Unnamed' in their name
    data = data.loc[:, ~data.columns.str.contains('^unnamed')]
    # Drop rows with any NA/null values
    data = data.dropna()
    checkColumns = ['id', 'severity', 'zipcode', 'start_time', 'end_time','visibility(mi)', 'weather_condition', 'country']
    data = data.dropna(subset=checkColumns)
    # Drop rows with less than 5 non-NA values
    data = data.dropna(thresh=5)
    # Remove rows where distance(mi) is 0
    data = data[data['distance(mi)'] != 0]
    # Extract first 5 characters of 'zipcode' column
    data['zipcode'] = data['zipcode'].astype(str).str[:5]
    # Convert 'start_time' and 'end_time' to datetime objects
    data['start_time'] = pd.to_datetime(data['start_time'])
    data['end_time'] = pd.to_datetime(data['end_time'])
    # Remove rows where 'end_time' equals 'start_time'
    data = data[data['end_time'] != data['start_time']]

    total_rows = len(data)
    print(f"[{time.strftime('%H:%M:%S')}] Total Rows Read after cleaning is: {total_rows}")
    
    end_time = time.time() # Record end time
    process_time = end_time - start_time # Calculate processing time
    print(f"\nTime to process is: {process_time:.2f} seconds")

    return data


def display_menu():
    # Function to display the menu options
    print("Menu:")
    print("1. Load data")
    print("2. Process data")
    print("3. Print Answers")
    print("4. Search Accidents (Use City, State, and Zip Code)")
    print("5. Search Accidents (Year, Month and Day)")
    print("6. Search Accidents (Temperature Range and Visibility Range)")
    print("7. Quit")

#Question 1 - 10
def question1(data):
    print("\n\t1. What are the 3 months with the highest amount accidents reported?")
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    # Count accidents per month and sort in descending order
    accidents_per_month = data['start_time'].dt.month.value_counts().sort_values(ascending=False)
    # Print the top 3 months with the highest accident counts
    for month_num, count in accidents_per_month.head(3).items():
        month_name = month_names[month_num]
        print(f"{month_name}: {count} accidents")
    print("")

def question2(data):
    print("\t2. What is the year with the highest amount of accidents reported?")
    # Count accidents per year
    accidents_per_year = data['start_time'].dt.year.value_counts()
    # Get the year with the maximum number of accidents
    max_year = accidents_per_year.idxmax()
    print(f"Year with the most accidents: {max_year}\n")

def question3(data):
    print("\t3. What is the state that had the most accidents of severity 2?, display the data per year.")
    # Filter data for severity 2 accidents
    severity_2_data = data[data['severity'] == 2]
    # Count severity 2 accidents per state
    accidents_per_state = severity_2_data['state'].value_counts()
    max_state = accidents_per_state.idxmax()
    print(f"The state that had the most accidents of severity 2: {max_state}")
    # Filter data for the state with the most severity 2 accidents
    state_data = severity_2_data[severity_2_data['state'] == max_state]
    # Count severity 2 accidents per year in the state
    accidents_per_year = state_data['start_time'].dt.year.value_counts().sort_index()
    print("Accidents per year:")
    for year, count in accidents_per_year.items():
        print(f"Year {year}: {count} accidents")
    print("")

def question4(data):
    print("\t4. What severity is the most common in Virginia, California, and Florida?")
    # List of states to analyze
    states = ['VA', 'CA', 'FL']
    for state in states:
        state_data = data[data['state'] == state] # Filter data for the state
        if not state_data.empty:
            severity_counts = state_data['severity'].value_counts() # Count severity occurrences in the state
            if not severity_counts.empty:
                most_common_severity = severity_counts.idxmax() # Get the most common severity
                print(f"Most common severity in {state}: Severity {most_common_severity}")
            else:
                print(f"No severity data available for {state}")
        else:
            print(f"No data available for {state}")
    print("")

def question5(data):
    print("\t5. What are the 5 cities that had the most accidents in in California? display the data per year.")
    # Filter data for California
    california_data = data[data['state'] == 'CA']
    # Group accidents by city and year, then count accidents per city per year
    accidents_per_city = california_data.groupby([california_data['city'], california_data['start_time'].dt.year]).size().reset_index(name='Accident Count')
    # Iterate over years and print top 5 cities with the most accidents each year
    for year, year_data in accidents_per_city.groupby('start_time'):
        print(f"Year {year}:")
        top_5 = year_data.nlargest(5, 'Accident Count')
        for index, row in top_5.iterrows():
            print(f"{row['city']}: {row['Accident Count']} accidents")
        print("")

def question6(data):
    print("\t6. What was the average humidity and average temperature of all accidents of severity 4 that occurred in the city of Boston? display the data per month.")
    # Filter data for severity 4 accidents in Boston
    boston_data = data[(data['severity'] == 4) & (data['city'] == 'Boston')]
    # Group data by month and calculate average humidity and temperature
    boston_data = boston_data.copy()
    boston_data['month'] = boston_data['start_time'].dt.month
    # Map month numbers to month names for readability
    monthly_average = boston_data.groupby('month').agg({'humidity(%)': 'mean', 'temperature(f)': 'mean'}).reset_index()
    monthly_average['month'] = monthly_average['month'].map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    print("Average Humidity and Temperature for Severity 4 Accidents in Boston:")
    print(monthly_average)
    print("")

def question7(data):
    print("\t7. What are the 3 most common weather conditions (weather_conditions) when accidents occurred in New York city? display the data per month.")
    # Filter data for New York City
    nyc_data = data[(data['city'] == 'New York') & (data['state'] == 'NY')]
    nyc_data = nyc_data.copy()
    # Extract month from start time
    nyc_data['month'] = nyc_data['start_time'].dt.month
    # Count occurrences of each weather condition per month
    weather_counts = nyc_data.groupby(['month', 'weather_condition']).size().reset_index(name='Count')
    weather_counts['month'] = weather_counts['month'].map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    # Iterate over unique months and print top 3 weather conditions for each month
    for month in weather_counts['month'].unique():
        month_data = weather_counts[weather_counts['month'] == month]
        top_3_weather_conditions = month_data.nlargest(3, 'Count').reset_index(drop=True)
        print(f"Top 3 weather conditions for {month}:")
        print(top_3_weather_conditions[['weather_condition', 'Count']].to_string(index=False))  
    print("\n")

def question8(data):
    print("\t8. What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire?")
    # Filter data for severity 2 accidents in New Hampshire
    nh_data = data[(data['state'] == 'NH') & (data['severity'] == 2)]
    # Check if there are any accidents with severity 2 in New Hampshire
    if nh_data.empty:
        print("No accidents with severity 2 found in the state of New Hampshire.")
    else:
        max_visibility = nh_data['visibility(mi)'].max()  # Calculate maximum visibility
        print(f"The maximum visibility of accidents with severity 2 in New Hampshire is: {max_visibility} miles.")
    print("")

def question9(data):
    print("\t9. How many accidents of each severity were recorded in Bakersfield? Display the data per year.")
    bakersfield_data = data[data['city'] == 'Bakersfield'] # Filter data for Bakersfield
    # Check if there are any accidents recorded in Bakersfield
    if bakersfield_data.empty:
        print("No accidents recorded in Bakersfield.")
    else:
        bakersfield_data = bakersfield_data.copy() # Extract year from start time
        bakersfield_data['year'] = bakersfield_data['start_time'].dt.year
        # Count occurrences of each severity per year
        severity_counts = bakersfield_data.groupby(['year', 'severity']).size().reset_index(name='Count')
        # Print severity counts per year
        for year in severity_counts['year'].unique():
            year_data = severity_counts[severity_counts['year'] == year]
            print(f"Year: {year}")
            print(year_data[['severity', 'Count']].to_string(index=False))
    print("")

def question10(data):
    print("\t10. What was the longest accident (in hours) recorded in Las Vegas in the Spring (March, April, and May)? Display the data per year.")
    # Filter data for Las Vegas during Spring
    lv_data = data[(data['city'] == 'Las Vegas') & (data['start_time'].dt.month.isin([3, 4, 5]))]
    # Check if there are any accidents recorded in Las Vegas during Spring
    if lv_data.empty:
        print("No accidents recorded in Las Vegas during Spring (March, April, May).")
    else:
        lv_data = lv_data.copy()  # Calculate duration of each accident in hours
        lv_data['duration'] = (lv_data['end_time'] - lv_data['start_time']).dt.total_seconds() / 3600
        # Find the longest accident per year
        longest_accidents_per_year = lv_data.groupby(lv_data['start_time'].dt.year)['duration'].max()
        print("Longest accident (in hours) recorded in Las Vegas in the Spring (March, April, and May) per year:")
        for year, duration in longest_accidents_per_year.items():
            print(f"Year: {year}, Duration: {duration:.2f} hours")
    print("\n")

def search_accidents_by_state_city_zip(data, state=None, city=None, zipcode=None):
    start_time = time.time()
    
    # Filter data based on input values
    filtered_data = data.copy()
    try:
        if state:
            filtered_data = filtered_data[filtered_data['state'] == state]
        if city:
            filtered_data = filtered_data[filtered_data['city'] == city]
        if zipcode:
            filtered_data = filtered_data[filtered_data['zipcode'] == zipcode]
    except KeyError:
            print("Error: Invalid column name. Please make sure your data contains 'state', 'city', and 'zipcode' columns.")
            return
    
    # Count the number of accidents
    num_accidents = len(filtered_data)
    
    print(f"Number of accidents in {state if state else 'all states'}, {city if city else 'all cities'}, {zipcode if zipcode else 'all zip codes'}: {num_accidents}")
    
    end_time = time.time()  # Record end time
    search_time = end_time - start_time
    print(f"Time to perform search: {search_time:.2f} seconds")

def search_accidents_by_year_month_day(data, year=None, month=None, day=None):
    start_time = time.time()

    datacopy = data.copy()
    datacopy['start_time'] = datacopy['start_time'].astype(str)
    filtered_data = datacopy.copy()
    if year:
        filtered_data = filtered_data[filtered_data['start_time'].str.startswith(str(year))]
    if month:
        filtered_data = filtered_data[filtered_data['start_time'].str[5:7] == str(month).zfill(2)]
    if day:
        filtered_data = filtered_data[filtered_data['start_time'].str[8:10] == str(day).zfill(2)]
    
    # Count the number of accidents
    num_accidents = len(filtered_data)
    
    print(f"Number of accidents in {year if year else 'all years'}-{month if month else 'all months'}-{day if day else 'all days'}: {num_accidents}")
    
    end_time = time.time()  # Record end time
    search_time = end_time - start_time
    print(f"Time to perform serach: {search_time:.2f} seconds")

def search_accidents_by_temperature_visibility(data, min_temp=None, max_temp=None, min_visibility=None, max_visibility=None):  
    start_time = time.time()

    required_columns = ['temperature(f)', 'visibility(mi)']

    # Validation: Check if input values are numbers
    if min_temp is not None and not min_temp.isdigit():
        print("Error: min_temp must be a number.")
        return
    if max_temp is not None and not max_temp.isdigit():
        print("Error: max_temp must be a number.")
        return
    if min_visibility is not None and not min_visibility.isdigit():
        print("Error: min_visibility must be a number.")
        return
    if max_visibility is not None and not max_visibility.isdigit():
        print("Error: max_visibility must be a number.")
        return
    
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
        filtered_data = filtered_data[(filtered_data['temperature(f)'] >= min_temp) & (filtered_data['temperature(f)'] <= max_temp)]
    if min_visibility and max_visibility:
        filtered_data = filtered_data[(filtered_data['visibility(mi)'] >= min_visibility) & (filtered_data['visibility(mi)'] <= max_visibility)]
    
    # Count the number of accidents
    num_accidents = len(filtered_data)
    
    print(f"Number of accidents with temperature between {min_temp if min_temp else 'any'} and {max_temp if max_temp else 'any'} Fahrenheit, and visibility between {min_visibility if min_visibility else 'any'} and {max_visibility if max_visibility else 'any'} miles: {num_accidents}")

    end_time = time.time()  # Record end time
    search_time = end_time - start_time
    print(f"Time to perform search: {search_time:.2f} seconds")

def main():

    # Main function to run the program
    start_time = time.time() # Record start time

    file_names = ["./data/US_Accidents_data.csv", "./data/InputDataSample.csv", "./data/Boston_Lyft_Uber_Data.csv"]  
    data = None
    data_loaded = False  # Flag to track whether data has been loaded
    data_processed = False

    while True:
        display_menu() # Display menu options
        choice = input("Enter your choice: ")

        if choice == "1":
            data = load_data()
            if data is not None:
                data_loaded = True
                print("Data loaded successfully.\n")
            else:
                print("Data unable to load.\n")

        elif choice == "2":
            if data_loaded:  # Check if data is loaded before processing
                data = clean_data(data)
                if data is not None:
                    data_processed = True
                    print("Data processed successfully.\n\n\n")
                else:
                    print("Data cannot be processed due to different column criteria.\n\n\n")
        elif choice == "3":
            if data_processed:
                print("Answering questions:\n")
                # Call functions to answer questions 1 to 10
                question1(data)
                question2(data)
                question3(data)
                question4(data)
                question5(data)
                question6(data)
                question7(data)
                question8(data)
                question9(data)
                question10(data)

                print("\n\n\n")
            else:
                print("Data not processed.\n\n\n")
        elif choice == "4":
            # Get input from user and call function to search accidents
            if data_processed:
                state = input("Enter a State(e.g CA): ").upper()  # Convert user input to uppercase
                city = input("Enter a city: ").capitalize()
                zipcode = input("Enter a zipcode: ") 
                search_accidents_by_state_city_zip(data, state, city, zipcode)
            else:
                print("Data not processed.\n\n\n")

            print("\n\n\n")
            pass
        elif choice == "5":
            # Get input from user and call function to search accidents
            if data_processed:
                year = input("Enter a year (YYYY): ")
                month = input("Enter a month (MM): ")
                day = input("Enter a day (DD): ") 
                search_accidents_by_year_month_day(data, year, month, day)
            else:
                print("Data not processed.\n\n\n")
            print("\n\n\n")
            pass
        elif choice == "6":
            # Get input from user and call function to search accidents
            if data_processed:
                min_t = input("Enter a minimum temperature (F): ")
                max_t = input("Enter a maximum temperature (F): ")
                min_v = input("Enter a minimum visibility (mi): ")
                max_v = input("Enter a maximum visibility (mi): ")
                search_accidents_by_temperature_visibility(data, min_t, max_t, min_v, max_v)
            else:
                print("Data not processed.\n\n\n")

            print("\n\n\n")
            pass
        elif choice == "7":
            print("Quitting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

    end_time = time.time()  # Record end time
    total_running_time = end_time - start_time # Calculate total running time
    print(f"Total running time: {total_running_time:.2f} seconds")


if __name__ == "__main__":
    main()
