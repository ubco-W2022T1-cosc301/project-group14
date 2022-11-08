import pandas as pd
def load_and_process(url_or_path_to_csv_file):
    
    df1 = (
        pd.read_csv("../data/raw/Bike-Sharing-Dataset/hour.csv")
        .rename(columns={"dteday":"date", "hr":"hour", "cnt":"count", "hum":"humidity"})
        .drop(['instant', 'mnth', 'yr', 'atemp', 'windspeed'], axis=1)
        .loc[:, ["date", "hour", "count", "casual", "registered", "season", "holiday", "weekday", "workingday", "weathersit", "temp", "humidity"]]
    )
    return df1
display(load_and_process("../data/raw/Bike-Sharing-Dataset/hour.csv"))


