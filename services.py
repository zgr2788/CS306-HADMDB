# HOSADM services provided by the backend
#
# @zgr2788

import database as _database
import models as _models
import schemas as _schemas
import sqlalchemy.orm as _orm
import sqlalchemy as _sql
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


# Insert some doctors, nurses, rooms, personnel and patients
async def insert_dummy_data(db : _orm.Session):
    
    # Doctors
    docNames = ["Gus Fring", "Michael Scott", "Yamac Kocovali", "Ramiz Karaeski", "Ezel Bayraktar", "Mahmut Orhan", "Ismet Inonu"]
    docSpecs = ["Heart Surgeon", "ENT Specialist", "Ophthalmologist", "Dermatologist", "Urologist", "ENT Specialist", "Dermatologist"]

    for i in range(len(docNames)):
        docObj = _models.Doctor(
        name = docNames[i],
        spec = docSpecs[i]  
        )
        db.add(docObj)
        db.commit()
        db.refresh(docObj)
    
    # Nurses
    nurseNames = ["Florence Nightingale", "Dorothea Dix", "Margaret Sanger", "Virginia Henderson", "Clara Barton", "Mary Eliza Mahoney", "Mary Breckinridge"]
    
    for i in range(len(nurseNames)):
        nurObj = _models.Nurse(
        name = nurseNames[i]  
        )
        db.add(nurObj)
        db.commit()
        db.refresh(nurObj)
    
    # Personnel
    perNames = ["Walter White", "Jesse Pinkman", "Mike Ehrmantraut", "Jimmy McGill", "Patrick Bateman", "Jack Napier", "Antonio Montana"]
    perSpecs = ["Cook", "Cook", "Security Specialist", "Legal Advisor", "Financial Advisor", "Workspace Ethics Advisor", "Security Specialist"]

    for i in range(len(perNames)):
        
        perObj = _models.Service(
        name = perNames[i],
        type = perSpecs[i]  
        )

        db.add(perObj)
        db.commit()
        db.refresh(perObj)

    # Rooms
    roNames = ["White Room", "Blue Room", "Red Room", "Pink Room", "Purple Room", "Orange Room", "Black Room"]
    roSizes = [250, 350, 270, 450, 160, 580, 330]

    for i in range(len(roNames)):
      
      roObj = _models.Room(
      name = roNames[i],
      size = roSizes[i]  
      )
      db.add(roObj)
      db.commit()
      db.refresh(roObj)

    # Patients
    patNames = ["Thomas Shelby", "Arthur Shelby", "John Shelby", "Ragnar Lothbrok", "Bjorn Lothbrok", "Miles Morales", "Michelle Obama"]
    patHist = ["Heart Attack", "Nosebleed", "Astigmatism + Myopia", "Vitiligo", "Syphilis", "Runny Nose", "Eczema"]
    patTreatBy = [1, 2, 3, 4, 5, 6, 7]

    for i in range(len(patNames)):
      
      patObj = _models.Patient(
      name = patNames[i],
      history = patHist[i],
      treated_by = patTreatBy[i]  
      )

      db.add(patObj)
      db.commit()
      db.refresh(patObj) 

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
    
    # Delete all patients of a doctor for cascade
    pats = db.query(_models.Patient).filter(_models.Patient.treated_by == doc_db.id).all()

    for pat in pats:
        await delete_pat(pat.id, db)

    db.delete(doc_db)
    db.commit()

# Get doctors by name
async def get_docs_by_name(doc_name : str, db : _orm.Session):
    items = db.query(_models.Doctor).filter(_models.Doctor.name.contains(doc_name))
    return list(map(_schemas.Doctor.from_orm, items))

# Get doctors by spec
async def get_docs_by_spec(spec_name : str, db : _orm.Session):
    items = db.query(_models.Doctor).filter(_models.Doctor.spec.contains(spec_name))
    return list(map(_schemas.Doctor.from_orm, items))

# Get all docs
async def get_docs(db : _orm.Session):
    items = db.query(_models.Doctor).filter(_models.Doctor.spec.contains(''))
    return list(map(_schemas.Doctor.from_orm, items))


#*********************************************************

# NURSES

#*********************************************************

# Nurse query by id
async def get_nur_by_id(id : int, db : _orm.Session):
    return db.query(_models.Nurse).filter(_models.Nurse.id == id).first()

# Create new nurse
async def create_nur(nur : _schemas._NurseCreate, db : _orm.Session):
        
    # New nurse object
    nurObj = _models.Nurse(
        name = nur.name,
    )

    # Write to db
    db.add(nurObj)
    db.commit()
    db.refresh(nurObj)
    return nurObj

# Delete nurse
async def delete_nur(nur_id : int , db : _orm.Session):
    nur_db =  await get_nur_by_id(nur_id, db)

    if nur_db is None:
        raise _fastapi.HTTPException(status_code=404, detail = "Nurse ID not found in database!")

    db.delete(nur_db)
    db.commit()

