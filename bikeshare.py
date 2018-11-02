import time
import datetime
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
    filters = {}
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input ("Which city's data would you like to look at? (Chicago, New York City or Washington)")
            break
        except (ValueError, KeyboardInterrpt, TypeError):
            print("Please enter either Chicago, New York City or Washington")
        finally:
            filters['city_name'] = city
            print("Looking at data for {}".format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input ("Which month's (January, February, March, April, May, June or all) data would you like to look at?")
            break
        except (ValueError, KeyboardInterrpt, TypeError):
            print("Please enter either all, January, February, March, April, May or June.")
        finally:
            filters['month_name'] = month
            print("Looking at data for {}".format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input ("Which day of the week would you like to look at data for?")
            break
        except (ValueError, KeyboardInterrpt, TypeError):
            print("Please enter either all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.")
        finally:
            filters['day_name'] = day
            print("Looking at data for {}".format(day))

    print('-'*40)
    return city, month, day


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("\nThe most popular month to travel is: {}".format(popular_month))

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print("\nThe most popular day to travel is: {}".format(popular_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most popular start hour to travel is: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def sec2time(sec, n_msec=3):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nThe most popular start station is: {}".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nThe most popular end station is: {}".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combo = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).head(1)
    print("\nThe most frequent trip from station to station is:")
    print(most_common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    total_time = sec2time(total_time)
    print("\nThe total travel time: {}".format(total_time))

    # TO DO: display mean travel time
    average_time = df['Trip Duration'].mean()
    average_time = sec2time(average_time)
    print("\nThe average travel time: {}".format(average_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print("\nThe count of gender: {}".format(user_gender))
    else:
        print("No gender data available for {}".format(city))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        most_common_birth_year = df['Birth Year'].mode()
        earliest_birth_year = df['Birth Year'].min()
        latest_birth_year = df['Birth Year'].max()
        print("\nThe most common birth year: {}".format(most_common_birth_year))
        print("\nThe earliest birth year: {}".format(str(earliest_birth_year)))
        print("\nThe most recent birth year: {}".format(str(latest_birth_year)))
    else:
        print("No Birth Year data available for {}".format(city))

    print("\nThe count of different user types:\n {}".format(user_types))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, city, n):
    """Displays raw data if requested by user"""
    print("Here is the raw data for the first 5 trips for {}".format(city))
    print(df.head(5+n))
    more_data = input('\nWould you like to see more? Enter yes or no.\n')
    if more_data.lower() != 'yes':
        pass
    else:
        return display_data(df, city, n + 5)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df, city, 0)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
