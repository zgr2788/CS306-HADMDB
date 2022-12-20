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


#*********************************************************

# NURSES

#*********************************************************
class _NurseCreate(_pydantic.BaseModel):
    name : str

    class Config:
        orm_mode = True 


class Nurse(_NurseCreate):
    id : int


    class Config:
        orm_mode = True


#*********************************************************

# SERVICES

#*********************************************************
class _ServiceCreate(_pydantic.BaseModel):
    name : str
    type : str

    class Config:
        orm_mode = True 


class Service(_ServiceCreate):
    id : int


    class Config:
        orm_mode = True


#*********************************************************

# ROOM

#*********************************************************
class _RoomCreate(_pydantic.BaseModel):
    size : int
    name : str

    class Config:
        orm_mode = True 


class Room(_RoomCreate):
    id : int
    occupied : bool
    occupied_by : int


    class Config:
        orm_mode = True


#*********************************************************

# PATIENT 

#*********************************************************

class _PatientCreate(_pydantic.BaseModel):
    name : str
    history : str
    treated_by: int

    class Config:
        orm_mode = True 


class Patient(_PatientCreate):
    id : int
    admitted_to : int
    


    class Config:
        orm_mode = True