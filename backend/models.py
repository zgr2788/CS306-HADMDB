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

