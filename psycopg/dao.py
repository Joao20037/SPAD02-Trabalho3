import psycopg

class Dao:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO northwind;")

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert_order(self, order_id, customer_id, employee_id, order_date):
        sql = "INSERT INTO orders (orderid, customerid, employeeid, orderdate) VALUES (%s, %s, %s, %s) RETURNING orderid;"
        self.cur.execute(sql, (order_id, customer_id, employee_id, order_date))
        order_id = self.cur.fetchone()[0]
        self.conn.commit()
        return order_id

    def insert_order_detail(self, order_id, product_id, quantity, unit_price):
        sql = "INSERT INTO order_details (orderid, productid, quantity, unitprice) VALUES (%s, %s, %s, %s);"
        self.cur.execute(sql, (order_id, product_id, quantity, unit_price))
        self.conn.commit()

    def get_order_details(self, order_id):
        sql = "SELECT p.productname, od.quantity, od.unitprice " \
              "FROM order_details od " \
              "JOIN products p ON od.productid = p.productid " \
              "WHERE od.orderid = %s;"
        self.cur.execute(sql, (order_id,))
        return self.cur.fetchall()

    def get_order_info(self, order_id):
        sql = "SELECT o.orderid, o.orderdate, c.companyname, e.lastname " \
              "FROM orders o " \
              "JOIN customers c ON o.customerid = c.customerid " \
              "JOIN employees e ON o.employeeid = e.employeeid " \
              "WHERE o.orderid = %s;"
        self.cur.execute(sql, (order_id,))
        return self.cur.fetchone()

    def get_employee_ranking(self, start_date, end_date):
        sql = "SELECT e.lastname, COUNT(o.orderid), SUM(od.quantity * od.unitprice) " \
              "FROM employees e " \
              "JOIN orders o ON e.employeeid = o.employeeid " \
              "JOIN order_details od ON o.orderid = od.orderid " \
              "WHERE o.orderdate BETWEEN %s AND %s " \
              "GROUP BY e.lastname " \
              "ORDER BY COUNT(o.orderid) DESC;"
        self.cur.execute(sql, (start_date, end_date))
        return self.cur.fetchall()
    
    def get_next_order_id(self):
        sql = "SELECT COALESCE(MAX(orderid), 0) FROM orders;"
        self.cur.execute(sql)
        max_order_id = self.cur.fetchone()[0]
        return max_order_id + 1
    
    def get_unit_price(self, product_id):
        sql = "SELECT unitprice FROM products WHERE productid = %s;"
        self.cur.execute(sql, (product_id,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None
