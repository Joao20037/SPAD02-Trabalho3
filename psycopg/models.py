from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(String(5), primary_key=True)
    company_name = Column(String(40))

class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True)
    last_name = Column(String(20))

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(String(5), ForeignKey('customers.customerid'))
    employee_id = Column(Integer, ForeignKey('employees.employeeid'))
    order_date = Column(Date)
    customer = relationship("Customer")
    employee = relationship("Employee")

class OrderDetail(Base):
    __tablename__ = 'order_details'
    order_id = Column(Integer, ForeignKey('orders.orderid'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.productid'), primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(Numeric)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(40))
