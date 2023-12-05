"""
Universidade de Brasilia
Instituto de Ciencias Exatas
Departamento de Ciencia da Computacao
Algoritmos e Programação de Computadores - 2/2023
Turma: Prof. Carla Castanho e Prof. Frank Ned
Aluno: Juliano dos Santos da Costa
Matricula: 232003590
Projeto Final - Parte 1
Descricao: < breve descricao do programa >
"""
import pygame
from pygame import mixer
pygame.init()
import random

fps = 20
FramesPerSecond = pygame.time.Clock() 

#variáveis de configurações jogo
tamanho = 5
altura_tela_jogo, largura_tela_jogo = 550, 800
probX, probF = 0, 0
combustivel, pontos = 400, 0

#fontes
fonteNomeJogo = pygame.font.Font('fonts/highspeed.ttf',70)
fonteSubtitulo = pygame.font.Font('fonts/highspeed.ttf', 15)

#cores pré-definidas
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

#variáveis de configuração do programa
nomeJogo = 'Meteor Blast'
tela = "TELAINICIAL" #está varíavel guia a ordem de ações do jogo
altura_tela_inicial_e_menu, largura_tela_inicial_e_menu = 550, 800
titulo = fonteNomeJogo.render(nomeJogo,True,BRANCO)

#imagens
imagemBackGround = pygame.image.load('assets/menuImageSpace.jpg') 
imagemBackGroundJogo = pygame.image.load('assets/menuImageSpace.jpg')

#background song
mixer.music.load('sound/ElevenMine.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0)

#tela do jogo
def jogo():
    global tela

    #esta parte cria e mostra a tela de jogabilidade
    tela_jogo = pygame.display.set_mode((largura_tela_jogo,altura_tela_jogo))
    pygame.display.set_caption(nomeJogo)

    #criação da classe jogador
    class Spaceship(pygame.sprite.Sprite):
        def __init__(jogador, x, y):
            pygame.sprite.Sprite.__init__(jogador)
            jogador.image = pygame.image.load('assets/spaceship.png')
            jogador.rect = jogador.image.get_rect()
            jogador.rect.center = [x, y]
            jogador.ultimo_tiro = pygame.time.get_ticks()

        def update(jogador):
            #velocidade de movimentação da nave
            velocidade_nave = 8
            #variavel cooldown do tempo do tiro
            cooldown = 500 #milisegundos
            #grava o tempo atual, serve para comparar junto com outra variável o tempo do último tiro com o tempo atual
            tempo_agora = pygame.time.get_ticks()

            #movimentação de acordo com a tecla pressionada
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and jogador.rect.top > 0:
                jogador.rect.y -= velocidade_nave
            if key[pygame.K_s] and jogador.rect.bottom < altura_tela_jogo:
                jogador.rect.y += velocidade_nave

            #tiro, atira-se pressionando space e existe um cooldown de um tiro para outro  
            if key[pygame.K_SPACE] and tempo_agora - jogador.ultimo_tiro > cooldown:
                bullets = Tiro(jogador.rect.centerx, jogador.rect.top)
                bullet_group.add(bullets)
                jogador.ultimo_tiro = tempo_agora

    #classe de tiro  
    class Tiro(pygame.sprite.Sprite):
        def __init__(bullet, x, y):
            pygame.sprite.Sprite.__init__(bullet)
            bullet.image = pygame.image.load('assets/bullet.png')
            bullet.rect = bullet.image.get_rect()
            bullet.rect.center = [x + 30, y + 37] #posiciona onde o tiro sai, está ajustado para sair da cabeça da nave
        
        def update(bullet):
            bullet.rect.x += 5 #"velocidade" de propagação do tiro no eixo x

    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    spaceship = Spaceship(largura_tela_jogo // 9, altura_tela_jogo - 270) #determina a posição da nave no mapa
    spaceship_group.add(spaceship)

    #desde que o looping seja True ele continua rodando, caso contrário o pygame fecha
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #atualiza a sprite de movimentação do jogador
        spaceship.update()

        #atualize as sprites dos demais grupos
        bullet_group.update()

        #faz o display da tela e a limpa para não ficar rastros
        tela_jogo.blit(imagemBackGroundJogo, (0, 0))

        #desenho os sprites na tela
        spaceship_group.draw(tela_jogo)
        bullet_group.draw(tela_jogo)

        FramesPerSecond.tick(fps)
        pygame.display.update()

#tela menu de jogar, configurações, ranking, instruções, sair
def menu_opcoes():
    global tela

    #esta parte cria e mostra uma segunda tela do jogo
    tela_menu = pygame.display.set_mode((largura_tela_inicial_e_menu,altura_tela_inicial_e_menu))
    tela_menu.blit(imagemBackGround, (0, 0))
    pygame.display.set_caption(nomeJogo)

    #desde que o looping seja True ele continua rodando, caso contrário o pygame fecha
    run = True
    while run:
        
        #essa tela mostra o título e subtítulos na segunda tela do jogo
        def segunda_tela(tela_menu):
            tela_menu.blit(titulo,(30,200))   
            subtitulo1 = fonteSubtitulo.render('Escolha uma opção:',True,BRANCO)
            tela_menu.blit(subtitulo1,(260,300))
            subtitulo2 = fonteSubtitulo.render('1 - Jogar',True,BRANCO)
            tela_menu.blit(subtitulo2,(310,340))
            subtitulo3 = fonteSubtitulo.render('2 - Configurações',True,BRANCO)
            tela_menu.blit(subtitulo3,(310,370))
            subtitulo4 = fonteSubtitulo.render('3 - Ranking',True,BRANCO)
            tela_menu.blit(subtitulo4,(310,400))
            subtitulo5 = fonteSubtitulo.render('4 - Intruções',True,BRANCO)
            tela_menu.blit(subtitulo5,(310,430))
            subtitulo6 = fonteSubtitulo.render('5 - Sair',True,BRANCO)
            tela_menu.blit(subtitulo6,(310,460))
            pygame.display.flip()
        
        segunda_tela(tela_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            #as keys direcionam a outras funções e/ou comandos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    tela = 'JOGO'
                    jogo()
                    run = False
                elif event.key == pygame.K_5:
                    run = False

        pygame.display.update()
        FramesPerSecond.tick(fps)

#tela de início
def menu_inicial():
    global tela

    #esta parte cria e mostra uma tela inicial
    tela_inicial = pygame.display.set_mode((largura_tela_inicial_e_menu,altura_tela_inicial_e_menu))
    tela_inicial.blit(imagemBackGround, (0, 0))
    pygame.display.set_caption(nomeJogo) 

    #desde que o looping seja True ele continua rodando, caso contrário o pygame fecha
    run = True
    while run:

        #essa tela mostra o título e subtítulo na primeira tela do jogo
        def primeira_tela(tela_inicial):
            tela_inicial.blit(titulo,(30,200))   
            subtitulo = fonteSubtitulo.render('Bem vindo jogador, pressione enter para continuar!',True,BRANCO)
            tela_inicial.blit(subtitulo,(90,310))
            pygame.display.flip()
        
        primeira_tela(tela_inicial)
        
        #existem duas opções para esse for, fechar o jogo ou pressionar enter e ir para a tela de menu opções
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            #as keys direcionam a outras funções e/ou comandos
            elif event.type == pygame.KEYDOWN:
                if tela == 'TELAINICIAL' and event.key == pygame.K_RETURN:
                    tela = 'MENU'
                    menu_opcoes()
                    run = False

        pygame.display.update()
        FramesPerSecond.tick(fps)

menu_inicial()