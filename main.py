# Driver code for the backend
#
# @zgr2788

import fastapi as _fastapi
import fastapi.templating as _templates
import fastapi.staticfiles as _StaticFiles
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas, models as _models, database as _database
import jinja2 as _jinja2
from typing import List


app = _fastapi.FastAPI()

_services.create_database()

app.mount("/static", _StaticFiles.StaticFiles(directory="static"), name="static")

templates = _templates.Jinja2Templates(directory = "templates")


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
    print(assigned, history, name)
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

# TREATMENTS & BILLING

#*********************************************************

# Get bill home
@app.get("/billing/home")
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
