import mysql.connector
from menu_lists import *
from menu_utils import *
from db_operations import *

connection = mysql.connector.connect(user='root', host='localhost', database='papelaria_chicotis', autocommit=True)
cursor_object = connection.cursor()

# Função que lida com a opção escolhida pelo cliente no menu principal de clientes
def handle_customer_menu_option(user_id):
    while True:
        clear_screen()
        display_menu_blue(CUSTOMER_MENU_OPTIONS, "ÁREA DE CLIENTE")
        userOption = get_integer_input("Insira uma opção: ", 1, len(CUSTOMER_MENU_OPTIONS))
        match userOption:
            case 1:
                clear_screen()
                process_shopping(cursor_object, user_id) # Função para realizar compras
            case 2:
                break # Volta atrás
        
# Função que lida com a opção escolhida pelo funcionário no menu principal de funcionários
def handle_employee_menu_option():
    while True:
        clear_screen()
        display_menu_blue(EMPLOYEE_MENU_OPTIONS, "ÁREA DE FUNCIONÁRIO")
        userOption = get_integer_input("Insira uma opção: ", 1, len(EMPLOYEE_MENU_OPTIONS))
        match userOption:
            case 1:
                clear_screen()
                insert_product_db(cursor_object) # Função para adicionar novo produto
            case 2:
                clear_screen() 
                add_to_product_quantity(cursor_object) # Função para adicionar unidades a produto existente
            case 3:
                break # Volta atrás

# Função que lida com a opção escolhida pelo administrador no menu de gestão de funcionários
def handle_employee_management_option():
    while True:
        clear_screen()
        display_menu_purple(EMPLOYEE_MANAGEMENT_OPTIONS, "GESTÃO DE FUNCIONÁRIOS")
        userOption = get_integer_input("Insira uma opção: ", 1, len(EMPLOYEE_MANAGEMENT_OPTIONS))
        match userOption:
            case 1:
                clear_screen()
                update_user_employee_db(cursor_object) # Função para atualizar funcionário
            case 2:
                clear_screen()
                insert_user_employee_db(cursor_object) # Função para adicionar funcionário
            case 3:
                clear_screen()
                remove_user_employee_db(cursor_object) # Função para remover
            case 4:
                break # Voltar atrás

# Função que lida com a opção escolhida pelo administrador no menu de gestão de relatórios
def handle_reports_management_option():
    while True:
        clear_screen()
        display_menu_purple(REPORT_TYPES_OPTIONS , "GESTÃO DE RELATÓRIOS")
        userOption = get_integer_input("Insira uma opção: ", 1, len(REPORT_TYPES_OPTIONS))
        match userOption:
            case 1:
                clear_screen()
                total_stock(cursor_object) # Função de stock por produto
            case 2:
                clear_screen()
                sales_by_product(cursor_object) # Função de "Vendas por produto"
            case 3:
                clear_screen()
                average_sale(cursor_object) # Função de média de valor por venda
            case 4:
                clear_screen()
                next_month_sale_product(cursor_object) # Função de estimativa de vendas do mês seguinte
                next_month_sale(cursor_object)
            case 5:
                print_scatter_sales_quantity(cursor_object) # Função de Gráfico de Vendas por Quantidade de Produto Vendido
            case 6:
                break # Volta atrás

# Função que lida com a opção escolhida pelo administrador no menu principal de administradores
def handle_manager_menu_option():
    while True:
        clear_screen()
        display_menu_blue(MANAGER_MENU_OPTIONS, "ÁREA DE ADMINISTRADOR")
        userOption = get_integer_input("Insira uma opção: ", 1, len(MANAGER_MENU_OPTIONS))
        match userOption:
            case 1:
                handle_employee_management_option()
            case 2:
                handle_reports_management_option()
            case 3:
                break # Volta atrás

# Função que lida com a opção escolhida pelo usuário no menu principal do sistema
def handle_main_menu_option():
    while True:
        clear_screen()
        display_menu_blue(MAIN_MENU_OPTIONS, "PAPELARIA CHICOTIS")
        userOption = get_integer_input("Insira uma opção: ", 1, len(MAIN_MENU_OPTIONS))
        match userOption:
            case 1:
                user = get_user_info(cursor_object) # Valida login e retorna informações do usuário
                role_code = user["role_code"]
                user_id = user["id"]
                match role_code:
                    case 1:
                        handle_manager_menu_option()
                    case 2:
                        handle_employee_menu_option()
                    case 3:
                        handle_customer_menu_option(user_id)
            case 2:
                clear_screen()
                insert_user_db(cursor_object) # Função para realizar registo de cliente
            case 2:
                break # Volta atrás


try:
    handle_main_menu_option()

finally:
    cursor_object.close()
    connection.close()