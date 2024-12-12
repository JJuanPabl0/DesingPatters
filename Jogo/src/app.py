import pygame

# Configurações gerais
LARGURA = 800
ALTURA = 600
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

class Placar:
    def __init__(self):
        self.pontos = [0, 0]
        self.publisher = Publisher()  # Publisher para o placar
        self.publisher.subscribe(self)  # O placar é um subscriber

    def atualizar(self, lado):
        if lado == "esquerda":
            self.pontos[0] += 1
        elif lado == "direita":
            self.pontos[1] += 1
        # Notificar os subscribers quando o placar for atualizado
        self.publisher.notify(f"Placar atualizado: {self.pontos}")

    def desenhar(self, tela, fonte):
        texto_esq = fonte.render(str(self.pontos[0]), True, BRANCO)
        texto_dir = fonte.render(str(self.pontos[1]), True, BRANCO)
        tela.blit(texto_esq, (LARGURA // 4, 20))
        tela.blit(texto_dir, (3 * LARGURA // 4, 20))

    def update(self, message):
        # Essa função será chamada quando o placar for atualizado
        print(message)  # Aqui você pode realizar ações como mostrar uma notificação ou alterar outros componentes

class Raquete:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)

    def mover(self, direcao, altura_tela):
        if direcao == "cima" and self.rect.top > 0:
            self.rect.y -= 5
        elif direcao == "baixo" and self.rect.bottom < altura_tela:
            self.rect.y += 5

    def desenhar(self, tela):
        pygame.draw.rect(tela, BRANCO, self.rect)

class Bola:
    def __init__(self):
        self.rect = pygame.Rect(LARGURA // 2 - 10, ALTURA // 2 - 10, 20, 20)
        self.velocidade_x = -5
        self.velocidade_y = 5

    def mover(self, largura_tela, altura_tela, placar):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        if self.rect.top <= 0 or self.rect.bottom >= altura_tela:
            self.velocidade_y *= -1

        if self.rect.left <= 0:
            placar.atualizar("direita")
            self.resetar()

        if self.rect.right >= largura_tela:
            placar.atualizar("esquerda")
            self.resetar()

    def resetar(self):
        self.rect.center = (LARGURA // 2, ALTURA // 2)
        self.velocidade_x *= -1

    def desenhar(self, tela):
        pygame.draw.ellipse(tela, BRANCO, self.rect)

class Jogo:
    def __init__(self):
        self.bola = Bola()
        self.raquete_esquerda = Raquete(10, ALTURA // 2 - 50)
        self.raquete_direita = Raquete(LARGURA - 20, ALTURA // 2 - 50)

    def atualizar(self, largura_tela, altura_tela, placar):
        self.bola.mover(largura_tela, altura_tela, placar)

        if self.bola.rect.colliderect(self.raquete_esquerda.rect) or self.bola.rect.colliderect(self.raquete_direita.rect):
            self.bola.velocidade_x *= -1

    def desenhar(self, tela):
        self.bola.desenhar(tela)
        self.raquete_esquerda.desenhar(tela)
        self.raquete_direita.desenhar(tela)

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 74)

# Instanciar os componentes do jogo
placar = Placar()
jogo = Jogo()

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento das raquetes
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        jogo.raquete_esquerda.mover("cima", ALTURA)
    if teclas[pygame.K_s]:
        jogo.raquete_esquerda.mover("baixo", ALTURA)
    if teclas[pygame.K_UP]:
        jogo.raquete_direita.mover("cima", ALTURA)
    if teclas[pygame.K_DOWN]:
        jogo.raquete_direita.mover("baixo", ALTURA)

    # Atualizar elementos do jogo
    jogo.atualizar(LARGURA, ALTURA, placar)

    # Renderizar elementos
    tela.fill(PRETO)
    jogo.desenhar(tela)
    placar.desenhar(tela, fonte)

    pygame.display.flip()

    # Controlar a taxa de quadros
    relogio.tick(60)

pygame.quit()
