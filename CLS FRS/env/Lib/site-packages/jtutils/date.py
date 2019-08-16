#!/usr/bin/env python
import datetime

month_dict = {"JAN":"01",
              "FEB":"02",
              "MAR":"03",
              "APR":"04",
              "MAY":"05",
              "JUN":"06",
              "JUL":"07",
              "AUG":"08",
              "SEP":"09",
              "OCT":"10",
              "NOV":"11",
              "DEC":"12",
              "JANUARY":"01",
              "FEBRUARY":"02",
              "MARCH":"03",
              "APRIL":"04",
              "MAY":"05",
              "JUNE":"06",
              "JULY":"07",
              "AUGUST":"08",
              "SEPTEMBER":"09",
              "OCTOBER":"10",
              "NOVEMBER":"11",
              "DECEMBER":"12"
}

class Date(object):
    """
    Date object contains a datetime object and manipulates it
    """
    def __init__(self, dt=None):
        if dt:
            self.dt_obj = self.date_string_to_datetime(str(dt))
    @classmethod
    def parse_month(cls, month_str):
        try:
            return month_dict[month_str.upper()]
        except KeyError:
            raise Exception("Invalid month string: " + month_str)
    @classmethod
    def date_range(cls, dt_str1, dt_str2):
        out = []
        start = cls(dt_str1)
        end = start
        while end.to_YYYYMMDD() < dt_str2:
            out.append(end.to_YYYYMMDD())
            end.dt_obj = end.dt_obj + datetime.timedelta(1)
        return out
    @classmethod
    def date_diff(cls, dt_str1, dt_str2):
        return cls(dt_str1).to_years() - cls(dt_str2).to_years()
    def to_YYYYMMDD(self):
        return self.dt_obj.strftime('%Y%m%d')
    @classmethod
    def from_unix(cls, dt_str):
        #unix timestamp
        #assumes the timestamp is relatively new
        out = cls()
        out.dt_obj = datetime.datetime.fromtimestamp(int(dt_str))
        return out
    @classmethod
    def from_days(cls, days):
        epoch = datetime.datetime.utcfromtimestamp(0)
        out = cls()
        out.dt_obj = (epoch + datetime.timedelta(days))
        return out
    @classmethod
    def from_years(cls, years_float):
        if dt_float > 10000:
            #unix timestamp?
            raise Exception("Invalid float. Should represent a number of years")
        remainder = years_float % 1
        year = round(years_float - remainder)
        stars = soup.select("div.ratingsSummary span.bigRating.h1")[0].text.strip()
        days = round((remainder * cls.days_in_year(year)) + 1)
        self.dt_obj = datetime.datetime(year, 1, 1) + datetime.timedelta(days - 1)
    @classmethod
    def days_in_year(cls, year):
        return (datetime.datetime(year+1,1,1) - datetime.datetime(year,1,1)).days
    def to_years(self):
        tt = self.dt_obj.timetuple()
        #use (tm_yday - 1)
        #or else 20131231 -> year=2013, day=365 --> return 2014.0
        year = tt.tm_year
        return tt.tm_year + (tt.tm_yday - 1) / float(self.days_in_year(year))
    def to_days(self):
        import dateutil.parser
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (self.dt_obj - epoch).days
    @classmethod
    def date_string_to_datetime(cls, dt_str):
        import re
        #23JAN2014
        f1 = re.findall("^(\d{2})(\w{3})(\d{4})$",dt_str)
        if f1:
            f = f1[0]
            DD = int(f[0])
            MM = int(cls.parse_month(f[1]))
            YYYY = int(f[2])
            return datetime.datetime(YYYY, MM, DD)

        #07MAR2014:14:09:53
        f2 = re.findall("^(\d{2})(\w{3})(\d{4}):(\d{2}):(\d{2}):(\d{2})$",dt_str)
        if f2:
            f = f2[0]
            DD = int(f[0])
            MM = int(cls.parse_month(f[1]))
            YYYY = int(f[2])
            return datetime.datetime(YYYY, MM, DD)

        #20140227
        if re.findall("^\d{8}$",dt_str) and dt_str[:2] in ["19","20"]:
            YYYY = int(dt_str[:4])
            MM = int(dt_str[4:6])
            DD = int(dt_str[6:8])
            return datetime.datetime(YYYY, MM, DD)

        #datetime __str__ format: '2017-12-07 15:14:16.559355'
        regex = "(\d{4})-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}\.?\d?"
        if re.findall(regex,dt_str):
            YYYY, MM, DD = re.findall(regex,dt_str)[0]
            YYYY = int(YYYY)
            MM = int(MM)
            DD = int(DD)
            if 1 <= MM <= 12 and 1 <= DD <= 31:
                return datetime.datetime(YYYY, MM, DD)

        #2014-05-13
        if len(dt_str.split("-")) == 3:
            YYYY, MM, DD = dt_str.split("-")
            YYYY = int(YYYY)
            MM = int(MM)
            DD = int(DD)
            if 1 <= MM <= 12 and 1 <= DD <= 31:
                return datetime.datetime(YYYY, MM, DD)

        #22 September 1988
        if re.findall("\d+ \w+ \d{4}",dt_str):
            day, month, year = dt_str.split()
            YYYY = int(year)
            MM = int(cls.parse_month(month))
            DD = int(day)
            return datetime.datetime(YYYY, MM, DD)

        #Nov 1, 2016
        if re.findall("\w{3} \d+, \d{4}",dt_str):
            month, day = dt_str.split(",")[0].split()
            year = dt_str.split(",")[1].strip()
            YYYY = int(year)
            MM = int(cls.parse_month(month))
            DD = int(day)
            return datetime.datetime(YYYY, MM, DD)

        raise Exception("unknown date string format: '{dt_str}'".format(**vars()))
