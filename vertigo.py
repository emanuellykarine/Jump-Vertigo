import random
import sys 
import time
from os import path

import pygame

# Iniciar o jogo
def game_init(width, heigth):
    pygame.init()
    size = width, heigth
    tela = pygame.display.set_mode((size))
    pygame.display.set_caption("Jump Vertigo")
    return tela

def draw_fundo(fundo_scroll):
    tela.blit(background_image, (0, 0 + fundo_scroll)) # Junta o primeiro fundo com a tela
    tela.blit(background_image2, (0, -600 + fundo_scroll)) #Junta o segundo fundo com a tela 

def draw_player(imagem, x, y):
    jogador = pygame.transform.scale(imagem, (50, 85))
    jogador_rect = jogador.get_rect()
    jogador_rect.center = (x, y)
    tela.blit(jogador, jogador_rect)
    
class Jogador():
    # construtor da classe, utiliza init para definir os valores dos atributos
    def __init__(self, x, y, player):
        self.image = pygame.transform.scale(player, (30, 60))
        # Minimizando o retangulo da imagem para melhorar as colisões
        self.width = 30
        self.heigth = 60
        self.rect = pygame.Rect(0, 0, self.width - 5, self.heigth - 5)
        self.rect.center = (x, y)
        self.velocidadeY = 0

    def draw(self):
        tela.blit(self.image, (self.rect.x, self.rect.y - 5))

    def moverBoneco(self):
        scroll = 0
        distancia_x = 0
        distancia_y = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            distancia_x -= 10
        if key[pygame.K_RIGHT]:
            distancia_x += 10
        
        self.velocidadeY += gravidade
        distancia_y += self.velocidadeY

        # Colisão com as extremidades do x
        if self.rect.left + distancia_x < 0:
            distancia_x = -self.rect.left
        if self.rect.right + distancia_x > 400:
            distancia_x = 400 - self.rect.right
        

        #Colisão na plataforma
        for plataforma in plataforma_group:
            if plataforma.rect.colliderect(self.rect.x, self.rect.y + distancia_y, self.width, self.heigth):
                if self.rect.bottom < plataforma.rect.centery:
                    if self.velocidadeY > 0:
                        self.rect.bottom = plataforma.rect.top
                        distancia_y = 0
                        self.velocidadeY = -20

        # Colisão com a parte de cima da tela
        if self.rect.top <= limite_scroll:
            if self.velocidadeY < 0:
                scroll = -distancia_y

        # Só aumenta depois das colisões serem verificadas
        self.rect.x += distancia_x
        self.rect.y += distancia_y + scroll

        return scroll


