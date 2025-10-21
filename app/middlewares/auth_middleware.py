from fastapi import Request, HTTPException
from jose import jwt
from urllib.parse import unquote
from app._core.config import settings
from app._core.logger import logger

def get_user_id_from_cookie(request: Request):
    token = request.cookies.get("accessToken")
    logger.info("TOKEN: " + str(token))
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = unquote(token)

    if token.startswith("s:"):
        token = token[2:]

    token = token.split(".")[0] + "." + token.split(".")[1] + "." + token.split(".")[2]

    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return decoded.get("userId")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
