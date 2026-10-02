# IMPORTA TODA A BIBLIOTECA PYGAME
import pygame
import sys
import random

# INICIA OS MODULOS INTERNOS DO PYGAME PARA UTILIZAR AS FUNÇÕES DA BIBLIOTECA
pygame.init()

# DEFINIMOS O TAMANHO DA TELA, LARGURA E ALTURA
LARGURA_TELA = 800
ALTURA_TELA = 600
# NOME QUE VAI APARECE QUANDO A JANELA ESTIVER INICIADA
TITULO_JANELA = "Mario o Aventureiro"
# TAXA DE ATUALIZACAO DE QUADROS POR SEGUNDO
FPS = 60

# CRIAR A JANELA COM 800 DE LARGURA E 600 DE ALTURA
janela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
# MUDA O NOME DA JANELA COM A VARIAVEL CRIADA ANTES
pygame.display.set_caption(TITULO_JANELA)

# CRIAR FONTES PARA MENSAGENS DA TELA DE INICIO, VITORIA E DERRORA, APENAS EDITA O ESTILO DA LETRA NESTA PARTE
fonte = pygame.font.SysFont("arial", 28, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 40, bold=True)

# CRIAR O PERSONAGEM
# CARREGA A IMAGEM DO NOSSO PERSONAGEM PROCURANDO O ARQUIVO DENTRO DO PC
try:
    imagem_player = pygame.image.load(r"C:\Users\NICO\Downloads\mario.png")
except pygame.error:
    # IMAGEM RESERVA CASO O CAMINHO NÃO SEJA ENCONTRADO DAI DESENHA UM QUADRADO AZUL TEMPORARIAMENTE
    imagem_player = pygame.Surface((50, 50))
    imagem_player.fill((0, 0, 255))

# AJUSTAR A IMAGEM DO PERSONAGEM PARA NAO PREENCHER A TELA TODA
# CRIO A VARIAVEL LARGURA CORRETA PARA REDIMENSIONAR A IMAGEM PARA FICAR DO TAMANHO IDEAL QUE EU QUERIA
largura_correta = 60
# NESTA PARTE CRIO A VARIAVEL PARA A PROPORCAO QUE O MARIO VAI FICAR, PEGO O 60 DA VARIAVEL LARGURA E DIVIDO PELA LARGURA ORIGINAL DO PNG DO MARIO QUE TENHO INSTALADO
proporcao_redimensionamento = largura_correta / imagem_player.get_width()
##PEGAMOS A ALTURA ORIGINAL DA ALTURA DA FOTO DO MARIO DENTRO DO COMPUTADOR E MULTIPLICAMOS PELO RESULTADO DA DIVISAO DA VARIAVEL ANTERIOR, O ROUND NA FRENTE SERIA APEANS PARA ARREDONDAR PAR AUM VALOR INTEIRO
altura_correta = round(imagem_player.get_height() * proporcao_redimensionamento)
imagem_player = pygame.transform.smoothscale(
    imagem_player, (largura_correta, altura_correta)
)

# PEGA O RETANGULO DA IMAGEM PARA GERENCIAR A POSICAO, POIS O RECT CRIA UMA HITBOX INVISIVEL EM VOLTA DO MARIO QUE SERIA UMA CAIXA QUE E O LIMITE DELE, SERIA AONDE ELE ENCOSTA NAS COISAS
player_rect = imagem_player.get_rect()

# DEFINIÇÃO DA ALTURA DO CHÃO E TAMANHO TOTAL DO MAPA
ALTURA_CHAO = 450
# O MAPA TEM 4 VEZES O TAMANHO DA TELA MAS ELE VAI ANDANDO CONFORME O MARIO CAMINHA NA TELA
LARGURA_MAPA = 3200

# PARTE DAS CORES AONDE PESQUISEI PARA SABER QUAIS CORES IRIAM FICAR LEGAM
COR_CEU = (135, 206, 235)  # Azul céu
COR_GRAMA = (76, 175, 80)  # Verde clarinho
COR_GRAMA_ESCURA = (56, 142, 60)  # Verde escuro para fazer sombra
COR_TERRA = (121, 85, 72)  # Castanho terra
COR_TERRA_ESCURA = (93, 64, 55)  # Castanho escuro
COR_PLATAFORMA_TOPO = (255, 183, 77)  # Laranja claro
COR_PLATAFORMA_CORPO = (230, 81, 0)  # Laranja escuro
COR_CASTELO = (120, 144, 156)  # Cinzento pedra
COR_PORTA = (62, 39, 35)  # Madeira escura

