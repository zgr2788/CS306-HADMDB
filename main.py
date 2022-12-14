# Driver code for the backend
#
# @zgr2788

import fastapi as _fastapi
from typing import Union
import fastapi.templating as _templates
import fastapi.staticfiles as _StaticFiles
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas, models as _models, database as _database
import jinja2 as _jinja2
import fastapi.security as _security
import jwt as _jwt
import json as _json
import random as _rnd
from typing import List
import datetime as _dt
from dateutil import tz as _tz

from_zone = _tz.gettz('UTC')
to_zone = _tz.gettz('Turkey')

app = _fastapi.FastAPI()

_services.create_database()

# NoSQL Database initialized here
message_id = 1
message_db = {}

app.mount("/static", _StaticFiles.StaticFiles(directory="static"), name="static")

templates = _templates.Jinja2Templates(directory = "templates")
JWT_SECRET_ADMIN = 'ADMINSECRETHADMDB'
adminJWT = {'name' : 'admin', 'password' : 'admin123'} # standard admin password

# On startup, add random data for the database
@app.on_event("startup")
async def startup():
    
    # If database is empty
    if await _services.get_docs(_database.SessionLocal()) == []:
        await _services.insert_dummy_data(_database.SessionLocal())
    return 0

# Main page
@app.get("/")
async def main_page(request: _fastapi.Request):
    return templates.TemplateResponse('homepage.html', context = {'request' : request})

# Admin Panel
@app.get("/adminpanel")
async def admin_panel(request: _fastapi.Request):
    return templates.TemplateResponse('admin_panel.html', context = {'request' : request})

#*********************************************************

# DOCTORS

#*********************************************************
# Get doctor home
@app.get("/home/doctors/")
async def home_doctor(request: _fastapi.Request):
    return templates.TemplateResponse('doctor_home.html', context = {'request' : request})

