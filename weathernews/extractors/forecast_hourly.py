from typing import List

from weathernews.extractors import Extractor
from weathernews.objects import Hourly, Icon, Precip
from weathernews.util import get_temp, get_datetime


class ForecastHourlyExtractor(Extractor):
    """Extract hourly data from html response."""

    def extract(soup) -> List[Hourly]:
        hourlies = []
        for d in soup.find_all("div", class_="weather-day"):
            date_pretty = d.find(
                "div", class_="weather-day__day"
            ).find("p").text

            for h in d.find_all("div", class_="weather-day__item"):
                hour = h.find("p", class_="weather-day__time").text
                hourly_dt = get_datetime(date=date_pretty, hour=hour)

                hourly_img = h.find("img")
                icon_filename = hourly_img["src"].split("/")[-1]
                if "dummy1.png" == icon_filename:
                    icon_filename = hourly_img["data-original"].split("/")[-1]
                icon_details = Icon(icon_filename)

                precip_text = h.find("p", class_="weather-day__r").text
                # Assumming mm/h units for precip amt
                if "mm/h" in precip_text:
                    precip_amt = float(precip_text.replace("mm/h", ""))

                temp = get_temp(h.find("p", class_="weather-day__t").text)

                # Assumming m/s units for wind speed
                wind_text = h.find(
                    "p", class_="weather-day__w"
                ).text.split("m/s")
                wind_speed = int(wind_text[0])
                wind_dir = wind_text[1]

                hourlies.append(Hourly(
                    datetime=hourly_dt,
                    icon=icon_filename,
                    short=icon_details.short,
                    detail=icon_details.long,
                    precip=Precip(amt=precip_amt),
                    temp=temp,
                    wind_speed=wind_speed,
                    wind_dir=wind_dir
                ))

                if len(hourlies) == 25:
                    break

        return hourlies
