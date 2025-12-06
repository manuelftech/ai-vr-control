from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException
import jwt

async def get_token_user_id(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    if not token:
        raise HTTPException(status_code=400, detail="Authentication 'token' is required.")
    
    user_id = jwt.decode(jwt=token, options={"verify_signature": False}).get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="The token claim 'user_id' is required.")
    return user_id