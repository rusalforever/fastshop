class BaseRoutesPrefixes:
    """
    Base route prefixes for different application modules.
    """
    swagger: str = '/docs'
    redoc: str = '/redoc'
    openapi: str = '/openapi.json'

    catalogue: str = '/catalogue'
    authentication: str = '/auth'
    account: str = '/account'
