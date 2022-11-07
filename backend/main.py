# Driver code for the backend
#
# @zgr2788

import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas, models as _models, database as _database
from typing import List


app = _fastapi.FastAPI()

_services.create_database()