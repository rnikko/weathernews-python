from weathernews.extractors import Extractor
from weathernews.objects import Comment, Daily, Dailies, Icon, Precip
from weathernews.util import get_temp, get_datetime, get_number


class ForecastTwodayExtractor(Extractor):
    """Extract two-day data from html response."""
    
    def extract(soup) -> Dailies:
        two_day_dailies = []
        two_day_wrapper = soup.find(
            "div",
            attrs={"class": "switchContent__item", "data-num": 2}
        )
        two_day = two_day_wrapper.find_all("div", class_="weather-2day__item")
        for d in two_day:
            date_pretty = d.find("p", class_="weather-2day__day").text
            date_dt = get_datetime(date=date_pretty)

            icon_filename = d.find("img")["src"].split("/")[-1]
            icon_details = Icon(icon_filename)

            temp_high = get_temp(d.find("p", class_="temp__h").contents[1])
            temp_low = get_temp(d.find("p", class_="temp__l").contents[1])

            rain_data = d.find("div", class_="weather-2day__rainy")
            rain_title = rain_data.find("div", class_="tit").find("p").text
            if rain_title != "降水確率":
                continue
            rain = rain_data.find("div", class_="cont").find_all("table")
            precip = []
            for r in rain:
                rain_zipped = list(zip(r.find_all("th"), r.find_all("td")))
                for rz in rain_zipped:
                    r_hr = get_number(rz[0].text)
                    r_pt = get_number(rz[1].text)

                    hr = int(r_hr.group())
                    pt = int(r_pt.group()) if r_pt else 0

                    precip.append(Precip(hour=hr, pt=pt))

            two_day_dailies.append(Daily(
                datetime=date_dt,
                icon=icon_filename,
                short=icon_details.short,
                detail=icon_details.long,
                high=temp_high,
                low=temp_low,
                precip=precip
            ))

        two_day_comment_p = two_day_wrapper.find(
            "div", class_="comment no-ja"
        ).find_all("p")

        return Dailies(
            data=two_day_dailies,
            comment=Comment(
                short=two_day_comment_p[0].text,
                detail=two_day_comment_p[1].text
            )
        )
