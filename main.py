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
def create_devices(todo: schemas.DeviceCreate, session: Session = Depends(get_session)):
    # create an instance of the ToDo database model
    tododb = models.FDDevice(description=todo.description)

    # add it to the session and commit it
    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    # return the todo object
    return tododb


@app.get("/v1/devices/{id}", response_model=schemas.FDDevice)
def read_devices(id: int, session: Session = Depends(get_session)):
    # get the todo item with the given id
    todo = session.query(models.FDDevice).get(id)

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo


@app.put("/v1/devices/{id}", response_model=schemas.FDDevice)
def update_devices(id: int, description: str, session: Session = Depends(get_session)):
    # get the todo item with the given id
    todo = session.query(models.FDDevice).get(id)

    # update todo item with the given description (if an item with the given id was found)
    if todo:
        todo.description = description
        session.commit()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo


@app.delete("/v1/devices/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_devices(id: int, session: Session = Depends(get_session)):
    # get the todo item with the given id
    todo = session.query(models.FDDevice).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None


@app.get("/v1/devices/", response_model=List[schemas.FDDevice])
def read_devices_list(session: Session = Depends(get_session)):
    # get all todo items
    todo_list = session.query(models.FDDevice).all()

    return todo_list
