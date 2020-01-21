import json
from datetime import datetime
from DataAccess import WeatherData



#class for pulling historical data from json file
formatted_data = []
class HistAccess():

    def getData(self):
        count = 1
        city1 = []
        city2 = []
        city3 = []
        city4 = []
        count_city1 = 0
        count_city2 = 0
        count_city3 = 0
        count_city4 = 0
        with open('C:/Users/Rohg/PycharmProjects/AI-Forecast/Data.json') as f:
            # this next line loads the entire file into data as an array of json objects. can access individual things like 2d array
            # and has 666604 json objects
            data = json.load(f)
            length = len(data)
            while(count < length):
                wd = WeatherData.WeatherData()
                wd.temp = data[count]['main']['temp']
                wd.temp_min = data[count]['main']['temp_min']
                wd.temp_max = data[count]['main']['temp_max']
                wd.pressure = data[count]['main']['pressure']
                wd.humidity = data[count]['main']['humidity']
                wd.wind_speed = data[count]['wind']['speed']
                wd.wind_dir = data[count]['wind']['deg']
                temp_date = data[count]['dt']
                temp_date = datetime.fromtimestamp(temp_date)
                wd.year = temp_date.year
                wd.month = temp_date.month
                wd.day = temp_date.day
                wd.hour = temp_date.hour
                if(data[count]['city_name'] == 'Buffalo'):
                    city1.append(wd)
                    count_city1 += 1
                elif(data[count]['city_name'] == 'Cleveland'):
                    city2.append(wd)
                    count_city2 += 1
                elif(data[count]['city_name'] == 'Pittsburgh'):
                    city3.append(wd)
                    count_city3 += 1
                elif (data[count]['city_name'] == 'Erie'):
                    city4.append(wd)
                    count_city4 += 1
                count += 1
            formatted_data.append(city1)
            formatted_data.append(city2)
            formatted_data.append(city3)
            formatted_data.append(city4)


test = HistAccess
test.getData(test)