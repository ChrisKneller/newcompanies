from typing import List

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from datagather import get_company_data
from database import SessionLocal, engine
from models import Company
from functions import alchemyencoder, to_json
import crud, models, schemas

import json
import datetime

# uvicorn main:app --reload
# env\Scripts\activate.bat

app = FastAPI()

# SESSION = connect_to_db(DB)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/company/{company_id}")
async def read_company(company_id: int):
    company = get_company_data(company_id)
    return company if company else None


@app.get("/cos/", response_model=List[schemas.Company])
def read_cos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cos = crud.get_cos(db, skip=skip, limit=limit)
    return cos

@app.get("/companies", response_model=List[schemas.Company])
def get_companies(
    year: int = None, month: int = None, day: int = None, number: int = None, 
    name: str = None, db: Session = Depends(get_db)):
    arguments = locals()
    arguments.pop("db")
    print(arguments)
    if not any(arguments.values()):
        return None
    myquery = db.query(models.Company)
    for key, value in arguments.items():
        print(f"{key}: {value}")
        if not value:
            continue
        if key == 'year' or key == 'month' or key == 'day':
            print("Is it doing it here?")
            myquery = crud.get_company_by_date(db, **{key:value})
        else:
            myquery = crud.filter_query(myquery, **{key:value})
    return myquery.all()
    # return {"companies": [i.as_json() for i in query]} if query else {None}

@app.get("/incorporated/today")
def read_cos_today(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    today = datetime.datetime.now()
    return crud.get_company_by_date(db, year=2020, month=5, day=1).all()


# @app.gt("/incorporated")
# def get_companies(**kwargs):



@app.get("/incorporated/{year}/{month}/{day}")
def get_companies_by_day(year: int, month: int, day: int):
    query = get_company_by_date(SESSION, year=year, month=month, day=day)
    # query = SESSION.query(Company).filter_by(incorporated_on=f"{year}-{month}-{day}").all()
    return {"companies": [i.as_json() for i in query]}


@app.get("/incorporated/{year}/{month}")
def get_companies_by_month(year: int, month: int):
    query = get_company_by_date(SESSION, year=year, month=month)
    return {"companies": [i.as_json() for i in query]}


@app.get("/incorporated/{year}")
def get_companies_by_year(year: int):
    query = get_company_by_date(SESSION, year=year)
    return {"companies": [i.as_json() for i in query]}


    

@app.get("/testrequest")
def test_request():
    query = SESSION.query(Company).order_by(Company.number).filter_by(name="PAARTI LTD")
    # return json.dumps({"company": i.to_dict() for i in query}, default=alchemyencoder)
    return {"company": [i for i in query]}
    # return Response(to_json(query[0])})

