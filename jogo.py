import pygame
from random import *

ALTURA = 650
LARGURA = 600
pygame.init()
myfont = pygame.font.SysFont('roboto', 30)

endimg = pygame.image.load("img/endgame.png")
fundo_img = pygame.image.load("img/trees2.jpg")
fundo_h = fundo_img.get_height()
fundo1_y = 0
fundo2_y = -fundo_h
pos = 0
pontuacao = 0


relogio = pygame.time.Clock()

VELOCIDADE_CARRO = 5
VELOCIDADE_MIN = 5
VELOCIDADE_MAX = 10
INIMIGO_RAIO = 24
PERSONAGEM_RAIO = 38
x_personagem = 0
y_personagem = -300


tela = pygame.display.set_mode((LARGURA, ALTURA))
inimigos = []

inimigos_imagems = []
inimigos_imagems.append(pygame.image.load("img/galinha_pequena_01.png"))
inimigos_imagems.append(pygame.image.load("img/galinha_pequena_02.png"))
inimigos_imagems.append(pygame.image.load("img/galinha_pequena_03.png"))
inimigos_imagems.append(pygame.image.load("img/galinha_pequena_02.png"))
carro = pygame.image.load("img/carro.png")

linhas_altura = [-150, 0, 150, 275]

# inimigo = [x, y, raio, vx, contador da imagem]
for i in range(len(linhas_altura)):
    inimigos.append([LARGURA//2, linhas_altura[i], INIMIGO_RAIO, randint(VELOCIDADE_MIN, VELOCIDADE_MAX), 0])

# função que transforma coordenadas de sistema cartesiano
def ret_para_cg(n):
    return (int(n[0] + LARGURA/2), int(-1*n[1] + ALTURA/2))
    
def colisao( obj0, obj1 ):
    distancia = ((obj0[0] - obj1[0])**2 + (obj0[1] - obj1[1])**2) ** (1/2.0)
    if distancia < obj0[2] + obj1[2]:
        return True
    return False

def pontos(texto,posicao):
    textsurface = myfont.render(texto, False, (255,255,255))
    tela.blit(textsurface, (posicao[0], posicao[1]))

# grade 
def desenhar_grade(tela, distx, disty):
    n = int((LARGURA/2)/distx)
    for i in range(n+1):
        pygame.draw.line(tela, (25,25,25), (int(LARGURA/2-i*distx),0),
            (int(LARGURA/2-i*distx),ALTURA))
    for i in range(n+1):
        pygame.draw.line(tela, (25,25,25), (int(LARGURA/2+i*distx),0),
            (int(LARGURA/2+i*distx),ALTURA))
    n = int((ALTURA/2)/disty)
    for i in range(n+1):
        pygame.draw.line(tela, (25,25,25), (0,int(LARGURA/2-i*disty)),
            (LARGURA,int(LARGURA/2-i*disty)))
    for i in range(n+1):
        pygame.draw.line(tela, (25,25,25), (0,int(LARGURA/2+i*disty)),
            (LARGURA,int(LARGURA/2+i*disty)))

# inicializa o ambiente do pygame

acabar = False

# loop principal
contador = 1

contar = [True, True, True, True]

while not acabar:
    tela.fill((0, 0, 0))
    tela.blit(fundo_img, (0,fundo1_y))
    tela.blit(fundo_img, (0,fundo2_y))
    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_personagem = x_personagem + 10
            if event.key == pygame.K_DOWN:
                y_personagem = y_personagem - 10
            if event.key == pygame.K_LEFT:
                x_personagem = x_personagem - 10
            if event.key == pygame.K_UP: 
                y_personagem = y_personagem + 10


    for i in range(len(inimigos)):
        imagem = inimigos_imagems[(inimigos[i][4]//2)%4]
        tela.blit(imagem,  imagem.get_rect(center=ret_para_cg((inimigos[i][0], inimigos[i][1]))))

        # desenha raio da galinha
        #pygame.draw.circle(tela, (0, 255, 0), ret_para_cg((inimigos[i][0],inimigos[i][1])), INIMIGO_RAIO, 1)
        inimigos[i][0] = inimigos[i][0] - inimigos[i][3]
        inimigos[i][4] += 1
        if inimigos[i][0] + inimigos[i][2] <= -LARGURA//2:
            inimigos[i][0] = LARGURA//2
            inimigos[i][3] = randint(VELOCIDADE_MIN, VELOCIDADE_MAX)

    tela.blit(carro, (ret_para_cg((x_personagem-31,y_personagem+38))))

    # desenha raio do carro
    #pygame.draw.circle(tela, (0, 255, 0), ret_para_cg((x_personagem,y_personagem)), PERSONAGEM_RAIO, 1)

    for i in inimigos:
        if colisao((x_personagem,y_personagem,PERSONAGEM_RAIO), (i[0], i[1], i[2])):
            acabar = True
            print("você perdeu")


    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        y_personagem = y_personagem + VELOCIDADE_CARRO
        fundo1_y += 10
        fundo2_y += 10
        pos += 10
        if (pos % fundo_h) == 0:
            fundo1_y = 0
            fundo2_y = -fundo_h

    if acabar == True:
        pygame.display.flip()
        tela.fill((0, 0, 0))
        tela.blit(endimg, (0,0))



    if y_personagem > 250:
        contar = [True, True, True, True]
        y_personagem = -300
        VELOCIDADE_MAX=VELOCIDADE_MAX+2
        VELOCIDADE_MIN=VELOCIDADE_MIN+2
        VELOCIDADE_CARRO=VELOCIDADE_CARRO+2


    if y_personagem > -150 and y_personagem <= 0 and contar[0]:
        pontuacao = pontuacao + 1 
        contar[0] = False
    if y_personagem > 0 and y_personagem <= 150 and contar[1]:
        pontuacao = pontuacao + 1
        contar[1] = False
    if y_personagem > 150 and y_personagem <= 250 and contar[2]:
        pontuacao = pontuacao + 1
        contar[2] = False
    
    pontos(str('Pontos: {:.0f}'.format(pontuacao)), (LARGURA-120, ALTURA-50))
    pygame.display.flip()
    relogio.tick(30)
