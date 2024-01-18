from menu_utils import red, green, header_cyan, clear_screen, display_menu_green, get_integer_input
from print_operations import print_all_user_info, print_all_products, print_chosen_products, print_bill, print_all_product_info, print_employee_list, print_employee
from input_validators import *
from menu_lists import PAYMENT_METHODS
import datetime
import time
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd

# Obtém as informações do usuário
def get_user_info(cursor_object):
    while True:
        clear_screen()
        header_cyan("SEJA BEM-VINDO(A)!")
        user_login = get_login()
        user_password = get_password()

        query = "SELECT * FROM user WHERE login_name LIKE (%s) AND password LIKE (%s)"
        cursor_object.execute(query, (user_login, user_password))

        result = cursor_object.fetchone()

        if result:
            return {"id" : result[0], "role_code" : result[-1]}
        else:
            red("Usuário não existe!")
            user_yes_no_answer =  get_yes_no_answer("Deseja tentar novamente? (s/n) ")
            if user_yes_no_answer is None:
                break

# Verifica se o nif inserido já existe na base de dados
def check_nif(cursor_object):
    while True:
        nif = get_nif()
        query = "SELECT nif FROM user WHERE nif LIKE (%s)"

        cursor_object.execute(query,(nif,))  
        result = cursor_object.fetchone()

        if result:
            red("ERRO! NIF inserido já tem cadastro. Tente novamente.")
        else:
            return nif

# Verifica se o número inserido já existe na base de dados
def check_phone(cursor_object):
    while True:
        phone = get_phone()
        query = "SELECT phone FROM user WHERE phone LIKE (%s)"

        cursor_object.execute(query,(phone,))  
        result = cursor_object.fetchone()

        if result:
            red("ERRO! Telemóvel inserido já está cadastrado. Tente novamente")
        else:
            return phone

# Verifica se o nome de usuário sugerido já existe na base de dados
def check_login_name(cursor_object):
    while True:
        login_name = get_new_login_name()
        query = "SELECT login_name FROM user WHERE login_name LIKE (%s)"

        cursor_object.execute(query,(login_name,))  
        result = cursor_object.fetchone()

        if result:
            red("ERRO! Nome de usuário já existe. Tente novamente")
        else:
            return login_name

# Obtém dados para resgisto de cliente
def get_registration_info(cursor_object):
    header_cyan("ÁREA DE REGISTO")
    nif = check_nif(cursor_object)
    name = get_name()
    phone = check_phone(cursor_object)
    city = get_city()
    login_name = check_login_name(cursor_object)
    password = get_new_login_password()
    role_code = 3

    return nif, name, phone, city, login_name, password, role_code

# Insere dados de usuário na base de dados
def insert_user_db(cursor_object):
    nif, name, phone, city, login_name, password, role_code = get_registration_info(cursor_object)

    query = "INSERT INTO user (nif, name, phone, city, login_name, password, role_code) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    try:
        cursor_object.execute(query, (nif, name, phone, city, login_name, password, role_code))
    except:
        red("ERRO! Algo deu errado no registo.")
    finally:
        clear_screen()
        print_all_user_info(nif, name, phone, city, login_name, password)
        green("\nRegisto realizado com sucesso!")
        input("\n(Pressione enter para voltar ao menu principal)")

# Seleciona todos os artigos da papelaria da base de dados e insere em uma variável
def select_all_products_out_of_card(cursor_object, selected_product_ids):
    query = "SELECT id, name, price, quantity FROM product WHERE quantity != 0"
    
    if selected_product_ids:  # não selecionar produtos que já estão no carrinho 
        excluded_ids = ','.join([str(product_id) for product_id in selected_product_ids])
        query += f" AND id NOT IN ({excluded_ids})"

    cursor_object.execute(query)
    result = cursor_object.fetchall()
    all_products = []
    for product in result:
        id, name, price, quantity = product
        dict_product = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': quantity
        }
        all_products.append(dict_product)

    if all_products:
        return all_products
    else:
        red("ERRO! Algo deu errado ao tentar selecionar dados.")

