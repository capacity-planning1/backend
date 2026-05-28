class NotFoundError(Exception):
    def __init__(self, message: str = 'Not Found'):
        self.message = message
        super().__init__(self.message)


class InternalServerError(Exception):
    def __init__(self, message: str = 'Internal server error'):
        self.message = message
        super().__init__(self.message)


class ForbiddenError(Exception):
    def __init__(self, message: str = 'Access denied'):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    def __init__(self, message: str = 'You must be authorized'):
        self.message = message
        super().__init__(self.message)


class BadRequestError(Exception):
    def __init__(self, message: str = 'Wrong request data'):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    def __init__(self, message: str = 'The request could not be completed because it conflicts with the current state of the resource'):
        self.message = message
        super().__init__(self.message)
