class JuiceWRLDAPIError(Exception):
    """Base exception for Juice WRLD API wrapper errors"""
    pass

class RateLimitError(JuiceWRLDAPIError):
    """Raised when API rate limit is exceeded"""
    pass

class NotFoundError(JuiceWRLDAPIError):
    """Raised when a requested resource is not found"""
    pass

class AuthenticationError(JuiceWRLDAPIError):
    """Raised when authentication fails"""
    pass

class ValidationError(JuiceWRLDAPIError):
    """Raised when input validation fails"""
    pass