# Obtém que o produto que o cliente deseja comprar 
def get_product_to_buy(cursor_object, selected_product_ids):
    clear_screen()
    all_products = select_all_products_out_of_card(cursor_object, selected_product_ids)
    print_all_products(all_products)

    chosen_product = get_user_selected_product(all_products)
    chosen_quantity = get_chosen_product_quantity(chosen_product)
    real_price = chosen_product['price'] + (chosen_product['price'] * 0.3) + (chosen_product['price'] * 0.23) 
    subtotal = real_price * chosen_quantity

    modified_product = {
        "id": chosen_product["id"],
        "name": chosen_product["name"],
        'quantity': chosen_quantity,
        'price': real_price,
        'subtotal': subtotal
    }

    return modified_product

# Calcula a soma de todos os preços, a soma de todos os impostos e o total a partir dos produtos no carrinho
def calculate_prices(card):
    sum_all_prices = 0
    for product in card:
        sum_all_prices += product['subtotal']

    total_iva = sum_all_prices * 0.23
    total_price = sum_all_prices + total_iva

    return sum_all_prices, total_iva, total_price

# Adiciona produtos ao carrinho de compras
def add_products_to_card(cursor_object):
    card = []
    while True:
        selected_product_ids = [product["id"] for product in card]
        product = get_product_to_buy(cursor_object, selected_product_ids)
        card.append(product)

        sum_all_prices, total_iva, total_price = calculate_prices(card)

        clear_screen()
        print_chosen_products(card, sum_all_prices, total_iva, total_price)
        user_yes_no_answer =  get_yes_no_answer("Deseja comprar outro produto? (s/n) ")
        if user_yes_no_answer is None:
            return card, sum_all_prices, total_iva, total_price

# Atualiza a quantidade do produto na base de dados
def update_product_quantity(cursor_object, product_quantity, product_id):
    query = "UPDATE product SET quantity = %s WHERE id = %s"

    try:
        cursor_object.execute(query, (product_quantity, product_id))
    except:
        red(f"Erro ao tentar atualizar quantidade de produto na base de dados")

# Acessa quantidade de determinado produto através do id
def select_product_quantity(cursor_object, product_id):
    query = "SELECT quantity FROM product WHERE id = %s"
    try:
        cursor_object.execute(query,(product_id,))   
        return cursor_object.fetchone()[0]
    except:
        red(f"Erro ao tentar retonar quantidade de produto da base de dados")

# Insere pedido na base de dados 
def insert_order(cursor_object, client_id):
    query = "INSERT INTO user_order (id_user) VALUES (%s)"
    try:
        cursor_object.execute(query, (client_id,))
    except:
        red(f"Erro ao tentar inserir pedido na base de dados")

# Obtém último pedido realizado de um cliente específico
def get_order_id(cursor_object, client_id):
    query = "SELECT MAX(id) FROM user_order WHERE id_user = (%s)"
    try: 
        cursor_object.execute(query, (client_id,))
        return cursor_object.fetchone()[0]
    except:
        red(f"Erro ao tentar selecionar pedido na base de dados")

# Insere venda na Base de dados
def insert_sale(cursor_object, product, user_id, order_id):
    query = "INSERT INTO sale (id_user, id_product, id_order, quantity, price, date) VALUES (%s, %s, %s, %s, %s, %s)"
    date_today = datetime.datetime.now()
    try:
        cursor_object.execute(query, (user_id, product["id"], order_id, product["quantity"], product['subtotal'], date_today))
        return date_today
    except:
        red(f"Erro ao tentar inserir venda na base de dados")

# Processa o método de pagamento do cliente
def process_payment_method(total_price):
    clear_screen()
    display_menu_green(PAYMENT_METHODS, "MÉTODO DE PAGAMENTO")
    get_integer_input("Insira uma opção: ", 1, len(PAYMENT_METHODS))

    time.sleep(1)
    print("...")
    time.sleep(1)

    print(f"O total é: {total_price:.2f}€")

    input("\n(Pressione enter para pagar)")

    clear_screen()
    print("Processando...")
    time.sleep(2)
    clear_screen()

    green("Pago com sucesso!")
    time.sleep(1)

