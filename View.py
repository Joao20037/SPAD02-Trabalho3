





def Main():

    input_value = 0 

    while input_value != -1:
        print()
        print("NorthWind Ltda")

        try:
            input_value = input("Digite:\n1 Cadastrar novo pedido\n2 Relatorio de pedido\n3 Relatorio de ranking de funcionarios por intervalo de tempo\nEnter ou -1 para encerrar o programa\n-> ")
            if not input_value: input_value = -1
            input_value = int(input_value)


            if input_value == 1:
                ...
                # Cadastro de pedido

            elif input_value == 2:
                ...
                # Relatorio de pedido

            elif input_value == 3:
                ...
                # Relatorio Ranking funcionarios

            else:
                if input_value != -1: print("Entrada invalida")
            
        except KeyboardInterrupt:
            print("\nCodigo encerrado")
        except ValueError:
            print("Entrada invalida")






if __name__ == "__main__":
    Main()
