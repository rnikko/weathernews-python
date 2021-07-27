from bs4 import BeautifulSoup

from weathernews.extractors import (ForecastHourlyExtractor, 
                                    ForecastTwodayExtractor,
                                    ForecastTendayExtractor)


class DataExtract:
    @staticmethod
    def forecast(response):
        """Extract forecast data from response."""

        soup = BeautifulSoup(response, "lxml")
        hourly = ForecastHourlyExtractor.extract(soup)
        twoday = ForecastTwodayExtractor.extract(soup)
        tenday = ForecastTendayExtractor.extract(soup)
        return (hourly, twoday, tenday)
