from weathernews import api_requestor
from weathernews.api_resources.location import Location
from weathernews.data_extract import DataExtract
from weathernews.error import ExtractorError
from weathernews.objects import Report


class Forecast:
    @classmethod
    def fetch(cls, q, metric=True) -> Report:
        """Fetch forecast from Weathernews."""

        requestor = api_requestor.APIRequestor()

        if isinstance(q, str):
            q = Location.search(q)[0]

        # weathernews doesnt use url parameters correctly, so
        # we hardcode it into the url
        url = f"/onebox/{q.lat}/{q.lon}/q={q.loc}&v={q.v}&lang=ja"

        resp, rcode = requestor.request("get", url, expect_json=False)

        try:
            h, tw, tn = DataExtract.forecast(resp)
        except Exception as e:
            raise ExtractorError(
                "Error extracting data from response\n"
                f"An exception \'{type(e).__name__}\' "
                f"occurred with args *{e.args}*",
                resp,
                rcode
            )

        return Report(
            loc=q.loc,
            lat=q.lat,
            lon=q.lon,
            url=q.url,
            metric=metric,
            hourly=h,
            today=tw.data[0],
            tomorrow=tw.data[1],
            twoday=tw,
            tenday=tn
        )
