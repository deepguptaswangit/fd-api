from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "Fall Detection"


@app.post("/v1/devices/", response_model=schemas.FDDevice, status_code=status.HTTP_201_CREATED)
def create_devices(fd: schemas.DeviceCreate, session: Session = Depends(get_session)):
    # create an instance of the FD database model
    fddb = models.FDDevice(deviceType=fd.deviceType,deviceId=fd.deviceId, active=fd.active,
                           department=fd.department, roomNumber=fd.roomNumber,
                           floorNumber=fd.floorNumber, status=fd.status, description=fd.description)

    # add it to the session and commit it
    session.add(fddb)
    session.commit()
    session.refresh(fddb)

    # return the fd object
    return fddb


@app.get("/v1/devices/{deviceId}", response_model=schemas.FDDevice)
def read_devices(deviceId: int, session: Session = Depends(get_session)):
    # get the fd item with the given id
    fd = session.query(models.FDDevice).get(deviceId)

    # check if fd item with given id exists. If not, raise exception and return 404 not found response
    if not fd:
        raise HTTPException(status_code=404, detail=f"fd item with id {deviceId} not found")

    return fd


@app.put("/v1/devices/{deviceId}", response_model=schemas.FDDevice)
def update_devices(deviceId: int, description: str, session: Session = Depends(get_session)):
    # get the fd item with the given id
    fd = session.query(models.FDDevice).get(deviceId)

    # update fd item with the given description (if an item with the given id was found)
    if fd:
        fd.description = description
        session.commit()

    # check if fd item with given id exists. If not, raise exception and return 404 not found response
    if not fd:
        raise HTTPException(status_code=404, detail=f"fd item with id {deviceId} not found")

    return fd


@app.delete("/v1/devices/{deviceId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_devices(deviceId: int, session: Session = Depends(get_session)):
    # get the fd item with the given deviceId
    fd = session.query(models.FDDevice).get(deviceId)

    # if fd item with given id exists, delete it from the database. Otherwise, raise 404 error
    if fd:
        session.delete(fd)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"fd item with deviceId {deviceId} not found")

    return None


@app.get("/v1/devices/", response_model=List[schemas.FDDevice])
def read_devices_list(session: Session = Depends(get_session)):
    # get all fd items
    fd_list = session.query(models.FDDevice).all()

    return fd_list
