import json

import weathernews
from weathernews import error, util


class APIRequestor:
    def __init__(self):
        self.session = weathernews.session
        self.api_base = weathernews.api_base

    def interpret_response(self, rbody, rcode, expect_json=False):
        if rcode != 200:
            raise error.APIError(
                "Invalid response from API",
                rbody,
                rcode
            )

        if expect_json:
            try:
                resp = util.json_or_jquery(rbody)
            except (IndexError, json.decoder.JSONDecodeError):
                raise error.UnrecognizedResponse(
                    "Unable to extract JSON from response body",
                    rbody,
                    rcode
                )
        else:
            resp = rbody

        return resp, rcode

    def request(
        self,
        method,
        url,
        params=None,
        headers=None,
        payload=None,
        expect_json=False
    ):
        _headers = {
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90",'
            '"Google Chrome";v="90"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36",
        }
        
        if headers:
            _headers.update(headers)

        abs_url = self.api_base + url

        r = self.session.request(
            method,
            abs_url,
            headers=_headers,
            params=params,
            data=payload
        )

        rbody = r.text
        rcode = r.status_code

        return self.interpret_response(rbody, rcode, expect_json)
