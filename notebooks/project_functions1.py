import pandas as pd

def load_and_process(url_or_path_to_csv_file):
    # Method Chain 1 (Load data and deal with missing data)
    
    new_col_order = ['date', 'hour', 'count', 'casual', 'reg', 'season', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'hum']
    days = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
    hours = {0: '12:00h', 1: '1:00h', 2: '2:00h', 3: '3:00h', 4: '4:00h', 5: '5:00h', 6: '6:00h', 7: '7:00h', 8: '8:00h', 9: '9:00h', 10: '10:00h', 11: '11:00h', 12: '12:00h', 13: '13:00h', 14: '14:00h', 15: '15:00h', 16: '16:00h', 17: '17:00h', 18: '18:00h', 19: '19:00h', 20: '20:00h', 21: '21:00h', 22: '22:00h', 23: '23:00h'}
    # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    df1 = (
        pd.read_csv(url_or_path_to_csv_file)
        .drop(['instant', 'mnth', 'yr', 'atemp', 'windspeed'], axis=1)
        .dropna(axis=0)
        .rename(columns={"dteday": "date", "hr": "hour", "cnt": "count", "registered": "reg"})
        .replace({"weekday": days, "hour": hours})
        .sort_values("count", ascending=False)[new_col_order]
    )
    
    return df1

def get_avg_from_month(df, month, day='', year=''):
    return df[['date', 'count']].loc[df['date'].str.contains(f'{str(year)}-{str(month)}-{str(day)}')].groupby(['date',], as_index=False).sum().sort_values('count', ascending=False).mean(numeric_only=True).round()[0]



if __name__ == "__main__":
    df = load_and_process("data/raw/Bike-Sharing-Dataset/hour.csv")
    print(df.head())