# Processa compra
def process_shopping(cursor_object, user_id):
    card, sum_all_prices, total_iva, total_price = add_products_to_card(cursor_object)

    process_payment_method(total_price)

    insert_order(cursor_object, user_id)
    order_id = get_order_id(cursor_object, user_id)

    for product in card:
        stock_quantity = select_product_quantity(cursor_object, product["id"])
        product_quantity = stock_quantity - product["quantity"]

        insert_sale(cursor_object, product, user_id, order_id)
        update_product_quantity(cursor_object, product_quantity, product["id"])

    print_bill(card, user_id, sum_all_prices, total_iva, total_price, order_id)
    input("\n(Press enter to continue)")

# Verifica se o nome do produto inserido já existe na base de dados
def check_product_name(cursor_object):
    while True:
        product_name = get_product_name()
        query = "SELECT name FROM product WHERE name LIKE (%s)"

        cursor_object.execute(query,(product_name,))  
        result = cursor_object.fetchone()

        if result:
            red("ERRO! Produto inserido já está cadastrado. Tente novamente")
        else:
            return product_name
        
# Pega informações relativamente ao produto
def get_product_info(cursor_object):
    header_cyan("REGISTO DE PRODUTO")
    product_name = check_product_name(cursor_object)
    product_price = get_product_price()
    product_quantity = get_product_quantity()

    return product_name, product_price, product_quantity

# Insere produto na base de dados
def insert_product_db(cursor_object):
    product_name, product_price, product_quantity = get_product_info(cursor_object)

    query = "INSERT INTO product (name, price, quantity) VALUES (%s, %s, %s)"

    try:
        cursor_object.execute(query, (product_name, product_price, product_quantity))
    except:
        red("ERRO! Algo deu errado no registo.")
    finally:
        green(f"\nRegisto do produto '{product_name}' realizado com sucesso!")
        input("\n(Pressione enter para voltar ao menu principal)")

# Seleciona todos os ids dos produtos e retorna em uma lista
def select_all_product_ids(cursor_object):
    product_ids = []
    query = "SELECT id FROM product"
    try:
        cursor_object.execute(query)
        result = cursor_object.fetchall()
        product_ids = [id for tuple_id in result for id in tuple_id] 
        return product_ids
    except:
        red("ERRO! Algo ao tentar selecionar ids de produtos.")

# Obtém todos os ids dos produtos e retorna-os em lista
def get_products_ids(all_products):
    products_ids = []
    for product in all_products:
        products_ids.append(product['id'])

    return products_ids

# Seleciona todos os produtos da base de dados
def select_all_products(cursor_object):
    query = "SELECT id, name, price, quantity FROM product"
    
    cursor_object.execute(query)
    result = cursor_object.fetchall()
    all_products = []
    for product in result:
        id, name, price, quantity = product
        dict_product = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': quantity
        }
        all_products.append(dict_product)

    if all_products:
        return all_products
    else:
        red("ERRO! Algo deu errado ao tentar selecionar dados.")

# Adiciona a quantidade de produto no stock 
def add_to_product_quantity(cursor_object):
    while True:
        clear_screen()
        all_products = select_all_products(cursor_object)
        products_ids = get_products_ids(all_products)

        print_all_product_info(all_products)

        product_id = get_chosen_product_id(products_ids)

        for product in all_products:
            if product["id"] == product_id:
                product_quantity = product["quantity"]

        new_quantity = get_new_product_quantity(product_quantity)

        update_product_quantity(cursor_object, new_quantity, product_id)

        clear_screen()
        green(f"Quantidade do produto com id {product_id} atualizada com suceso!")
        
        user_yes_no_answer =  get_yes_no_answer("\nDeseja atualizar quantidade de outro produto? (s/n) ")
        if user_yes_no_answer is None:
            return
        
# Obtém dados para resgisto de funcionário
def get_employee_registration_info(cursor_object):
    header_cyan("ÁREA DE REGISTO")
    nif = check_nif(cursor_object)
    name = get_name()
    phone = check_phone(cursor_object)
    city = get_city()
    login_name = check_login_name(cursor_object)
    password = get_new_login_password()
    role_code = 2

    return nif, name, phone, city, login_name, password, role_code

