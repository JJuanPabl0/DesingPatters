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

# Raquete
raquete_largura = 10
raquete_altura = 100
velocidade_raquete = 6

# Posição inicial das raquetes
raquete_esquerda_y = (ALTURA // 2) - (raquete_altura // 2)
raquete_direita_y = (ALTURA // 2) - (raquete_altura // 2)

# Bola
bola_raio = 10
bola_x = LARGURA // 2
bola_y = ALTURA // 2
velocidade_bola_x = 4
velocidade_bola_y = 4

# Pontuação
pontuacao_esquerda = 0
pontuacao_direita = 0

# Relógio
relogio = pygame.time.Clock()

# Adapter para entrada
class InputAdapter:
    def __init__(self):
        self.teclas = {}

    def mapear_teclas(self, acao, tecla):
        self.teclas[acao] = tecla

    def acao_press(self, acao, teclas_pressionadas):
        return teclas_pressionadas[self.teclas.get(acao, None)]

# Criar instância do adaptador
input_adapter = InputAdapter()
input_adapter.mapear_teclas("raquete_esquerda_cima", pygame.K_w)
input_adapter.mapear_teclas("raquete_esquerda_baixo", pygame.K_s)
input_adapter.mapear_teclas("raquete_direita_cima", pygame.K_UP)
input_adapter.mapear_teclas("raquete_direita_baixo", pygame.K_DOWN)

# Facade para gerenciamento do jogo
class PingPongFacade:
    def __init__(self):
        self.raquete_esquerda_y = raquete_esquerda_y
        self.raquete_direita_y = raquete_direita_y
        self.bola_x = bola_x
        self.bola_y = bola_y
        self.velocidade_bola_x = velocidade_bola_x
        self.velocidade_bola_y = velocidade_bola_y
        self.pontuacao_esquerda = pontuacao_esquerda
        self.pontuacao_direita = pontuacao_direita

    def mover_raquete(self, lado, direcao):
        if lado == "esquerda":
            if direcao == "cima" and self.raquete_esquerda_y > 0:
                self.raquete_esquerda_y -= velocidade_raquete
            elif direcao == "baixo" and self.raquete_esquerda_y < ALTURA - raquete_altura:
                self.raquete_esquerda_y += velocidade_raquete
        elif lado == "direita":
            if direcao == "cima" and self.raquete_direita_y > 0:
                self.raquete_direita_y -= velocidade_raquete
            elif direcao == "baixo" and self.raquete_direita_y < ALTURA - raquete_altura:
                self.raquete_direita_y += velocidade_raquete

    def mover_bola(self):
        self.bola_x += self.velocidade_bola_x
        self.bola_y += self.velocidade_bola_y

        # Colisão com as paredes
        if self.bola_y - bola_raio <= 0 or self.bola_y + bola_raio >= ALTURA:
            self.velocidade_bola_y *= -1

        # Colisão com as raquetes
        if (self.bola_x - bola_raio <= raquete_largura and
            self.raquete_esquerda_y <= self.bola_y <= self.raquete_esquerda_y + raquete_altura):
            self.velocidade_bola_x *= -1

        if (self.bola_x + bola_raio >= LARGURA - raquete_largura and
            self.raquete_direita_y <= self.bola_y <= self.raquete_direita_y + raquete_altura):
            self.velocidade_bola_x *= -1

        # Verificar pontuação
        if self.bola_x < 0:
            self.pontuacao_direita += 1
            self.resetar_bola()
        if self.bola_x > LARGURA:
            self.pontuacao_esquerda += 1
            self.resetar_bola()

    def resetar_bola(self):
        self.bola_x = LARGURA // 2
        self.bola_y = ALTURA // 2
        self.velocidade_bola_x *= -1

    def desenhar(self):
        tela.fill(PRETO)
        pygame.draw.rect(tela, BRANCO, (10, self.raquete_esquerda_y, raquete_largura, raquete_altura))
        pygame.draw.rect(tela, BRANCO, (LARGURA - 20, self.raquete_direita_y, raquete_largura, raquete_altura))
        pygame.draw.ellipse(tela, BRANCO, (self.bola_x - bola_raio, self.bola_y - bola_raio, bola_raio * 2, bola_raio * 2))
        pygame.draw.line(tela, BRANCO, (LARGURA // 2, 0), (LARGURA // 2, ALTURA), 1)

        # Desenhar a pontuação
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"{self.pontuacao_esquerda} - {self.pontuacao_direita}", True, BRANCO)
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 10))
        pygame.display.flip()

# Criar instância da facade
jogo = PingPongFacade()

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento das raquetes
    teclas = pygame.key.get_pressed()
    if input_adapter.acao_press("raquete_esquerda_cima", teclas):
        jogo.mover_raquete("esquerda", "cima")
    if input_adapter.acao_press("raquete_esquerda_baixo", teclas):
        jogo.mover_raquete("esquerda", "baixo")
    if input_adapter.acao_press("raquete_direita_cima", teclas):
        jogo.mover_raquete("direita", "cima")
    if input_adapter.acao_press("raquete_direita_baixo", teclas):
        jogo.mover_raquete("direita", "baixo")

    # Movimento da bola
    jogo.mover_bola()

    # Desenhar a tela
    jogo.desenhar()

    # Controlar a taxa de quadros
    relogio.tick(60)

pygame.quit()