# SEGMENTOS DO CHÃO COM OS ESPAÇOS - CADA UM DESDES RECT É UMA ILHA AONDE PODE PISAR EM CIMA, ONDE NAO TEM O RECT É O BURACO
chao_secoes = [
    pygame.Rect(0, ALTURA_CHAO, 500, 150),
    pygame.Rect(720, ALTURA_CHAO, 450, 150),  #PRIMEIRO BURACO
    pygame.Rect(1420, ALTURA_CHAO, 500, 150),  # 2 BURACO
    pygame.Rect(2570, ALTURA_CHAO, 900, 150),  # TERCEIRO BURACO MAIOR
]



# PLATAFORMAS DO PARKOUR REDISTRIBUÍDAS PARA OS ESPACOS MAIORES
plataformas = [
    # ORDEM DOS NUMEROS X - Y  -LARGURA E ALTURA
    # DOIS PRIMEIROS BLOCOS ANTES DE CHEGAR NO PRIMEIRO BURACO
    pygame.Rect(200, 370, 100, 25),
    pygame.Rect(350, 300, 100, 25),
    # OS DOIS BLOCOS PARA PULAR O PRIMEIRO BURACO
    pygame.Rect(520, 330, 90, 25),
    pygame.Rect(630, 270, 90, 25),
    # PLATAFORMAS PARA PULAR O SEGUNDO BURACO
    pygame.Rect(1200, 350, 90, 25),
    pygame.Rect(1310, 260, 90, 25),
    # PLATAFORMAS PARA PULAR O TERCEIRO BURACO
    pygame.Rect(1940, 340, 90, 25),
    pygame.Rect(2060, 250, 90, 25),
    # BLOCOS DE APOIO ANTES DE CHEGAR NO CASTELO
    pygame.Rect(2350, 360, 100, 25),
    pygame.Rect(2550, 290, 120, 25),
]


# CASTELO FEITO EM BLOCOS NO FINAL DA FASE PARA SER A LINHA DE CHEGADA
# X - Y - LARGURA E ALTURA
castelo_rect = pygame.Rect(2850, ALTURA_CHAO - 160, 140, 160)


#VARIAVEL PARA CONTROLAR O ESTADO DO JOGO, SE ESTA NO INICIO, JOGANDO, VITORIA OU GAMEOVER
estado_jogo = "INICIO"


#QUANTOS PASSOS O MARIO VAI DAR PARA CADA TECLA PRESSIONADA
velocidade = 5  
# VARIAVEL DE CONTROLE QUE DEFINE SE CONTINUA RODANDO OU NAO, GRAVIDADE E RELOGIO E A CAMERA
rodando = True
tempo = pygame.time.Clock()

gravidade = 0.7
##VELOCIDADE VERTICAL (PRA CIMA) NEGATIVA FAZ SUBIR E A POSITIVA FAZ DESCER PQ O INICIO DE Y E O CANTO SUPERIOR ESQUERDO DA TELA QUE E O 0 E ELE VAI AUMENTANDO PRA BAIXO 
velocidade_y = 0
# DESLOCAMENTO DA CAMERA PARA ACOMPANHAR O MARIO, INICIALMENTE ELE FICA NO INICIO DO MAPA, TENDO O VALOR DE 0, MAS A MEDIDA QUE O MARIO ANDA PARA A DIREITA, O VALOR VAI AUMENTANDO PARA QUE A CAMERA SEJA DESLOCADA PARA A DIREITA JUNTO COM O MARIO
camera_x = 0

#FUNCAO PARA REINICIAR O JOGO COLOCANDO O MARIO E A CAMERA DE VOLTA NO COMECO
def resetar_jogo():
    """RESTAURA A POSIÇÃO INICIAL DO JOGADOR E DA CÂMARA."""
    global velocidade_y, camera_x
    player_rect.x = 50
    player_rect.bottom = ALTURA_CHAO
    velocidade_y = 0
    camera_x = 0


def desenhar_bloco_chao(superficie, rect_tela):
    """DESENHA BLOCOS DE CHÃO BEM ACABADOS COM TIPO GRAMA E TERRA."""
    #PINTA A TERRA POR BAIXO E A GRAMA
    pygame.draw.rect(superficie, COR_TERRA, rect_tela)
    pygame.draw.rect(
        superficie,
        COR_TERRA_ESCURA,
        (rect_tela.x, rect_tela.y + 35, rect_tela.width, rect_tela.height - 35),
    )
    pygame.draw.rect(
        superficie, COR_GRAMA, (rect_tela.x, rect_tela.y, rect_tela.width, 15)
    )
    pygame.draw.rect(
        superficie,
        COR_GRAMA_ESCURA,
        (rect_tela.x, rect_tela.y + 12, rect_tela.width, 4),
    )


