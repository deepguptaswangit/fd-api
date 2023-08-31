from sqlalchemy import Column, Integer, String
from database import Base


# Define FD Device class inheriting from Base
class FDDevice(Base):
    __tablename__ = 'fd'
    deviceId = Column(Integer, primary_key=True)
    description = Column(String(256))
