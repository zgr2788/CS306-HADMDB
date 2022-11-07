# HOSADM services provided by the backend
#
# @zgr2788

import database as _database
import models as _models
import schemas as _schemas
import sqlalchemy.orm as _orm
import json as _json
import fastapi as _fastapi
import datetime as _dt
from dateutil import tz as _tz


# Define timezones
from_zone = _tz.gettz('UTC')
to_zone = _tz.gettz('Turkey')

# Create
def create_database():
    return _database.Base.metadata.create_all(bind = _database.engine)

# Get db
def get_db():
    db = _database.SessionLocal()
    
    try:
        yield db
    finally:
        db.close()




#*********************************************************

# DOCTORS 

#*********************************************************

# Doctor query by id
async def get_doc_by_id(id : int, db : _orm.Session):
    return db.query(_models.Doctor).filter(_models.Doctor.id == id).first()

# Create new doctor
async def create_doc(doc : _schemas._DoctorCreate, db : _orm.Session):
        
    # New doctor object
    docObj = _models.Doctor(
        name = doc.name,
        spec = doc.spec  
    )

    # Write to db
    db.add(docObj)
    db.commit()
    db.refresh(docObj)
    return docObj

# Delete doctor
async def delete_doc(doc_id : int , db : _orm.Session):
    doc_db =  await get_doc_by_id(doc_id, db)

    if doc_db is None:
        raise _fastapi.HTTPException(status_code=404, detail = "Doctor ID not found in database!")

    db.delete(doc_db)
    db.commit()