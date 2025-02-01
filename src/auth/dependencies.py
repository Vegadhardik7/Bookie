from src.db.models import User
from typing import List, Any
from .service import UserService
from src.db.main import get_session
from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from src.db.redis import token_in_blocklist
from fastapi.exceptions import HTTPException
from src.auth.utils import decode_access_token
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security.http import HTTPAuthorizationCredentials

user_service = UserService()

# Custom TokenBearer class to validate tokens
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        """
        Initialize the TokenBearer class, inheriting from FastAPI's HTTPBearer.
        :param auto_error: Whether to automatically raise an exception if authentication fails.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        """
        Override the __call__ method to extract and validate the token from the request.
        :param request: The incoming HTTP request.
        :return: Decoded token data if valid.
        :raises HTTPException: If the token is missing, invalid, or expired.
        """
        # Call the parent class's __call__ method to extract credentials
        credentials = await super().__call__(request)
        
        if credentials is None:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        
        token = credentials.credentials  # Extract the token

        if token is None:
            raise HTTPException(status_code=403, detail="Please provide an access token")

        # Check if the token is valid
        if not self.token_valid(token):
            raise HTTPException(status_code=403, detail={
                "error": "Token is invalid or expired", 
                "resolution": "Please get a new token"
            })
        
        # Decode the token to get token data
        token_data = decode_access_token(token)

        # Check if the token is in the blocklist (revoked or blacklisted)
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(status_code=403, detail={
                "error": "Token is invalid or has been revoked", 
                "resolution": "Please get a new token"
            })

        # Verify token-specific data (to be implemented by child classes)
        self.verify_token_data(token_data)

        return token_data  # type: ignore # Return the validated token data

    def token_valid(self, token: str) -> bool:
        """
        Check if the token is valid by decoding it.
        :param token: The token string.
        :return: True if the token is valid, otherwise False.
        """
        token_data = decode_access_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        """
        Verify the token data. Must be implemented in child classes.
        :param token_data: Decoded token data.
        :raises NotImplementedError: If the method is not overridden in child classes.
        """
        raise NotImplementedError("Please override this method in child class")

# Custom class for validating access tokens
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        """
        Verify the token data to ensure it's an access token.
        :param token_data: Decoded token data.
        :raises HTTPException: If the token is not an access token.
        """
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=403, detail="Provide valid access token")
        
# Custom class for validating refresh tokens
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        """
        Verify the token data to ensure it's a refresh token.
        :param token_data: Decoded token data.
        :raises HTTPException: If the token is not a refresh token.
        """
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=403, detail="Provide valid refresh token")

# Dependency to fetch the currently authenticated user
async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), 
                           session: AsyncSession = Depends(get_session)):
    """
    Dependency to fetch the currently authenticated user from the database.
    :param token_details: Decoded token data from the access token.
    :param session: Database session (AsyncSession).
    :return: The user object corresponding to the token's email.
    :raises HTTPException: If the user does not exist in the database.
    """
    # Extract user email from the token details
    user_email = token_details['user']['email']
    
    # Fetch the user object from the database
    user = await user_service.get_user_by_email(user_email, session)
    
    # Return the user object
    return user

# Check the role of the user
class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(status_code=403, detail="Access Denied. You are not permitted to perform this action.")
