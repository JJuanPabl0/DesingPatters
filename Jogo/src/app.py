import pygame

# Inicializar o pygame
pygame.init()

# Dimensões da janela
LARGURA = 800
ALTURA = 600

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Configurações da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Ping Pong")

# Relógio
relogio = pygame.time.Clock()

# Fonte para o placar
fonte = pygame.font.Font(None, 74)

# Padrão Singleton: Gerenciador de Estado do Jogo
class GerenciadorEstadoJogo:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GerenciadorEstadoJogo, cls).__new__(cls)
            cls._instancia.estado = "em_andamento"
        return cls._instancia

    def obter_estado(self):
        return self.estado

    def definir_estado(self, novo_estado):
        self.estado = novo_estado

# Instância do Singleton
gerenciador_estado = GerenciadorEstadoJogo()

# Padrão Bridge: Interface para renderização
class Renderizador:
    def renderizar(self, tela, elemento):
        raise NotImplementedError("Deve ser implementado pela subclasse")

# Implementação concreta do Renderizador
class Renderizador2D(Renderizador):
    def renderizar(self, tela, elemento):
        elemento.desenhar(tela)

# Padrão Composite: Interface comum para elementos do jogo
class ElementoJogo:
    def atualizar(self):
        pass

    def desenhar(self, tela):
        pass

# Raquete como um Leaf do Composite
class Raquete(ElementoJogo):
    def __init__(self, x, y, largura, altura, velocidade):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade

    def mover(self, direcao, altura_maxima):
        if direcao == "cima" and self.y > 0:
            self.y -= self.velocidade
        elif direcao == "baixo" and self.y < altura_maxima - self.altura:
            self.y += self.velocidade

    def desenhar(self, tela):
        pygame.draw.rect(tela, BRANCO, (self.x, self.y, self.largura, self.altura))

# Bola como outro Leaf do Composite
class Bola(ElementoJogo):
    def __init__(self, x, y, raio, velocidade_x, velocidade_y):
        self.x = x
        self.y = y
        self.raio = raio
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.velocidade_inicial = (velocidade_x, velocidade_y)

    def atualizar(self, largura, altura, raquete_esq, raquete_dir, placar):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        # Colisão com paredes
        if self.y - self.raio <= 0 or self.y + self.raio >= altura:
            self.velocidade_y *= -1

        # Colisão com raquetes
        if (self.x - self.raio <= raquete_esq.x + raquete_esq.largura and
            raquete_esq.y <= self.y <= raquete_esq.y + raquete_esq.altura):
            self.velocidade_x *= -1

        if (self.x + self.raio >= raquete_dir.x and
            raquete_dir.y <= self.y <= raquete_dir.y + raquete_dir.altura):
            self.velocidade_x *= -1

        # Verifica se alguém pontuou
        if self.x < 0:
            placar[1] += 1
            self.resetar_posicao(largura, altura)
        elif self.x > largura:
            placar[0] += 1
            self.resetar_posicao(largura, altura)

    def resetar_posicao(self, largura, altura):
        self.x = largura // 2
        self.y = altura // 2
        self.velocidade_x, self.velocidade_y = self.velocidade_inicial

    def desenhar(self, tela):
        pygame.draw.ellipse(tela, BRANCO, (self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2))

# Composite principal que agrega elementos do jogo
class ComponenteJogo(ElementoJogo):
    def __init__(self):
        self.elementos = []

    def adicionar(self, elemento):
        self.elementos.append(elemento)

    def atualizar(self, largura, altura, placar):
        for elemento in self.elementos:
            if isinstance(elemento, Bola):
                elemento.atualizar(largura, altura, self.elementos[0], self.elementos[1], placar)

    def desenhar(self, tela):
        for elemento in self.elementos:
            elemento.desenhar(tela)

# Padrão Adapter: Gerenciamento de entrada
class InputAdapter:
    def __init__(self):
        self.teclas = None

    def atualizar_entrada(self):
        self.teclas = pygame.key.get_pressed()

    def mover_raquete(self, raquete, tecla_cima, tecla_baixo, altura):
        if self.teclas[tecla_cima]:
            raquete.mover("cima", altura)
        if self.teclas[tecla_baixo]:
            raquete.mover("baixo", altura)

# Padrão Facade: Abstração do jogo
class FacadeJogo:
    def __init__(self):
        self.jogo = ComponenteJogo()
        self.renderizador = Renderizador2D()
        self.input_adapter = InputAdapter()
        self.placar = [0, 0]

        # Criar elementos do jogo
        self.raquete_esquerda = Raquete(10, ALTURA // 2 - 50, 10, 100, 6)
        self.raquete_direita = Raquete(LARGURA - 20, ALTURA // 2 - 50, 10, 100, 6)
        self.bola = Bola(LARGURA // 2, ALTURA // 2, 10, 4, 4)

        # Adicionar elementos ao componente principal
        self.jogo.adicionar(self.raquete_esquerda)
        self.jogo.adicionar(self.raquete_direita)
        self.jogo.adicionar(self.bola)

    def atualizar(self):
        self.input_adapter.atualizar_entrada()
        self.input_adapter.mover_raquete(self.raquete_esquerda, pygame.K_w, pygame.K_s, ALTURA)
        self.input_adapter.mover_raquete(self.raquete_direita, pygame.K_UP, pygame.K_DOWN, ALTURA)
        self.jogo.atualizar(LARGURA, ALTURA, self.placar)

    def renderizar(self):
        tela.fill(PRETO)
        self.renderizador.renderizar(tela, self.jogo)

        # Renderizar o placar
        texto_esq = fonte.render(str(self.placar[0]), True, BRANCO)
        texto_dir = fonte.render(str(self.placar[1]), True, BRANCO)
        tela.blit(texto_esq, (LARGURA // 4, 20))
        tela.blit(texto_dir, (3 * LARGURA // 4, 20))

# Instância do Facade
facade = FacadeJogo()

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualizar e renderizar o jogo
    facade.atualizar()
    facade.renderizar()

    pygame.display.flip()

    # Controlar a taxa de quadros
    relogio.tick(60)

pygame.quit()
