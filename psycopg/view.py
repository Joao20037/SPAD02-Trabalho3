from controller import Controller

class View:
    def __init__(self, dbname, user, password):
        self.controller = Controller(dbname, user, password)

    def get_order_info_from_user(self):
        try:
            customer_id = input("Digite o ID do cliente (varchar): ")
            employee_id = input("Digite o ID do vendedor (int): ")
            return customer_id, employee_id
        except Exception as e:
            print("Ocorreu um erro ao obter as informações do cliente e vendedor:", e)
            return None, None

    def get_order_details_from_user(self, order_id):
        order_details = []

        while True:
            try:
                product_id = input("Digite o ID do produto (ou 'fim' para encerrar): ")
                if product_id.lower() == 'fim':
                    break
                
                unit_price = self.controller.get_unit_price(product_id)
                if unit_price is None:
                    print("Produto não encontrado. Por favor, insira um ID de produto válido.")
                    continue
                
                quantity = int(input("Digite a quantidade: "))
                order_details.append((order_id, product_id, unit_price, quantity))
            except ValueError:
                print("Quantidade inválida. Por favor, insira um número inteiro.")
            except Exception as e:
                print("Ocorreu um erro ao obter os detalhes do pedido:", e)

        return order_details

    def display_menu(self):
        print("\nMenu:")
        print("1. Inserir Pedido")
        print("2. Obter Informações do Pedido")
        print("3. Obter Ranking de Funcionários")
        print("4. Sair")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Escolha uma opção: ")

            if choice == '1':
                try:
                    customer_id, employee_id = self.get_order_info_from_user()
                    order_id = self.controller.get_next_order_id()
                    order_details = self.get_order_details_from_user(order_id)
                    
                    if order_details:
                        self.controller.insert_order(order_id, customer_id, employee_id)
                        self.controller.insert_order_details(order_details)
                        print("Pedido inserido com sucesso!")
                    else:
                        print("Não foram fornecidos detalhes do pedido. Pedido não foi inserido.")
                except Exception as e:
                    print("Ocorreu um erro ao inserir o pedido:", e)
            elif choice == '2':
                try:
                    order_id = input("Digite o ID do pedido: ")
                    self.controller.get_order_info(order_id)
                except Exception as e:
                    print("Ocorreu um erro ao obter informações do pedido:", e)
            elif choice == '3':
                try:
                    start_date = input("Digite a data de início (YYYY-MM-DD): ")
                    end_date = input("Digite a data de término (YYYY-MM-DD): ")
                    self.controller.get_employee_ranking(start_date, end_date)
                except Exception as e:
                    print("Ocorreu um erro ao obter o ranking de funcionários:", e)
            elif choice == '4':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
