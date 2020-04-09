import json
import pickle
from datetime import datetime
from DataAccess import WeatherData



#class for pulling historical data from json file
formatted_data = []
class HistAccess():


    def getData(self, num_cities, city_names, start_year, end_year):
        count = 1

        if(start_year > end_year): #ensures start year is the earliest year
            temp = end_year
            self.end_year = start_year
            self.start_year = temp
        city_array = []
        #creates 2d array with rows equal to number of cities being used
        for x in range(num_cities):
            temp_array = []
            city_array.append(temp_array)
        with open('/Users/tigergoodbread/PycharmProjects/AI-Forecast/Data.json') as f:
            # this next line loads the entire file into data as an array of json objects. can access individual things like 2d array
            # and has 666604 json objects
            data = json.load(f)
            length = len(data)
            while(count < length):
                wd = WeatherData.WeatherData()
                temp_date = data[count]['dt']
                temp_date = datetime.fromtimestamp(temp_date)
                wd.year = temp_date.year
                wd.month = temp_date.month / 12.0
                wd.day = temp_date.day/31.0
                wd.hour = temp_date.hour/24.0
                if wd.year >= start_year and wd.year <= end_year: #if year is within specified range
                    #F: -20 = 244K
                    #F: 120 = 322K
                    wd.temp = (data[count]['main']['temp'] - 244) / (323 - 244)  # divide by 50 Celsius (323K)
                    wd.temp_min = (data[count]['main']['temp_min'] - 244) / (323 - 244)
                    wd.temp_max = (data[count]['main']['temp_max'] - 244) / (323 - 244)
                    wd.pressure = (data[count]['main']['pressure'] - 900) / (1100-900) #avg is about 1013, doesn't seem to vary much
                    wd.humidity = data[count]['main']['humidity'] - 50 / (100 - 50)
                    wd.wind_speed = data[count]['wind']['speed'] / 50 #~50 mph (knots)
                    wd.wind_dir = data[count]['wind']['deg'] / 360
                    for x in range(num_cities):
                        if data[count]['city_name'] == city_names[x]:
                            city_array[x].append(wd)
                count += 1
            print(len(city_array[0]), " ", len(city_array[1]), " ", len(city_array[2]), " ", len(city_array[3]))


            # This block of code wrties all attributes of weather data objects for each surrounding city for each time stamp within the selected range into a text file
            # Each row = 1 city; Every 4 rows = 1 time stamp
            x = 0
            length = (int)(.7 * len(city_array[0]))
            with open("training.pkl", 'wb') as f_train:  # Overwrites any existing file.
                for i in range(length):
                    out_array = []
                    x = x + 1
                    for j in range(4):
                        temp = []

                        #temp.append(city_array[j][i].year)
                        temp.append(city_array[j][i].month)
                        temp.append(city_array[j][i].day)
                        temp.append(city_array[j][i].hour)
                        temp.append(city_array[j][i].temp)
                        temp.append(city_array[j][i].temp_min)
                        temp.append(city_array[j][i].temp_max)
                        temp.append(city_array[j][i].pressure)
                        temp.append(city_array[j][i].humidity)
                        temp.append(city_array[j][i].wind_speed)
                        temp.append(city_array[j][i].wind_dir)
                        out_array.append(temp)
                    pickle.dump(out_array, f_train, pickle.HIGHEST_PROTOCOL)
            f_train.close()
            t = x
            length = int(.85 * len(city_array[0]))
            with open("validation.pkl", 'wb') as f_validate:
                for i in range(x, length):
                    out_array = []
                    t = t + 1
                    for j in range(4):
                        temp = []
                        #temp.append(city_array[j][i].year)
                        temp.append(city_array[j][i].month)
                        temp.append(city_array[j][i].day)
                        temp.append(city_array[j][i].hour)
                        temp.append(city_array[j][i].temp)
                        temp.append(city_array[j][i].temp_min)
                        temp.append(city_array[j][i].temp_max)
                        temp.append(city_array[j][i].pressure)
                        temp.append(city_array[j][i].humidity)
                        temp.append(city_array[j][i].wind_speed)
                        temp.append(city_array[j][i].wind_dir)
                        out_array.append(temp)

                    pickle.dump(out_array, f_validate, pickle.HIGHEST_PROTOCOL)
            f_validate.close()
            with open("testing.pkl", 'wb') as f_test:
                for i in range(t, len(city_array[0])):
                    out_array = []
                    for j in range(4):
                        temp = []
                        #temp.append(city_array[j][i].year)
                        temp.append(city_array[j][i].month)
                        temp.append(city_array[j][i].day)
                        temp.append(city_array[j][i].hour)
                        temp.append(city_array[j][i].temp)
                        temp.append(city_array[j][i].temp_min)
                        temp.append(city_array[j][i].temp_max)
                        temp.append(city_array[j][i].pressure)
                        temp.append(city_array[j][i].humidity)
                        temp.append(city_array[j][i].wind_speed)
                        temp.append(city_array[j][i].wind_dir)
                        out_array.append(temp)

                    pickle.dump(out_array, f_test, pickle.HIGHEST_PROTOCOL)
            f_test.close()

test = HistAccess
test.getData(test, 4, ['Buffalo', 'Cleveland', 'Pittsburgh', 'Erie'], 2010, 2019)