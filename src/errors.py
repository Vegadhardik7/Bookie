"""
This file defines custom error classes for the application.
These custom exceptions are used to handle specific error cases and provide meaningful error messages.
All custom errors are derived from the base `BookieException` class.
"""

# All the custom error that we are going to defined are going to made from this default exception class
class BookieException(Exception):
    """
        Base class for all the exceptions
    """
    pass


class InvalidToken(BookieException):
    """
        User has provided invalid or expire token
    """
    pass

class RevokedToken(BookieException):
    """
        User has provided a revoked token
    """
    pass

class AccessTokenRequired(BookieException):
    """
        User has provided a refresh token when an access token is required
    """
    pass

class RefreshTokenRequired(BookieException):
    """
        User has provided a access token when a refresh token is required
    """
    pass

class UserAlreadyExists(BookieException):
    """
        User has provided a email which already exists
    """
    pass

class InsufficientPermission(BookieException):
    """
        User does not have the neccessary permissions to perform an action.
    """ 
    pass

class BookNotFound(BookieException) :
    """
        Book Not found
    """
    pass

class UserNotFound(BookieException):
    """
        Tag Not found
    """
    pass    
