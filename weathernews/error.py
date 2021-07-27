class WeathernewsError(Exception):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None
    ):

        self._message = message
        self.http_body = http_body
        self.http_status = http_status

    def __str__(self):
        return self._message or "<empty message>"


class APIError(WeathernewsError):
    pass


class ExtractorError(WeathernewsError):
    pass


class ParserError(WeathernewsError):
    pass


class NoResultsError(WeathernewsError):
    pass


class LocationObjNotFoundError(WeathernewsError):
    pass


class UnrecognizedResponse(WeathernewsError):
    pass


class IconNotFoundError(WeathernewsError):
    pass
