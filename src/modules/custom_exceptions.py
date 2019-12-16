### Module: custom_exceptions ###
### Custom Exceptions ###

class NotConnectedError(Exception):
    pass

class QueryNotFoundError(Exception):
    pass

class NotHandledError(Exception):
    pass

class DBNotSpecifiedError(Exception):
    pass

class NotAuthenticatedError(Exception):
    pass