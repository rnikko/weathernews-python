from typing import List

from weathernews import api_requestor
from weathernews.objects import Location as LocationObj
from weathernews.error import LocationObjNotFoundError, NoResultsError


class Location:
    @classmethod
    def search(cls, q) -> List[LocationObj]:
        """Search location on Weathernews."""

        requestor = api_requestor.APIRequestor()

        url = "/onebox/api_search.cgi"
        params = {"query": q}

        resp, rcode = requestor.request(
            "get",
            url,
            params,
            expect_json=True
        )
        if len(resp) == 0:
            raise NoResultsError(
                f"Found no results for query: \'{q}\'",
                resp,
                rcode
            )

        try:
            return [LocationObj(**loc) for loc in resp]
        except TypeError:
            raise LocationObjNotFoundError(
                f"Location object not found in response\'{q}\'",
                resp,
                rcode
            )
