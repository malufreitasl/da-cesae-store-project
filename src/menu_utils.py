import os

# Imprime linhas 
def line(size=42):
    return "-" * size

# Imprime linhas e um texto centralizado
def print_menu_header(txt):
    print(line()) 
    print(txt.center(40))
    print(line())

# Imprime linhas e um texto centralizado roxo
def print_menu_header_blue(txt):
    print(line()) 
    print("\033[0;34m{}\033[0m".format(txt.center(40)))
    print(line())

# Imprime linhas e um texto centralizado roxo
def print_menu_header_purple(txt):
    print(line()) 
    print("\033[0;35m{}\033[0m".format(txt.center(40)))
    print(line())

# Imprime linhas e um texto centralizado em verde
def print_menu_header_green(txt):
    print(line())  
    print("\033[0;32m{}\033[0m".format(txt.center(40)))  
    print(line()) 

# Imprime linhas e um texto centralizado em ciano
def header_cyan(txt):
    print(line())  
    print("\033[1;36m {}\033[0m".format(txt.center(40)))  
    print(line()) 

# Função para imprimir texto em vermelho
def red(txt):
    print("\033[0;31m{}\033[0m".format(txt)) 

# Função para imprimir texto em verde
def green(txt):
    print("\033[0;32m{}\033[0m".format(txt))  

# Imprime menu
def display_menu(menu_name, title):
    print_menu_header(title)
    i = 1
    for item in menu_name:
        print(f"({i}) {item}")
        i += 1
    print(line())

# Imprime menu com título em roxo
def display_menu_blue(menu_name, title):
    print_menu_header_blue(title)
    i = 1
    for item in menu_name:
        print(f"({i}) {item}")
        i += 1
    print(line())
    
# Imprime menu com título em roxo
def display_menu_purple(menu_name, title):
    print_menu_header_purple(title)
    i = 1
    for item in menu_name:
        print(f"({i}) {item}")
        i += 1
    print(line())

# Imprime menu com título em verde
def display_menu_green(menu_name, title):
    print_menu_header_green(title)
    i = 1
    for item in menu_name:
        print(f"({i}) {item}")
        i += 1
    print(line())


# Obtém valor inteiro válido de usuário
def get_integer_input(input_msg, min_val, max_val):
    while(True):
        try:
            userInput = int(input(input_msg))
        except (ValueError, TypeError):
            red("ERRO! Insira uma opção válida")
        else: 
            if userInput < min_val or userInput > max_val:
                red("ERRO! Opção não existe")
            else:
                return userInput

# Limpa a linha de comando
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 