# Insere dados de usuário na base de dados
def insert_user_employee_db(cursor_object):
    nif, name, phone, city, login_name, password, role_code = get_employee_registration_info(cursor_object)

    query = "INSERT INTO user (nif, name, phone, city, login_name, password, role_code) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    try:
        cursor_object.execute(query, (nif, name, phone, city, login_name, password, role_code))
    except:
        red("ERRO! Algo deu errado no registo.")
    finally:
        clear_screen()
        print_all_user_info(nif, name, phone, city, login_name, password)
        green("\nRegisto realizado com sucesso!")
        input("\n(Pressione enter para voltar ao menu principal)")

# Lista todos os empregados
def display_employee_list(cursor_object):
    query = "SELECT id, name, nif, phone, city, login_name, password FROM user WHERE role_code = 2"

    try:
        cursor_object.execute(query)
        employees = cursor_object.fetchall()

        if not employees:
            print("Nenhum funcionário encontrado.")
        else:
            print_employee_list(employees)

    except:
        red("ERRO! Algo deu errado ao obter a lista de funcionários.")

# Verifica se o nif de funcionário inserido existe 
def check_nif_exist(cursor_object):
    while True:
        nif = get_nif()
        query = "SELECT nif FROM user WHERE nif LIKE (%s)"

        cursor_object.execute(query,(nif,))  
        result = cursor_object.fetchone()

        if result == None:
            red("ERRO! NIF não existe. Tente novamente.")
        else:
            return nif

# Seleciona o funcionário com determinado NIF
def display_employee_info(cursor_object, nif):
    query_print = "SELECT id, name, nif, phone, city, login_name, password FROM user WHERE nif = %s"

    try:
        cursor_object.execute(query_print, (nif,))
        employee = cursor_object.fetchone()
        if employee:
            print_employee(employee)
            return employee
        else:
            red("ERRO! Funcionário não encontrado.")
    except:
        red("ERRO! Não foi possível obter informações do funcionário.")


# Atualiza dados de funcionário na base de dados
def update_user_employee_db(cursor_object):
    display_employee_list(cursor_object)
    nif = check_nif_exist(cursor_object)

    clear_screen()
    display_employee_info(cursor_object, nif)
    print("ATUALIZAÇÃO DE DADOS:")
    new_name = get_name()
    new_phone = check_phone(cursor_object)
    new_city = get_city()
    new_login = check_login_name(cursor_object)
    new_password = get_new_login_password()

    query_update = "UPDATE user SET name = %s, phone = %s, city = %s, login_name = %s, password = %s WHERE nif = %s AND role_code = 2"

    try:
        cursor_object.execute(query_update, (new_name, new_phone, new_city, new_login, new_password, nif))
        green("\nAtualização realizada com sucesso!")
    finally:
        input("\n(Pressione enter para voltar ao menu principal)")

# Deleta funcionário após mostrar lista e inserir NIF do funcionário que deseja apagar
def remove_user_employee_db(cursor_object):
    display_employee_list(cursor_object)
    nif = check_nif_exist(cursor_object)

    clear_screen()
    display_employee_info(cursor_object, nif)
  
    query = "DELETE FROM user WHERE nif = %s AND role_code = 2"
    
    try:
        cursor_object.execute(query, (nif,))
        green("\nRemoção realizada com sucesso!")
    finally:
        input("\n(Pressione enter para voltar ao menu principal)")

# Retorna total do stock total
def total_stock(cursor_object):
    header_cyan("ESTOQUE TOTAL")
    query = "SELECT SUM(quantity) FROM product"

    try:
        cursor_object.execute(query)
        total_stock_data = cursor_object.fetchone()

        for i in total_stock_data:
            print(f"Total Estoque: {total_stock_data[0]}")

    except Exception as e:
        print(f"ERRO! Não foi possível gerar relatório. Erro: {e}")

    finally:
        input("\n(Pressione enter para voltar ao menu principal)")

# Retorna total do valor de vendas por produto
def sales_by_product(cursor_object):
    header_cyan("TOTAL VENDIDO POR PRODUTO")
    query = """
        SELECT product.id AS product_id, product.name,
        SUM(sale.price * sale.quantity) AS total_sale_product,
        COUNT(sale.quantity) AS total_quantity_sold
        FROM product
        INNER JOIN sale ON product.id = sale.id_product
        GROUP BY product.id, product.name
        ORDER BY total_sale_product DESC
    """

    try:
        cursor_object.execute(query)
        sales_product = cursor_object.fetchall()

        for i in sales_product:
            print(f"ID do Produto: {i[0]}\nProduto: {i[1]}\nTotal Venda: {i[2]:.2f}€\nQuantidade Vendida: {i[3]}\n")

    except:
        print(f"ERRO! Não foi possível gerar relatório.")

    finally:
        input("\n(Pressione enter para voltar ao menu principal)")

