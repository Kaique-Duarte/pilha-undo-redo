import socket
import threading

# Cria um nó da pilha
def initialize_node(value):
    return {
        'value': value,
        'next': None
    }


# Cria uma pilha vazia
def initialize_stack():
    return {
        'top': None,
        'size': 0
    }


# Verifica se a pilha está vazia
def is_empty(stack):
    return stack['top'] is None


# Insere um elemento no topo da pilha
def push(stack, value):
    new_node = initialize_node(value)
    new_node['next'] = stack['top']
    stack['top'] = new_node
    stack['size'] += 1


# Remove o elemento do topo
def pop(stack):
    if is_empty(stack):
        return "erro: stack is empty"

    removed_node = stack['top']
    stack['top'] = removed_node['next']
    stack['size'] -= 1

    return removed_node['value']


# Cria a pilha
pilha = initialize_stack()


# Recebe os comandos do cliente
def receber_comandos():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("127.0.0.1", 2567))
    servidor.listen()

    print("Servidor iniciado na porta 2567!")

    while True:
        conexao, endereco = servidor.accept()

        with conexao:
            comando = conexao.recv(1024).decode().strip().upper()

            if comando == "POP":
                resposta = pop(pilha)

            elif comando == "IS_EMPTY":
                resposta = str(is_empty(pilha))

            elif comando == "PRINT_SIZE":
                resposta = str(pilha['size'])

            else:
                resposta = "Comando invalido"

            conexao.sendall(resposta.encode())


# Inicia o Socket em uma thread
threading.Thread(target=receber_comandos, daemon=True).start()


# Permite inserir palavras na pilha
while True:
    palavra = input("Digite uma palavra para PUSH: ")
    push(pilha, palavra)
    print("Palavra inserida!")

