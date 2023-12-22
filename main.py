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
'''a probInimigoAparecer funciona da seguinte maneira:
 ela começa em um número n e vai aumentando até chegar 
 na probInimigoMáxima, qualquer pequena alteração nas probabilidades
 aumenta bastante a dificuldade'''
probInimigoAparecer = 3
probInimigoMaxima = 7 #"dificuldade máxima"
probCombustivelAparecer = 0
valor_inicial_combustivel = 400 #isto serve para na tela de game over o combustivel voltar a ter o valor inicial
combustivel, pontos = valor_inicial_combustivel, 0

#fontes
fonteNomeJogo = pygame.font.Font('fonts/highspeed.ttf',70)
fonteSubtitulo = pygame.font.Font('fonts/highspeed.ttf', 15)
fonte_pontosEcombustivel = pygame.font.Font('fonts/highspeed.ttf', 15)

#cores pré-definidas
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

#variáveis de configuração do programa
nomeJogo = 'Star Blaster'
altura_tela_inicial_e_menu, largura_tela_inicial_e_menu = 550, 800
titulo = fonteNomeJogo.render(nomeJogo,True,BRANCO)

#imagens
imagemBackGround = pygame.image.load('assets/menuImageSpace.jpg') 
imagemBackGroundJogo = pygame.image.load('assets/menuImageSpace.jpg')

