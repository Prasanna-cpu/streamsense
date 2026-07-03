from decouple import config as decouple_config

from sqlalchemy.engine import default

DATABASE_URL = decouple_config("DATABASE_URL", default = "")
