
import pygame
import os
import random
import neat

#ia jogando = True para IA jogar. Se mudar para False, ficara para o usuario comum jogar com a barra de espaço
ia_jogando = True
numero_da_geracao = 0

#Tamanho da tela
largura_tela = 500
altura_tela = 800

#Definindo as imagens
img_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
img_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
img_fundo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
img_passaro = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]

#Definindo a fonte do texto/letras
pygame.font.init()
fonte_letra = pygame.font.SysFont('lexend', 50)

#------------------------------------- Agora vamos desenvolver a logica do Flappy Bird --------------------------
class Passaro:
    imgs = img_passaro
    
    # animações da rotação
    giro_maximo = 25
    velocidade_maxima = 20
    tempo_movimentacao = 5

    #os dados que o passaro terá. Ex: altura, tamanho
    def __init__(self, x, y):
        self.x = x          #posição X
        self.y = y          #posicção Y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.imgs[0]

    #criar a função de salto do passaro
    def pulo(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y


    #criar a função de movimentação do passaro
    def mover(self):
        # calcular o movimento do passaro
        self.tempo += 1
        movimento_passaro = 1.5 * (self.tempo**2) + self.velocidade * self.tempo #Formula fisica utlizada: S = So +Vot +at²/2

        #Limitando a movimentacao para nao ficar infinitamente.
        if movimento_passaro > 16:
            movimento_passaro = 16
        elif movimento_passaro < 0:
            movimento_passaro -= 2

        self.y += movimento_passaro

        #Criando o angulo do passaro
        if movimento_passaro < 0 or self.y < (self.altura + 50):
            if self.angulo < self.giro_maximo:
                self.angulo = self.giro_maximo
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_maxima

        #Criar a função para desenha o passaro no game
    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_img += 1

        if self.contagem_img < self.tempo_movimentacao:
            self.imagem = self.imgs[0]
        elif self.contagem_img < self.tempo_movimentacao*2:
            self.imagem = self.imgs[1]
        elif self.contagem_img < self.tempo_movimentacao*3:
            self.imagem = self.imgs[2]
        elif self.contagem_img < self.tempo_movimentacao*4:
            self.imagem = self.imgs[1]
        elif self.contagem_img >= self.tempo_movimentacao*4 + 1:
            self.imagem = self.imgs[0]
            self.contagem_img = 0


        #O passaro deve parar de bater as asas quando o jogador perder/cair
        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contagem_img = self.tempo_movimentacao*2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posicao_superior = 0
        self.posicao_inferior = 0
        self.cano_superior = pygame.transform.flip(img_cano, False, True)
        self.cano_inferior = img_cano
        self.passagem_cano = False
        self.definicao_altura()

    def definicao_altura(self):
        self.altura = random.randrange(50, 450)
        self.posicao_superior = self.altura - self.cano_superior.get_height()
        self.posicao_inferior = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_superior, (self.x, self.posicao_superior))
        tela.blit(self.cano_inferior, (self.x, self.posicao_inferior))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_superior)
        base_mask = pygame.mask.from_surface(self.cano_inferior)

        distancia_cano_superior = (self.x - passaro.x, self.posicao_superior - round(passaro.y))
        distancia_cano_inferior = (self.x - passaro.x, self.posicao_inferior - round(passaro.y))

        colisao_cano_superior = passaro_mask.overlap(topo_mask, distancia_cano_superior)
        colisao_cano_inferior = passaro_mask.overlap(base_mask, distancia_cano_inferior)

        if colisao_cano_inferior or colisao_cano_superior:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = img_chao.get_width()
    imagem = img_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontuacao):
    tela.blit(img_fundo, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_letra.render(f"Pontuação: {pontuacao}", 1, (255, 255, 255))
    tela.blit(texto, (largura_tela - 10 - texto.get_width(), 10))

    if ia_jogando:
        texto = fonte_letra.render(f"Geração: {numero_da_geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    pygame.display.update()

#Função principal que vai rodar o jogo
def main(genomas, config):
    global numero_da_geracao
    numero_da_geracao +=1

    if ia_jogando:
        redes_neurais = []
        todos_genomas = []
        passaros = []
        
        for _, genoma in genomas:
            redes = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes_neurais.append(redes)
            genoma.fitness = 0
            todos_genomas.append(genoma)
            passaros.append(Passaro(230, 350))

    else:
        passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pontuacao = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        #Fechando e parando o game quando apertar no X
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            #Identificando o botao de espaço como pular caso a Ia nao esteja jogando                  
            if not ia_jogando:   
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pulo()

        indice_cano = 0
        if len(passaros)> 0:
            if len(canos) > 1 and passaros[0].x > canos[0].x + canos[0].cano_superior.get_width():
                indice_cano = 1

        else:
            rodando = False
            break

        #Fazendo as cosias do jogo de mexerem
        for i, passaro in enumerate(passaros):
            passaro.mover()
            
            todos_genomas[i].fitness += 0.1
            output = redes_neurais[i].activate((passaro.y, abs(passaro.y - canos[indice_cano].altura),abs(passaro.y - canos[indice_cano].posicao_inferior)))
            if output[0] > 0.5:
                passaro.pulo()


        chao.mover()

        #Criação e remocção de canos novos a cada passsagem do passaro em um cano
        criar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ia_jogando:
                        todos_genomas[i].fitness -= 1
                        todos_genomas.pop(i)
                        redes_neurais.pop(i)

                if not cano.passagem_cano and passaro.x > cano.x:
                    cano.passagem_cano = True
                    criar_cano = True
            cano.mover()
            if cano.x + cano.cano_superior.get_width() < 0:
                remover_canos.append(cano)

        if criar_cano:
            pontuacao += 1
            canos.append(Cano(600))
            for genoma in todos_genomas:
                genoma.fitness += 5
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ia_jogando:
                    todos_genomas.pop(i)
                    redes_neurais.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontuacao)

def play(caminho_arq_IA):
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                caminho_arq_IA)

    #A IA ira reportar os dados estatisticos sobre o seu aprendizado. 
    populacao_de_passaros = neat.Population(config)
    populacao_de_passaros.add_reporter(neat.StdOutReporter(True))
    populacao_de_passaros.add_reporter(neat.StatisticsReporter())

    if ia_jogando:
        populacao_de_passaros.run(main, 20)
    else:
        main(None, None)

if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_arq_IA = os.path.join(caminho, 'IA.txt')
    play(caminho_arq_IA)