# Create a doctor
@app.get("/create/doctors/")
async def create_doctor(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('doctor_insert.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/create/doctors/")
async def create_doctor(request : _fastapi.Request, name : str =  _fastapi.Form(), spec : str = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    doc = _schemas._DoctorCreate(
        name = name,
        spec = spec
    )
    new_doc = await _services.create_doc(doc, db)
    statusMessage = "Successfully added doctor " + str(new_doc.name) + " with ID: " + str(new_doc.id) + "."
    return templates.TemplateResponse('doctor_insert.html', context = {'request': request, 'statusMessage': statusMessage})

# Delete a doctor
@app.get("/delete/doctors/")
async def delete_doctor(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('doctor_delete.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/delete/doctors/", status_code = 204)
async def delete_doctor(request : _fastapi.Request, doctor_id : int = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    doc_db = await _services.get_doc_by_id(doctor_id, db)

    if not doc_db:
        statusMessage = "Doctor with id " + str(doctor_id) + " does not exist in database!"

    else:
        name = doc_db.name
        await _services.delete_doc(doc_id = doctor_id , db = db)
        statusMessage = "Successfully deleted " + str(name) + " with ID: " + str(doctor_id) + " from the database."

    return templates.TemplateResponse('doctor_delete.html', context = {'request': request, 'statusMessage' : statusMessage})

# Get doctors by name
@app.get("/get/doctors/")
async def get_doctors_by_name(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('doctor_selection.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/get/doctors/", status_code = 200)
async def get_doctors_by_name(request: _fastapi.Request, doctor_name : str = _fastapi.Form(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    statusMessage = ""

    # Wildcard search
    if doctor_name == "*":
        doc_list = await _services.get_docs(db=db)
        return templates.TemplateResponse('doctor_selection.html', context = {'request': request, 'docs_list': doc_list, 'statusMessage' : statusMessage})

    doc_list = await _services.get_docs_by_name(doc_name = doctor_name, db = db)

    if not doc_list:
        statusMessage = "No doctors found!"

    return templates.TemplateResponse('doctor_selection.html', context = {'request': request, 'docs_list': doc_list, 'statusMessage' : statusMessage})

# Get all doctors - debug
@app.get("/getall/doctors", status_code = 200)
async def get_all_doctors(request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    docs_list = await _services.get_docs(db = db)
    return templates.TemplateResponse('doctor_display.html', context = {'request' : request, 'docs_list' : docs_list})


#*********************************************************

# NURSES

#*********************************************************
# Get nurse home
@app.get("/home/nurses/")
async def home_nurse(request: _fastapi.Request):
    return templates.TemplateResponse('nurse_home.html', context = {'request' : request})

# Create a nurse
@app.get("/create/nurses/")
async def create_nurse(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('nurse_insert.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/create/nurses/")
async def create_nurse(request : _fastapi.Request, name : str =  _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    nur = _schemas._NurseCreate(
        name = name
    )
    new_nur = await _services.create_nur(nur, db)
    statusMessage = "Successfully added nurse " + str(new_nur.name) + " with ID: " + str(new_nur.id) + "."
    return templates.TemplateResponse('nurse_insert.html', context = {'request': request, 'statusMessage': statusMessage})

# Delete a doctor
@app.get("/delete/nurses/")
async def delete_nurse(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('nurse_delete.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/delete/nurses/", status_code = 204)
async def delete_nurse(request : _fastapi.Request, nurse_id : int = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    nur_db = await _services.get_nur_by_id(nurse_id, db)

    if not nur_db:
        statusMessage = "Nurse with id " + str(nurse_id) + " does not exist in database!"

    else:
        name = nur_db.name
        await _services.delete_nur(nur_id = nurse_id , db = db)
        statusMessage = "Successfully deleted " + str(name) + " with ID: " + str(nurse_id) + " from the database."

    return templates.TemplateResponse('nurse_delete.html', context = {'request': request, 'statusMessage' : statusMessage})

# Get doctors by name
@app.get("/get/nurses/")
async def get_nurses_by_name(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('nurse_selection.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/get/nurses/", status_code = 200)
async def get_nurses_by_name(request: _fastapi.Request, nurse_name : str = _fastapi.Form(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    statusMessage = ""

    # Wildcard search
    if nurse_name == "*":
        nurse_list = await _services.get_nurses(db=db)
        return templates.TemplateResponse('nurse_selection.html', context = {'request': request, 'docs_list': nurse_list, 'statusMessage' : statusMessage})

    nurse_list = await _services.get_nurs_by_name(nur_name = nurse_name, db = db)

    if not nurse_list:
        statusMessage = "No nurses found!"

    return templates.TemplateResponse('nurse_selection.html', context = {'request': request, 'docs_list': nurse_list, 'statusMessage' : statusMessage})

# Get all doctors - debug
@app.get("/getall/nurses", status_code = 200)
async def get_all_nurses(request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    nurs_list = await _services.get_nurses(db = db)
    return templates.TemplateResponse('nurse_display.html', context = {'request' : request, 'docs_list' : nurs_list})


#*********************************************************

# SERVICES

#*********************************************************
# Get service home
@app.get("/home/services/")
async def home_service(request: _fastapi.Request):
    return templates.TemplateResponse('service_home.html', context = {'request' : request})

# Create aservice
@app.get("/create/services/")
async def create_service(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('service_insert.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/create/services/")
async def create_service(request : _fastapi.Request, name : str =  _fastapi.Form(), type : str = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    ser = _schemas._ServiceCreate(
        name = name,
        type = type
    )
    new_ser = await _services.create_ser(ser, db)
    statusMessage = "Successfully added personnel " + str(new_ser.name) + " with ID: " + str(new_ser.id) + "."
    return templates.TemplateResponse('service_insert.html', context = {'request': request, 'statusMessage': statusMessage})

# Delete a service
@app.get("/delete/services/")
async def delete_service(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('service_delete.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/delete/services/", status_code = 204)
async def delete_service(request : _fastapi.Request, service_id : int = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    ser_db = await _services.get_ser_by_id(service_id, db)

    if not ser_db:
        statusMessage = "Personnel with id " + str(service_id) + " does not exist in database!"

    else:
        name = ser_db.name
        await _services.delete_ser(ser_id = service_id , db = db)
        statusMessage = "Successfully deleted " + str(name) + " with ID: " + str(service_id) + " from the database."

    return templates.TemplateResponse('service_delete.html', context = {'request': request, 'statusMessage' : statusMessage})

# Get services by name
@app.get("/get/services/")
async def get_services_by_name(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('service_selection.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/get/services/", status_code = 200)
async def get_services_by_name(request: _fastapi.Request, service_name : str = _fastapi.Form(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    statusMessage = ""

    # Wildcard search
    if service_name == "*":
        service_list = await _services.get_sers(db=db)
        return templates.TemplateResponse('service_selection.html', context = {'request': request, 'docs_list': service_list, 'statusMessage' : statusMessage})

    service_list = await _services.get_sers_by_name(ser_name = service_name, db = db)

    if not service_list:
        statusMessage = "No personnel found!"

    return templates.TemplateResponse('service_selection.html', context = {'request': request, 'docs_list': service_list, 'statusMessage' : statusMessage})

# Get all services - debug
@app.get("/getall/services", status_code = 200)
async def get_all_services(request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    sers_list = await _services.get_sers(db = db)
    return templates.TemplateResponse('service_display.html', context = {'request' : request, 'docs_list' : sers_list})


#*********************************************************

# ROOMS

#*********************************************************
# Get room home
@app.get("/home/rooms/")
async def home_room(request: _fastapi.Request):
    return templates.TemplateResponse('room_home.html', context = {'request' : request})

# Create a room
@app.get("/create/rooms/")
async def create_room(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('room_insert.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/create/rooms/")
async def create_room(request : _fastapi.Request, size : str =  _fastapi.Form(), name : str = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    try :
        sizeNum = int(size)
    except :
        statusMessage = "Please enter numeric value for size!"
        return templates.TemplateResponse('room_insert.html', context = {'request': request, 'statusMessage': statusMessage}) 
    
    ro = _schemas._RoomCreate(
        size = sizeNum,
        name = name
    )
    new_ro = await _services.create_ro(ro, db)
    statusMessage = "Successfully added room " + str(new_ro.name) + " with ID: " + str(new_ro.id) + "."
    return templates.TemplateResponse('room_insert.html', context = {'request': request, 'statusMessage': statusMessage})

# Delete a room
@app.get("/delete/rooms/")
async def delete_room(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('room_delete.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/delete/rooms/", status_code = 204)
async def delete_room(request : _fastapi.Request, room_id : int = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    ro_db = await _services.get_ro_by_id(room_id, db)

    if not ro_db:
        statusMessage = "Room with id " + str(room_id) + " does not exist in database!"

    else:
        name = ro_db.name
        await _services.delete_ro(ro_id = room_id , db = db)
        statusMessage = "Successfully deleted " + str(name) + " with ID: " + str(room_id) + " from the database."

    return templates.TemplateResponse('room_delete.html', context = {'request': request, 'statusMessage' : statusMessage})

# Get rooms by name
@app.get("/get/rooms/")
async def get_rooms_by_name(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('room_selection.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/get/rooms/", status_code = 200)
async def get_rooms_by_name(request: _fastapi.Request, room_name : str = _fastapi.Form(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    statusMessage = ""

    # Wildcard search
    if room_name == "*":
        room_list = await _services.get_ros(db=db)
        return templates.TemplateResponse('room_selection.html', context = {'request': request, 'docs_list': room_list, 'statusMessage' : statusMessage})

    room_list = await _services.get_ros_by_name(ro_name = room_name, db = db)

    if not room_list:
        statusMessage = "No room found!"

    return templates.TemplateResponse('room_selection.html', context = {'request': request, 'docs_list': room_list, 'statusMessage' : statusMessage})

# Get all rooms - debug
@app.get("/getall/rooms", status_code = 200)
async def get_all_rooms(request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    ros_list = await _services.get_ros(db = db)
    return templates.TemplateResponse('room_display.html', context = {'request' : request, 'docs_list' : ros_list})



#*********************************************************

# PATIENTS

#*********************************************************
# Get patient home
@app.get("/home/patients/")
async def home_patient(request: _fastapi.Request):
    return templates.TemplateResponse('patient_home.html', context = {'request' : request})

# Create a patient
@app.get("/create/patients/")
async def create_patient(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('patient_insert.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/create/patients/")
async def create_patient(request : _fastapi.Request, assigned : str =  _fastapi.Form(), history : str =  _fastapi.Form(), name : str = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    try :
        assignedNum = int(assigned)
    except :
        statusMessage = "Please enter numeric value for assigned doctor ID!"
        return templates.TemplateResponse('patient_insert.html', context = {'request': request, 'statusMessage': statusMessage})

    assigned_doc = await _services.get_doc_by_id(assignedNum, db)

    if not assigned_doc:
        statusMessage = "Doctor ID not found in database!"
        return templates.TemplateResponse('patient_insert.html', context = {'request': request, 'statusMessage': statusMessage})

    pat = _schemas._PatientCreate(
        history = history,
        name = name,
        treated_by = assigned_doc.id
    )

    new_pat = await _services.create_pat(pat, db)
    statusMessage = "Successfully registered patient " + str(new_pat.name) + " under doctor " + str(assigned_doc.name) + "."
    return templates.TemplateResponse('patient_insert.html', context = {'request': request, 'statusMessage': statusMessage})

# Delete a patient
@app.get("/delete/patients/")
async def delete_patient(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('patient_delete.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/delete/patients/", status_code = 204)
async def delete_patient(request : _fastapi.Request, patient_id : int = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    pat_db = await _services.get_pat_by_id(patient_id, db)

    if not pat_db:
        statusMessage = "Patient with id " + str(patient_id) + " does not exist in database!"

    else:
        name = pat_db.name
        await _services.delete_pat(pat_id = patient_id , db = db)
        statusMessage = "Successfully deleted patient " + str(name) + " with ID: " + str(patient_id) + " from the database."

    return templates.TemplateResponse('patient_delete.html', context = {'request': request, 'statusMessage' : statusMessage})

# Get patients by name
@app.get("/get/patients/")
async def get_patients_by_name(request: _fastapi.Request):
    statusMessage = ""
    return templates.TemplateResponse('patient_selection.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/get/patients/", status_code = 200)
async def get_patients_by_name(request: _fastapi.Request, patient_name : str = _fastapi.Form(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    statusMessage = ""

    # Wildcard search
    if patient_name == "*":
        patient_list = await _services.get_pats(db=db)
        return templates.TemplateResponse('patient_selection.html', context = {'request': request, 'docs_list': patient_list, 'statusMessage' : statusMessage})

    patient_list = await _services.get_pats_by_name(pat_name = patient_name, db = db)

    if not patient_list:
        statusMessage = "No patients found!"

    return templates.TemplateResponse('patient_selection.html', context = {'request': request, 'docs_list': patient_list, 'statusMessage' : statusMessage})

# Get all rooms - debug
@app.get("/getall/patients", status_code = 200)
async def get_all_patients(request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pats_list = await _services.get_pats(db = db)
    return templates.TemplateResponse('patient_display.html', context = {'request' : request, 'docs_list' : pats_list})






#*********************************************************

# TREATMENTS & BILLING - FIRST FUNCTIONALITY

#*********************************************************

# Get bill home
@app.get("/bill/home")
async def home_billing(request: _fastapi.Request,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pats_list = await _services.get_pats(db = db)
    return templates.TemplateResponse('bill_treatments.html', context = {'request' : request, 'patients_list' : pats_list})

# Get bill for patient
@app.get("/billing/{pat_id}")
async def bill_patient(request: _fastapi.Request, pat_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pat_db = await _services.get_pat_by_id(pat_id, db)
    name = pat_db.name
    id = pat_db.id
    statusMessage = ""
    return templates.TemplateResponse('bill_patient.html', context = {'request' : request, 'patient_id' : id, 'patient_name' : name, 'statusMessage' : statusMessage})

# Set bill for patient
@app.post("/billing/{pat_id}")
async def bill_patient(request: _fastapi.Request, pat_id: int, name : str =  _fastapi.Form(), cost : str =  _fastapi.Form(),  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    try :
        costNum = int(cost)
    except :
        statusMessage = "Please enter numeric value for treatment cost!"
        return templates.TemplateResponse('bill_patient.html', context = {'request' : request, 'patient_id' : id, 'patient_name' : name, 'statusMessage' : statusMessage}) 
    

    pat_db = await _services.get_pat_by_id(pat_id, db)
    pat_id = pat_db.id

    trt = _models.Treatment(
        name = name,
        cost = cost,
        billed_to = pat_id
    )

    db.add(trt)
    db.commit()
    db.refresh(trt)

    statusMessage = "Successfully billed treatment " + str(name) + " to patient " + str(pat_db.name) + "."

    return templates.TemplateResponse('bill_patient.html', context = {'request' : request, 'patient_id' : id, 'patient_name' : name, 'statusMessage' : statusMessage})

# Get bill check
@app.get("/bill/check")
async def home_billing(request: _fastapi.Request,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pats_list = await _services.get_pats(db = db)
    return templates.TemplateResponse('check_bills.html', context = {'request' : request, 'patients_list' : pats_list})


# Get bills list for patient
@app.get("/billcheck/{pat_id}")
async def check_patient(request: _fastapi.Request, pat_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pat_db = await _services.get_pat_by_id(pat_id, db)
    bills_list = db.query(_models.Treatment).filter(_models.Treatment.billed_to == pat_id).all()
    name = pat_db.name
    id = pat_db.id
    total = sum([trt.cost for trt in bills_list])
    return templates.TemplateResponse('bills_table_patient.html', context = {'request' : request, 'patient_id' : id, 'patient_name' : name, 'pat_treat_list' : bills_list, 'total' : total})



#*********************************************************

# ROOM STATUS AND ADMISSION - SECOND FUNCTIONALITY

#*********************************************************

# Get Admission Home
@app.get("/admission/home")
async def home_room_admit(request: _fastapi.Request,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    rooms_list = await _services.get_ros(db = db)
    return templates.TemplateResponse('admit_rooms.html', context = {'request' : request, 'rooms_list' : rooms_list})

# Get admit for room
@app.get("/admitting/{room_id}")
async def admit_patient(request: _fastapi.Request, room_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    ro_db = await _services.get_ro_by_id(room_id, db)
    pats_list = await _services.get_pats(db)
    name = ro_db.name
    id = ro_db.id
    statusMessage = ""
    return templates.TemplateResponse('admitting_patient.html', context = {'request' : request, 'room_id' : room_id, 'patients_list' : pats_list, 'room_name' : name, 'statusMessage' : statusMessage})

# Get admit confirmation
@app.get("/admitting/{room_id}/{pat_id}")
async def admitting_patient(request: _fastapi.Request, room_id: int, pat_id : int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pat_db = await _services.get_pat_by_id(pat_id, db)
    room_db = await _services.get_ro_by_id(room_id, db)
    statusMessage = "Are you sure you want to admit " + pat_db.name + " to " + room_db.name + "?"
    return templates.TemplateResponse('admitting_areyousure.html', context = {'request' : request, 'room_id' : room_id, 'pat_id' : pat_id, 'room_name' : room_db.name, 'pat_name' : pat_db.name, 'statusMessage' : statusMessage})

# Confirm admission, post method
@app.post("/admitting/{room_id}/{pat_id}")
async def admitted_patient(request: _fastapi.Request, room_id: int, pat_id : int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    # Get pat and room
    pat_db = await _services.get_pat_by_id(pat_id, db)
    room_db = await _services.get_ro_by_id(room_id, db)

    # Admit and connect both
    pat_db.admitted_to = room_db.id
    room_db.occupied_by = pat_db.id
    room_db.occupied = True


    db.commit()
    db.refresh(pat_db)
    db.refresh(room_db)

    statusMessage = "Successfully admitted " + pat_db.name + " to " + room_db.name + "!"
    return templates.TemplateResponse('admitting_areyousure.html', context = {'request' : request, 'statusMessage' : statusMessage})

# Get Discharge Home
@app.get("/admission/discharge")
async def home_discharge(request: _fastapi.Request,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pats_list = await _services.get_pats(db = db)
    
    admitted_pats = []
    for pat in pats_list:
        if pat.admitted_to != 0:
            admitted_pats.append(pat)
    
    return templates.TemplateResponse('discharge_rooms.html', context = {'request' : request, 'pats_list' : admitted_pats})

# Get discharge confimation
@app.get("/admission/discharge/confirm/{pat_id}")
async def discharging_patient(request: _fastapi.Request, pat_id : int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pat_db = await _services.get_pat_by_id(pat_id, db)
    room_db = await _services.get_ro_by_id(pat_db.admitted_to, db)
    statusMessage = "Are you sure you want to discharge " + pat_db.name + " from " + room_db.name + "?"
    return templates.TemplateResponse('discharge_areyousure.html', context = {'request' : request, 'pat_id' : pat_id, 'room_id': room_db.id, 'room_name' : room_db.name, 'pat_name' : pat_db.name, 'statusMessage' : statusMessage})

# Confirm discharge, post method
@app.post("/admission/discharge/confirm/{pat_id}")
async def discharged_patient(request: _fastapi.Request, pat_id : int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    # Get pat and room
    pat_db = await _services.get_pat_by_id(pat_id, db)
    room_db = await _services.get_ro_by_id(pat_db.admitted_to, db)

    # Discharge both
    pat_db.admitted_to = 0
    room_db.occupied_by = 0
    room_db.occupied = False


    db.commit()
    db.refresh(pat_db)
    db.refresh(room_db)

    statusMessage = "Successfully discharged " + pat_db.name + " from " + room_db.name + "!"
    return templates.TemplateResponse('discharge_areyousure.html', context = {'request' : request, 'statusMessage' : statusMessage})



#*********************************************************

# MESSAGE BOARD

#*********************************************************

# Get main page
@app.get("/messageboard")
async def messageboard(request: _fastapi.Request, account_type: Union[str, None] = _fastapi.Cookie(default=None), guest_name: Union[str, None] = _fastapi.Cookie(default=None)):
    global message_id

    if not account_type == "Admin" and not guest_name:
        acc_type = "Guest"
        guest_nam = None
        resp = templates.TemplateResponse('messageboard.html', context = {'request' : request, 'account_type' : acc_type, 'guest_name' : guest_nam})
        resp.set_cookie(key='account_type', value='Guest')
        resp.set_cookie(key='token', value=str(_jwt.encode(_json.loads(_json.dumps({'sessionID' : str(_rnd.randint(10000000000000, 1000000000000000000000000))}, indent = 4, sort_keys=True, default=str)), JWT_SECRET_ADMIN)))    
    
    elif guest_name:
        acc_type = "Guest"
        guest_nam = guest_name
        
        
        mess_list = [message_db[i] for i in range(1,message_id) if  message_db[i]['sender'] == guest_name or message_db[i]['receiver'] == guest_name]

        resp = templates.TemplateResponse('messageboard.html', context = {'request' : request, 'account_type' : acc_type, 'guest_name' : guest_nam, 'mess' : mess_list})

    else:
        guest_nam = None 
        acc_type = "Admin"

        mess_list = [message_db[i] for i in range(1,message_id) if message_db[i]['receiver'] == "Admin"]

        resp = templates.TemplateResponse('messageboard.html', context = {'request' : request, 'account_type' : acc_type, 'guest_name' : guest_nam, 'mess' : mess_list})

    return resp


# Guest set name 
@app.post("/messageboard")
async def messageboard(request: _fastapi.Request, name : str = _fastapi.Form("")):
    if name != "":
        acc_type = "Guest"
        guest_nam = name
        resp = templates.TemplateResponse('messageboard.html', context = {'request' : request, 'account_type' : acc_type, 'guest_name' : guest_nam})
        resp.set_cookie(key='guest_name', value=name)
        return resp
    
    else:
        acc_type = "Guest"
        guest_nam = None
        resp = templates.TemplateResponse('messageboard.html', context = {'request' : request, 'account_type' : acc_type, 'guest_name' : guest_nam})
        resp.delete_cookie(key='guest_name')
        return resp

# On exit
@app.get("/exitmessages")
async def on_exit(request: _fastapi.Request):
    resp = templates.TemplateResponse('homepage.html', context = {'request' : request})
    resp.delete_cookie(key='guest_name')
    resp.delete_cookie(key='account_type')
    resp.delete_cookie(key='token')
    return resp

# Admin auth
@app.post("/messageboard/admin")
async def messageboard_admin(request: _fastapi.Request, password : str = _fastapi.Form("admin123")):
    acc_type = "Guest"
    guest_nam = None

    token, check = await _services.auth_admin(password)
    
    if not check:
        return _fastapi.responses.RedirectResponse(url='/messageboard')
    
    else:
        acc_type = "Admin"
        mess_list = [message_db[i] for i in range(1,message_id) if message_db[i]['receiver'] == "Admin"]

        resp = templates.TemplateResponse('messageboard.html', context = {'request' : request, 'account_type' : acc_type, 'guest_name' : guest_nam, 'mess' : mess_list})
        resp.set_cookie(key='account_type', value='Admin')
        resp.set_cookie(key='token', value=str(_jwt.encode(_json.loads(_json.dumps({'name' : 'admin', 'password' : 'admin123'}, indent = 4, sort_keys=True, default=str)), JWT_SECRET_ADMIN)))    
        
        return resp

# Send message - Guest
@app.get("/messageboard/post")
async def messageboard_post_guest(request: _fastapi.Request, subject : str = "", messagecontent : str = "", guest_name: Union[str, None] = _fastapi.Cookie(default=None)):
    global message_id

    message = {
        'id' : message_id, 
        'sender' : guest_name,
        'receiver' : "Admin",        
        'content' :  messagecontent,
        'subject' : subject,
        'date' : _dt.datetime.utcnow().replace(tzinfo=from_zone).astimezone(to_zone)
    }
    
    

    message_db[message_id] = message

    message_id += 1

    return _fastapi.responses.RedirectResponse("/messageboard")


# Send message - Admin
@app.get("/messageboard/admin/post/{mes_id}/{guest_name}/{subject}")
async def messageboard_post_admin(request: _fastapi.Request, mes_id : int, guest_name : str, subject : str):
    return templates.TemplateResponse("message_response.html", context={'request' : request, 'mes_id' : mes_id, 'guest_name' : guest_name, 'subject' : subject})

@app.post("/messageboard/admin/post/{mes_id}/{guest_name}/{subject}")
async def messageboard_post_admin(request: _fastapi.Request, mes_id : int, guest_name : str, subject : str, messagecontent : str = _fastapi.Form()):
    global message_id

    message = {
        'id' : message_id, 
        'sender' : "Admin",
        'receiver' : guest_name,        
        'content' :  messagecontent,
        'subject' : "Reply to " + subject,
        'date' : _dt.datetime.utcnow().replace(tzinfo=from_zone).astimezone(to_zone)
    }

    message_db[message_id] = message

    message_id += 1

    return _fastapi.responses.RedirectResponse("/messageboard/admin")
