import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Welcome to our program. Here, we will be exploring some US bikeshare data!\n')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    
    while city.lower() not in CITY_DATA.keys():
        print("\nThe cities we will be exploring are: \n1. Chicago 2. New York City 3. Washington)")
        print("\nNOTE!!! \nAccepted input includes: full name of city; not case sensitive (e.g. chicago or CHICAGO) and full name in title case (e.g. Chicago).")
        #Taking user input and converting into lower to standardize them
        city = input("\nPlease enter your city: ")

        if city.lower() not in CITY_DATA.keys():
            print("\nPlease check your input, it doesn\'t appear to be conforming to any of the accepted input formats.")
            print("\nRestarting...")
            
    print(f"\nYou have selected {city.title()} as your city.")
    
    # TO DO: get user input for month (all, january, february, ... , june)
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month.lower() not in MONTH_DATA.keys():
        print("\nOverhere, you will be entering the month, between January to June, for which you're seeking the data.")
        print("NOTE!\n Accepted input includes:Full month name; not case sensitive (e.g. january or JANUARY) and \nfull month name in title case (e.g. May). You may also opt to view data for all months by typing 'All'.")
        month = input("\nEnter the Month of the data required: ")

        if month.lower() not in MONTH_DATA.keys():
            print("\nInvalid input. Please try again in the accepted input format.")
            print("\nRestarting...")

    print(f"You have chosen {month.title()} as your month.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day.lower() not in DAY_LIST:
        print("\nHere we will be entering a day in the week of your choice for which you're seeking the data.")
        print("NOTE!\nAccepted input includes:\nDay name; not case sensitive (e.g. monday or MONDAY) and \nDay name in title case (e.g. Monday). You can also view the data for all days in a week by inputing 'All'.")
        day = input("\nEnter the day of week for which you seek the data: ")

        if day.lower() not in DAY_LIST:
            print("\nInvalid input. Please try again in one of the accepted input formats.")
            print("\nRestarting...")

    print(f"You have chosen {day.title()} as your day.")
    
    print(f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")

    print('-'*40)
    return city, month, day;


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    # TO DO: display the most common day of week
    df['hour'] = df['Start Time'].dt.hour
    popular_day = df['day_of_week'].mode()[0]
    print(f"\nMost Popular Day: {popular_day}")


    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print(f"\nMost Popular Start Hour: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}")

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station: {common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]
    print(f"\nThe most frequent combination of trips are from {combo}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")


    # TO DO: display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"The types of users by number are given below:\n\n{user_type}")

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

#Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        rdata = input()
        #the raw data from the df is displayed if user opts for it
        if rdata.lower() == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input()
        #If user opts for it, this displays next 5 rows of data
        if rdata.lower() == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*40)
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
