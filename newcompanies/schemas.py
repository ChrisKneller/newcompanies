import datetime

from pydantic import BaseModel, BaseConfig, Schema
from typing import List, Dict, Set

from functions import to_camelcase


class APIBase(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        alias_generator = to_camelcase
        allow_population_by_field_name = True


class AddressBase(APIBase):
    address_line1 : str = None
    postcode: str = None


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    address_line2 : str = None
    address_line3 : str = None
    po_box : str = None
    post_town : str = None
    county : str = None
    postcode : str = None
    country : str = None


class CompanyBase(APIBase):
    number: int
    name: str


class CompanyCreate(CompanyBase):
    incorporated : datetime.date


class Company(CompanyBase):
    incorporated : datetime.date
    address: Address