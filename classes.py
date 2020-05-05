from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Sequence

Base = declarative_base()

class Company(Base):
     __tablename__ = 'companies'

     number = Column(Integer, primary_key=True)
     name = Column(String)
     incorporated_on = Column(Date)

     def __repr__(self):
        return f"<Company(company='{self.name}', number={self.number}, incorporated_on={self.incorporated_on})>" 


class Test(Base):
    __tablename__ = 'testtable'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    testfield = Column(String)

    def __repr__(self):
        return f"<Test(id='{self.id}', testfield={self.testfield})>" 
