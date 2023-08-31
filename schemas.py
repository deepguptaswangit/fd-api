from pydantic import BaseModel
from datetime import datetime


# Create Device Schema (Pydantic Model)
class DeviceCreate(BaseModel):
    deviceId: int
    deviceType: str
    active: str
    department: str
    roomNumber: int
    floorNumber: int
    status: str
    description: str
    dateTime: datetime


# Complete Device Schema (Pydantic Model)
class FDDevice(BaseModel):
    deviceId: int
    description: str
    deviceType: str
    active: str
    department: str
    roomNumber: int
    floorNumber: int
    status: str
    dateTime: datetime

    class Config:
        from_attributes = True
