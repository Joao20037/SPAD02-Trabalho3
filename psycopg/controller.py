# controller.py
from datetime import datetime
from dao import Dao

class Controller:
    def __init__(self, dbname, user, password):
        self.dao = Dao(dbname, user, password)

    

    def insert_order(self):
        customer_id = input("Digite o ID do cliente (varchar): ")
        employee_id = input("Digite o ID do vendedor (int): ")
        order_id = self.dao.get_next_order_id()  
        order_date = datetime.now().date()

        self.dao.insert_order(order_id, customer_id, employee_id, order_date)

        while True:
            product_id = input("Digite o ID do produto (ou 'fim' para encerrar): ")
            if product_id.lower() == 'fim':
                break
            
            unit_price = self.dao.get_unit_price(product_id)
            if unit_price is None:
                print("Produto não encontrado. Por favor, insira um ID de produto válido.")
                continue
            
            quantity = int(input("Digite a quantidade: "))
            self.dao.insert_order_detail(order_id, product_id, quantity, unit_price)

        print("Pedido inserido com sucesso!")

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
