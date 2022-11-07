# Schemas for the database
#
# @zgr2788

import datetime as _dt
import pydantic as _pydantic

# For this project, the POST and GET schemas will be the same
# Security concerns will be disregarded




#*********************************************************

# DOCTORS 

#*********************************************************
class _DoctorCreate(_pydantic.BaseModel):
    spec : str
    name : str

    class Config:
        orm_mode = True 


class Doctor(_DoctorCreate):
    id : int


    class Config:
        orm_mode = True
