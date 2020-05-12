import json
import datetime

from typing import List

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

import crud, models, schemas
from datagather import get_company_data
from database import SessionLocal, engine
from functions import alchemyencoder, to_json
from models import Company, Address

# uvicorn main:app --reload
# env\Scripts\activate.bat

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/company/{company_id}")
async def read_company(company_id: int):
    
    company = get_company_data(company_id)
    
    return company if company else None


@app.get("/companies", response_model=List[schemas.Company])
def get_companies(
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


<<<<<<< HEAD
@app.get("/incorporated/today",
         response_model=List[schemas.Company],
         response_model_exclude_defaults=True)
=======
@app.get("/incorporated/today", response_model=List[schemas.Company])
>>>>>>> 0e9147aac53922f29ddd4021f53e77e0df9659ee
def read_cos_today(skip: int = 0, limit: int = 100, 
                   db: Session = Depends(get_db)):
    
    today = datetime.datetime.now()
    
<<<<<<< HEAD
    return crud.get_company_by_date(db, year=2020, month=5, day=11).all()
=======
    return crud.get_company_by_date(db, year=2020, month=5, day=1).all()
>>>>>>> 0e9147aac53922f29ddd4021f53e77e0df9659ee