class Plataforma(pygame.sprite.Sprite):
    def __init__ (self, x, y, width, movendo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(plataforma_img, (width, 10))
        self.movendo = movendo
        self.cont = random.randint(0, 50) #Cont para a plataforma mover
        self.direcao = random.choice([-1, 1])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        if self.movendo == True:
            self.cont += 0.5
            self.rect.x += self.direcao

        # Mudando direcao da plataforma
        if self.cont >= 100 or self.rect.left < 0 or self.rect.right > 400:
            self.direcao *= -1 
            self.cont = 0

        # Mudar a posição vertical 
        self.rect.y += scroll

        # Se a plataforma tiver fora da tela
        if self.rect.top > 600:
            self.kill()

# Iniciando a tela
tela = game_init(840, 600)
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.Font(None, 32)
text_color = (255, 255, 255)
black = (0, 0, 0)

# Variáveis do jogo
limite_scroll = 200 #Quando o rect do boneco alcançar o scroll vai ser ativado
gravidade = 1
max_plataformas = 10
scroll = 0
fundo_scroll = 0
score = 0

# Carregando imagens
capa_jogo = pygame.image.load("CapaJogo.png")
fim_jogo = pygame.image.load("FimCaiu.png")
win_jogo = pygame.image.load("WinJogo.png")
selecionar_jogador = pygame.image.load("SelecionarJogador.png") 
background_image = pygame.image.load("Fundo.png")
background_image2 = pygame.image.load("Fundo2.png")
boneco_img = pygame.image.load("Boneco.png")
boneca_img = pygame.image.load("Boneca.png")
plataforma_img = pygame.image.load("Plataforma.png")

# Transição das imagens
fade_img = pygame.Surface((840, 600)).convert_alpha()
fade_img.fill("black")
fade_alpha = 255

# Carregando grupo de plataformas
plataforma_group = pygame.sprite.Group()

# Plataforma inicial
plataforma = Plataforma(400 // 2 - 50, 600 - 50, 100, False)
plataforma_group.add(plataforma)


estado = "menu"
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if estado == "menu":
        if fade_alpha > 0:
            fade_alpha -= 4
            fade_img.set_alpha(fade_alpha)
        tela.blit(capa_jogo, (0,0))
        tela.blit(fade_img, (0,0))
        if keys[pygame.K_s]:
            estado = "escolher_jogador"

    elif estado == "escolher_jogador":
        tela.blit(selecionar_jogador, (0, 0))
        draw_player(boneca_img, 350, 300)
        draw_player(boneco_img, 150, 300)
        if keys[pygame.K_j]:
            player = Jogador(400 // 2, 600 - 150, boneco_img)
            estado = "jogando"
        if keys[pygame.K_m]:
            player = Jogador(400 // 2, 600 - 150, boneca_img)
            estado = "jogando"
    
    elif estado == "jogando":
        scroll = player.moverBoneco()
        # Desenha fundo
        fundo_scroll += scroll
        if fundo_scroll >= 600:
            fundo_scroll = 600
        draw_fundo(fundo_scroll)

        #Grupo de plataformas
        if len(plataforma_group) < max_plataformas:
            w = random.randint(40, 60)
            x = random.randint(0, 400 - w)
            y = plataforma.rect.y - random.randint(100, 130)
            tipo = random.randint(1, 2) #Mover plataformas
            if tipo == 1:
                mover_plataforma = True
            else:
                mover_plataforma = False
            plataforma = Plataforma(x, y, w, mover_plataforma)
            plataforma_group.add(plataforma)

        plataforma_group.update(scroll) #Update plataforma

        # Incrementa o score
        if scroll > 0:
            score += scroll

        plataforma_group.draw(tela) #Desenha plataforma
        player.draw() #Desenha o boneco

        if player.rect.top > 600:
            estado = "game_over"
            fade_alpha = 255

        
        if score >= 2000:
            estado = "win"
            fade_alpha = 255

        #Desenha o score
        text = font.render("Score: " + str(score), True, text_color)
        tela.blit(text, (10, 10))


    elif estado == "win":
        if fade_alpha > 0:
            fade_alpha -= 4
            fade_img.set_alpha(fade_alpha)

        if keys[pygame.K_i]:
            estado = "menu"
            scroll = 0
            score = 0
            player.rect.center = (400 // 2, 600 - 150)
            plataforma_group.empty()
            plataforma = Plataforma(400 // 2 - 50, 600 - 50, 100, False)
            plataforma_group.add(plataforma)
            fade_alpha = 255
            
        tela.blit(win_jogo, (0, 0))
        tela.blit(fade_img, (0,0))

    elif estado == "game_over":
        if fade_alpha > 0:
            fade_alpha -= 4
            fade_img.set_alpha(fade_alpha)
        
        if keys[pygame.K_i]:
            estado = "menu"
            scroll = 0
            score = 0
            player.rect.center = (400 // 2, 600 - 150)
            plataforma_group.empty()
            plataforma = Plataforma(400 // 2 - 50, 600 - 50, 100, False)
            plataforma_group.add(plataforma)
            fade_alpha = 255

        text_score = font.render("Score: " + str(score), True, text_color)
        tela.blit(fim_jogo, (0,0))
        tela.blit(fade_img, (0,0))
        tela.blit(text_score, (10, 10))


    pygame.display.flip()

