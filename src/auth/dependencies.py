from fastapi import Request, HTTPException
from src.auth.utils import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        # override the init method
        super().__init__(auto_error = auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        # override the call method
        credentials = await super().__call__(request)
        
        if credentials is None:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        
        token  = credentials.credentials
        
        if token is None:
            raise HTTPException(status_code=403, detail="Please provide an access token")

        if not self.token_valid:
            raise HTTPException(status_code=403, detail="Invalid token or expired token")
        
        token_data = decode_access_token(token)
        self.verify_token_data(token_data)

        return token_data # type: ignore

    # validate the token
    def token_valid(self, token: str) -> bool:
        token_data = decode_access_token(token)
        return True if token_data is not None else False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child class")

# check for access token
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=403, detail="Provide valid access token")
        

# check for refresh token
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=403, detail="Provide valid refresh token")