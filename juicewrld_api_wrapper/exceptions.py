class JuiceWRLDAPIError(Exception):
    pass

class RateLimitError(JuiceWRLDAPIError):
    pass

class NotFoundError(JuiceWRLDAPIError):
    pass

class AuthenticationError(JuiceWRLDAPIError):
    pass

class ValidationError(JuiceWRLDAPIError):
    pass
