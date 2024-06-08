from controller import Controller

class View:
    def __init__(self, dbname, user, password):
        self.controller = Controller(dbname, user, password)

    def run(self):
        while True:
            print("\nMenu:")
            print("1. Inserir Pedido")
            print("2. Ver Informações de um Pedido")
            print("3. Ver Ranking dos Funcionários por Intervalo de Tempo")
            print("0. Sair")
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
