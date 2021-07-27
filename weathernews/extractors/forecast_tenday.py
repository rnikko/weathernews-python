from weathernews.extractors import Extractor
from weathernews.objects import Comment, Daily, Dailies, Icon, Precip
from weathernews.util import get_temp, get_datetime, get_number


class ForecastTendayExtractor(Extractor):
    """Extract ten-day data from html response."""

    def extract(soup) -> Dailies:
        ten_day_dailies = []
        ten_day_wrapper = soup.find("div", class_="weather-10day")
        ten_day = ten_day_wrapper.find_all("div", class_="weather-10day__item")
        for offset, d in enumerate(ten_day, 1):
            icon_filename = d.find("img")["src"].split("/")[-1]
            icon_details = Icon(icon_filename)

            date_pretty = d.find("p", class_="weather-10day__day").text
            date_dt = get_datetime(
                date=date_pretty,
                offset=offset
            )

            high = get_temp(d.find("p", class_="txt-h").text)
            low = get_temp(d.find("p", class_="txt-l").text)

            precip_text = d.find("p", class_="weather-10day__r").text
            precip_pt = get_number(precip_text)

            ten_day_dailies.append(Daily(
                datetime=date_dt,
                icon=icon_filename,
                short=icon_details.short,
                detail=icon_details.long,
                high=high,
                low=low,
                precip=[Precip(pt=precip_pt), ]
            ))

        ten_day_comment_p = ten_day_wrapper.find(
            "div", class_="comment no-ja"
        ).find_all("p")

        return Dailies(
            data=ten_day_dailies,
            comment=Comment(
                short=ten_day_comment_p[0].text,
                detail=ten_day_comment_p[1].text
            )
        )
