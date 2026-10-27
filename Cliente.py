import socket


# Envia comandos para o servidor
def execute_remote(comando):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente.connect(("127.0.0.1", 2567))
    cliente.sendall(comando.encode())

    resposta = cliente.recv(1024).decode()
    cliente.close()

    return resposta


# Menu do cliente
while True:
    print("\n===== MENU DA PILHA =====")
    print("PUSH - Inserir palavra")
    print("POP - Remover palavra")
    print("UNDO - Desfazer ultima acao")
    print("REDO - Refazer ultima acao")
    print("LISTAR - Mostrar pilha")
    print("IS_EMPTY - Verificar se esta vazia")
    print("PRINT_SIZE - Mostrar tamanho")
    print("SAIR - Encerrar")

    comando = input("\nDigite um comando: ").strip().upper()

    if comando == "SAIR":
        print("Cliente encerrado!")
        break

    if comando == "PUSH":
        palavra = input("Digite a palavra: ")

        if not palavra.strip():
            print("Digite uma palavra valida!")
            continue

        comando = "PUSH " + palavra

    resultado = execute_remote(comando)
    print("\nResultado:", resultado)
