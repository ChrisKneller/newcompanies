from typing import List
from pydantic import BaseModel
import datetime

class CompanyBase(BaseModel):
    number: int
    title: str


class CompanyCreate(CompanyBase):
    incorporated : datetime.date


class Company(CompanyBase):
    incorporated : datetime.date

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    line_1 : str
    postcode: str


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):

    line_2 : str
    line_3 : str
    po_box : str
    post_town : str
    county : str
    postcode : str
    country : str


    class Config:
        orm_mode = True