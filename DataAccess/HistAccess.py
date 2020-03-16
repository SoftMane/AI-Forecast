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
        with open('C:/Users/Rohg/PycharmProjects/AI-Forecast/Data.json') as f:
            # this next line loads the entire file into data as an array of json objects. can access individual things like 2d array
            # and has 666604 json objects
            data = json.load(f)
            length = len(data)
            while(count < length):
                wd = WeatherData.WeatherData()
                temp_date = data[count]['dt']
                temp_date = datetime.fromtimestamp(temp_date)
                wd.year = temp_date.year
                wd.month = temp_date.month
                wd.day = temp_date.day
                wd.hour = temp_date.hour
                if wd.year >= start_year and wd.year <= end_year: #if year is within specified range
                    #F: -20 = 244K
                    #F: 120 = 322K
                    wd.temp = data[count]['main']['temp'] / 323  # divide by 50 Celsius (323K)
                    wd.temp_min = data[count]['main']['temp_min'] / 323
                    wd.temp_max = data[count]['main']['temp_max'] / 323
                    wd.pressure = data[count]['main']['pressure'] / 1100 #avg is about 1013, doesn't seem to vary much
                    wd.humidity = data[count]['main']['humidity'] / 100
                    wd.wind_speed = data[count]['wind']['speed'] / 50 #~50 mph (knots)
                    wd.wind_dir = data[count]['wind']['deg'] / 360
                    for x in range(num_cities):
                        if data[count]['city_name'] == city_names[x]:
                            city_array[x].append(wd)
                            # count_city1 += 1
                    # elif(data[count]['city_name'] == 'Cleveland'):
                    #     city2.append(wd)
                    #     count_city2 += 1
                    # elif(data[count]['city_name'] == 'Pittsburgh'):
                    #     city3.append(wd)
                    #     count_city3 += 1
                    # elif (data[count]['city_name'] == 'Erie'):
                    #     city4.append(wd)
                    #     count_city4 += 1
                count += 1
            # formatted_data.append(city1)
            # formatted_data.append(city2)
            # formatted_data.append(city3)
            # formatted_data.append(city4)
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
                        # f.write(str(city_array[j][i].year) + " ")
                        # f.write(str(city_array[j][i].month) + " ")
                        # f.write(str(city_array[j][i].day) + " ")
                        # f.write(str(city_array[j][i].hour) + " ")
                        # f.write(str(city_array[j][i].temp) + " ")
                        # f.write(str(city_array[j][i].temp_min) + " ")
                        # f.write(str(city_array[j][i].temp_max) + " ")
                        # f.write(str(city_array[j][i].pressure) + " ")
                        # f.write(str(city_array[j][i].humidity) + " ")
                        # f.write(str(city_array[j][i].wind_speed) + " ")
                        # f.write(str(city_array[j][i].wind_dir) + '\n')

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
test.getData(test, 4, ['Buffalo', 'Cleveland', 'Pittsburgh', 'Erie'], 2017, 2019)