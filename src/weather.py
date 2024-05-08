# *Based on documentation from open-meteo.com site.

import openmeteo_requests

import requests_cache
import pandas
from retry_requests import retry
import time

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=13600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def weather_request(df_original, first_date, last_date):
    """
    This function sends api request to openweather for each airport location.

    As result, we get answer from server with all weather during period between first_date and last_date for location x.
    We send multiple requests as count of different airports that are present at our dataset.

    :param df_original: dataframe we worked with, right after completing stage 3 of processing.
    :param first_date (str): format YYYY-MM-01 example: 2023-01-01
    :param last_date (str): format YYYY-MM-01 example: 2024-01-01
    :return df: dataframe that contains weather forecast combined from all requests.
    """
    DEBUG_MODE = False

    df_clean = df_original.drop('WEATHER_CANCEL', axis=1).drop('localDateTime', axis=1)
    df_clean = df_clean.drop_duplicates(subset=['latitude_deg', 'longitude_deg'])

    if DEBUG_MODE:
        df_clean.to_csv('out\\debug\\airport_locations_raw.csv', index=False)  # Debug, To know count of future requests as count of lines in this dataframe.
        print('[Debug] airport_locations_raw export: Success')  # Debug

    # clean_testing_dataframe = {
    # 	'latitude_deg': [40.651773, 32.4113006592, 35.039976],
    # 	'longitude_deg': [-75.442797, -99.68190002440001, -106.608925]
    # }
    df_clean = pandas.DataFrame(df_clean)


    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"

    dataframes_list = []

    def actual_request(row, real_counter):
        latitude = row['latitude_deg']
        longitude = row['longitude_deg']

        params_daily = {
            "latitude": {latitude},
            "longitude": {longitude},
            "start_date": {first_date},
            "end_date": {last_date},
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "precipitation_sum",
                "rain_sum",
                "snowfall_sum",
                "precipitation_hours",
                "sunrise",
                "sunset",
                "sunshine_duration",
                "daylight_duration",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "wind_direction_10m_dominant",
                "shortwave_radiation_sum",
                "et0_fao_evapotranspiration"
            ]
        }

        if DEBUG_MODE: print(f"[Debug] sent request {real_counter}")  # Debug
        responses = openmeteo.weather_api(url, params=params_daily)  # ERROR IN OFFICIAL DOCUMENTATION KH%&*(Q#^*XJ!!!!!
        if DEBUG_MODE: print(f"[Debug] got responce {real_counter}, processing...")  # Debug

        response = responses[0]
        # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        # print(f"Elevation {response.Elevation()} m asl")
        # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        weather_code = daily.Variables(0).ValuesAsNumpy()
        temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
        apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
        precipitation_sum = daily.Variables(5).ValuesAsNumpy()
        rain_sum = daily.Variables(6).ValuesAsNumpy()
        snowfall_sum = daily.Variables(7).ValuesAsNumpy()
        precipitation_hours = daily.Variables(8).ValuesAsNumpy()
        sunrise = daily.Variables(9).ValuesAsNumpy()
        sunset = daily.Variables(10).ValuesAsNumpy()
        sunshine_duration = daily.Variables(11).ValuesAsNumpy()
        daylight_duration = daily.Variables(12).ValuesAsNumpy()
        wind_speed_10m_max = daily.Variables(13).ValuesAsNumpy()
        wind_gusts_10m_max = daily.Variables(14).ValuesAsNumpy()
        wind_direction_10m_dominant = daily.Variables(15).ValuesAsNumpy()
        shortwave_radiation_sum = daily.Variables(16).ValuesAsNumpy()
        et0_fao_evapotranspiration = daily.Variables(17).ValuesAsNumpy()

        daily_data = {"date": pandas.date_range(
            start=pandas.to_datetime(daily.Time(), unit="s", utc=True),
            end=pandas.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pandas.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )}
        print('daily_data:', daily_data)

        daily_data["weather_code"] = weather_code
        daily_data["temperature_2m_max"] = temperature_2m_max
        daily_data["temperature_2m_min"] = temperature_2m_min
        daily_data["apparent_temperature_max"] = apparent_temperature_max
        daily_data["apparent_temperature_min"] = apparent_temperature_min
        daily_data["precipitation_sum"] = precipitation_sum
        daily_data["rain_sum"] = rain_sum
        daily_data["snowfall_sum"] = snowfall_sum
        daily_data["precipitation_hours"] = precipitation_hours
        # daily_data["sunrise"] = sunrise  # for now we are not using that data, might be need later.
        # daily_data["sunset"] = sunset
        # daily_data["sunshine_duration"] = sunshine_duration
        # daily_data["daylight_duration"] = daylight_duration
        daily_data["wind_speed_10m_max"] = wind_speed_10m_max
        daily_data["wind_gusts_10m_max"] = wind_gusts_10m_max
        daily_data["wind_direction_10m_dominant"] = wind_direction_10m_dominant
        daily_data["shortwave_radiation_sum"] = shortwave_radiation_sum
        daily_data["et0_fao_evapotranspiration"] = et0_fao_evapotranspiration

        # add location (of airport) that was used for this request
        daily_data["latitude_deg"] = latitude
        daily_data["longitude_deg"] = longitude

        daily_dataframe = pandas.DataFrame(data=daily_data)

        if DEBUG_MODE:  # Backup Result for every request (debug/testing)
            daily_dataframe.to_csv(f'out\\weather_debug\\daily_dataframe_stage4_df{real_counter}.csv', index=False)

        # print('Getting weather : Success')
        # print("daily_dataframe:", daily_dataframe)

        return daily_dataframe

    real_counter = 1  # we need it to track the number of requests in real time,
    #                       because we dropped index columns in df and now index variable counting wrong
    for index, row in df_clean.iterrows():

        dataframes_list.append(actual_request(row, real_counter))

        print(f"Response {real_counter} was processed successfully.")
        real_counter = real_counter + 1

        time.sleep(4)  # seconds, to not exceed max limit of requests per minute and per hour

    # loop end
    print("for loop ended successfully.")

    # concatenation of data about each location to one dataframe
    df = pandas.concat(dataframes_list)

    # clean up the date column at format 'YYYY-MM-DD 00:00:00+00:00' to keep only YYYY-MM-DD format.
    df['date'] = df['date'].dt.strftime("%Y-%m-%d")

    df.to_csv(f'out\\weather\\daily_dataframe_stage4_global.csv', index=False)  # Result

    print('[Stage4] Getting and concat weather dataframes: Success')
    return df
