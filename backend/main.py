# Driver code for the backend
#
# @zgr2788

import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas, models as _models, database as _database
from typing import List


app = _fastapi.FastAPI()

_services.create_database()




#*********************************************************

# DOCTORS 

#*********************************************************

# Create a doctor
@app.post("/api/doctors")
async def create_doctor(doc: _schemas._DoctorCreate, db:_orm.Session = _fastapi.Depends(_services.get_db)):

    return await _services.create_doc(doc, db)

# Delete a doctor
@app.delete("/api/doctors/deleteDoc/{doctor_id}", status_code = 204)
async def delete_doctor(doctor_id : int, db:_orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_doc(doc_id = doctor_id , db = db)
    return {"message" : "Successfully deleted doctor with id " + str(doctor_id)}

# Get all doctors
@app.get("/api/doctors", status_code = 200)
async def get_all_doctors(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_docs(db = db)

# Display doctors by name
@app.get("/api/doctors/name/{doctor_name}", status_code = 200)
async def get_doctors_by_name(doctor_name: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_docs_by_name(doc_name = doctor_name, db = db)

# Display doctors by specialization
@app.get("/api/doctors/spec/{spec_name}", status_code = 200)
async def get_doctors_by_spec(specialization: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_docs_by_spec(spec_name = specialization, db = db)