#background song
mixer.music.load('sound/Interstellar by HansZimmer.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.3) #volume

#tela de game over
def game_over():
    global pontos, combustivel

    #esta parte cria e mostra uma última tela
    tela_gameover = pygame.display.set_mode((largura_tela_inicial_e_menu,altura_tela_inicial_e_menu))
    tela_gameover.blit(imagemBackGround, (0, 0))
    pygame.display.set_caption(nomeJogo)

    #desde que o looping seja True ele continua rodando, caso contrário o pygame fecha
    run = True
    while run:

        #essa tela mostra uma mensagem de Game Over(utiliza a fonte do nome do jogo), a pontuação, uma mensagem de reiniciar ou voltar ao menu de opções
        def quarta_tela(tela_gameover):
            gameover = fonteNomeJogo.render('Game Over',True,BRANCO)
            tela_gameover.blit(gameover,(110,200))
            pontuaçãofinal = fonteSubtitulo.render(f'Pontuação final: {pontos}',True, VERDE)
            tela_gameover.blit(pontuaçãofinal,(260,300))
            reiniciar = fonteSubtitulo.render('1 - Reiniciar',True,BRANCO)
            tela_gameover.blit(reiniciar, (190,400))
            menu = fonteSubtitulo.render('2 - Menu Principal',True,BRANCO)
            tela_gameover.blit(menu, (380,400))

        quarta_tela(tela_gameover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #as keys direcionam a outras funções e/ou comandos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: #reiniciar
                    pontos = 0
                    combustivel = valor_inicial_combustivel
                    run = False
                    jogo()
                elif event.key == pygame.K_2: #menu_opcoes
                    pontos = 0
                    combustivel = valor_inicial_combustivel
                    menu_opcoes()
                    run = False

        pygame.display.update()
        FramesPerSecond.tick(fps)

#tela do jogo
def jogo():
    global probInimigoAparecer, probInimigoMaxima

    #esta parte cria e mostra a tela de jogabilidade
    tela_jogo = pygame.display.set_mode((largura_tela_jogo,altura_tela_jogo))
    pygame.display.set_caption(nomeJogo)

    #classe de jogador
    class Spaceship(pygame.sprite.Sprite):
        def __init__(jogador, x, y):
            pygame.sprite.Sprite.__init__(jogador)
            jogador.image = pygame.image.load('assets/spaceship.png')
            jogador.rect = jogador.image.get_rect()
            jogador.rect.center = [x, y]
            jogador.ultimo_tiro = pygame.time.get_ticks()

        def update(jogador):
            global combustivel
            #velocidade de movimentação da nave
            velocidade_nave = 10
            #variavel cooldown do tempo do tiro
            cooldown = 500 #milisegundos
            #grava o tempo atual, serve para comparar junto com outra variável o tempo do último tiro com o tempo atual
            tempo_agora = pygame.time.get_ticks()

            #colisão entre jogador e inimigo é game over
            colisoes_inimigo_jogador = pygame.sprite.spritecollide(jogador, inimigo_group, False)
            if colisoes_inimigo_jogador:
                game_over()

            #colisão entre jogador e combustivel aumenta em 40 unidades o combustivel
            colisoes_combustivel_jogador = pygame.sprite.spritecollide(jogador, combustivel_group, False)
            if colisoes_combustivel_jogador:
                combustivel += 3.5 #2,3 = 40 unidades

            #movimentação de acordo com a tecla pressionada
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and jogador.rect.top > 0:
                jogador.rect.y -= velocidade_nave
                combustivel -= 1 #movimentar gasta n qnt_combustivel
            if key[pygame.K_s] and jogador.rect.bottom < altura_tela_jogo:
                jogador.rect.y += velocidade_nave
                combustivel -= 1 #movimentar gasta n qnt_combustivel

            #tiro, atira-se pressionando space e existe um cooldown de um tiro para outro  
            if key[pygame.K_SPACE] and tempo_agora - jogador.ultimo_tiro > cooldown:
                bullets = Tiro(jogador.rect.centerx, jogador.rect.top)
                bullet_group.add(bullets)
                jogador.ultimo_tiro = tempo_agora
                combustivel -= 1.4 #atirar gasta n qnt_combustivel
            
            #decrementar n ponto de combustível se o jogador não estiver se movimentando
            if not key[pygame.K_w] and not key[pygame.K_s]:
                combustivel -= 0.1

            if combustivel <= 0:
                game_over()

    #classe de tiro  
    class Tiro(pygame.sprite.Sprite):
        def __init__(bullet, x, y):
            pygame.sprite.Sprite.__init__(bullet)
            bullet.image = pygame.image.load('assets/bullet.png')
            bullet.rect = bullet.image.get_rect()
            bullet.rect.center = [x + 30, y + 37] #posiciona onde o tiro sai, está ajustado para sair da cabeça da nave

        def update(bullet):
            bullet.rect.x += 10 #"velocidade" de propagação do tiro no eixo x
            if bullet.rect.x > 784: #é o "alcance" que o tiro tem, o alcance é limitado por determinado valor do eixo x
                bullet.kill() #para não ficar utilizando memória, o tiro é destruído quando chega no limite do alcance

    #classe de inimigo 
    class Inimigo(pygame.sprite.Sprite):
        def __init__(inimigo, x, y):
            pygame.sprite.Sprite.__init__(inimigo)
            inimigo.image = pygame.image.load('assets/alien' + str(random.randint(1,4)) + '.png') #random gera um número de 1 a 3 e escolhe a imagem do alien aleatoriamente
            inimigo.rect = inimigo.image.get_rect()
            inimigo.rect.x = x
            inimigo.rect.y = y
            inimigo.velocidade = random.randint(3, 9)  #velocidade aleatória do inimigo
                
        def update(inimigo):
            global pontos
            inimigo.rect.x -= inimigo.velocidade #movimentação do inimigo no eixo x

            if inimigo.rect.right < 0:
                inimigo.kill() #remove o inimigo quando ele estiver fora da tela
                
            colisoes_inimigo_tiro = pygame.sprite.spritecollide(inimigo, bullet_group, True)  #remove o tiro ao colidir com inimigo
            if colisoes_inimigo_tiro:
                inimigo.kill()  #remove o inimigo quando há colisão
                pontos += 50

    #classe de combustivel
    class Combustivel(pygame.sprite.Sprite):
        def __init__(fuel, x, y):
            pygame.sprite.Sprite.__init__(fuel)
            fuel.image = pygame.image.load('assets/gasolina.png') 
            fuel.rect = fuel.image.get_rect()
            fuel.rect.x = x
            fuel.rect.y = y
            fuel.velocidade = random.randint(4, 7)  #velocidade aleatória do combustível
                
        def update(fuel):
            global pontos
            fuel.rect.x -= fuel.velocidade #movimentação do combustível no eixo x

            if fuel.rect.right < 0:
                fuel.kill() #remove o combustivel quando ele estiver fora da tela
                
            colisoes_combustivel_tiro = pygame.sprite.spritecollide(fuel, bullet_group, True)  #remove o tiro ao colidir com o combustivel
            if colisoes_combustivel_tiro:
                fuel.kill()  #remove o combustivel quando há colisão

    #criação das sprites dos grupos
    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    inimigo_group = pygame.sprite.Group()
    combustivel_group = pygame.sprite.Group()

    spaceship = Spaceship(largura_tela_jogo // 9, altura_tela_jogo - 270) #determina a posição da nave no mapa
    spaceship_group.add(spaceship)

    def cria_inimigo():
        randomicoEixoY = random.randint(0, altura_tela_jogo - 50)
        #cria o inimigo no canto direito da tela
        alien = Inimigo(largura_tela_jogo, randomicoEixoY)
        inimigo_group.add(alien)
        
    def cria_combustivel():
        randomicoEixoY = random.randint(0, altura_tela_jogo - 50)
        #cria o combustivel no canto direito da tela
        c = Combustivel(largura_tela_jogo, randomicoEixoY)
        combustivel_group.add(c)

    #desde que o looping seja True ele continua rodando, caso contrário o pygame fecha
    run = True
    while run:

        def terceira_tela(tela_jogo):
            #esta função é responsável por exibir os pontos e combústivel na tela
            points = fonte_pontosEcombustivel.render(f'Pontos: {pontos}',True,BRANCO)
            tela_jogo.blit(points,(10,15))
            fuel = fonte_pontosEcombustivel.render(f'Combustível: {combustivel:.0f}',True,BRANCO)
            tela_jogo.blit(fuel,(10,520))
            pygame.display.flip()

        terceira_tela(tela_jogo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #cria um novo inimigo com uma chance aleatória
        if random.randint(1, 100) < probInimigoAparecer: 
            #a dificuldade vai aumentando de acordo com o número escolhido, até um nível máximo
            if probInimigoAparecer < probInimigoMaxima:
                probInimigoAparecer += 0.10
            elif probInimigoAparecer >= probInimigoMaxima:
                probInimigoAparecer = probInimigoMaxima
            cria_inimigo()
        
        #cria um novo combustível com uma chance aleatória
        if random.randint(0, 100) < 2: 
            cria_combustivel()

        #atualiza a sprite de movimentação do jogador
        spaceship.update()
        #atualize as sprites dos demais grupos
        bullet_group.update()
        inimigo_group.update()
        combustivel_group.update()

        #faz o display da tela e a atualiza para não ficar rastros
        tela_jogo.blit(imagemBackGroundJogo, (0, 0))

        #desenha os sprites na tela
        spaceship_group.draw(tela_jogo)
        bullet_group.draw(tela_jogo)
        inimigo_group.draw(tela_jogo)
        combustivel_group.draw(tela_jogo)

        FramesPerSecond.tick(fps)
        pygame.display.update()

#tela menu de jogar, configurações, ranking, instruções, sair
def menu_opcoes():

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
                    pygame.quit()

        pygame.display.update()
        FramesPerSecond.tick(fps)

#tela de início
def menu_inicial():

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
                if event.key == pygame.K_RETURN:
                    menu_opcoes()
                    run = False
                    
        pygame.display.update()
        FramesPerSecond.tick(fps)

menu_inicial()