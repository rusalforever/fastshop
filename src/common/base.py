import json


class CustomExceptionError(Exception):
    message = None

    def __str__(self) -> str:
        return json.dumps(self.message)


class ObjectDoesNotExistException(CustomExceptionError):
    def __init__(self) -> None:
        self.message = 'Object does not exist.'


class ObjectAlreadyExistException(CustomExceptionError):
    def __init__(self) -> None:
        self.message = 'Object already exist.'
