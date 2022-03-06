"""
Assignment 0
CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.
"""

from datetime import date, timedelta
from typing import Tuple, Dict, Optional, TextIO, Union
import os

# The column numbers where each kind of information appears.  For example,
# column 9 contains maximum temperature.
LONG, LAT = 0, 1
STN_NAME, CL_ID = 2, 3
DATE, YEAR, MONTH, DAY = 4, 5, 6, 7
DATA_QUALITY = 8
MAX_TEMP, MAX_TEMP_FLAG = 9, 10
MIN_TEMP, MIN_TEMP_FLAG = 11, 12
MEAN_TEMP, MEAN_TEMP_FLAG = 13, 14
HEAT_DEG_DAYS, HEAT_DEG_DAYS_FLAG = 15, 16
COOL_DEG_DAYS, COOL_DEG_DAYS_FLAG = 17, 18
TOTAL_RAIN, TOTAL_RAIN_FLAG = 19, 20
TOTAL_SNOW, TOTAL_SNOW_FLAG = 21, 22
TOTAL_PRECIP, TOTAL_PRECIP_FLAG = 23, 24
SNOW_ON_GRND, SNOW_ON_GRND_FLAG = 25, 26
DIR_MAX_GUST, DIR_MAX_GUST_FLAG = 27, 28
SPD_MAX_GUST, SPD_MAX_GUST_FLAG = 29, 30


class DailyWeather:
    """Weather facts for a single day.

    === Instance Attributes ===
    avg_temp: Average temperature on this day, in degrees Celsius
    low_temp: Minimum temperature on this day, in Celsius
    high_temp: Maximum temperature on this day, in Celsius
    precipitation: Total precipitation on this day in mm,
        or -1 if there were only "trace amounts" of precipitation
    rainfall: Total rainfall on this day in mm,
        or -1 for trace amounts
    snowfall: Total snowfall on this day in cm,
        or -1 for trace amounts

    === Representation Invariants ===
    - precipitation >= -1
    - rainfall >= -1
    - snowfall >= -1
    - low_temp <= avg_temp <= high_temp

    === Sample Usage ===
    >>> weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
    >>> print(weather.avg_temp)
    13.1
    >>> print(weather.low_temp)
    9.2
    >>> print(weather.high_temp)
    20.3
    >>> print(weather.precipitation)
    5
    """
    avg_temp: float
    low_temp: float
    high_temp: float
    precipitation: float
    snowfall: float
    rainfall: float

    def __init__(self, temperature_statistics: Tuple[float, float, float],
                 precipitation_statistics: Tuple[float, float, float]) -> None:
        """Initialize this day's weather.

        temperature_statistics[0] is the average temperature in Celsius
        temperature_statistics[1] is the minimum temperature in Celsius
        temperature_statistics[2] is the maximum temperature in Celsius

        precipitation_statistics[0] is the total precipitation in mm
        precipitation_statistics[1] is the total rainfall in mm
        precipitation_statistics[2] is the total snowfall in cm

        For all values, -1 indicates trace amounts.

        Preconditions:
            - all float values in the tuples are >= -1
            - minimum temperature <= average temperature <= high temperature

        >>> weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
        >>> print(weather.avg_temp)
        13.1
        """
        self.avg_temp = temperature_statistics[0]
        self.low_temp = temperature_statistics[1]
        self.high_temp = temperature_statistics[2]
        self.precipitation = precipitation_statistics[0]
        self.snowfall = precipitation_statistics[2]
        self.rainfall = precipitation_statistics[1]

    # Note: We will just test that the string returned includes the 6 values,
    # We will not test the full content or format of the string.
    def __str__(self) -> str:
        """Return a str representing this DailyWeather.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> print(weather)
        Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 Rain: 0
        """
        return f'Average: {self.avg_temp} Low: {self.low_temp} ' \
               f'High: {self.high_temp} Precipitation: {self.precipitation} ' \
               f'Snow: {self.snowfall} Rain: {self.rainfall}'


