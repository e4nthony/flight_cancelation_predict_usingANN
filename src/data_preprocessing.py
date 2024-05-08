import os
import pandas
import numpy
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

import weather


directory = os.getcwd()
print('Current Directory: ', directory)
assets_path = f"{os.path.dirname(directory)}\\assets"


# Display all the columns
pandas.set_option('display.max_columns', None)


def flights_concat(months):
    """
        This function is reads flight_reports [source1] files and processes it.

    Parameters:
        months (list): list of months that user prepared at directory ..\\assets\\flight_reports\\
    Returns:
        dataframe : that containing the
                                        localDateTime, - date of departure or arrival of flight,
                                        longitude and latitude - location of departure or arrival,
                                        IATA_LOCATION - location in format of IATA airport indexing. (3 letters)
                                        WEATHER_CANCEL is_weather_canceled
    """

    # Stage 1
    # This stage, we will read dataset and clean it up.

    dataframes_list = []

    # for each month in the list load dataset
    for one_month in months:

        # access to the dataset, where each file is month
        file_path = f"{assets_path}\\flight_reports\\{one_month}\\T_ONTIME_REPORTING.csv"

        # read file at file_path
        dataframes_list.append(pandas.read_csv(file_path, na_values='', keep_default_na=False, dtype=str))

    # concatenation of data about each month together
    df = pandas.concat(dataframes_list)
    # note that 'ORIGIN' and 'DEST' fields here is actually represented by IATA Airport Indeficator format (3 symbols)

    # clean up FL_DATE column, as result M/D/YYYY format
    df['FL_DATE'] = df['FL_DATE'].apply(lambda x: x.split(' ')[0])

    # ORIGIN column ok

    # DEST column ok

    # reformat DEP_TIME column
    df.rename(columns={"CRS_DEP_TIME": "DEP_TIME"}, inplace=True)

    # reformat ARR_TIME column
    df.rename(columns={"CRS_ARR_TIME": "ARR_TIME"}, inplace=True)

    # drop CANCELLED column
    df = df.drop('CANCELLED', axis=1)

    # CANCELLATION_CODE: replace every not B value with 0
    df.loc[df['CANCELLATION_CODE'] != 'B', 'CANCELLATION_CODE'] = 0
    df.loc[df['CANCELLATION_CODE'] == 'B', 'CANCELLATION_CODE'] = 1
    df.rename(columns={"CANCELLATION_CODE": "WEATHER_CANCEL"}, inplace=True)

    # testing output
    df.to_csv('out\\dataset1_processed_stage1.csv', index=False)  # test
    print('[Stage1]: Success')

    """
    Stage 2
    This stage, we will divide each row at dataset into separate row containing the departure info
                                                    and separate row containing the arrival info of specific flight.
    """

    df_divided_list = []

    # Select Origin info
    df_temp1 = df[['FL_DATE', 'ORIGIN', 'DEP_TIME', 'WEATHER_CANCEL']].copy()
    df_temp1.rename(columns={'ORIGIN': 'IATA_LOCATION',
                             'DEP_TIME': 'LOCAL_TIME', }, inplace=True)
    df_divided_list.append(df_temp1)

    # Select Destination info
    df_temp2 = df[['FL_DATE', 'DEST', 'ARR_TIME', 'WEATHER_CANCEL']].copy()
    df_temp2.rename(columns={'DEST': 'IATA_LOCATION',
                             'ARR_TIME': 'LOCAL_TIME'}, inplace=True)
    df_divided_list.append(df_temp2)

    # Combine, (dataframes are in the same format)
    df = pandas.concat(df_divided_list)

    def by_hours(df):
        """
        reformat LOCAL_TIME column to YYYY-MM-DD-THH:MM to be at the same format as weather data
        Use that function if we can find solution to work with scale of hourly weather reports.
        :param df: the dataframe we work with
        :return df: the dataframe we work with
        """
        df['localDateTime'] = df.apply(lambda row: row['FL_DATE'] + row['LOCAL_TIME'], axis=1)
        df = df.drop('FL_DATE', axis=1).drop('LOCAL_TIME', axis=1)

        # converts date and time string at format '%m/%d/%Y%H%M' to datetime object.
        df['localDateTime'] = pandas.to_datetime(df['localDateTime'], format='%m/%d/%Y%H%M')

        # reformat
        df['localDateTime'] = df['localDateTime'].dt.strftime("%Y-%m-%dT%H:%M")

        return df
    def by_days(df):
        """
        reformat LOCAL_TIME column to YYYY-MM-DD to be at the same format as weather data
        Use that function if we choose to work with scale of daily weather reports.
        :param df: the dataframe we work with
        :return df: the dataframe we work with
        """
        df = df.drop('LOCAL_TIME', axis=1)

        # converts date string at format '%m/%d/%Y' to datetime object
        df['FL_DATE'] = pandas.to_datetime(df['FL_DATE'], format='%m/%d/%Y')
        df.rename(columns={'FL_DATE': 'localDateTime'}, inplace=True)

        # reformat
        df['localDateTime'] = df['localDateTime'].dt.strftime("%Y-%m-%d")
        return df

    df = by_days(df)  # in this case we use daily weather reports.

    df.to_csv('out\\dataset1_processed_stage2.csv', index=False)   # Result
    print('[Stage2] Import and concat flight dataframes: Success')
    return df


