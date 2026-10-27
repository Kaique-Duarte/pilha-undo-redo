
import socket

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


# Verifica se está vazia
def is_empty(stack):
    return stack['top'] is None


# Insere na pilha
def push(stack, value):
    new_node = initialize_node(value)
    new_node['next'] = stack['top']
    stack['top'] = new_node
    stack['size'] += 1


# Remove da pilha
def pop(stack):
    if is_empty(stack):
        return "Pilha vazia"

    removed_node = stack['top']
    stack['top'] = removed_node['next']
    stack['size'] -= 1

    return removed_node['value']


# Cria a pilha e os históricos
pilha = initialize_stack()
historico = []
refazer = []


# Desfaz a última ação
def undo():
    if not historico:
        return "Nenhuma acao para desfazer"

    acao, palavra = historico.pop()

    if acao == "PUSH":
        pop(pilha)
        resposta = f"UNDO: '{palavra}' removida"

    else:
        push(pilha, palavra)
        resposta = f"UNDO: '{palavra}' recuperada"

    refazer.append((acao, palavra))
    return resposta


# Refaz a última ação desfeita
def redo():
    if not refazer:
        return "Nenhuma acao para refazer"

    acao, palavra = refazer.pop()

    if acao == "PUSH":
        push(pilha, palavra)
        resposta = f"REDO: '{palavra}' inserida novamente"

    else:
        pop(pilha)
        resposta = f"REDO: '{palavra}' removida novamente"

    historico.append((acao, palavra))
    return resposta


# Lista os elementos
def listar():
    elementos = []
    atual = pilha['top']

    while atual is not None:
        elementos.append(str(atual['value']))
        atual = atual['next']

    if elementos:
        return " -> ".join(elementos)

    return "Pilha vazia"


# Executa os comandos recebidos
def executar_comando(requisicao):
    partes = requisicao.strip().split(" ", 1)
    comando = partes[0].upper()

    if comando == "PUSH":
        if len(partes) < 2 or not partes[1].strip():
            return "Digite uma palavra"

        palavra = partes[1].strip()
        push(pilha, palavra)
        historico.append(("PUSH", palavra))
        refazer.clear()
        return f"'{palavra}' inserida!"

    elif comando == "POP":
        if is_empty(pilha):
            return "Pilha vazia"

        palavra = pop(pilha)
        historico.append(("POP", palavra))
        refazer.clear()
        return f"'{palavra}' removida!"

    elif comando == "UNDO":
        return undo()

    elif comando == "REDO":
        return redo()

    elif comando == "LISTAR":
        return listar()

    elif comando == "IS_EMPTY":
        return str(is_empty(pilha))

    elif comando == "PRINT_SIZE":
        return str(pilha['size'])

    else:
        return "Comando invalido"


# Inicia o servidor Socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("127.0.0.1", 2567))
servidor.listen()

print("Servidor iniciado na porta 2567!")
print("Aguardando comandos do cliente...")

while True:
    conexao, endereco = servidor.accept()

    with conexao:
        comando = conexao.recv(1024).decode()
        resposta = executar_comando(comando)
        conexao.sendall(resposta.encode())
