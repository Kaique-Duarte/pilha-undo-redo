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


# Esvazia uma pilha
def clear(stack):
    stack['top'] = None
    stack['size'] = 0


# Cria a pilha principal e as pilhas de histórico (undo/redo)
pilha = initialize_stack()
historico = initialize_stack()
refazer = initialize_stack()


# Desfaz a última ação
def undo():
    if is_empty(historico):
        return "Nenhuma acao para desfazer"

    acao, palavra = pop(historico)

    if acao == "PUSH":
        pop(pilha)
        resposta = f"UNDO: '{palavra}' removida"
    else:
        push(pilha, palavra)
        resposta = f"UNDO: '{palavra}' recuperada"

    push(refazer, (acao, palavra))
    return resposta


# Refaz a última ação desfeita
def redo():
    if is_empty(refazer):
        return "Nenhuma acao para refazer"

    acao, palavra = pop(refazer)

    if acao == "PUSH":
        push(pilha, palavra)
        resposta = f"REDO: '{palavra}' inserida novamente"
    else:
        pop(pilha)
        resposta = f"REDO: '{palavra}' removida novamente"

    push(historico, (acao, palavra))
    return resposta


# Lista os elementos (topo -> base)
def listar():
    atual = pilha['top']

    if atual is None:
        return "Pilha vazia"

    resultado = str(atual['value'])
    atual = atual['next']

    while atual is not None:
        resultado += " -> " + str(atual['value'])
        atual = atual['next']

    return resultado


# Executa os comandos recebidos
def executar_comando(requisicao):
    partes = requisicao.strip().split(" ", 1)
    comando = partes[0].upper()

    if comando == "PUSH":
        if len(partes) < 2 or not partes[1].strip():
            return "Digite uma palavra"

        palavra = partes[1].strip()
        push(pilha, palavra)
        push(historico, ("PUSH", palavra))
        clear(refazer)
        return f"'{palavra}' inserida!"

    elif comando == "POP":
        if is_empty(pilha):
            return "Pilha vazia"

        palavra = pop(pilha)
        push(historico, ("POP", palavra))
        clear(refazer)
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