def load_previous_procecced_data_from_stage2():
    file_path = "out\\dataset1_processed_stage2.csv"
    df = pandas.read_csv(file_path, na_values='', keep_default_na=False, dtype=str)

    print('load_previous_procecced_data_from_stage2(): Success')
    return df


def airports_location_process(dataframe_flights):
    """
    This function is combines between actual location of airport to time and date of the flight.
    It adds two columns of latitude_deg and longitude_deg to dataframe accordingly to IATA code of airport at the row.
    uses source[4]
    :param dataframe_flights: the dataframe right after completing stage 2
    :return combined_df:
    """

    dataframe_flights.rename(columns={'IATA_LOCATION': 'iata_code'}, inplace=True)

    # access to the airports dataset
    file_path = f"{assets_path}\\airports_data\\source4\\airports.csv"
    # note that 'iata_code' field here is in IATA Airport Indeficator format (3 symbols)

    # Loading the dataset
    df = pandas.read_csv(file_path, na_values='', keep_default_na=False, dtype=str)

    # select only relevant columns
    df = df[['latitude_deg', 'longitude_deg', 'iata_code']]

    # df.to_csv('out\\debug\\airports_data_out.csv', index=False)  # Testing

    # Concatenation of data about location and weather
    combined_df = pandas.merge(df, dataframe_flights, on='iata_code', how='inner')

    combined_df = combined_df.drop('iata_code', axis=1)

    combined_df.to_csv('out\\combined_stage3.csv', index=False)  # Result
    print('[Stage3] airports_location_process(..) : Success')

    return combined_df


def load_previous_procecced_data_from_stage3():
    file_path = "out\\combined_stage3.csv"
    df = pandas.read_csv(file_path, na_values='', keep_default_na=False, dtype=str)

    print('load_previous_procecced_data_from_stage3(): Success')
    return df


def load_previous_weather_data_from_stage4():
    file_path = "out\\weather\\daily_dataframe_stage4_global.csv"
    df = pandas.read_csv(file_path, na_values='', keep_default_na=False, dtype=str)

    print('load_previous_weather_data_from_stage4(): Success')
    return df

def load_previous_weather_data_from_stage5():
    file_path = "out\\combined_stage5.csv"
    df = pandas.read_csv(file_path, na_values='', keep_default_na=False, dtype=str)

    print('load_previous_weather_data_from_stage5(): Success')
    return df


def weather_and_cancelationcode_concat(df_flights, weather_responce):
    """
    This function is combines between weather data to cancelation_code of particular flight.
    After concatenation, it drops columns that are not relevant for model.

    :param df_flights: the dataframe right after completing stage 3.
    :param weather_responce: the dataframe we got as responce from server (stage 4).
    :return df:
    """

    df_flights.rename(columns={"localDateTime": "date"}, inplace=True)

    print('shift daily weather reports one day foward... \t weather_responce.iloc[0]', weather_responce.iloc[0]['date'])  # Debug
    # we shift daily weather reports one day foward.
    # so now weather at date x-1 will point to flight at date x.
    weather_responce['date'] = pandas.DatetimeIndex(weather_responce['date']) + pandas.DateOffset(1)
    weather_responce['date'] = weather_responce['date'].dt.strftime("%Y-%m-%d")
    print('new value:, \t weather_responce.iloc[0]', weather_responce.iloc[0]['date'])  # Debug

    combined_df = pandas.merge(df_flights, weather_responce, on=['longitude_deg', 'latitude_deg', 'date'], how='inner')

    # drop irrelevant data
    combined_df = combined_df.drop('longitude_deg', axis=1).drop('latitude_deg', axis=1).drop('date', axis=1)

    combined_df.to_csv('out\\combined_stage5.csv', index=False)  # Result
    print('[Stage5] weather_and_cancelationcode_concat : Success')
    return combined_df


def data_preprocessing(MONTHS, REPROCESS_FLIGHT_DATA, REREQUEST_WEATHER_DATA):
    if not REPROCESS_FLIGHT_DATA and not REREQUEST_WEATHER_DATA:
        return load_previous_weather_data_from_stage5()

    if REPROCESS_FLIGHT_DATA:
        # [Stage1-2]
        df_flights = flights_concat(MONTHS)
        # [Stage3]
        df_flights = airports_location_process(df_flights)
    else:
        # Load from memory [Stage1-2-3]
        df_flights = load_previous_procecced_data_from_stage3()

    # [Stage4]
    if REREQUEST_WEATHER_DATA:
        first_date = MONTHS[0] + '-01'
        last_date = (datetime.strptime(MONTHS[-1], "%Y-%m") + relativedelta(months=1)).strftime("%Y-%m") + '-01'
        weather_responce = weather.weather_request(df_flights, first_date, last_date)
    else:
        # Load from memory
        weather_responce = load_previous_weather_data_from_stage4()

    # [Stage5]
    return weather_and_cancelationcode_concat(df_flights, weather_responce)