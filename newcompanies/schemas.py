import datetime

from pydantic import BaseModel, BaseConfig, Schema
from typing import List, Dict, Set, Optional

from functions import to_camelcase


class APIBase(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        alias_generator = to_camelcase
        allow_population_by_field_name = True


class AddressBase(APIBase):
    address_line1 : str = None
    address_line2 : str = None
    address_line3 : str = None
    postcode: str = None


class AddressCreate(AddressBase):
    pass


class Address(APIBase):
    address_line1 : str = None
    address_line2 : str = None
    address_line3 : str = None
    po_box : str = None
    post_town : str = None
    county : str = None
    postcode : str = None
    country : str = None


class SICCode(APIBase):
    code: int
    text: str



class CompanyBase(APIBase):
    number: int
    name: str


class CompanyIncorporated(CompanyBase):
    incorporated: datetime.date


class CompanyCreate(CompanyBase):
    incorporated : datetime.date


class Company(CompanyBase):
    incorporated: datetime.date
    address: Optional[Address]
    sic_codes: Optional[List[SICCode]]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None


class UserInDB(User):
    hashed_password: str