from flask_sqlalchemy import SQLAlchemy
from configs import Configurator, DEFAULT_CONFIG_PATH


db = SQLAlchemy()
settings = Configurator().from_py_file(DEFAULT_CONFIG_PATH)

