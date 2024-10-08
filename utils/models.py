from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime, date

Base = declarative_base()


class LineReserve(Base):
    __tablename__ = "line_reserves"

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

    def as_dict(self):
        return {
            c.key: (
                getattr(self, c.key).strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(getattr(self, c.key), datetime)
                else (
                    getattr(self, c.key).strftime("%Y-%m-%d")
                    if isinstance(getattr(self, c.key), date)
                    else getattr(self, c.key)
                )
            )
            for c in class_mapper(self.__class__).columns
        }


class LineUser(Base):
    __tablename__ = "line_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_id = Column(String(255))
    name = Column(String(255))
    name_kana = Column(String(255))
    phone_number = Column(String(20))
    age = Column(Integer)
    adult = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
