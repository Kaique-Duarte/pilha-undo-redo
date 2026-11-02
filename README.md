# Pilha Encadeada com UNDO/REDO e Sockets TCP

Projeto desenvolvido para a disciplina de **Estrutura de Dados I**, utilizando **Python**.

## Objetivo

Implementar uma **pilha encadeada** e demonstrar suas operações fundamentais, aplicando o princípio **LIFO (Last In, First Out)**: o último elemento inserido é o primeiro a ser removido.

Além das operações básicas, o projeto permite **desfazer (UNDO)** e **refazer (REDO)** alterações e utiliza **Sockets TCP** para a comunicação entre dois programas: um cliente e um servidor.

> **A estrutura principal do trabalho é a pilha encadeada.** A comunicação TCP é o meio de interação entre os programas; UNDO e REDO são funcionalidades adicionais.

## Como a pilha funciona

Cada elemento é representado por um nó com dois campos:

- `value`: armazena a palavra;
- `next`: aponta para o próximo nó da pilha.

A pilha mantém uma referência ao topo (`top`) e a quantidade de elementos (`size`). As inserções e remoções ocorrem **sempre pelo topo**.

Exemplo:

```text
PUSH A       A
PUSH B       B -> A
PUSH C       C -> B -> A
POP          B -> A       (remove C)
```

## Funcionalidades

| Comando | O que faz |
| --- | --- |
| `PUSH` | Insere uma palavra no topo da pilha. |
| `POP` | Remove e retorna a palavra do topo. |
| `LISTAR` | Mostra os elementos do topo até a base. |
| `IS_EMPTY` | Informa se a pilha está vazia (`True` ou `False`). |
| `PRINT_SIZE` | Mostra a quantidade de elementos. |
| `UNDO` | Desfaz a última inserção ou remoção. |
| `REDO` | Refaz a última ação desfeita. |
| `SAIR` | Encerra o programa cliente. |

O servidor utiliza duas listas auxiliares, `historico` e `refazer`, para registrar as operações de UNDO e REDO. **A pilha principal, porém, é implementada com nós encadeados**, e não com uma lista pronta do Python.

## Organização dos arquivos

```text
pilha-undo-redo/
├── Servidor.py    # Implementação da pilha, histórico e servidor TCP
├── Cliente.py     # Menu interativo e envio dos comandos
└── README.md      # Documentação do projeto
```

## Comunicação TCP/IP

O cliente envia os comandos ao servidor por meio de **Sockets TCP**.

- **IP:** `127.0.0.1` — endereço de loopback, que representa o próprio computador.
- **Porta:** `2567` — porta na qual o servidor aguarda conexões.
- **Protocolo:** TCP (`socket.SOCK_STREAM`).

Fluxo de uma operação:

```text
Usuário digita um comando no Cliente.py
                 |
                 v
     Cliente envia via TCP
       127.0.0.1:2567
                 |
                 v
Servidor recebe e executa na pilha
                 |
                 v
Servidor devolve a resposta via TCP
                 |
                 v
    Cliente mostra o resultado
```

O cliente e o servidor podem ser executados **no mesmo computador**, em dois terminais separados.

## Requisitos

- **Python 3** instalado;
- Windows, Linux ou macOS;
- Terminal (CMD, PowerShell ou equivalente).

**Não é necessário instalar bibliotecas externas.** O módulo `socket` já faz parte da biblioteca padrão do Python.

## Como executar

1. Baixe ou clone o repositório e abra a pasta que contém `Servidor.py` e `Cliente.py`.
2. Abra um terminal nessa pasta e inicie o servidor:

   ```bash
   python Servidor.py
   ```

   No Windows, você também pode usar `py Servidor.py`.

   A mensagem esperada é:

   ```text
   Servidor iniciado na porta 2567!
   Aguardando comandos do cliente...
   ```

3. **Mantenha o servidor aberto.** Abra um **segundo terminal**, na mesma pasta, e execute:

   ```bash
   python Cliente.py
   ```

   No Windows, também é possível usar `py Cliente.py`.

4. Digite os comandos no menu do cliente. Para `PUSH`, o programa solicitará a palavra a inserir.

> **Importante:** inicie o servidor **antes** do cliente. O servidor precisa continuar aberto enquanto os comandos são executados.

## Exemplo de utilização

No menu do cliente, faça a sequência abaixo:

| Ação no cliente | Resultado esperado |
| --- | --- |
| `PUSH` e palavra `ola` | `'ola' inserida!` |
| `PUSH` e palavra `mundo` | `'mundo' inserida!` |
| `LISTAR` | `mundo -> ola` |
| `PRINT_SIZE` | `2` |
| `POP` | `'mundo' removida!` |
| `UNDO` | `UNDO: 'mundo' recuperada` |
| `LISTAR` | `mundo -> ola` |
| `REDO` | `REDO: 'mundo' removida novamente` |
| `IS_EMPTY` | `False` |

**Como funcionam UNDO e REDO?**

- Se a última ação foi um `PUSH`, `UNDO` remove o elemento inserido.
- Se a última ação foi um `POP`, `UNDO` reinsere o elemento removido.
- `REDO` reaplica a última ação desfeita.
- Um novo `PUSH` ou `POP` limpa a possibilidade de refazer ações anteriores.

## Limitações desta versão

- Os dados ficam **somente na memória**: ao reiniciar o servidor, a pilha e os históricos são reiniciados.
- O servidor processa **uma conexão por vez**.
- A comunicação foi configurada para execução **local** (`127.0.0.1`).
- Se o servidor não estiver em execução, o cliente não conseguirá estabelecer a conexão.

## Conceitos aplicados

**Estruturas de dados:** pilha, nós encadeados, LIFO, inserção e remoção pelo topo.

**Programação:** funções, dicionários, listas auxiliares, estruturas condicionais e de repetição.

**Redes:** arquitetura cliente-servidor, Socket TCP, endereço IP e porta.

---

**Disciplina:** Estrutura de Dados I  
**Linguagem:** Python  
**Projeto acadêmico desenvolvido em grupo.**
