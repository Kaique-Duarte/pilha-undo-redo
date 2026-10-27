
import socket


# Envia um comando para o servidor
def execute_remote(comando):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente.connect(("127.0.0.1", 2567))
    cliente.sendall(comando.encode())

    resposta = cliente.recv(1024).decode()
    cliente.close()

    return resposta


# Permite digitar os comandos
while True:
    comando = input("Digite POP, is_empty, PRINT_SIZE ou SAIR: ")

    if comando.upper() == "SAIR":
        break

    resultado = execute_remote(comando)
    print("Resultado:", resultado)
