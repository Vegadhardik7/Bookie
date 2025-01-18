from fastapi import Request
from fastapi.security import HTTPBearer
from src.auth.utils import decode_access_token
from fastapi.exceptions import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        
        creds = await super().__call__(request)
        
        # token cannot be none
        if creds is None or creds.credentials is None:
            raise HTTPException(status_code=403, detail="Please provide valid access token")
        
        token = creds.credentials
        token_data = decode_access_token(token)

        # toke is valid or not
        if not self.token_valid(token):
            raise HTTPException(status_code=403, detail="Invalid or expired token")
        
        # if refresh token is provided
        if token_data["refresh"]:
            raise HTTPException(status_code=403, detail="Please provide valid access token")
        
        return creds

    # token validation
    def token_valid(self, token: str):
        
        token_data = decode_access_token(token)

        return True if token_data is not None else False