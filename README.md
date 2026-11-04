# Pilha Encadeada com UNDO/REDO e Sockets TCP

Projeto acadêmico desenvolvido em **Python** para a disciplina de **Estrutura de Dados I**.

## Objetivo

Implementar uma **pilha encadeada** e demonstrar suas operações fundamentais, aplicando o princípio **LIFO** (*Last In, First Out*): o último elemento inserido é o primeiro a ser removido.

Além das operações básicas, o projeto implementa **UNDO** (desfazer) e **REDO** (refazer), usando outras duas pilhas encadeadas, e estabelece a comunicação entre dois programas por meio de **Sockets TCP**.

> **O foco do trabalho é a estrutura de dados PILHA.** O Socket TCP permite a comunicação entre cliente e servidor, enquanto UNDO e REDO demonstram uma aplicação prática de pilhas.

## Como a pilha foi implementada

A implementação **não utiliza listas nativas do Python como pilhas**. Cada nó é representado por um dicionário com:

- `value`: dado armazenado no nó (palavra ou registro de operação);
- `next`: referência ao próximo nó, em direção à base da pilha.

Cada pilha mantém também:

- `top`: referência ao nó do topo;
- `size`: quantidade de elementos.

As funções `initialize_node()`, `initialize_stack()`, `push()`, `pop()` e `is_empty()` são reutilizadas nas três pilhas.

### As três pilhas encadeadas

| Pilha | Finalidade |
| --- | --- |
| `pilha` | Armazena as palavras inseridas pelo usuário. |
| `historico` | Registra as operações `PUSH` e `POP` realizadas. |
| `refazer` | Guarda operações desfeitas que podem ser refeitas. |

As três são criadas com `initialize_stack()`. Os históricos armazenam registros como `("PUSH", "ola")`, usando os mesmos nós encadeados da pilha principal.

## Funcionalidades

| Comando | O que faz |
| --- | --- |
| `PUSH` | Insere uma palavra no topo da pilha. |
| `POP` | Remove a palavra do topo. |
| `UNDO` | Desfaz a última inserção ou remoção. |
| `REDO` | Refaz a última operação desfeita. |
| `LISTAR` | Exibe os elementos do topo para a base. |
| `IS_EMPTY` | Informa se a pilha está vazia (`True` ou `False`). |
| `PRINT_SIZE` | Exibe a quantidade de elementos. |
| `SAIR` | Encerra o programa cliente. |

### Como funcionam UNDO e REDO?

Quando ocorre um `PUSH` ou `POP`, o servidor registra a operação em `historico` por meio de `push(historico, ...)`.

- **UNDO:** retira a última operação de `historico` com `pop(historico)`, executa sua ação inversa e a guarda em `refazer`.
- **REDO:** retira a última operação de `refazer`, executa-a novamente e a devolve para `historico`.
- **Nova alteração:** um novo `PUSH` ou `POP` executa `clear(refazer)`, invalidando a sequência anterior de refazer.

A função `clear()` esvazia uma pilha, definindo `top` como `None` e `size` como `0`.

## Comunicação cliente-servidor

O projeto contém dois arquivos Python:

- **`Servidor.py`**: mantém as três pilhas na memória, interpreta os comandos e executa as operações.
- **`Cliente.py`**: apresenta o menu, recebe os comandos do usuário e exibe as respostas do servidor.

A comunicação utiliza **TCP** (`socket.AF_INET` e `socket.SOCK_STREAM`) com:

- **Endereço IP:** `127.0.0.1` (o próprio computador);
- **Porta:** `2567`.

Fluxo simplificado:

```text
Usuário → Cliente.py → Socket TCP → Servidor.py
                                      ↓
                               Operação na pilha
                                      ↓
Usuário ← Cliente.py ← Socket TCP ← Resposta
```

## Requisitos

- Python 3 instalado;
- Terminal ou Prompt de Comando (CMD) do Windows;
- Os arquivos `Servidor.py` e `Cliente.py` na mesma pasta.

Não é necessário instalar bibliotecas externas: o projeto usa o módulo `socket`, incluído no Python.

## Como executar

Abra **dois terminais** na pasta do projeto. No Windows, é possível abrir a pasta no Explorador de Arquivos, digitar `cmd` na barra de endereço e pressionar Enter.

**Terminal 1 — iniciar o servidor:**

```bash
py Servidor.py
```

Mensagem esperada:

```text
Servidor iniciado na porta 2567!
Aguardando comandos do cliente...
```

**Terminal 2 — iniciar o cliente:**

```bash
py Cliente.py
```

O menu aparecerá no cliente. Digite os comandos por ele; não é necessário digitar operações no terminal do servidor.

> Em sistemas onde o comando `py` não está disponível, utilize `python Servidor.py` e `python Cliente.py`.

## Exemplo de utilização

Com o servidor recém-iniciado:

```text
Comando: PUSH
Digite a palavra: ola
Resultado: 'ola' inserida!

Comando: PUSH
Digite a palavra: mundo
Resultado: 'mundo' inserida!

Comando: LISTAR
Resultado: mundo -> ola

Comando: UNDO
Resultado: UNDO: 'mundo' removida

Comando: LISTAR
Resultado: ola

Comando: REDO
Resultado: REDO: 'mundo' inserida novamente

Comando: PRINT_SIZE
Resultado: 2
```

## Organização do repositório

```text
pilha-undo-redo/
├── Cliente.py
├── Servidor.py
├── README.md
└── LICENSE
```

## Limitações e possibilidades de melhoria

- Os dados permanecem **somente na memória** e são perdidos quando o servidor é encerrado.
- O servidor atende **uma conexão por vez**.
- O endereço `127.0.0.1` permite a comunicação local, no mesmo computador.
- Uma evolução possível seria adicionar persistência em arquivo, tratamento de falhas de conexão e atendimento simultâneo de clientes.

## Conclusão

O projeto demonstra o funcionamento de uma **pilha encadeada**, suas operações LIFO e sua reutilização em **três estruturas independentes**: a pilha de dados, a pilha de histórico e a pilha de refazer. A comunicação por Socket TCP permite executar essas operações a partir de um programa cliente separado.
