import psycopg
from model import Order, OrderDetail, Customer, Employee, Product

class Dao:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO northwind;")

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert_order(self, order):
        try:
            sql = "INSERT INTO orders (orderid, customerid, employeeid, orderdate) VALUES (%s, %s, %s, %s) RETURNING orderid;"
            self.cur.execute(sql, (order.orderid, order.customerid, order.employeeid, order.orderdate))
            order_id = self.cur.fetchone()[0]
            self.conn.commit()
            return order_id
        except Exception as e:
            print("Ocorreu um erro ao inserir o pedido:", e)

    def insert_order_detail(self, order_details):
        try:
            sql = "INSERT INTO order_details (orderid, productid, quantity, unitprice) VALUES (%s, %s, %s, %s);"
            self.cur.execute(sql, (order_details.orderid, order_details.productid, order_details.quantity, order_details.unitprice))
            self.conn.commit()
        except Exception as e:
            print("Ocorreu um erro ao inserir o pedido:", e)
            

    def get_order_details(self, order_id):
        try:
            sql = "SELECT p.productname, od.quantity, od.unitprice " \
                "FROM order_details od " \
                "JOIN products p ON od.productid = p.productid " \
                "WHERE od.orderid = %s;"
            self.cur.execute(sql, (order_id,))
            return self.cur.fetchall()
        except Exception as e:
            print("Ocorreu um erro ao gerar relatório:", e)

    def get_order_info(self, order_id):
        try:
            sql = "SELECT o.orderid, o.orderdate, c.companyname, e.lastname " \
                "FROM orders o " \
                "JOIN customers c ON o.customerid = c.customerid " \
                "JOIN employees e ON o.employeeid = e.employeeid " \
                "WHERE o.orderid = %s;"
            self.cur.execute(sql, (order_id,))
            return self.cur.fetchone()
        except Exception as e:
            print("Ocorreu um erro ao gerar relatório:", e)

    def get_employee_ranking(self, start_date, end_date):
        try:
            sql = "SELECT e.lastname, COUNT(o.orderid), SUM(od.quantity * od.unitprice) AS total_sales " \
                "FROM employees e " \
                "JOIN orders o ON e.employeeid = o.employeeid " \
                "JOIN order_details od ON o.orderid = od.orderid " \
                "WHERE o.orderdate BETWEEN %s AND %s " \
                "GROUP BY e.lastname " \
                "ORDER BY total_sales DESC;"
            self.cur.execute(sql, (start_date, end_date))
            return self.cur.fetchall()
        except Exception as e:
            print("Ocorreu um erro ao gerar relatório:", e)
    
    def get_next_order_id(self):
        try:
            sql = "SELECT COALESCE(MAX(orderid), 0) FROM orders;"
            self.cur.execute(sql)
            max_order_id = self.cur.fetchone()[0]
            return max_order_id + 1
        except Exception as e:
            print("Não foi possível recuperar o próximo orderid:", e)
    
    def get_unit_price(self, product_id):
        sql = "SELECT unitprice FROM products WHERE productid = %s;"
        self.cur.execute(sql, (product_id,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None