def desenhar_bloco_plataforma(superficie, rect_tela):
    """DESENHA BLOCOS DE PLATAFORMA BEM ACABADOS COM BORDAS E DESTAQUES."""
    #PINTA OS BLOCOS NO AR DE APOIO
    pygame.draw.rect(superficie, COR_PLATAFORMA_CORPO, rect_tela, border_radius=5)
    pygame.draw.rect(
        superficie,
        COR_PLATAFORMA_TOPO,
        (rect_tela.x, rect_tela.y, rect_tela.width, 6),
        border_top_left_radius=5,
        border_top_right_radius=5,
    )
    pygame.draw.rect(superficie, (180, 60, 0), rect_tela, width=2, border_radius=5)


def desenhar_castelo_blocos(superficie, rect_tela):
    """DESENHA O CASTELO DE CHEGADA EM FORMA DE BLOCOS ARQUITETÔNICOS."""
    #CONSTROI O CASTELAO
    pygame.draw.rect(superficie, COR_CASTELO, rect_tela)
    for y in range(rect_tela.y, rect_tela.bottom, 20):
        pygame.draw.line(
            superficie, (90, 110, 120), (rect_tela.x, y), (rect_tela.right, y), 2
        )
    for x in range(rect_tela.x, rect_tela.right, 28):
        pygame.draw.rect(superficie, COR_CASTELO, (x, rect_tela.y - 15, 18, 15))
    porta = pygame.Rect(rect_tela.centerx - 20, rect_tela.bottom - 50, 40, 50)
    pygame.draw.rect(
        superficie,
        COR_PORTA,
        porta,
        border_top_left_radius=15,
        border_top_right_radius=15,
    )


