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

import time  # Import the time module for time-related operations
import pandas as pd  # Import the pandas library for data manipulation

def loadData(filePath):
    # Function to load the dataset from a CSV file
    print("Loading and cleaning input data set:")
    print("************************************")

    start_time = time.time()  # Record start time for loading data

    # Read CSV file
    print(f"[{time.strftime('%H:%M:%S')}] Starting Script")
    print(f"[{time.strftime('%H:%M:%S')}] Loading {filePath}")
    data = pd.read_csv(filePath)

    total_columns = len(data.columns)  # Calculate total columns in the dataset
    print(f"[{time.strftime('%H:%M:%S')}] Total Columns Read: {total_columns}")

    # Calculate total rows in the dataset
    total_rows = len(data)
    print(f"[{time.strftime('%H:%M:%S')}] Total Rows Read: {total_rows}")

    end_time = time.time()  # Record end time for loading data
    load_time = end_time - start_time  # Calculate time taken to load data
    print(f"\nTime to load is: {load_time:.2f} seconds")

    return data  # Return the loaded data

def cleanData(data):
    # Function to clean the input dataset
    print("Processing input data set:")
    print("**************************")

    start_time = time.time()  # Record start time for data cleaning
    print(f"[{time.strftime('%H:%M:%S')}] Performing Data Clean Up")

    # Data cleaning operations
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

    total_rows = len(data)  # Calculate total rows after cleaning
    print(f"[{time.strftime('%H:%M:%S')}] Total Rows Read after cleaning is: {total_rows}")

    end_time = time.time()  # Record end time for data cleaning
    process_time = end_time - start_time  # Calculate time taken for data cleaning
    print(f"\nTime to process is: {process_time:.2f} seconds")

    return data  # Return the cleaned data

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

# Functions for answering questions
# Question 1 - 10

def search_accidents_by_state_city_zip(data, state=None, city=None, zipcode=None):
    # Function to search accidents by state, city, and zip code
    start_time = time.time()  # Record start time for the search

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

    # Print the number of accidents and time taken for the search
    print(f"Number of accidents in {state if state else 'all states'}, {city if city else 'all cities'}, {zipcode if zipcode else 'all zip codes'}: {num_accidents}")

    end_time = time.time()  # Record end time for the search
    search_time = end_time - start_time  # Calculate time taken for the search
    print(f"Time to perform search: {search_time:.2f} seconds")

def search_accidents_by_year_month_day(data, year=None, month=None, day=None):
    # Function to search accidents by year, month, and day
    start_time = time.time()  # Record start time for the search

    # Convert data types and filter data based on input values
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

    # Print the number of accidents and time taken for the search
    print(f"Number of accidents in {year if year else 'all years'}-{month if month else 'all months'}-{day if day else 'all days'}: {num_accidents}")

    end_time = time.time()  # Record end time for the search
    search_time = end_time - start_time  # Calculate time taken for the search
    print(f"Time to perform search: {search_time:.2f} seconds")

def search_accidents_by_temperature_visibility(data, min_temp=None, max_temp=None, min_visibility=None, max_visibility=None):
    # Function to search accidents by temperature and visibility range
    start_time = time.time()  # Record start time for the search

    # Convert input values to float if they are not None
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

    # Print the number of accidents and time taken for the search
    print(f"Number of accidents with temperature between {min_temp if min_temp else 'any'} and {max_temp if max_temp else 'any'} Fahrenheit, and visibility between {min_visibility if min_visibility else 'any'} and {max_visibility if max_visibility else 'any'} miles: {num_accidents}")

    end_time = time.time()  # Record end time for the search
    search_time = end_time - start_time  # Calculate time taken for the search
    print(f"Time to perform search: {search_time:.2f} seconds")

def main():
    start_time = time.time()  # Record start time for the program

    filePath = "US_Accidents_data.csv"  # Path to the dataset file
    data = None  # Initialize data variable

    while True:
        display_menu()  # Display the menu options
        choice = input("Enter your choice: ")  # Get user input for menu choice

        if choice == "1":
            if data is None:
                data = loadData(filePath)  # Load data if not already loaded
                print("Data loaded successfully.\n\n\n")
            else:
                print("Data is already loaded.\n\n\n")
        elif choice == "2":
            if data is not None:
                data = cleanData(data)  # Process data if data is loaded
                print("Data processed successfully.\n\n\n")
            else:
                print("Please load data first.\n\n\n")
        elif choice == "3":
            if data is not None:
                # Answer questions if data is loaded
                print("Answering questions:\n")
                Question1(data)
                Question2(data)
                Question3(data)
                # More question functions can be called here...
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

    end_time = time.time()  # Record end time for the program
    total_running_time = end_time - start_time  # Calculate total running time
    print(f"Total running time: {total_running_time:.2f} seconds")


if __name__ == "__main__":
    main()


