from datetime import datetime, timedelta
from schemas import TokenData
from jose import JWTError, jwt
# from main import TokenData

# import SECRET_KEY from .env
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("username")
		email: str = payload.get("email")
		is_superuser: bool = payload.get("is_superuser")
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username, email=email, is_superuser=is_superuser)
		return token_data
	except JWTError:
	    raise credentials_exception