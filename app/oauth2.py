from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secret key, algorithm, expiration date
Secret_key = settings.secret_key
Algorithm = settings.algorithm
Expiration = settings.expiration

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=Secret_key, algorithm=Algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, key=Secret_key, algorithms=Algorithm)
        id: int = payload.get('user_id')
        email: str = payload.get('email')
        epoch_time: int = payload.get('exp')
        # print(id, email, t)
        # print(datetime.fromtimestamp(t))
        if not id and not email:
            raise credentials_exception
        # print(datetime.utcnow()+timedelta(hours=8))
        # if t < datetime.timestamp(datetime.utcnow()+timedelta(hours=8)):
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credentials have expired')
        token_data = schemas.TokenData(id=id, email=email, epoch_time=epoch_time)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='could not validate credentials', headers={'WWW-Authenticate': "Bearer"})
    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user