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
import pygame, sys
pygame.init()
import random

fps = 20
FramesPerSecond = pygame.time.Clock() 

#variáveis ???
tamanho = 5
altura_tabuleiro, largura_tabuleiro = 10, 135
probX, probF = 0, 0
combustivel, pontos = 400, 0

#fontes
fonteNomeJogo = pygame.font.SysFont('Impact',120)
fonteSubtitulo = pygame.font.SysFont('Arial', 20)

#cores pré-definidas
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

#variáveis de configuração
nomeJogo = 'Meteor Blast'
tela = "TELAINICIAL" #está varíavel mantém a ordem de ações do jogo
altura_tela_inicial_e_menu, largura_tela_inicial_e_menu = 550, 800
titulo = fonteNomeJogo.render(nomeJogo,True,BRANCO)

#imagens
imagemTelaInicial = pygame.image.load('assets/menuImageSpace.jpg') 

#tela menu de jogar, configurações, ranking, instruções, sair
def menu_opcoes():
    tela_menu = pygame.display.set_mode((largura_tela_inicial_e_menu,altura_tela_inicial_e_menu))
    tela_menu.blit(imagemTelaInicial, (0, 0))
    #tela_menu.fill(PRETO)
    pygame.display.set_caption(nomeJogo)

    #desde que o looping seja True ele continua rodando, caso contrário o pygame fecha
    run = True
    while run:
        
        #essa tela mostra o título e subtítulos na segunda tela do jogo
        def segunda_tela(tela_menu):
            tela_menu.blit(titulo,(90,160))   
            subtitulo1 = fonteSubtitulo.render('Escolha uma opção:',True,BRANCO)
            tela_menu.blit(subtitulo1,(170,310))
            subtitulo2 = fonteSubtitulo.render('1 - Jogar',True,BRANCO)
            tela_menu.blit(subtitulo2,(400,310))
            subtitulo3 = fonteSubtitulo.render('2 - Configurações',True,BRANCO)
            tela_menu.blit(subtitulo3,(400,340))
            subtitulo4 = fonteSubtitulo.render('3 - Ranking',True,BRANCO)
            tela_menu.blit(subtitulo4,(400,370))
            subtitulo5 = fonteSubtitulo.render('4 - Intruções',True,BRANCO)
            tela_menu.blit(subtitulo5,(400,400))
            subtitulo6 = fonteSubtitulo.render('5 - Sair',True,BRANCO)
            tela_menu.blit(subtitulo6,(400,430))
            pygame.display.flip()
        
        segunda_tela(tela_menu)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
        FramesPerSecond.tick(fps)

#tela de início
def menu_inicial():
    
    #esta parte cria e mostra uma tela inicial
    tela_inicial = pygame.display.set_mode((largura_tela_inicial_e_menu,altura_tela_inicial_e_menu))
    tela_inicial.blit(imagemTelaInicial, (0, 0))
    #tela_inicial.fill(PRETO)
    pygame.display.set_caption(nomeJogo) 

    #desde que o looping seja True ele continua rodando, caso contrário o pygame fecha
    run = True
    while run:
        
        #essa tela mostra o título e subtítulo na primeira tela do jogo
        def primeira_tela(tela_inicial):
            tela_inicial.blit(titulo,(90,160))   
            subtitulo = fonteSubtitulo.render('Bem vindo jogador, pressione enter para continuar!',True,BRANCO)
            tela_inicial.blit(subtitulo,(170,310))
            pygame.display.flip()
        
        primeira_tela(tela_inicial)
        
        #existem duas opções para esse for, fechar o jogo ou pressionar enter e ir para a tela de menu opções
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            elif event.type == pygame.KEYDOWN:
                if tela == 'TELAINICIAL' and event.key == pygame.K_RETURN:
                    tela == 'MENU'
                    menu_opcoes()
                    run == False

        pygame.display.update()
        FramesPerSecond.tick(fps)

menu_inicial()