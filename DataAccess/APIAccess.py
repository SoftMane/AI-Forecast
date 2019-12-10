import requests
import json
from datetime import datetime

class APIAccess():
    # Cleveland: 5150529
    # Buffalo: 5110629
    # Pittsburgh: 5206379
    # Chicago: 4887398
    # Erie: 5188843


    def getCurrent(self):
        key = 'aa91a3b5b86f47f610e04485584c5693'
        url = 'http://api.openweathermap.org/data/2.5/weather'
        id = 5188843
        id_1 = 5150529
        id_2 = 5110629
        id_3 = 5206379
        # for Erie
        params = {'APPID': key, 'id': id}
        response = requests.get(url, params=params)
        json_data = json.loads(response.text) # json response from API
        # get and convert date to understandable format
        date = json_data.get('dt')
        date = datetime.fromtimestamp(date)
        # retrieve needed inputs from date
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.hour = date.hour
        # retrieve needed inputs
        self.temp = json_data.get('main').get('temp')
        self.min_temp = json_data.get('main').get('temp_min')
        self.max_temp = json_data.get('main').get('temp_max')
        self.pressure = json_data.get('main').get('pressure')
        self.humidity = json_data.get('main').get('humidity')
        self.wind_speed = json_data.get('wind').get('speed')
        self.wind_dir = json_data.get('wind').get('deg')
        print(json_data)

        # For first city
        params = {'APPID': key, 'id': id_1}
        response = requests.get(url, params=params)
        json_data = json.loads(response.text)  # json response from API
        # get and convert date to understandable format
        date = json_data.get('dt')
        date = datetime.fromtimestamp(date)
        # retrieve needed inputs from date
        self.year_1 = date.year
        self.month_1 = date.month
        self.day_1 = date.day
        self.hour_1 = date.hour
        # retrieve needed inputs
        self.temp_1 = json_data.get('main').get('temp')
        self.min_temp_1 = json_data.get('main').get('temp_min')
        self.max_temp_1 = json_data.get('main').get('temp_max')
        self.pressure_1 = json_data.get('main').get('pressure')
        self.humidity_1 = json_data.get('main').get('humidity')
        self.wind_speed_1 = json_data.get('wind').get('speed')
        self.wind_dir_1 = json_data.get('wind').get('deg')
        print(json_data)

        # For second city
        params = {'APPID': key, 'id': id_2}
        response = requests.get(url, params=params)
        json_data = json.loads(response.text)  # json response from API
        # get and convert date to understandable format
        date = json_data.get('dt')
        date = datetime.fromtimestamp(date)
        # retrieve needed inputs from date
        self.year_2 = date.year
        self.month_2 = date.month
        self.day_2 = date.day
        self.hour_2 = date.hour
        # retrieve needed inputs
        self.temp_2 = json_data.get('main').get('temp')
        self.min_temp_2 = json_data.get('main').get('temp_min')
        self.max_temp_2 = json_data.get('main').get('temp_max')
        self.pressure_2 = json_data.get('main').get('pressure')
        self.humidity_2 = json_data.get('main').get('humidity')
        self.wind_speed_2 = json_data.get('wind').get('speed')
        self.wind_dir_2 = json_data.get('wind').get('deg')
        print(json_data)

        # For third city
        params = {'APPID': key, 'id': id_3}
        response = requests.get(url, params=params)
        json_data = json.loads(response.text)  # json response from API
        # get and convert date to understandable format
        date = json_data.get('dt')
        date = datetime.fromtimestamp(date)
        # retrieve needed inputs from date
        self.year_3 = date.year
        self.month_3 = date.month
        self.day_3 = date.day
        self.hour_3 = date.hour
        # retrieve needed inputs
        self.temp_3 = json_data.get('main').get('temp')
        self.min_temp_3 = json_data.get('main').get('temp_min')
        self.max_temp_3 = json_data.get('main').get('temp_max')
        self.pressure_3 = json_data.get('main').get('pressure')
        self.humidity_3 = json_data.get('main').get('humidity')
        self.wind_speed_3 = json_data.get('wind').get('speed')
        self.wind_dir_3 = json_data.get('wind').get('deg')
        print(json_data)
