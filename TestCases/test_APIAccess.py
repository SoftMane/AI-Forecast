from unittest import TestCase
from DataAccess import APIAccess

class TestAPIAccess(TestCase):
    def setUp(self):
        self.api_access = APIAccess.APIAccess

    def test_getCurrent(self):
        self.api_access.getCurrent(self.api_access)

        self.assertNotEqual(self.api_access.year, None)
        self.assertNotEqual(self.api_access.hour, None)
        self.assertNotEqual(self.api_access.day, None)
        self.assertNotEqual(self.api_access.month, None)
        self.assertNotEqual(self.api_access.temp, None)
        self.assertNotEqual(self.api_access.min_temp, None)
        self.assertNotEqual(self.api_access.max_temp, None)
        self.assertNotEqual(self.api_access.pressure, None)
        self.assertNotEqual(self.api_access.humidity, None)
        self.assertNotEqual(self.api_access.wind_speed, None)
        self.assertNotEqual(self.api_access.wind_dir, None)

        self.assertNotEqual(self.api_access.year_1, None)
        self.assertNotEqual(self.api_access.hour_1, None)
        self.assertNotEqual(self.api_access.day_1, None)
        self.assertNotEqual(self.api_access.month_1, None)
        self.assertNotEqual(self.api_access.temp_1, None)
        self.assertNotEqual(self.api_access.min_temp_1, None)
        self.assertNotEqual(self.api_access.max_temp_1, None)
        self.assertNotEqual(self.api_access.pressure_1, None)
        self.assertNotEqual(self.api_access.humidity_1, None)
        self.assertNotEqual(self.api_access.wind_speed_1, None)
        self.assertNotEqual(self.api_access.wind_dir_1, None)

        self.assertNotEqual(self.api_access.year_2, None)
        self.assertNotEqual(self.api_access.hour_2, None)
        self.assertNotEqual(self.api_access.day_2, None)
        self.assertNotEqual(self.api_access.month_2, None)
        self.assertNotEqual(self.api_access.temp_2, None)
        self.assertNotEqual(self.api_access.min_temp_2, None)
        self.assertNotEqual(self.api_access.max_temp_2, None)
        self.assertNotEqual(self.api_access.pressure_2, None)
        self.assertNotEqual(self.api_access.humidity_2, None)
        self.assertNotEqual(self.api_access.wind_speed_2, None)
        self.assertNotEqual(self.api_access.wind_dir_2, None)

        self.assertNotEqual(self.api_access.year_3, None)
        self.assertNotEqual(self.api_access.hour_3, None)
        self.assertNotEqual(self.api_access.day_3, None)
        self.assertNotEqual(self.api_access.month_3, None)
        self.assertNotEqual(self.api_access.temp_3, None)
        self.assertNotEqual(self.api_access.min_temp_3, None)
        self.assertNotEqual(self.api_access.max_temp_3, None)
        self.assertNotEqual(self.api_access.pressure_3, None)
        self.assertNotEqual(self.api_access.humidity_3, None)
        self.assertNotEqual(self.api_access.wind_speed_3, None)
        self.assertNotEqual(self.api_access.wind_dir_3, None)
