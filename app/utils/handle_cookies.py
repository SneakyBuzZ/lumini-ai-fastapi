from jose import jwt, JWTError
from fastapi import HTTPException, Request
from app._core.config import settings
from urllib.parse import unquote

def get_user_id_from_cookie(request: Request):
    cookie_value = request.cookies.get("accessToken")
    print("RAW COOKIE VALUE:", cookie_value)

    if not cookie_value:
        raise HTTPException(status_code=401, detail="Missing accessToken cookie")

    decoded_cookie = unquote(cookie_value)

    if decoded_cookie.startswith("s:"):
        token = decoded_cookie[2:]
        parts = token.rsplit('.', 1)
        if len(parts) == 2:
            jwt_token = parts[0]
        else:
            jwt_token = token
    else:
        jwt_token = decoded_cookie

    try:
        decoded = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=["HS256"])
        return decoded.get("userId")
    
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired JWT token")
