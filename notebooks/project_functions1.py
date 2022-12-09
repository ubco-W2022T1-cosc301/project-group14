import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

def load_and_process(url_or_path_to_csv_file):
    '''Method Chain 1 (Loads data and reorganizes columns)'''
    
    new_col_names = ['instant', 'dteday', 'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    new_col_order = ['date', 'hour', 'count', 'casual', 'registered', 'season', 'holiday', 'weekday', 'workingday', 'weather', 'temp', 'humidity']

    dfCols = pd.read_csv(url_or_path_to_csv_file).reset_index()[new_col_names]

    # days = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
    days = { 0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday' }
    hours = {0: '12:00h', 1: '1:00h', 2: '2:00h', 3: '3:00h', 4: '4:00h', 5: '5:00h', 6: '6:00h', 7: '7:00h', 8: '8:00h', 9: '9:00h', 10: '10:00h', 11: '11:00h', 12: '12:00h', 13: '13:00h', 14: '14:00h', 15: '15:00h', 16: '16:00h', 17: '17:00h', 18: '18:00h', 19: '19:00h', 20: '20:00h', 21: '21:00h', 22: '22:00h', 23: '23:00h'}
    # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    df1 = (
        dfCols
        .drop(['instant', 'mnth', 'yr', 'atemp', 'windspeed'], axis=1)
        .dropna(axis=0)
        .rename(columns={"dteday": "date", "hr": "hour", "cnt": "count", "weathersit": "weather", "hum": "humidity"})
        .replace({"weekday": days, "hour": hours})
        .sort_values("count", ascending=False)[new_col_order]
    )

    # make date datetime object
    df1['date'] = pd.to_datetime(df1['date'], format='%Y-%m-%d')
    
    return df1


def save_fig(ax, filename):
    '''Saves a plot axes object to a file'''
    fig = ax.get_figure()
    # fig.subplots_adjust(bottom=0.25)
    fig.tight_layout()
    fig.savefig(filename)


def get_avg_from_month(df, month, day=0, year=0):
    '''Returns the average number of users for a given month. This also accepts a day and year parameter for specificity.'''
    dateRange = df
    if year != 0:
        dateRange = dateRange[dateRange['date'].dt.year == year]
    dateRange = dateRange[dateRange['date'].dt.month == month]
    if day != 0:
        dateRange = dateRange[dateRange['date'].dt.day == day]

    return dateRange['count'].mean().round()
    

def get_reg_users_from_week_df(df):
    '''Returns a dataframe with the average number of registered users for each weekday.'''
    return df[['weekday', 'registered']].groupby(['weekday',], as_index=False).mean().round(0).sort_values('registered', ascending=False).rename({'weekday': 'Weekday', 'registered': 'Avg. Registered Users'}, axis=1)


def get_count_users_years_df(df):
    '''Returns a dataframe with the total number of users for each year.'''
    return df[['date', 'count']].groupby(df['date'].map(lambda x: x.year)).sum(numeric_only=True).sort_values('count', ascending=False).rename({'date': 'Year', 'count': 'Total Users'}, axis=1)


def get_annual_users_barplot(df):
    '''Returns a barplot of the total number of users for each year.'''
    frame = get_count_users_years_df(df)
    ax = sns.barplot(data=frame, x=frame.index, y='Total Users')
    ax.set_title('Total Users by Year')
    ax.tick_params(bottom=False)
    ax.set(xlabel='Year', ylabel='Total Users')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    sns.despine()
    return ax


def avg_reg_users_barplot(df):
    '''Returns a barplot of the average number of registered users for each weekday.'''
    ax = sns.barplot(data=get_reg_users_from_week_df(df), x='Weekday', y='Avg. Registered Users', palette=sns.color_palette("hls", 7))
    ax.set_title('Average Registered Users by Weekday')
    ax.tick_params(bottom=False)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    sns.despine()
    return ax


def create_count_by_holiday_barplot(df):
    # SELECT SUM(count) AS totalCount FROM df_to_analyze WHERE holiday = 1 GROUP BY date HAVING ORDER BY totalCount DESC;
    holiday = df[['date', 'count']].loc[df['holiday'] == 1].groupby(['date',], as_index=False).sum().sort_values('count', ascending=False)
    #.groupby(['holiday'], as_index=False).mean().round().sort_values('count', ascending=False)

    xlabels = holiday['date'].dt.strftime('%Y-%m-%d').unique()

    mnth_day = holiday['date'].dt.strftime('%m-%d').unique()

    holiday_strings = {
        '01-02': 'New Years',
        '01-16': 'Martin Luther King Jr. Day',
        '01-17': 'Martin Luther King Jr. Day',
        '02-20': 'Presidents Day',
        '02-21': 'Presidents Day',
        '04-15': 'Emancipation Day (DC)',
        '04-16': 'Emancipation Day (DC)',
        '05-28': 'Memorial Day',
        '05-30': 'Memorial Day',
        '07-04': 'Independence Day',
        '09-03': 'Labor Day',
        '09-05': 'Labor Day',
        '10-08': 'Columbus Day',
        '10-10': 'Columbus Day',
        '11-11': 'Veterans Day',
        '11-12': 'Veterans Day',
        '11-22': 'Thanksgiving',
        '11-24': 'Thanksgiving',
        '12-25': 'Christmas Day',
        '12-26': 'Christmas Day',
    }

    for k,v in holiday_strings.items():
        for d in range(len(xlabels)):
            if k in xlabels[d]:
                xlabels[d] = f"{v} ({xlabels[d][:4]})"


    ax = sns.barplot(data=holiday, y='date', x='count', palette='Blues_d')
    ax.set_title("Total Count of Bikes Rented on Holidays")
    ax.set(xlabel='Count', ylabel='Holiday')
    ax.set_yticklabels(labels=xlabels)
    sns.despine()
    return ax


def month_2012_weather_barplot(df, m, mname=''):
    weather_df = df[['weather', 'date']].loc[lambda row: row['date'].dt.strftime("%Y-%m") == f"2012-{str(m).zfill(2)}"]
    ax = sns.countplot(data=weather_df, x='weather', hue='weather', dodge=False, palette='Blues_d')
    ax.set_title(f"Counts of Weather Conditions in {mname} 2012")
    ax.set(xlabel='Weather', ylabel='Count')
    ax.tick_params(bottom=False)
    ax.get_legend().remove()
    sns.despine()
    return ax


def save_april_weather_barplot(df):
    save_fig(month_2012_weather_barplot(df, 4, "April"), '../images/april_weather_barplot.png')

def save_march_weather_barplot(df):
    save_fig(month_2012_weather_barplot(df, 3, "March"), '../images/march_weather_barplot.png')


def avg_temp_from_month(df, month):
    return f"{(df[['temp', 'date']].loc[lambda row: row['date'].dt.strftime('%m') == str(month).zfill(2)].mean(numeric_only=True).round(1)[0] * 39):.2f}" + '°C'

if __name__ == "__main__":
    df = load_and_process("data/raw/Bike-Sharing-Dataset/hour.csv")
    print(df.head())