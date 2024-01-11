from werkzeug.exceptions import BadRequest


class InvalidParameterException(BadRequest):
    """
    Exception class representing errors related to invalid request parameters.

    This exception is typically raised when there are issues with parsing or validating
    the parameters provided in a request.

    :param message: A custom error message describing the issue. If not provided, a
                    default message is used.
    """

    def __init__(self, message="There were some errors while parsing request params"):
        super().__init__(description=message)


class MissingParameterException(BadRequest):
    """
    Exception class representing errors related to missing request parameters.

    This exception is typically raised when some of the parameters are missing
    from the url query param.

    :param message: A custom error message describing the issue. If not provided, a
                    default message is used.
    """

    def __init__(self, message="Some parameters might be missing from the request"):
        super().__init__(description=message)
