# view.py
from controllerDriver import Controller
from controllerORM import ControllerORM
class View:
    def __init__(self, dbname, user, password):
        # self.controller = Controller(dbname, user, password)
        self.dbname = dbname
        self.user = user
        self.password = password
        self.controller = None

    @property
    def controller(self):
        return self.controller
    
    @property.setter
    def controller(self, controller):
        self.controller = controller
    
    def run(self):
        while True:
            print("\nMenu:")
            print("Escolha o modo de conexão:")
            print("1. ORM (Object-Relational Mapping)")
            print("2. Driver de conexão")
            option_connection = input("Escolha uma opção: ")
            if option_connection == "1":
                self.controller = ControllerORM(self.dbname, self.user, self.password)
            elif option_connection == "2":
                self.controller = Controller(self.dbname, self.user, self.password)
            else:
                print("Entrada Invalida")
                continue

            print("1. Inserir Pedido")
            print("2. Ver Informações de um Pedido")
            print("3. Ver Ranking dos Funcionários por Intervalo de Tempo")
            print("0. Sair")
            try: 
                option = input("Escolha uma opção: ")

                if option == '1':
                    self.controller.insert_order()
                elif option == '2':
                    order_id = input("Digite o número do pedido: ")
                    print('\n')
                    self.controller.get_order_info(order_id)
                elif option == '3':
                    start_date = input("Digite a data de início (YYYY-MM-DD): ")
                    end_date = input("Digite a data de fim (YYYY-MM-DD): ")
                    print('\n')
                    self.controller.get_employee_ranking(start_date, end_date)
                elif option == '0':
                    print("Saindo...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")

            except KeyboardInterrupt:
                print("\nCodigo encerrado")
                break
            except ValueError:
                print("Entrada invalida")

