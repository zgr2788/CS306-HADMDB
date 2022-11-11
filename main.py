# Driver code for the backend
#
# @zgr2788

import fastapi as _fastapi
import fastapi.templating as _templates
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas, models as _models, database as _database
from typing import List


app = _fastapi.FastAPI()

_services.create_database()

templates = _templates.Jinja2Templates(directory = "templates")


#*********************************************************

# DOCTORS 

#*********************************************************

# Create a doctor
@app.get("/create/doctors/")
async def create_doctor(request: _fastapi.Request):
    statusMessage = "Start typing names..."
    return templates.TemplateResponse('doctor_insert.html', context = {'request': request, 'statusMessage': statusMessage})

@app.post("/create/doctors/")
async def create_doctor(request : _fastapi.Request, name : str =  _fastapi.Form(), spec : str = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    statusMessage = "Successfully added doctor " + name + "."
    doc = _schemas._DoctorCreate(
        name = name,
        spec = spec 
    )
    await _services.create_doc(doc, db)
    return templates.TemplateResponse('doctor_insert.html', context = {'request': request, 'statusMessage': statusMessage})

# Delete a doctor
@app.get("/delete/doctors/")
async def delete_doctor(request: _fastapi.Request):
    statusMessage = "Type the id of the doctor you would like to delete..."
    return templates.TemplateResponse('doctor_delete.html', context = {'request': request, 'statusMessage': statusMessage})


@app.post("/delete/doctors/", status_code = 204)
async def delete_doctor(request : _fastapi.Request, doctor_id : int = _fastapi.Form(), db:_orm.Session = _fastapi.Depends(_services.get_db)):
    doc_db = await _services.get_doc_by_id(doctor_id, db)

    if not doc_db:
        statusMessage = "Doctor with id " + str(doctor_id) + " does not exist in database!"
    
    else:
        name = doc_db.name
        await _services.delete_doc(doc_id = doctor_id , db = db)
        statusMessage = "Successfully deleted " + str(name) + " from the database."

    return templates.TemplateResponse('doctor_delete.html', context = {'request': request, 'statusMessage' : statusMessage})


# Get doctors by name
@app.get("/get/doctors/")
async def get_doctors_by_name(request: _fastapi.Request):
    statusMessage = "Start typing name..."
    return templates.TemplateResponse('doctor_select.html', context = {'request': request, 'result': statusMessage})

@app.post("/get/doctors/", status_code = 200)
async def get_doctors_by_name(request: _fastapi.Request, doctor_name : str = _fastapi.Form(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    doc_list = [(doctor.name, doctor.spec, doctor.id) for doctor in await _services.get_docs_by_name(doc_name = doctor_name, db = db)]
    
    if doc_list:
        statusMessage = doc_list
    
    else:
        statusMessage = "No doctors found!"

    return templates.TemplateResponse('doctor_select.html', context = {'request': request, 'result': statusMessage})

# Get all doctors - debug
@app.get("/api/get/doctors", status_code = 200)
async def get_all_doctors(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_docs(db = db)



## Display doctors by specialization
#@app.get("/api/doctors/spec/{spec_name}", status_code = 200)
#async def get_doctors_by_spec(specialization: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
#    return await _services.get_docs_by_spec(spec_name = specialization, db = db)