# Retorna média de valor por vendas
def average_sale(cursor_object):
    header_cyan("MÉDIA DE VENDAS")
    query = """
        SELECT
            AVG(s.price * s.quantity) AS overall_avg_value_per_sale
        FROM
            sale s"""

    try:
        cursor_object.execute(query)
        avg_product = cursor_object.fetchall()

        for i in avg_product:
            print(f"A média de valor por vendas é: {i[0]:.2f}€")

    except:
        print(f"ERRO! Não foi possível gerar relatório.")

    finally:
        input("\n(Pressione enter para voltar ao menu principal)")

# Estimativa de vendas de cada produto do mês seguinte com base no histórico
def next_month_sale_product(cursor_object):
    header_cyan("ESTIMATIVA DE VENDAS PRÓXIMO MÊS")
    query = """
    SELECT
        p.id,
        p.name,
        DATE_FORMAT(s.date, '%Y-%m') AS sale_month,
        SUM(s.price * s.quantity) AS total_sale_product,
        COUNT(s.quantity) AS total_quantity_sold
    FROM
        sale s
    JOIN
        product p ON s.id_product = p.id
    GROUP BY
        p.id, p.name, sale_month
    ORDER BY
        sale_month DESC, p.id
    """

    cursor_object.execute(query)
    results = cursor_object.fetchall()

    df = pd.DataFrame(results, columns=['id', 'name', 'sale_month', 'total_sale_product', 'total_quantity_sold'])

    unique_products = df['id'].unique()

    for product_id in unique_products:
        product_data = df[df['id'] == product_id]
        X_v = product_data[['total_quantity_sold']]
        y_v = product_data['total_sale_product']

        model = LinearRegression()
        model.fit(X_v, y_v)

        X_v.columns = ['total_quantity_sold']

        y_next_month_pred = model.predict(X_v)

        print(f"{product_data['name'].iloc[0]} (ID: {product_id}): {y_next_month_pred[0]:.2f}€")

# Estimativa de vendas total do mês seguinte com base no histórico
def next_month_sale(cursor_object):
    query = """
    SELECT 
        DATE_FORMAT(sale.date, '%Y-%m') AS sale_month,
        SUM(sale.price * sale.quantity) AS total_sale_product, 
        COUNT(sale.quantity) AS total_quantity_sold 
    FROM 
        sale
    GROUP BY 
        sale_month 
    ORDER BY 
        sale_month DESC;
    """
 
    cursor_object.execute(query)
    results = cursor_object.fetchall()

    df = pd.DataFrame(results, columns=['sale_month', 'total_sale_product', 'total_quantity_sold'])
    X_v = df[['total_quantity_sold']]
    y_v = df['total_sale_product']

    model = LinearRegression()
    model.fit(X_v, y_v)

    y_next_month_pred = model.predict(X_v)

    print(f"\nTotal previsto para próximo mês: {y_next_month_pred[0]:.2f}€")
    input("\n(Pressione enter para voltar atrás)")

# Gráfico de Dispersão Vendas por Quantidade de Produto Vendido
def print_scatter_sales_quantity(cursor_object):
    query = """
        SELECT product.id AS product_id, product.name,
        SUM(sale.price * sale.quantity) AS total_sale_product,
        COUNT(sale.quantity) AS total_quantity_sold
        FROM product
        INNER JOIN sale ON product.id = sale.id_product
        GROUP BY product.id, product.name
        ORDER BY total_sale_product DESC
    """

    quantities = []
    sales = []
    
    cursor_object.execute(query)
    results = cursor_object.fetchall()

    for row in results:
        quantities.append(row[3])  
        sales.append(row[2])
    

    plt.figure(figsize=(8, 6))
    plt.scatter(quantities, sales, color='blue', alpha=0.7)
    plt.title('Vendas em relação à Quantidade de Produtos Vendidos')
    plt.xlabel('Quantidade Vendida')
    plt.ylabel('Vendas')
    plt.show()