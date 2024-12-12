# *Ping Pong Game com Pygame*

Este projeto é um jogo simples de Ping Pong desenvolvido em Python utilizando a biblioteca Pygame. Ele implementa um sistema de entrada adaptável, utiliza padrões de design como Facade e possui elementos básicos de física e lógica de jogo.

---

## Requisitos do Sistema

Antes de começar, certifique-se de que seu ambiente atenda aos seguintes requisitos:

- **Python 3.7 ou superior**
- **Biblioteca Pygame**

---

## Configuração do Ambiente

### 1. Instalar o Python
Certifique-se de que você tem o Python instalado em seu sistema. Para verificar, execute:
```bash
python --version
```
Se o Python não estiver instalado, faça o download e a instalação a partir do site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/).

### 2. Instalar o Pygame
Instale o Pygame usando o pip. Execute o comando abaixo no terminal:
```bash
pip install pygame
```

---

## Execução do Jogo

### 1. Clonar o Repositório
Clone este repositório em sua máquina local:
```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

### 2. Executar o Jogo
No diretório do projeto, execute o arquivo Python principal:
```bash
python <NOME_DO_ARQUIVO>.py
```

---

## Estrutura do Código

### 1. **Inicialização do Jogo**
- O jogo é inicializado configurando a janela, dimensões, cores e outras variáveis importantes.
- As dimensões da tela são definidas como 800x600 pixels.

### 2. **Raquetes e Bola**
- Raquetes:
  - Cada jogador controla uma raquete com dimensões de 10x100 pixels.
  - A raquete esquerda é controlada pelas teclas `W` (cima) e `S` (baixo).
  - A raquete direita é controlada pelas setas `↑` (cima) e `↓` (baixo).
- Bola:
  - A bola se movimenta pela tela e muda de direção ao colidir com paredes ou raquetes.

### 3. **Pontuação**
- Pontos são adicionados quando a bola ultrapassa uma das bordas horizontais da tela.
- O placar é exibido no topo da tela.

### 4. **Adapter para Entrada**
- Um `InputAdapter` é usado para mapear as teclas de entrada de forma flexível.

### 5. **Facade para Gerenciamento**
- A classe `PingPongFacade` gerencia os movimentos, colisões, reinício da bola e desenho da interface do jogo.

### 6. **Loop Principal**
- O jogo roda continuamente, processando eventos, movimentando os objetos e desenhando a tela até que o usuário feche a janela.

---

## Controles

| Ação                     | Tecla        |
|--------------------------|--------------|
| Mover raquete esquerda ↑ | W            |
| Mover raquete esquerda ↓ | S            |
| Mover raquete direita ↑  | ↑ (Seta cima)|
| Mover raquete direita ↓  | ↓ (Seta baixo)|

---

## Melhorias Futuras

- Adicionar níveis de dificuldade.
- Implementar suporte para multiplayer online.
- Adicionar sons e efeitos visuais.

---

## Autor
>Juan Pablo Silvério Silva

>Vinícius Pires de Souza

>Luís Henrique Sampaio

