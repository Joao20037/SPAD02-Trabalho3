import sqlalchemy
from modelORM import *

class Dao:
    
    def __init__(self, dbname, user, password, host="localhost", port=5432):

        self.engine = sqlalchemy.create_engine(f"postegresql+psycopg://{user}:{password}@{host}:{port}/{dbname}")

    def create_session(self):
        Session = sqlalchemy.sessionmaker()
        session = Session()
        return session

    def insert_order(self, model_order):

        session = self.create_session()

        session.add(model_order)

        session.commit()

        order = session.query(model_order)

        session.close()

        return order.id    

    def insert_order_detail(self, model_detail):

        session = self.create_session()

        session.add(model_detail)

        session.commit()
        session.close()

    def get_order_details(self, order_id):
        
        session = self.create_session()

        order_dt = session.query(OrderDetail.product.productname, OrderDetail.quantity, OrderDetail.unitprice
                                 ).filter(OrderDetail.orderid == order_id).first()

        session.commit()
        session.close()

        return order_dt
    
    def get_order_info(self, order_id):

        session = self.create_session()

        order = session.query(Order.orderid, Order.costumer.companyname, Order.employee.lastname
                              ).filter(Order.orderid == order_id).first()

        session.commit()
        session.close()

        return order
        
    def get_employee_ranking(self, start_date, end_date):

        session = self.create_session()

        employee_rank = session.query(Employee.lastname,
                      sqlalchemy.func.count(Order.orderid).label('order_count'),
                      sqlalchemy.func.sum(OrderDetail.quantity * OrderDetail.unitprice).label('total_sales')
            ).filter(
                Order.orderdate.between(start_date, end_date)
            ).group_by(
                Employee.lastname
            ).order_by(
                sqlalchemy.func.count(Order.orderid).desc()
            ).all()
        
        session.close()

        return employee_rank
    
    def get_next_order_id(self):

        session = self.create_session()

        max_order_id = session.query(sqlalchemy.func.coalesce(sqlalchemy.func.max(Order.orderid), 0)).scalar()

        max_order_id += 1

        session.close()

        return max_order_id
    
    def get_unit_price(self, product_id):

        session = self.create_session()

        unit_price = session.query(Product.unitprice).filter(Product.productid == product_id)

        session.close()

        return unit_price