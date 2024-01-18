from menu_utils import print_menu_header_purple, print_menu_header_blue, line
from tabulate import tabulate

# Imprime todas as informações de usuário
def print_all_user_info(nif, name, phone, city, login_name, password):
    print_menu_header_blue("INFORMAÇÕES DE USUÁRIO")
    print(f"""\nNIF: {nif}
Nome: {name}
Telemóvel: {phone}
Localidade: {city}
Nome de usuário: {login_name}
Palavra-passe: {password}""")

# Imprime todos os produtos com o preço e quantidade em stock
def print_all_products(all_products):
    print_menu_header_blue("PRODUTOS DA PAPELARIA CHICOTIS")
    for product in all_products:
        sale_price = product['price'] + (product['price'] * 0.3)
        print(f"""{product['name']}
{sale_price:.2f}€      
Qtd: {product['quantity']}
""")
        
# Imprime o produto escolhido para a compra.
def print_chosen_products(card, subtotal_price, iva, total_price):
    print_menu_header_purple("DADOS DA COMPRA")
    print("")
    for product in card:
        print(f"""{product['name']}
Qtd: {product['quantity']}
{product['subtotal']:.2f}€ ({product['price']:.2f}€/un)
""")
    print(line())
    print(f"""                      Total s/ IVA: {subtotal_price:.2f}€
                          IVA: {iva:.2f}€ (23%)
                             TOTAL: {total_price:.2f}€\n""")

# Imprime o talão
def print_bill(card, customer_id, sum_all_prices, total_iva, total_price, order_id):
    print("\nAqui está o seu talão:\n")
    print(line())  
    print("\033[0;32m{}\033[0m".format("FATURA".center(40)))
    print(f"Nº: {order_id}".center(40))  
    print(f"Nº de cliente: {customer_id}".center(40))  
    print(line()) 
    print("")
    for product in card:
        print(f"""{product['name']}
Qtd: {product['quantity']}
{product['subtotal']:.2f}€ ({product['price']:.2f}€/un)
""")
    print(line())
    print(f"""                      Total s/ IVA: {sum_all_prices:.2f}€
                          IVA: {total_iva:.2f}€ (23%)
                             TOTAL: {total_price:.2f}€\n""")

# Imprime todos os produtos 
def print_all_product_info(all_products):
    all_products_info = [["ID", "Nome", "Quantidade", "Preço (€)"]]

    for product in all_products:
        all_products_info.append([product['id'], product['name'], product['quantity'], product['price']])
    
    print(line(53))
    print("STOCK".center(51))
    print(line(53))
    print(tabulate(all_products_info, headers="firstrow", tablefmt="pretty"), "\n")

# Imprime as venda por produtos 
def print_sales_by_products(all_products, header, measure):
    all_products_info = [["ID", "Produto", measure]]

    for product in all_products:
        all_products_info.append([product[0], product[1], product[2]])
    
    print(line(43))
    print("\033[1;36m {}\033[0m".format(header.center(41)))
    print(line(43))
    print(tabulate(all_products_info, headers="firstrow", tablefmt="pretty"), "\n")

# Imprime a lista de todos funcionários
def print_employee_list(employees):
    all_employee_info = [["ID", "Nome", "NIF", "Telemóvel", "City", "Nome de Usuário", "Palavra-passe"]]

    for employee in employees:
        all_employee_info.append([employee[0], employee[1], employee[2], employee[3], employee[4], employee[5], employee[6]])

    print(line(101))
    print("\033[1;36m {}\033[0m".format("FUNCIONÁRIOS DA PAPELARIA CHICOTIS".center(98)))
    print(line(101))
    print(tabulate(all_employee_info, headers="firstrow", tablefmt="pretty"), "\n")

# Imprime dados de um funcionário
def print_employee(employee):
    employee_info = [["ID", "Nome", "NIF", "Telemóvel", "City", "Nome de Usuário", "Palavra-passe"], [employee[0], employee[1], employee[2], employee[3], employee[4], employee[5], employee[6]]]

    print("\nDADOS DO FUNCIONÁRIO:")
    print(tabulate(employee_info, headers="firstrow", tablefmt="pretty"), "\n")

