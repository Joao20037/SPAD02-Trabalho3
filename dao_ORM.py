import sqlalchemy
from model_ORM import *

class Dao_ORM:
    
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        # print(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}")
        self.engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

    def create_session(self):
        Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        session = Session()
        return session

    def insert_order(self, model_order):
        try:
            session = self.create_session()

            session.add(model_order)

            session.commit()

            order = session.query(Order).filter(Order.orderid == model_order.orderid).first()

            session.close()

            return order.orderid    
        except Exception as e:
            print(f"Ocorreu um erro ao inserir o pedido: {e}")

    def insert_order_detail(self, model_detail):
        try:
            session = self.create_session()

            session.add(model_detail)

            session.commit()
            
            session.close()

        except Exception as e:
            print(f"Ocorreu um erro ao inserir os detalhes do pedido: {e}")

    def get_order_details(self, order_id):
        try:
            session = self.create_session()

            order_dt = session.query(
                Product.productname,
                OrderDetail.quantity,
                OrderDetail.unitprice
            ).join(
                Product, OrderDetail.productid == Product.productid
            ).filter(
                OrderDetail.orderid == order_id
            ).all()

            session.commit()
            session.close()

            return order_dt
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o relatório: {e}")
    
    def get_order_info(self, order_id):
        try:
            session = self.create_session()

            order = session.query(
                Order.orderid, Order.orderdate ,Customer.companyname, Employee.lastname
            ).join(
                Customer, Order.customerid == Customer.customerid
            ).join(
                Employee, Order.employeeid == Employee.employeeid
            ).filter(
                Order.orderid == order_id
            ).first()

            session.commit()
            session.close()

            return order
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o relatório: {e}")

    def get_employee_ranking(self, start_date, end_date):
        try:
            session = self.create_session()

            employee_rank = session.query(Employee.lastname,
                        sqlalchemy.func.count(Order.orderid).label('order_count'),
                        sqlalchemy.func.sum(OrderDetail.quantity * OrderDetail.unitprice).label('total_sales')
                ).join(
                    Order, Employee.employeeid == Order.employeeid
                ).join(
                    OrderDetail, Order.orderid == OrderDetail.orderid
                ).filter(
                    Order.orderdate.between(start_date, end_date)
                ).group_by(
                    Employee.lastname
                ).order_by(
                    sqlalchemy.func.count(Order.orderid).desc()
                ).all()
            
            session.close()

            return employee_rank
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o relatório: {e}")
    def get_next_order_id(self):
        try:
            session = self.create_session()

            max_order_id = session.query(sqlalchemy.func.coalesce(sqlalchemy.func.max(Order.orderid), 0)).scalar()

            max_order_id += 1

            session.close()

            return max_order_id
        except Exception as e:
            print("Não foi possível recuperar o próximo orderid:", e)
    
    def get_unit_price(self, product_id):
        try:
            session = self.create_session()

            unit_price = session.query(Product.unitprice).filter(Product.productid == product_id)

            session.close()

            return unit_price
        except Exception as e:
            print(f"Não foi possivel recuperar o preço unitário de {product_id}: {e}")