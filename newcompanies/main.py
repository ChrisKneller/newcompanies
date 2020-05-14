import json
import datetime

from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

import crud, models, schemas
import datagather as dg
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


@app.get("/company/{company_id}", response_model=schemas.Company)
def read_company(company_id: int, db: Session = Depends(get_db)):
    
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


@app.get("/search", response_model=List[schemas.CompanyIncorporated])
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


@app.get("/incorporated/today",
         response_model=List[schemas.CompanyIncorporated],
         response_model_exclude_defaults=True)
def read_companies_incorporated_today(skip: int = 0, limit: int = 100, 
                   db: Session = Depends(get_db)):
    
    today = datetime.datetime.now()
    
    return crud.get_company_by_date(db, 
                                    year=today.year, 
                                    month=today.month, 
                                    day=today.day).all()
