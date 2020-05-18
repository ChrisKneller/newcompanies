import json
import datetime
import os

import jwt
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
import datagather as dg
import users as u
from database import SessionLocal, engine
from functions import alchemyencoder, to_json
from responses import PrettyJSONResponse
from models import Company, Address
from schemas import Token

# uvicorn main:app --reload
# env\Scripts\activate.bat
# 12592621

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


### USER / LOGIN SECTION ###


@app.post("/signup", response_model=schemas.User2)
async def signup(db: Session = Depends(get_db),
                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.create_user(db, form_data.username, form_data.password)
    if not user[0]:
        if user[1] == "User already exists":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=user[1]
            )
        elif user[1] == "Email address not valid":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=user[1]
            )
    return user[0]


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = u.authenticate_user(u.fake_users_db, 
                               form_data.username, 
                               form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=u.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = u.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(u.get_current_active_user)):
    return current_user


### COMPANY SECTION ###


@app.get("/api/company/{company_id}", 
         response_model=schemas.Company,
         response_model_exclude_defaults=True,
         response_class=PrettyJSONResponse)
def read_company(company_id: int, 
                 db: Session = Depends(get_db),
                 token: str = Depends(u.oauth2_scheme),
                 current_user: schemas.User = Depends(u.get_current_active_user)):
    co = db.query(models.Company).filter_by(number=company_id).one_or_none()

    if not co:
        data = dg.get_company_data(company_id)
        if not data:
            raise HTTPException(status_code=404,
                                detail="Invalid company number")
        co = dg.data_to_company(data)
        co = crud.get_or_create(db, Company, number=co.number, 
                                 name=co.name, 
                                 incorporated=co.incorporated)
    elif not all([co.address, co.sic_codes]):
        data = dg.get_company_data(company_id)

    if not co.address:
        address = dg.data_to_address(data)[1]
        co.address = address

    if not co.sic_codes:
        sic_codes = dg.data_to_sic(data, db)
        co.sic_codes = sic_codes

    db.add(co)
    db.commit()

    co = db.query(models.Company).filter_by(number=company_id).one_or_none()

    return co if co else None


@app.get("/api/search", 
         response_model=List[schemas.CompanyIncorporated],
         response_model_exclude_defaults=True,
         response_class=PrettyJSONResponse)
def search_companies(
    year: int = None, month: int = None, day: int = None, number: int = None, 
    name: str = None, db: Session = Depends(get_db)):
    
    name = name.upper() if name else None

    arguments = locals()
    arguments.pop("db")
    
    if not any(arguments.values()):
        return None
    
    myquery = db.query(models.Company)
    datedict = {}

    for key, value in arguments.items():
        if key == "number" and datedict:
            myquery = crud.get_company_by_date(db, **datedict)
        
        if not value:
            continue
        
        if key == 'year' or key == 'month' or key == 'day':
            datedict[key] = value
        else:
            myquery = crud.filter_query(myquery, **{key:value})
    
    return myquery.all()


@app.get("/api/incorporated/today",
         response_model=List[schemas.CompanyIncorporated],
         response_model_exclude_defaults=True,
         response_class=PrettyJSONResponse)
def read_companies_incorporated_today(skip: int = 0, limit: int = 100, 
                   db: Session = Depends(get_db)):
    
    today = datetime.datetime.now()
    
    return crud.get_company_by_date(db, 
                                    year=today.year, 
                                    month=today.month, 
                                    day=today.day).all()