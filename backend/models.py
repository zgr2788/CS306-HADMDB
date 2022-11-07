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