def desenhar_texto_centralizado(texto, fonte, cor, deslocamento_y=0):
    """FUNÇÃO AUXILIAR PARA DESENHAR TEXTOS CENTRALIZADOS NA TELA."""
    # BOTA QUALQUER FRASE NO MEIO DA TELA
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect(
        center=(LARGURA_TELA // 2, (ALTURA_TELA // 2) + deslocamento_y)
    )
    janela.blit(superficie, rect)


# INICIALIZA O ESTADO E AS POSIÇÕES INICIAIS
resetar_jogo()

# A BASE DO JOGO É O WHILE
while rodando:

    # VERIFICA SE FOI APERTADO ALGUMA TECLA
    for evento in pygame.event.get():
        # VERIFICA SE O USUARIO CLICOU NO BOTÃO DE FECHAR A JANELA E SE CLICOU MUDA A VARIAVEL DE CONTROLE PARA FALSE E INTERROMPE O WHILE
        if evento.type == pygame.QUIT:
            rodando = False
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            # SE O JOGO ESTIVER NA TELA DE INÍCIO OU DE FIM, O ESPAÇO RECOMEÇA O JOGO
            if estado_jogo in ["INICIO", "VITORIA", "GAMEOVER"]:
                if evento.key == pygame.K_SPACE:
                    resetar_jogo()
                    estado_jogo = "JOGANDO"

            # SO PODE PULAR QUANDO ESTIVER NO CHAO OU EM ALGUMA PLATAFORMA
            elif estado_jogo == "JOGANDO":
                if evento.key == pygame.K_SPACE:
                    # VERIFICA SE O MARIO ESTA PISANDO EM ALGUM LOCAL COM CHAO
                    esta_apoiado = False
                    for chao in chao_secoes:
                        if (
                            player_rect.bottom == chao.top
                            and player_rect.right > chao.left
                            and player_rect.left < chao.right
                        ):
                            esta_apoiado = True
                            break
                    if not esta_apoiado:
                        for plat in plataformas:
                            if (
                                player_rect.bottom == plat.top
                                and player_rect.right > plat.left
                                and player_rect.left < plat.right
                            ):
                                esta_apoiado = True
                                break
                    # SE ESTIVER APOIADO NO CHAO VAI DIMINUIR O Y OU SEJA IR PRA CIMA GERANDO UM PULO
                    if esta_apoiado:
                        velocidade_y = -12.5

    #MOVIMENTACOA SO FUNCIONA QUANDO ESTIVER JOGANDO
    if estado_jogo == "JOGANDO":
        # VERIFICA SE TEVE ALGUM INPUT DE W,A,S,D, SPACE E FAZ O PERSONAGEM SE MOVER
        teclas = pygame.key.get_pressed()
        # if teclas[pygame.K_w]:
        #    player_rect.y -= velocidade
        if teclas[pygame.K_a]:
            player_rect.x -= velocidade  # Anda para a esquerda
        # if teclas[pygame.K_s]:
        #    player_rect.y += velocidade
        if teclas[pygame.K_d]:
            player_rect.x += velocidade  # Anda para a direita

        #VELOCIDADE QUE O PERSONAGEM SE MOVE VERTICALMENTE NO EIXO Y
        velocidade_y += gravidade
        player_rect.y += velocidade_y

        ##SE O JOGADOR ESTIVER NA POSICAO MENOR QUE 0 VAI MUDAR SEU VALOR PARA 0 PARA NAO PASSAR DO VALOR DE X
        if player_rect.left < 0:
            player_rect.left = 0
        ##SE O VALOR DE JOGADOR FOR MAIOR QUE O LIMITE DO MAPA ELE FICA NO LIMITE
        if player_rect.right > LARGURA_MAPA:
            player_rect.right = LARGURA_MAPA

        ##SE O VALOR DO PLAYER FOR MENOS QUE 0 QUE SERIA O INICIO DO y (Teto)
        if player_rect.top < 0:
            player_rect.top = 0
            if velocidade_y < 0:
                velocidade_y = 0

        # COLISÃO COM OS SEGMENTOS DE CHÃO (SÓ QUANDO CAI)
        if velocidade_y > 0:
            for chao in chao_secoes:
                if (
                    player_rect.colliderect(chao)
                    and player_rect.bottom - velocidade_y <= chao.top
                ):
                    player_rect.bottom = chao.top
                    velocidade_y = 0

        # METODO DE COLISAO COM A PLATAFORMA, SOMENTE QUANDO PARA EM CIMA, SE PASSAR PELO MEIO VAI EM EMBORA
        if velocidade_y > 0:
            for plat in plataformas:
                if (
                    player_rect.colliderect(plat)
                    and player_rect.bottom - velocidade_y <= plat.top
                ):
                    player_rect.bottom = plat.top
                    velocidade_y = 0

        # ATUALIZAR A CÂMARA PARA SEGUIR O JOGADOR E MANTER ELE NO MEIO DA TELA
        camera_x = player_rect.centerx - LARGURA_TELA // 2
        camera_x = max(0, min(camera_x, LARGURA_MAPA - LARGURA_TELA))

        # SE CAIR NO BURACO ONDE NÃO HÁ CHÃO O JOGO RECOMECA
        if player_rect.top > ALTURA_TELA:
            estado_jogo = "GAMEOVER"

        # VERIFICA A CHEGADA AO CASTELO (VITÓRIA)
        if player_rect.colliderect(castelo_rect):
            estado_jogo = "VITORIA"

    ##DESENHO DAS TELAS
    # PREENCHE O FUNDO DA TELA COM A COR AZUL QUE DEFINIMOS A VARIAVEL ANTERIORMENTE
    janela.fill(COR_CEU)

    #MOSTRA A TELA CERTA DEPENDENDO DE COMO ESTA A PARTIDA
    if estado_jogo == "INICIO":
        desenhar_texto_centralizado(
            "PARKOUR DO MARIO", fonte_titulo, (255, 255, 255), -40
        )
        desenhar_texto_centralizado(
            "Pressione ESPAÇO para Começar", fonte, (255, 255, 0), 20
        )

    elif estado_jogo == "JOGANDO":
        # DESENHA SBTRAINDO O CAMERA_X PARA OS OBJETIS ANDAREM NA TELA CONFORME A CAMERA SE MOVE
        # Desenha tudo subtraindo o "camera_x" para os objetos andarem na tela conforme a câmara se move!

        # DESENHA OS BLOCOS DE CHÃO SÓLIDO
        for chao in chao_secoes:
            chao_tela = chao.move(-camera_x, 0)
            desenhar_bloco_chao(janela, chao_tela)

        # DESENHA AS PLATAFORMAS DO PARKOUR
        for plat in plataformas:
            plat_tela = plat.move(-camera_x, 0)
            desenhar_bloco_plataforma(janela, plat_tela)

        # DESENHA O CASTELO DE CHEGADA EM BLOCOS
        castelo_tela = castelo_rect.move(-camera_x, 0)
        desenhar_castelo_blocos(janela, castelo_tela)

        # DESENHA O PERSONAGEM
        player_tela = player_rect.move(-camera_x, 0)
        janela.blit(imagem_player, player_tela)

    elif estado_jogo == "VITORIA":
        desenhar_texto_centralizado(
            "CHEGOU AO CASTELO!", fonte_titulo, (255, 255, 255), -40
        )
        desenhar_texto_centralizado(
            "Pressione ESPAÇO para Jogar Novamente", fonte, (255, 255, 0), 20
        )

    elif estado_jogo == "GAMEOVER":
        desenhar_texto_centralizado("CAIU NO ABISMO!", fonte_titulo, (255, 80, 80), -40)
        desenhar_texto_centralizado(
            "Pressione ESPAÇO para Tentar Novamente", fonte, (255, 255, 255), 20
        )

    # ATUALIZA A TELA EXIBINDO TUDO QUE FOI DESENHADO NA JANELA DURANTE O CICLO
    pygame.display.flip()

    # GARANTE QUE O JOGO RODE NO MAXIMO A 60FPS
    tempo.tick(FPS)

pygame.quit()