# Get nurses by name
async def get_nurs_by_name(nur_name : str, db : _orm.Session):
    items = db.query(_models.Nurse).filter(_models.Nurse.name.contains(nur_name))
    return list(map(_schemas.Nurse.from_orm, items))

# Get all nurses
async def get_nurses(db : _orm.Session):
    items = db.query(_models.Nurse).filter(_models.Nurse.name.contains(''))
    return list(map(_schemas.Nurse.from_orm, items))


#*********************************************************

# SERVICES 

#*********************************************************

# Service query by id
async def get_ser_by_id(id : int, db : _orm.Session):
    return db.query(_models.Service).filter(_models.Service.id == id).first()

# Create new ser
async def create_ser(ser : _schemas._ServiceCreate, db : _orm.Session):
        
    # New doctor object
    serObj = _models.Service(
        name = ser.name,
        type = ser.type  
    )

    # Write to db
    db.add(serObj)
    db.commit()
    db.refresh(serObj)
    return serObj

# Delete ser
async def delete_ser(ser_id : int , db : _orm.Session):
    ser_db =  await get_ser_by_id(ser_id, db)

    if ser_db is None:
        raise _fastapi.HTTPException(status_code=404, detail = "Personnel ID not found in database!")

    db.delete(ser_db)
    db.commit()

# Get sers by name
async def get_sers_by_name(ser_name : str, db : _orm.Session):
    items = db.query(_models.Service).filter(_models.Service.name.contains(ser_name))
    return list(map(_schemas.Service.from_orm, items))

# Get all sers
async def get_sers(db : _orm.Session):
    items = db.query(_models.Service).filter(_models.Service.type.contains(''))
    return list(map(_schemas.Service.from_orm, items))


#*********************************************************

# ROOMS

#*********************************************************

# ro query by id
async def get_ro_by_id(id : int, db : _orm.Session):
    return db.query(_models.Room).filter(_models.Room.id == id).first()

# Create new ro
async def create_ro(ro : _schemas._RoomCreate, db : _orm.Session):
        
    # New doctor object
    roObj = _models.Room(
        name = ro.name,
        size = ro.size  
    )

    # Write to db
    db.add(roObj)
    db.commit()
    db.refresh(roObj)
    return roObj

# Delete ro
async def delete_ro(ro_id : int , db : _orm.Session):
    ro_db =  await get_ro_by_id(ro_id, db)

    if ro_db is None:
        raise _fastapi.HTTPException(status_code=404, detail = "Room ID not found in database!")
    
    if ro_db.occupied:
        pat_id = ro_db.occupied_by
        pat_db = await get_pat_by_id(pat_id,db)
        pat_db.admitted_to = 0
        
        db.commit()
        db.refresh(pat_db)



    db.delete(ro_db)
    db.commit()

# Get ros by name
async def get_ros_by_name(ro_name : str, db : _orm.Session):
    items = db.query(_models.Room).filter(_models.Room.name.contains(ro_name))
    return list(map(_schemas.Room.from_orm, items))

# Get all ros
async def get_ros(db : _orm.Session):
    items = db.query(_models.Room).filter(_models.Room.name.contains(''))
    return list(map(_schemas.Room.from_orm, items))




#*********************************************************

# PATIENTS

#*********************************************************

# pat query by id
async def get_pat_by_id(id : int, db : _orm.Session):
    return db.query(_models.Patient).filter(_models.Patient.id == id).first()

# Create new pat
async def create_pat(pat : _schemas._RoomCreate, db : _orm.Session):
        
    # New doctor object
    patObj = _models.Patient(
        name = pat.name,
        history = pat.history, 
        treated_by = pat.treated_by 
    )

    # Write to db
    db.add(patObj)
    db.commit()
    db.refresh(patObj)
    return patObj

# Delete pat
async def delete_pat(pat_id : int , db : _orm.Session):
    pat_db =  await get_pat_by_id(pat_id, db)

    if pat_db is None:
        raise _fastapi.HTTPException(status_code=404, detail = "Patient ID not found in database!")

    if pat_db.admitted_to:
        ro_id = pat_db.admitted_to
        ro_db = await get_ro_by_id(ro_id, db)

        ro_db.occupied = False
        ro_db.occupied_by = 0
        
        db.commit()
        db.refresh(ro_db)

    db.delete(pat_db)
    db.commit()

# Get pats by name
async def get_pats_by_name(pat_name : str, db : _orm.Session):
    items = db.query(_models.Patient).filter(_models.Patient.name.contains(pat_name))
    return list(map(_schemas.Patient.from_orm, items))

# Get all pats
async def get_pats(db : _orm.Session):
    items = db.query(_models.Patient).filter(_models.Patient.name.contains(''))
    return list(map(_schemas.Patient.from_orm, items))

