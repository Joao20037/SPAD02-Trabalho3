from dao import Dao_Driver
from dao_ORM import Dao_ORM
from model import Order, OrderDetail
from datetime import datetime

class Controller:
    def __init__(self):
        self.dao = None
    
    def set_dao(self, type_dao, dbname, user, password):
        if type_dao == "1":
            self.dao = Dao_ORM(dbname=dbname, user=user, password=password)
        if type_dao == "2":
            self.dao = Dao_Driver(dbname=dbname, user=user, password=password)

    def insert_order(self, order_id, customer_id, employee_id):
        order_date = datetime.now().date()
        order = Order(orderid=order_id, customerid=customer_id, employeeid=employee_id, orderdate=order_date)
        self.dao.insert_order(order)

    def insert_order_details(self, order_details):
        for order_detail in order_details:
            order_detail_obj = OrderDetail(orderid=order_detail[0], productid=order_detail[1], unitprice=order_detail[2], quantity=order_detail[3])
            self.dao.insert_order_detail(order_detail_obj)

    def get_unit_price(self, product_id):
        return self.dao.get_unit_price(product_id)

    def get_next_order_id(self):
        return self.dao.get_next_order_id()
    
    def get_order_info(self, order_id):
        order_info = self.dao.get_order_info(order_id)
        if order_info:
            print("Informações do Pedido:")
            print(f"Número do Pedido: {order_info[0]}")
            print(f"Data do Pedido: {order_info[1]}")
            print(f"Nome do Cliente: {order_info[2]}")
            print(f"Nome do Vendedor: {order_info[3]}")
            order_details = self.dao.get_order_details(order_id)
            print("Itens do Pedido:")
            for detail in order_details:
                print(f"Produto: {detail[0]}, Quantidade: {detail[1]}, Preço: {detail[2]}")
        else:
            print("Pedido não encontrado.")

    def get_employee_ranking(self, start_date, end_date):
        employee_ranking = self.dao.get_employee_ranking(start_date, end_date)
        print("Ranking dos Funcionários:")
        for rank in employee_ranking:
            print(f"Funcionário: {rank[0]}, Total de Pedidos: {rank[1]}, Total Vendido: {rank[2]}")
