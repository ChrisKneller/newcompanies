from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Sequence, ForeignKey, DateTime

try:
    from .functions import to_camelcase
except:
    from functions import to_camelcase

# alembic revision -m "Your message"
# alembic revision --autogenerate -m "Your message"
# alembic upgrade head

Base = declarative_base()


class ToDictMixin(object):
    def to_dict(self, camelcase=True):
        if camelcase:
            return {to_camelcase(column.key): getattr(self, attr) for attr, column in self.__mapper__.c.items()}
        else:
            return {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}


class TimestampMixin(object):
    record_created = Column('record_created', DateTime, default=datetime.now())


class Company(Base, ToDictMixin, TimestampMixin):
    __tablename__ = 'companies'

    number = Column(Integer, primary_key=True)
    name = Column(String)
    incorporated = Column(Date)
    address_id  = Column(Integer, ForeignKey("addresses.id"))

    address = relationship("Address", back_populates="occupier")

    def __repr__(self):
        return f"<Company(number='{self.number}', name='{self.name}', "\
             + f"incorporated='{self.incorporated.isoformat}')>"


class Address(Base, ToDictMixin, TimestampMixin):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    address_line1 = Column(String)
    address_line2 = Column(String)
    address_line3 = Column(String)
    po_box = Column(String)
    post_town = Column(String)
    county = Column(String)
    postcode = Column(String)
    country = Column(String)
    # occupier_id = Column(Integer, ForeignKey("companies.number"))

    occupier = relationship("Company", back_populates="address")

    def __repr__(self):
        return f"<Address(address_line1='{self.address_line1}', "\
             + f"postcode='{self.postcode}')>"

class SICCode(Base):
    __tablename__ = 'siccodes'

    code = Column(Integer, primary_key=True)
    text = Column(String)

class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    first_names = Column('firstNames', String)
    last_name = Column('lastName', String)

# class CompanyAddresses(Base):
#     __tablename__ = 'companyaddresses'

#     dttm = Column(DateTime, default=datetime.utcnow)

# class CompanySICCodes(Base):
#     __tablename__ = 'companysiccodes'

#     dttm = Column(DateTime, default=datetime.utcnow)
    

# class CompanyDirectors(Base):
#     __tablename__ = 'companydirectors'

#     dttm = Column(DateTime, default=datetime.utcnow)

class Test(Base):
    __tablename__ = 'testtable'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    testfield = Column(String)

    def __repr__(self):
        return f"<Test(id='{self.id}', testfield={self.testfield})>" 
