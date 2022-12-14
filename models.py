# Models for the database
# 
# @zgr2788


import datetime as _dt
from dateutil import tz as _tz
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import database as _database

# Define timezones
from_zone = _tz.gettz('UTC')
to_zone = _tz.gettz('Turkey')



#*********************************************************

# DOCTORS 

#*********************************************************

class Doctor(_database.Base):

    # Name
    __tablename__ = "doctors"

    #Columns
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)  # Unique doctor id - pkey
    spec = _sql.Column(_sql.String, index = True)      # Specialization
    name = _sql.Column(_sql.String, index = True)      # Name


#*********************************************************

# NURSES 

#*********************************************************

class Nurse(_database.Base):

    # Name
    __tablename__ = "nurses"

    #Columns
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)  # Unique nurse id - pkey
    name = _sql.Column(_sql.String, index = True)      # Name


#*********************************************************

# SERVICES 

#*********************************************************

class Service(_database.Base):

    # Name
    __tablename__ = "services"

    #Columns
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)  # Unique services id - pkey
    type = _sql.Column(_sql.String, index = True)      # Type
    name = _sql.Column(_sql.String, index = True)      # Name

#*********************************************************

# ROOMS 

#*********************************************************

class Room(_database.Base):

    # Name
    __tablename__ = "rooms"

    #Columns
    occupied_by = _sql.Column(_sql.Integer,  index = True, default = 0)  # Unique patient.id for occupation of room - fkey - constraint enforced via dbms
    occupied = _sql.Column(_sql.Boolean, index = True, default = False) # Is room occupied
    name = _sql.Column(_sql.String, index = True)  # Room name
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)  # Unique rooms id - pkey
    size = _sql.Column(_sql.Integer, index = True)      # Room size


#*********************************************************

# PATIENT 

#*********************************************************

class Patient(_database.Base):

    # Name
    __tablename__ = "patients"

    #Columns
    admitted_to = _sql.Column(_sql.Integer,  index = True, default = 0)  # Unique room_id for occupation of room - fkey - constraint enforced via dbms
    treated_by = _sql.Column(_sql.Integer, _sql.ForeignKey('doctors.id', ondelete="CASCADE"),  index = True)  # Unique doctor_id for treatment - fkey
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)  # Unique patient id - pkey
    history = _sql.Column(_sql.String, index = True)      # History
    name = _sql.Column(_sql.String, index = True)      # Name

#*********************************************************

# TREATMENTS 

#*********************************************************

class Treatment(_database.Base):

    # Name
    __tablename__ = "treatments"

    #Columns
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)  # Unique treatment id - pkey 
    billed_to = _sql.Column(_sql.Integer, _sql.ForeignKey('patients.id', ondelete="CASCADE"),  index = True)  # Unique patient.id for billed_to - fkey
    cost = _sql.Column(_sql.Integer, index = True)      # Cost
    name = _sql.Column(_sql.String, index = True)      # Name

#*********************************************************