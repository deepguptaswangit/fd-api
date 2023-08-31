from pydantic import BaseModel


# Create Device Schema (Pydantic Model)
class DeviceCreate(BaseModel):
    description: str


# Complete Device Schema (Pydantic Model)
class FDDevice(BaseModel):
    deviceId: int
    description: str

    class Config:
        from_attributes = True
