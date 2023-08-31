from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime


# Define FD Device class inheriting from Base
class FDDevice(Base):
    __tablename__ = 'fd'
    deviceId = Column(Integer, primary_key=True)
    deviceType = Column(String(256))
    active = Column(String(256))
    department = Column(String(256))
    roomNumber = Column(Integer)
    floorNumber = Column(Integer)
    status = Column(String(256))
    description = Column(String(256))
    # dateTime = datetime
