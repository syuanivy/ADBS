from flask import jsonify


class Error:
    """
    Representation of error response from server.
    """
    ERR_OTHER = "ERR_OTHER"
    ERR_SHIP_COLLIDE = "ERR_SHIP_COLLIDE"
    ERR_INVALID_LOC = "ERR_INVALID_LOC"
    ERRS = {
        ERR_OTHER: "An unhandled error occurred",
        ERR_SHIP_COLLIDE: "A ship already exists on the map at this location",
        ERR_INVALID_LOC: "Invalid position on the map"
    }

    def __init__(self, code, message=None):
        """
        Create an error code with an optional message. If no message is provided
        the default value for that code is used instead. A ValueError is raised
        if the code is invalid.
        """
        if code not in Error.ERRS:
            raise ValueError("Invalid error code: %s" % code)
        self.code = code
        self.message = message

    def create_response(self):
        """
        Return a server response containing a JSON representation of the error.
        """
        if not self.message:
            message = Error.ERRS[self.code]
        else:
            message = self.message
        response = jsonify({'code': self.code, 'message': message})
        response.status_code = 400
        return response
