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
