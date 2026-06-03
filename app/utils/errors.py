from typing import Optional


class NotFoundError(Exception):
    message: str = 'Not Found'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.message
        super().__init__(self.message)


class InternalServerError(Exception):
    message: str = 'Internal server error'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.message
        super().__init__(self.message)


class ForbiddenError(Exception):
    message: str = 'Access denied'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    message: str = 'You must be authorized'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.message
        super().__init__(self.message)


class BadRequestError(Exception):
    message: str = 'Wrong request data'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.message
        super().__init__(self.message)


class ConflictError(Exception):
    message: str = 'The request could not be completed because it conflicts with the current state of the resource'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.message
        super().__init__(self.message)


class GoneError(Exception):
    message: str = 'The requested resource is no longer available.'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.message
        super().__init__(self.message)
