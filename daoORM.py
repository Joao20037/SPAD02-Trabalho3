import sqlalchemy

class Dao:
    
    def __init__(self, dbname, user, password, host="localhost", port=5432):

        self.engine = sqlalchemy.create_engine(f"postegresql+psycopg://{user}:{password}@{host}:{port}/{dbname}")


    def insert_order(self, model_order):

        Session = sqlalchemy.sessionmaker()
        session = Session()

        session.add(model_order)

        session.commit()

        order = session.query(model_order)

        return order.id    