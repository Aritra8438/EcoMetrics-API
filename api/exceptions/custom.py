from werkzeug.exceptions import BadRequest


class InvalidParameterException(BadRequest):
    def __init__(self, message="There were some errors while parsing request params"):
        super().__init__(description=message)


class MissingParameterException(BadRequest):
    def __init__(self, message="Some parameters might be missing from the request"):
        super().__init__(description=message)
