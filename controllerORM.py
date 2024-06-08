import sqlalchemy
from daoORM import Dao

class ControllerORM:

    def __init__(self, dbname, user, password):
        self.dao = Dao(dbname, user, password)