class HistoricalWeather:
    """A record of historical weather information for a fixed place on Earth.

    === Instance Attributes ===
    name: The name of the place for which the weather is being recorded.
    coordinates: The latitude and longitude of this place.

    === Private Attributes ===
    _records: The daily weather records for this place. Each key is a
        date and its value is the location's weather on that day. There may
        be gaps in the data. For example, there could be data for Jan 1, 2020
        and Jan 5, 2020, but not for the days in between.

    === Representation Invariants ===
    - coordinates[0] is a valid latitude (between -90 and 90)
    - coordinates[1] is a valid longitude (between -180 and 180)

    === Sample Usage ===
    >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
    >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    >>> toronto_weather.add_weather(date.today(), weather)
    >>> print(toronto_weather.name)
    Toronto
    >>> print(toronto_weather.coordinates)
    (43.6529, -79.3849)
    >>> print(toronto_weather.retrieve_weather(date.today()).avg_temp)
    13
    """
    name: str
    coordinates: Tuple[float, float]
    _records: Dict[date, DailyWeather]

    def __init__(self, name: str, coordinates: Tuple[float, float]) -> None:
        """Initialize this historical weather record with these coordinates,
        place name, and no recorded weather so far.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> print(toronto_weather.name)
        Toronto
        """
        self.name = name
        self.coordinates = coordinates
        self._records = {}

    # We will not test this method, but we recommend that you write and use it.
    def __str__(self) -> str:
        """Return a str representing this HistoricalWeather.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> loc = HistoricalWeather('Toronto', (43.6, -79.63))
        >>> loc.add_weather(date(2020,7,13), weather)
        >>> print(loc)
        Toronto (43.6, -79.63):
        2020-07-13: Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 \
    Rain: 0
        """
        list_of_keys = list(self._records.keys())
        s = ''
        for item in list_of_keys:
            key = item
            w = self._records[item]
            s = s + f'{key}: Average: {w.avg_temp} Low: {w.low_temp} High: ' \
                    f'{w.high_temp} Precipitation: {w.precipitation} Snow: ' \
                    f'{w.snowfall} Rain: {w.rainfall}\n'

        return f'{self.name} {self.coordinates}: \n' \
               f'{s}'

    def add_weather(self, d: date, w: DailyWeather) -> None:
        """Record that w was the weather on the date d.

        If a record for date d already exists, then do nothing (i.e. do not
        change the information that is already recorded).

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> print(toronto_weather.retrieve_weather(date.today()).avg_temp)
        13
        """
        if d not in self._records:
            self._records[d] = w

    def retrieve_weather(self, d: date) -> Optional[DailyWeather]:
        """Return the weather on day d if available, otherwise return None.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> toronto_weather.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if d in self._records:
            return self._records[d]
        else:
            return None

    def record_high(self, m: int, d: int) -> int:
        """Return the highest temperature recorded at this location on month m
        and day d in any year. Note that months are represented by numbers 1-12.

        Preconditions:
            - 1 <= m <= 12
            - 1 <= d <= 31 and d is possible day for the month m. For example,
              if m is 9 (for September), m will not be 31, since September has
              30 days.
            - The weather on month m and day d has been recorded for this
              location in at least one year.

        >>> weather1 = DailyWeather((13, 10, 40), (0, 0, 0))
        >>> weather2 = DailyWeather((13, 10, 30), (0, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> day1 = date(2020, 6, 8)
        >>> day2 = date(2019, 6, 8)
        >>> toronto_weather.add_weather(day1, weather1)
        >>> toronto_weather.add_weather(day2, weather2)
        >>> toronto_weather.record_high(6, 8)
        40
        """
        temps = []
        for item in self._records:
            if item.month == m and item.day == d:
                temps.append(self._records[item].high_temp)
        return int(max(temps))

    def monthly_average(self) -> Dict[str, float]:
        """For each of the 12 months, return the average of the minimum
        temperatures for all dates in that month (in any year) that have
        weather recorded.

        Return the result in a dictionary mapping month name to average,
        and using these three-character names for the months:
            Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec.
        If a month has no weather recorded in any year, map that month name
        to the value None.

        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> jan1_weather = DailyWeather((13, 11, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2019, 1, 1), jan1_weather)
        >>> jan2_weather = DailyWeather((13, 10, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2019, 1, 2), jan2_weather)
        >>> jan2020_weather = DailyWeather((13, 0, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2020, 1, 18), jan2020_weather)
        >>> feb_weather = DailyWeather((13, 11, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2019, 2, 1), feb_weather)
        >>> d = toronto_weather.monthly_average()
        >>> d['Jan'] == 7.0
        True
        >>> d['Feb'] == 11.0
        True
        >>> d['Mar'] is None
        True
        """
        months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                  'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        result = {}
        dates = list(self._records.keys())

        for m in months:
            temps = []
            for d in dates:
                if months[m] == d.month:
                    minimum = self._records[d].low_temp
                    temps.append(minimum)
            if len(temps) != 0:
                ave = sum(temps) / len(temps)
                result[m] = ave
            else:
                result[m] = None

        return result

    def contiguous_precipitation(self) -> Tuple[date, int]:
        """Return the start date and length of the longest sequence of
        consecutive days that had precipitation.

        A day is considered to have had precipitation if its precipitation
        value is either above 0 or is -1 (indicating that there were trace
        amounts of precipitation). The days in a sequence must have been
        consecutive, that is, there can be no day between them. For example.
        if we have recorded weather for July 3rd, 5th, and 6th, that is not
        a sequence of consecutive days.

        In the case of a tie for the longest sequence, any one of the tied
        start dates can be returned.

        Precondition: At least one day's weather has been recorded.

        >>> weather1 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> weather2 = DailyWeather((0, 0, 0), (2, 0, 0))
        >>> weather3 = DailyWeather((0, 0, 0), (0, 0, 0))
        >>> weather4 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> day = timedelta(days=1)
        >>> toronto_weather.add_weather(date.today(), weather1)
        >>> toronto_weather.add_weather(date.today() + day, weather2)
        >>> toronto_weather.add_weather(date.today() + 2 * day, weather3)
        >>> toronto_weather.add_weather(date.today() + 3 * day, weather4)
        >>> result = toronto_weather.contiguous_precipitation()
        >>> result[0] == date.today()
        True
        >>> result[1]
        2
        """
        dates = list(self._records.keys())
        mydict = {}

        i = 0
        days = 0
        while i < len(dates):
            d = dates[i]
            if self._records[d].precipitation != 0:
                days += 1
                i += 1
                if i == len(dates):
                    mydict[d] = days
            else:
                mydict[d - timedelta(1)] = days
                i += 1
                days = 0
                continue

        dts = list(mydict.keys())
        preps = list(mydict.values())
        max_days = max(preps)
        ind = preps.index(max_days)
        k = dts[ind]  # gives date
        if mydict[k] > 1:
            k_actual = k - timedelta(mydict[k] - 1)
        else:
            k_actual = k
        tup = (k_actual, mydict[k])

        return tup

    def percentage_snowfall(self) -> float:
        """Return the fraction of the snowfall and rainfall at this location
        that was snowfall, across all dates when weather was recorded there.

        The answer returned should be calculated as:
            total snowfall / (total snowfall + total rainfall)

        Do not count trace amounts in this calculation. Ignore the units in
        the calculation.  (This is equivalent to assuming that 1 mm of
        rain is equivalent to 1 cm of snow.)

        Precondition: At least one day's weather has been recorded where
            snowfall > 0 or rainfall > 0 or both.

        >>> weather1 = DailyWeather((0, 0, 0), (1, 0, 1))
        >>> weather2 = DailyWeather((0, 0, 0), (3, 3, 0))
        >>> today = date(2020, 5, 1)
        >>> day = timedelta(days=1)
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(today, weather1)
        >>> toronto_weather.add_weather(today + day, weather2)
        >>> toronto_weather.percentage_snowfall()
        0.25
        """
        vals = list(self._records.values())
        snow = 0
        rain = 0
        for v in vals:
            if v.snowfall != -1:
                snow += v.snowfall
            if v.rainfall != -1:
                rain += v.rainfall
        perc = snow / (snow + rain)
        return perc


class Country:
    """ The weather records for various locations in a country.

    === Instance Attributes ===
    name: Name of the country.

    === Private Attributes ===
    _histories:
        The weather records for this country. Each key is a locations's name
        and it's value is that locations's weather history

    === Sample Usage ===
    >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
    >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
    >>> toronto_weather.add_weather(date.today(), weather)
    >>> canada = Country('Canada')
    >>> canada.add_history(toronto_weather)
    >>> yyz = canada.retrieve_history('YYZ')
    >>> yyz.retrieve_weather(date.today()).avg_temp == 13
    True

    === Representation Invariants ===
    - For each key, k, of _histories, k == _histories[k].name
    """

    name: str
    _histories: Dict[str, HistoricalWeather]

    def __init__(self, n: str) -> None:
        """ Initialize this Country with name n and no weather history so far.

        >>> canada = Country('Canada')
        >>> print(canada.name)
        Canada
        """
        self.name = n
        self._histories = {}

    # We will not test this method, but recommend that you write and use it.
    def __str__(self) -> str:
        """Return a str representing this Country.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> weather_2 = DailyWeather((14, 10, 21), (5, 0, 2.0))
        >>> canada = Country('Canada')
        >>> the_date = date(2020,7,13)
        >>> loc1_data = HistoricalWeather('Toronto', (43.6, -79.63))
        >>> loc1_data.add_weather(the_date, weather)
        >>> loc2_data = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> loc2_data.add_weather(the_date - timedelta(1), weather)
        >>> loc2_data.add_weather(the_date + timedelta(1), weather_2)
        >>> canada.add_history(loc1_data)
        >>> canada.add_history(loc2_data)
        >>> print(canada)
        Canada:
        Toronto (43.6, -79.63):
        2020-07-13: Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 \
Rain: 0
        YYZ (43.6529, -79.3849):
        2020-07-12: Average: 13 Low: 9 High: 20 Precipitation: 5 Snow: 0 \
Rain: 0
        2020-07-14: Average: 14 Low: 10 High: 21 Precipitation: 5 Snow: 2.0 \
Rain: 0
        """

    def add_history(self, hw: HistoricalWeather) -> None:
        """ Add a location to this Country. hw is the location's weather
        history, and hw.name is the location's name.

        If a location with the name hw.name is already recorded in this Country,
        then do nothing (i.e. do not change the data that is already present
        for that location).

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> yyz = canada.retrieve_history('YYZ')
        >>> yyz.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if hw.name not in self._histories:
            self._histories[hw.name] = hw

    def retrieve_history(self, name: str) -> Optional[HistoricalWeather]:
        """Return the weather history for the location called name, or
        None if no such location has been recorded in this Country.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> yyz = canada.retrieve_history('YYZ')
        >>> yyz.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if name in self._histories:
            return self._histories[name]
        else:
            return None

    def snowiest_location(self) -> Union[Tuple[str, float], Tuple[None, None]]:
        """Return the name of location with the highest percentage snowfall in
        this Country, and its percentage snowfall.

        In the case of a tie, any one of the tied locations can be returned.

        If there are no locations in this Country, return (None, None).

        Precondition: For all locations in this Country, at least one day's
            weather has been recorded where snowfall > 0 or rainfall > 0
            or both.

        >>> weather = DailyWeather((13, 9, 20), (5, 2, 3))
        >>> other_weather = DailyWeather((13, 4, 20), (5, 2, 2))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> mtl_weather = HistoricalWeather('Montreal', (45.47, -73.74))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> mtl_weather.add_weather(date.today(), other_weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> canada.add_history(mtl_weather)
        >>> result = canada.snowiest_location()
        >>> result[0]
        'YYZ'
        >>> result[1]
        0.6
        """
        if self._histories != {}:
            percs = {}
            for loc in self._histories:
                percs[loc] = self._histories[loc].percentage_snowfall()
            locs = list(percs.keys())
            percentages = list(percs.values())

            max_snow = max(percentages)
            ind = percentages.index(max_snow)
            k = locs[ind]
            tup = (k, percs[k])
            return tup
        else:
            return (None, None)

    def generate_summary(self) -> None:
        """
        Write a summary of interesting statistics for the locations
        in this Country to a markdown file called report.md

        Precondition:
        - All locations in this Country have at least one row of data
          recorded in December of any year
        - Data has been recorded for Dec 25 in at least one year
        """

        headers = ["Location", "record high <br/> for Dec 25",
                   "december <br/> average",
                   "contiguous <br/> precipitation",
                   "percentage <br/> snowfall"]

        with open("report.md", 'w') as f:
            f.write(" | ".join(headers) + "\n")
            f.write(":|-".join(["-" * len(col) for col in headers]) + ":\n")
            for key in self._histories:
                loc = self._histories[key]
                (rec_high, mon_avg,
                 ctgs_prec, perc_snow) = (loc.record_high(12, 25),
                                          loc.monthly_average(),
                                          loc.contiguous_precipitation(),
                                          loc.percentage_snowfall())
                f.write(f"{key : <20} | {rec_high : <10.4} | "
                        f"{mon_avg['Dec']} | "
                        f"{ctgs_prec[1] : <24} | {perc_snow : <18.2}\n")


def load_data(f: TextIO) -> Optional[HistoricalWeather]:
    """Return a HistoricalWeather record representing the weather data in the
    already open csv file f.

    If f contains no lines of data aside from its header, return None.

    The data might not consistently cover consecutive days, but will be
    in order from oldest dates to most recent dates. Do not add daily weather
    for days where there is missing data (as defined in the handout). A "T"
    in the file indicates that there were trace values. Record trace values
    as -1 in the corresponding attribute.

    Preconditions:
        - f is open and is set to the beginning of the file.
        - The first line of f is a header, and the remaining lines
          follow the format specified in the handout.
        - There may be no lines of data, but there is at least a header.
    """

    lines = f.readlines()
    master = []  # a nested list, each list contains column values of a row

    if len(lines) < 2:
        return None

    for line in lines:
        vals = line.split(",")
        master.append(vals)

    name = master[1][STN_NAME]
    coordinates = (float(master[1][LAT]), float(master[1][LONG]))
    hw = HistoricalWeather(name, coordinates)

    for row in master[1:]:
        if (row[TOTAL_SNOW_FLAG] != '') and (row[TOTAL_SNOW_FLAG] != 'T'):
            continue
        elif (row[TOTAL_RAIN_FLAG] != '') and (row[TOTAL_RAIN_FLAG] != 'T'):
            continue
        elif (row[TOTAL_PRECIP_FLAG] != '') and (row[TOTAL_PRECIP_FLAG] != 'T'):
            continue
        precip = row[TOTAL_PRECIP]
        rain = row[TOTAL_RAIN]
        snow = row[TOTAL_SNOW]
        if row[TOTAL_SNOW_FLAG] == 'T':
            snow = -1
        if row[TOTAL_RAIN_FLAG] == 'T':
            rain = -1
        if row[TOTAL_PRECIP_FLAG] == 'T':
            precip = -1
        try:
            dt = date(int(row[YEAR]), int(row[MONTH]), int(row[DAY]))
            dw = DailyWeather((float(row[MEAN_TEMP]), float(row[MIN_TEMP]),
                               float(row[MAX_TEMP])), (float(precip),
                                                       float(rain),
                                                       float(snow)))
            hw.add_weather(dt, dw)
        except ValueError:
            continue

    return hw


def load_country(folder_name: str, name: str) -> Country:
    """ Return a Country called name that contains all the historical weather
     data stored in the files that are in the folder called folder_name.

    Precondition:
    - Each file in the folder called folder_name:
        - is a .csv files that obeys the format specified in the handout
        - contains data for one location within this Country
    """
    country = Country(name)
    for filename in os.listdir(folder_name):
        # If there are any "dot files", ignore them.
        if not filename.startswith('.'):
            location_file = open(os.path.join(folder_name, filename), 'r')
            history = load_data(location_file)
            if history is not None:
                country.add_history(history)

    return country


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['load_country', 'generate_summary'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'datetime', 'os'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })

    import doctest
    doctest.testmod()

    # # Example use (1):
    # # Create weather day "by hand" and examine it using __str__ methods
    # # defined in the various classes.
    # weather_1 = DailyWeather((13, 9, 20), (5, 0, 0))
    # weather_2 = DailyWeather((14, 10, 21), (5, 0, 2.0))
    # canada = Country('Canada')
    # the_date = date(2020, 7, 13)
    # loc1_data = HistoricalWeather('Toronto', (43.6, -79.63))
    # loc1_data.add_weather(the_date, weather_1)
    # loc2_data = HistoricalWeather('YYZ', (43.6529, -79.3849))
    # loc2_data.add_weather(the_date - timedelta(1), weather_1)
    # loc2_data.add_weather(the_date + timedelta(1), weather_2)
    # canada.add_history(loc1_data)
    # canada.add_history(loc2_data)
    # # Try printing instances of each of the 3 classes.
    # print(f'----- a DailyWeather object:\n{weather_1}')
    # print(f'----- a HistoricalWeather object:\n{loc1_data}')
    # print(f'----- a Country object:\n{canada}')

    # # Example use (2):
    # # Load all the data in a folder, and generate a file "report.md"
    # # containing a simple summary of that data.
    # # Note: The file uses a format called "markdown", which includes
    # # special symbols describing desired formatting.  Open report.md in
    # # Pycharm, and it will show you a formatted version.
    # canada = load_country('./student_data/', 'Canada')
    # canada.generate_summary()
    # print('bye')
