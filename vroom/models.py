import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TEXT, TIMESTAMP


engine = create_engine(os.environ['DB_CONNECTION'])

Base = declarative_base()

Session = sessionmaker(bind=engine)


# Booking table for rental car booking information
class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    external_id = Column(TEXT, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(TEXT, nullable=False)
    car = Column(TEXT, nullable=False)
    company_name = Column(TEXT, nullable=False)
    company_address = Column(TEXT, nullable=False)
    price = Column(Float(precision=2, asdecimal=True), nullable=False)
    created = Column(TIMESTAMP(timezone=False), default=datetime.utcnow,
        nullable=False)
