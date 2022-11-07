# HOSADM services provided by the backend
#
# @zgr2788

import database as _database
import models as _models
import schemas as _schemas
import sqlalchemy.orm as _orm
import json as _json
import fastapi as _fastapi
import datetime as _dt
from dateutil import tz as _tz


# Define timezones
from_zone = _tz.gettz('UTC')
to_zone = _tz.gettz('Turkey')
