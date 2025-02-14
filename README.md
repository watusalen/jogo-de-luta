# Jogo de Luta de Personagens

## Descrição do Projeto

Este projeto simula uma arena onde personagens (representados como threads) lutam entre si até que reste apenas um vencedor. Cada personagem é uma thread independente que realiza ataques aleatórios contra outros personagens. O jogo continua até que apenas um personagem permaneça com vida.

## Estrutura do Projeto

O projeto é composto por duas classes principais:

1. **Arena**: Gerencia a batalha entre os personagens, exibe o status da batalha e controla o fluxo do jogo.
2. **Personagem**: Representa um personagem na arena, capaz de atacar outros personagens e ser atacado.

### Classe `Arena`

A classe `Arena` é responsável por:

- Inicializar os personagens.
- Gerenciar o estado da batalha.
- Exibir o status dos personagens e o log de ações.
- Controlar o início e o término da batalha.

#### Métodos Principais

- **`__init__(self, nomes)`**: Inicializa a arena com uma lista de nomes de personagens.
- **`registrar_acao(self, acao)`**: Registra uma ação no log da arena.
- **`exibir_estado(self)`**: Exibe o status dos personagens e o log de ações no terminal.
- **`iniciar_batalha(self)`**: Inicia a batalha entre os personagens.

### Classe `Personagem`

A classe `Personagem` é uma subclasse de `threading.Thread` e representa um personagem na arena. Cada personagem:

- Possui um nome e uma quantidade de vida.
- Pode atacar outros personagens.
- É executado em uma thread separada.

#### Métodos Principais

- **`__init__(self, nome, vida, arena)`**: Inicializa o personagem com nome, vida e referência à arena.
- **`atacar(self)`**: Realiza um ataque aleatório contra outro personagem.
- **`run(self)`**: Método principal da thread, onde o personagem realiza ataques enquanto estiver vivo e o jogo estiver ativo.

## Regras do Jogo

1. **Inicialização**: Cada personagem começa com 100 pontos de vida.
2. **Ataques**: Em cada rodada, os personagens escolhem aleatoriamente um oponente para atacar, causando um dano entre 5 e 20 pontos.
3. **Eliminação**: Se a vida de um personagem chegar a zero, ele é eliminado da batalha.
4. **Vencedor**: O último personagem com vida restante é declarado o vencedor.

## Exemplo de Uso

```python
# Exemplo de como iniciar uma batalha com 4 personagens
nomes_personagens = ["Guerreiro", "Mago", "Arqueiro", "Assassino"]
arena = Arena(nomes_personagens)
arena.iniciar_batalha()
```

```sh
python main.py
```

# Requisitos
- Python 3.x
- Biblioteca `rich` para exibição formatada no terminal.

## Instalação
Para instalar a biblioteca `rich`, execute o seguinte comando:

```bash
pip install rich
```

## Execução
Para executar o jogo, basta rodar o script Python que contém as classes `Arena` e `Personagem`.  
O jogo será exibido no terminal, mostrando o status dos personagens e as ações realizadas durante a batalha.

## Recursos e Funcionalidades

- **Multithreading** para execução simultânea dos personagens.  
- **Atualização em tempo real** do status no terminal.  
- **Sistema de combate aleatório** com variação de dano.  
- **Exibição visual** da vida dos personagens usando `rich`. 

## Conclusão
Este projeto é uma excelente maneira de praticar conceitos de programação concorrente e manipulação de threads em Python.  
Ele demonstra como threads podem ser usadas para simular interações complexas entre múltiplos agentes em um ambiente controlado.

---

**Autor:** Cairon Ferreira Prado, Cícero Andrade Santos e Matusalen Costa Alves 
**Disciplina:** Sistemas Operacionais  
**Professor:** Maykol Sampaio  
**Data:** 14/02/2025