from menu_utils import red

# Obtém nome de usuário válido
def get_login(): 
    while True:
        user_login = input("Nome de utilizador: ")
        if user_login.strip():
            return user_login
        else:
            red("Erro! Campo deve ser preenchido")

# Obtém palavra-passe válida
def get_password():
    while True:
        user_password = input("Palavra-passe: ")
        if user_password.strip():
            return user_password
        else:
            red("Erro! Campo deve ser preenchido")

# Obtém resposta válida de sim ou não do usuário
def get_yes_no_answer(input_msg):
    while True:
        user_input = input(input_msg)
        if user_input.lower() in ['s', 'sim']:
            return user_input
        elif user_input.lower() in ['n', 'não', 'nao']:
            break
        else:
            red("Erro! Por favor, insira uma resposta válida.")


# Obtém valor de NIF válido 
def get_nif():
    while True:
        try:
            nif = int(input("NIF: "))
        except (ValueError, TypeError):
            red("ERRO! Insira NIF válido.")
        else: 
            if len(str(nif)) != 9:
                red("ERRO! Insira um NIF válido (mínimo 9 dígitos).")
            else:
                return nif

# Obtém nome válido
def get_name():
    while True:
        full_name = input("Primeiro e último nome: ").strip()
        names = full_name.split()
        if len(names) != 2:
            red("Erro! Digite exatamete o primeiro e o último nome.")
        elif len(names[0]) < 4  or len(names[1]) < 4:
            red("Erro! Por favor, digite um nome válido")
        elif not all(name.isalpha() for name in names):
            red("Erro! Nome não pode conter números ou caracteres especiais.")
        else:
            break

    return full_name.title()

# Obtém número de telefone válido
def get_phone():
    while True:
        try:
            phone_number = int(input("Telemóvel: "))
        except (ValueError, TypeError):
            red("ERRO! Insira número válido.")
        else: 
            if len(str(phone_number)) != 9:
                red("ERRO! Insira um número de telemóvel válido (9 dígitos).")
            else:
                return f"{str(phone_number)[:3]} {str(phone_number)[3:6]} {str(phone_number)[6:]}"

# Obtém nome de cidade válido
def get_city():
    while True:
        city_name = input("Localidade: ")
        if city_name.strip():
            return city_name.title()
        elif len(city_name) < 3:
            red("Erro! Por favor, digite um nome de cidade válido.")
        else:
            red("Erro! Campo deve ser preenchido.")

# Obtem nome de usuário válido
def get_new_login_name():
    while True:
        login_name = input("Nome de usuário: ")
        if login_name.split() == 0:
            red("Erro! Campo deve ser preenchido.")
        elif " " in login_name:
            red("Erro! Nome não deve conter espaços.")
        elif len(login_name) <  4:
            red("Erro! Por favor, insira um nome com o mínimo de 4 caracteres.")
        else:
            return login_name

# Obtém palavra passe válida
def get_new_login_password():
    while True:
        password = input("Palavra-passe: ")
        if password.split() == 0:
            red("Erro! Campo deve ser preenchido.")
        elif " " in password:
            red("Erro! Palavra-passe não deve conter espaços.")
        elif len(password) <  5:
            red("Erro! Por favor, insira uma palavra-passe com o mínimo de 5 caracteres.")
        else:
            return password

# Obtém nome de produto válido que o usuário deseja comprar
def get_user_selected_product(all_products):
    while True:
        product_name = input("Insira o nome do produto que deseja comprar: ")
        for product in all_products:
            if product_name.lower() == product['name'].lower():
                return product
        red("Erro! Por favor digite um nome de produto válido.")

# Obtém quantidade válida que o usuário deseja do produto
def get_chosen_product_quantity(product):
    while True:
        try: 
            product_quantity = int(input("Quantidade: "))
        except (ValueError, TypeError):
            red("ERRO! Insira quantidade válida.")
        else: 
            print(product)
            if product_quantity < 1 or product_quantity > product["quantity"]:
                red("ERRO! Quantidade inválida.")
            else:
                return product_quantity

# Obtém nome de produto válido
def get_product_name():
    while True:
        product_name = input("Insira o nome do produto: ")
        if (product_name.strip() and len(product_name) > 3):
            return product_name.title()
        else:
            red("ERRO! Por favor, digite um nome de produto válido.")
    
# Obtém preço de produto válido
def get_product_price():
    while True:
        try:
            product_price = float(input("Preço: "))
        except (ValueError, TypeError):
            red("ERRO! Insira preço válido.")
        else: 
            if product_price < 1 or product_price > 50000:
                red("ERRO! Insira um preço válido.")
            else:
                return product_price
        
# Obtém quantidade de produto válida
def get_product_quantity():
    while True:
        try:
            product_quantity = int(input("Quantidade: "))
        except (ValueError, TypeError):
            red("ERRO! Insira uma quantidade válida.")
        else: 
            if product_quantity < 1 or product_quantity > 5000:
                red("ERRO! Insira uma quantidade válida.")
            else:
                return product_quantity
            
# Obtém um id válido de produto
def get_chosen_product_id(products_ids):
    while True:
        try:
            product_id = int(input("Insira o id do produto: "))
        except (ValueError, TypeError):
            red("ERRO! Insira uma id válido.")
        else:
            if product_id in products_ids:
                return product_id
            else:
                red("ERRO! Id de produto não existe")

# Obtém nova quantidade de produto 
def get_new_product_quantity(product_quantity):
    while True:
        try: 
            add_to_quantity = int(input(f"Quantas unidades deseja adicionar ao stock: "))
        except (ValueError, TypeError):
            red("ERRO! Insira quantidade válida.")
        else: 
            if add_to_quantity < 1 or add_to_quantity > 100:
                red("ERRO! Por favor insira quantidade acima de 0.")
            else:
                return product_quantity + add_to_quantity
            
