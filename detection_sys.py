import os
import pandas as pd
from datetime import datetime

VEHICLES_DF = {}

def read_file(filename_with_path):
    """
    Method to read the csv file
    :return:
    """
    try:
        if not os.path.exists(filename_with_path):
            return False, "Please pass the valid filepath"
        df = pd.read_csv(filename_with_path, header=0)
        return True, df
    except Exception as exp:
        return False, exp


def build_unique_vehicle_df(df):
    """
    Method to build data frame for each vehicle with any no of entries
    :return:
    """
    try:
        vehicle_column = df['Number'].to_list()
        VEHICLES_DF = dict.fromkeys(vehicle_column)
        for index, row in df.iterrows():
            if VEHICLES_DF[row['Number']] is None:
                vehicle_df = pd.DataFrame(columns=df.columns)
                vehicle_df.loc[0] = row
                VEHICLES_DF[row['Number']] = vehicle_df
            else:
                VEHICLES_DF[row['Number']] = VEHICLES_DF[row['Number']].append(row)
        return VEHICLES_DF
    # key Error handle
    except as Exception:
        VEHICLES_DF = {}
        print(traceback.print_exc())
        return VEHICLES_DF
        


def get_avg_time(vehicles_df):
    """
    This returns avg time a vehicle is parked
    :param vehicles_df:
    :return:
    """
    avg_time = {}

    for vehicle, data_frame in vehicles_df.items():
        print(vehicle)
        date_index = data_frame.columns.get_loc("Date")
        # TOTAL DAYS CALCULATED
        date_col = data_frame["Date"].to_list()
        total_days = len(list(dict.fromkeys([i.split(" ")[0] for i in
                                             date_col])))
        vehicles_data_list = data_frame.values.tolist()
        avg_hours = 0
        flag = 0
        for i in range(len(vehicles_data_list)-1):
            FMT = '%Y-%m-%d %H:%M:%S.%f'
            if len(vehicles_data_list) % 2 != 0 and not flag:
                dt = datetime.strptime(vehicles_data_list[-1][date_index], FMT)
                avg_hours = avg_hours + 24 - dt.hour
                flag = 1
                print("AVG", avg_hours, vehicle)
            if i % 2 == 0:
                print(i, vehicles_data_list[i+1])
                dt1 = datetime.strptime(vehicles_data_list[i][date_index], FMT)
                dt2 = datetime.strptime(vehicles_data_list[i+1][date_index], FMT)
                diff = dt2 - dt1
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds // 3600
                avg_hours = avg_hours + hours
        avg_time[vehicle] = ["Avg hour per day:", avg_hours/total_days,
                             "Total Days:", total_days]
    return avg_time


status, df = read_file("sample.csv")
data = build_unique_vehicle_df(df)
print(get_avg_time(data))
