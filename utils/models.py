from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LineReserve(Base):
    __tablename__ = 'line_reserves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer)
    reservation_date = Column(Date)
    check_in = Column(Date)
    check_out = Column(Date)
    line_id = Column(String(255))
    name = Column(String(255))
    phone_number = Column(String(20))
    status = Column(String(50))
    count_of_person = Column(Integer)
    room_type = Column(String(50))
    option_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class LineUser(Base):
    __tablename__ = 'line_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_id = Column(String(255))
    name = Column(String(255))
    name_kana = Column(String(255))
    phone_number = Column(String(20))
    age = Column(Integer)
    adult = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
