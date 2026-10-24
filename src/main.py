# ================================================================
# FLAPPY BIRD — SPRINT 04 AMPLIADA | Programação para Engenharia
# Código didático: classes, eventos, estados, sprites, áudio e JSON
# ================================================================
from pathlib import Path
import json
import random
import time
import pygame

# ================================================================
# 1. CONFIGURAÇÕES GERAIS, FÍSICA E DIFICULDADE
# ================================================================
# Constantes em maiúsculas reúnem parâmetros que o estudante pode
# localizar e ajustar sem procurar valores espalhados pelo programa.
# As coordenadas são expressas em pixels da superfície lógica.
# FPS indica quantos quadros são processados por segundo.
LARGURA, ALTURA, FPS = 575, 860, 30
FATOR_TELA = 0.85
# IMPULSO negativo faz o pássaro subir: no Pygame, y cresce para baixo.
# GRAVIDADE é uma variação de velocidade por quadro, em px/quadro²;
# não representa diretamente a aceleração gravitacional em m/s².
GRAVIDADE, IMPULSO = 1.1, -8
VELOCIDADE_CANOS, VELOCIDADE_CHAO = 4, 4
# ABERTURA_CANOS é a passagem vertical entre os obstáculos.
# ESPACO_ENTRE_CANOS determina o espaçamento horizontal de geração.
ABERTURA_CANOS, ESPACO_ENTRE_CANOS = 290, 300
VIDAS_INICIAIS = 6
TEMPO_TEMA = 20
TEMPO_FASE = 260  # 260 s normal + 260 s especial
TEMPO_INVULNERAVEL_MS = 1200
USAR_MASCARAS = True
# __file__ é o caminho deste script; parent.parent sobe de src/
# para a raiz do projeto. Assim os recursos não dependem do terminal.
RAIZ = Path(__file__).resolve().parent.parent
IMAGENS = RAIZ / 'assets' / 'imgs'
AUDIOS = RAIZ / 'assets' / 'audio'
ARQUIVO_RECORDE = RAIZ / 'data' / 'recorde.json'
# Cada entrada da lista ocupa TEMPO_TEMA segundos. Repetições são
# intencionais e fazem parte da sequência de fundos do jogo.
TEMAS = ['bg','bg1','night','bg2','bg3','bg4','bg5','bg6',
         'background','bg7','bg8','bg1','night']
TEMAS_DIA = {'bg','bg2','bg3','bg6','background'}
TEMAS_TARDE = {'bg1','bg4','bg7','bg8'}
PASSAROS_ESPECIAIS = ['Blue','Bubble','Chuck','Doge','Dude','Fishy',
    'FloatKirby','Floppy','Girl','Glasses','Gray','Green','GreenFish',
    'Grellow','HOTpink','Jungle','Kirby','Lime','Orange','ParasolKirby',
    'Pink','Police','Propellor','Purple','Rainbow','Red','Sad','Speed',
    'Ukraine','Yellow']

# ================================================================
# 2. FUNÇÕES AUXILIARES — IMAGENS, SONS E ARQUIVO JSON
# ================================================================
# Função: bloco reutilizável definido com def; pode receber parâmetros
# e devolver um resultado com return.

def imagem(nome, fator=2):
    """Carrega um PNG com transparência e amplia suas dimensões.

    fator=2 significa largura e altura duplicadas; a área quadruplica.
    """
    img = pygame.image.load(str(IMAGENS / nome)).convert_alpha()
    return pygame.transform.scale(img, (img.get_width()*fator,
                                        img.get_height()*fator))

def som(nome):
    """Tenta carregar um efeito sonoro; retorna None se indisponível.

    None permite ao jogo prosseguir mesmo sem dispositivo de áudio.
    """
    if not pygame.mixer.get_init():
        return None
    try:
        return pygame.mixer.Sound(str(AUDIOS / nome))
    except (OSError, pygame.error) as erro:
        print(f'Aviso: som {nome} indisponível: {erro}')
        return None

def ler_recorde():
    """Lê pontos e nome do recordista do JSON, com valores seguros.

    O bloco with fecha o arquivo automaticamente, inclusive em erros.
    """
    try:
        with ARQUIVO_RECORDE.open(encoding='utf-8') as arq:
            dados = json.load(arq)
        pontos = dados.get('pontos', 0)
        nome = dados.get('nome', 'Anônimo')
        return (pontos if type(pontos) is int and pontos >= 0 else 0,
                nome if isinstance(nome, str) else 'Anônimo')
    except (OSError, ValueError, TypeError):
        return 0, 'Anônimo'

def salvar_recorde(pontos, nome):
    """Cria a pasta data/ e grava o recorde em JSON UTF-8.

    Retorna True quando a escrita termina e False quando falha.
    """
    try:
        ARQUIVO_RECORDE.parent.mkdir(parents=True, exist_ok=True)
        with ARQUIVO_RECORDE.open('w', encoding='utf-8') as arq:
            # ensure_ascii=False mantém acentos; indent=2 formata o JSON.
            json.dump({'pontos': pontos, 'nome': nome}, arq,
                      ensure_ascii=False, indent=2)
        return True
    except OSError as erro:
        print(f'Aviso: não foi possível gravar recorde: {erro}')
        return False

# ================================================================
# 3. CLASSE RECURSOS — CARREGAMENTO CENTRALIZADO
# ================================================================
# Classe é um molde para criar objetos. Aqui agrupamos imagens e sons
# para carregá-los uma vez, em vez de reler arquivos a cada quadro.
class Recursos:
    """Reúne sprites de cenários, personagens, interface e efeitos."""

    def __init__(self):
        # Dicionário: cada chave identifica o recurso correspondente.
        self.fundos = {nome: imagem(nome+'.png') for nome in set(TEMAS)}
        self.chao = imagem('base.png')
        self.cano_dia = imagem('pipe.png')
        self.cano_noite = imagem('pipe_night.png')
        self.passaros = {
            'dia': [imagem(f'bird{i}.png') for i in (1,2,3)],
            'tarde': [imagem(f'bird{i}_tarde.png') for i in (1,2,3)],
            'noite': [imagem(f'bird{i}_night.png') for i in (1,2,3)],
        }
        self.especiais = {nome: imagem(nome+'.png')
                          for nome in PASSAROS_ESPECIAIS}
        self.logo = imagem('Flappy_Bird_logo.png')
        self.gameover = imagem('gameover.png')
        self.moldura = imagem('moldura.png')
        self.medalhas = {nome: imagem(nome+'.png')
                         for nome in ('bronze','prata','ouro')}
        self.numeros = {str(i): imagem(f'{i}.png') for i in range(10)}
        self.sons = {nome: som(arquivo) for nome,arquivo in {
            'pulo':'wing.wav', 'ponto':'point.wav', 'colisao':'hit.wav',
            'morte':'die.wav', 'inicio':'chiptune_begin.mp3',
            'fim':'game_over.mp3', 'arcade':'game_over_arcade.mp3'
        }.items()}

# ================================================================
# 4. OBJETOS DO JOGO — PROGRAMAÇÃO ORIENTADA A OBJETOS
# ================================================================
# Atributos guardam o estado do objeto; métodos definem ações.
# self identifica a instância que está executando o método.
class Passaro:
    """Representa o jogador: posição, velocidade e animação."""
    def __init__(self, recursos):
        self.recursos = recursos
        self.x, self.y, self.vy = 200.0, 350.0, 0.0
        self.indice, self.contador = 0, 0
        self.familia = 'dia'

    def pular(self):
        """Aplica impulso vertical quando há clique ou barra de espaço."""
        self.vy = IMPULSO

    def atualizar(self):
        # Integração discreta: primeiro velocidade, depois posição.
        # A cada quadro: vy <- vy + gravidade; y <- y + vy.
        # min(..., 16) limita a velocidade de queda.
        self.vy = min(self.vy + GRAVIDADE, 16)
        self.y += self.vy
        self.contador += 1
        if self.contador >= 5:
            self.contador = 0
            self.indice = (self.indice + 1) % 3

    @property
    def sprite(self):
        """Seleciona o quadro atual; acesso como atributo: self.sprite.

        @property permite consultar o método sem escrever self.sprite().
        """
        return self.recursos.passaros[self.familia][self.indice]

    def retangulo(self):
        return self.sprite.get_rect(topleft=(int(self.x), int(self.y)))

    def desenhar(self, tela):
        # A rotação é visual; o retângulo/máscara usa sprite sem giro.
        angulo = max(-75, min(25, -self.vy*5))
        rot = pygame.transform.rotate(self.sprite, angulo)
        tela.blit(rot, rot.get_rect(center=self.retangulo().center))

class Obstaculo:
    """Representa um par de canos ou de pássaros da fase especial."""
    def __init__(self, x, recursos, especial=False, tema='bg'):
        self.x = float(x)
        self.topo_passagem = random.randint(150, 400)
        self.passou = False
        self.especial = especial
        if especial:
            nomes = random.sample(PASSAROS_ESPECIAIS, 2)
            # Rotação de 180° vira o pássaro superior de cabeça para baixo.
            # Uma rotação de 360° devolveria a orientação original.
            self.cima = pygame.transform.rotate(recursos.especiais[nomes[0]], 180)
            self.baixo = recursos.especiais[nomes[1]]
        else:
            self.baixo = (recursos.cano_dia if tema != 'night' and tema != 'bg5'
                          else recursos.cano_noite)
            self.cima = pygame.transform.flip(self.baixo, False, True)
        self.largura = max(self.cima.get_width(), self.baixo.get_width())

    def atualizar(self):
        self.x -= VELOCIDADE_CANOS

    def retangulos(self):
        x = int(self.x)
        topo = self.cima.get_rect(bottomleft=(x, self.topo_passagem))
        base = self.baixo.get_rect(topleft=(x, self.topo_passagem+ABERTURA_CANOS))
        return topo, base

    def desenhar(self, tela):
        a,b = self.retangulos()
        tela.blit(self.cima, a)
        tela.blit(self.baixo, b)

    def colide(self, passaro):
        """Verifica colisão usando retângulos e, opcionalmente, máscaras.

        Retângulos fazem o teste rápido; máscaras refinam pixel a pixel.
        """
        ret_p = passaro.retangulo()
        # A máscara distingue pixels opacos dos transparentes no PNG.
        mascara_p = pygame.mask.from_surface(passaro.sprite) if USAR_MASCARAS else None
        for sprite,ret in zip((self.cima,self.baixo),self.retangulos()):
            if not ret_p.colliderect(ret):
                continue
            if not USAR_MASCARAS:
                return True
            mascara = pygame.mask.from_surface(sprite)
            desloc = (ret.x-ret_p.x,ret.y-ret_p.y)
            if mascara_p.overlap(mascara, desloc) is not None:
                return True
        return False

class Chao:
    """Desenha uma faixa de chão repetida para simular movimento."""
    def __init__(self, sprite):
        self.sprite = sprite
        self.x = 0
        self.y = ALTURA - 100

    def atualizar(self):
        self.x = (self.x-VELOCIDADE_CHAO) % self.sprite.get_width()

    def desenhar(self, tela):
        # A imagem é repetida sem deixar lacunas no eixo horizontal.
        x = int(self.x)-self.sprite.get_width()
        while x < LARGURA:
            tela.blit(self.sprite,(x,self.y))
            x += self.sprite.get_width()

# ================================================================
# 5. CLASSE JOGO — ESTADOS, EVENTOS E LOOP PRINCIPAL
# ================================================================
# MENU: tela inicial; JOGO: simulação ativa; GAMEOVER: encerramento.
# A separação por estados evita que a mesma tecla execute ações
# incompatíveis em diferentes momentos.
class Jogo:
    """Coordena janela, recursos, física, entrada e desenho das telas."""
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        escala = min(info.current_w*FATOR_TELA/LARGURA,
                     info.current_h*FATOR_TELA/ALTURA, 1.0)
        self.tamanho = (max(1,int(LARGURA*escala)),max(1,int(ALTURA*escala)))
        self.janela = pygame.display.set_mode(self.tamanho,pygame.RESIZABLE)
        pygame.display.set_caption('Flappy Bird — Sprint 04 ampliada')
        self.tela = pygame.Surface((LARGURA,ALTURA))
        self.relogio = pygame.time.Clock()
        self.recursos = Recursos()
        pygame.display.set_icon(self.recursos.passaros['dia'][0])
        self.fonte = pygame.font.Font(None, 28)
        self.fonte_grande = pygame.font.Font(None, 52)
        self.som_ativo = True
        self.recorde,self.nome_recorde = ler_recorde()
        self.reiniciar()

    def tocar(self, nome, volume=0.5):
        efeito = self.recursos.sons.get(nome)
        if self.som_ativo and efeito is not None:
            efeito.set_volume(volume)
            efeito.play()

    def reiniciar(self):
        """Prepara uma nova partida sem apagar o recorde persistente."""
        self.estado = 'MENU'
        self.passaro = Passaro(self.recursos)
        self.chao = Chao(self.recursos.chao)
        self.obstaculos = []
        self.pontos = 0
        self.vidas = VIDAS_INICIAIS
        self.pausado = False
        self.tempo_ativo = 0.0
        self.tema = 'bg'
        self.especial = False
        self.ultimo_dano = -TEMPO_INVULNERAVEL_MS
        self.nome_digitado = ''
        self.digitando = False
        self.fim_iniciado = 0.0
        self.ultimo_arcade = 0.0
        self.contador_arcade = 0
        self.tocar('inicio')

    def iniciar(self):
        self.estado = 'JOGO'
        self.tempo_ativo = 0.0
        self.obstaculos = [Obstaculo(LARGURA,self.recursos)]
        if self.recursos.sons['inicio']:
            self.recursos.sons['inicio'].stop()

    def finalizar(self):
        """Muda para GAMEOVER e solicita nome se houve novo recorde."""
        self.estado = 'GAMEOVER'
        self.fim_iniciado = time.monotonic()
        self.contador_arcade = 0
        self.ultimo_arcade = 0.0
        self.digitando = self.pontos > self.recorde
        self.nome_digitado = ''
        self.tocar('fim')

    def perder_vida(self, agora_ms):
        if agora_ms-self.ultimo_dano < TEMPO_INVULNERAVEL_MS:
            return
        self.ultimo_dano = agora_ms
        self.vidas -= 1
        self.tocar('colisao')
        self.tocar('morte')
        if self.vidas <= 0:
            self.finalizar()
        else:
            # Reinicia o pássaro e obstáculos, preservando pontos/tempo.
            self.passaro = Passaro(self.recursos)
            self.obstaculos = [Obstaculo(LARGURA,self.recursos,self.especial,self.tema)]

    def tema_por_tempo(self):
        """Escolhe cenário e fase pelo tempo ativo, sem contar pausas."""
        # Ciclo total de 520 s, 13 temas de 20 s por fase.
        tempo_ciclo = self.tempo_ativo % (2*TEMPO_FASE)
        self.especial = tempo_ciclo >= TEMPO_FASE
        indice = int((tempo_ciclo % TEMPO_FASE)//TEMPO_TEMA)
        self.tema = TEMAS[indice % len(TEMAS)]
        self.passaro.familia = ('dia' if self.tema in TEMAS_DIA else
                                'tarde' if self.tema in TEMAS_TARDE else 'noite')

    def atualizar(self, dt, agora_ms):
        """Avança a simulação, cria obstáculos e detecta colisões.

        dt é o intervalo em segundos; agora_ms é o relógio em milissegundos.
        """
        if self.estado != 'JOGO' or self.pausado:
            return
        self.tempo_ativo += dt
        self.tema_por_tempo()
        self.passaro.atualizar()
        self.chao.atualizar()
        if not self.obstaculos or self.obstaculos[-1].x < LARGURA-ESPACO_ENTRE_CANOS:
            self.obstaculos.append(Obstaculo(LARGURA,self.recursos,self.especial,self.tema))
        for obstaculo in self.obstaculos:
            obstaculo.atualizar()
            if obstaculo.colide(self.passaro):
                self.perder_vida(agora_ms)
                break
            if not obstaculo.passou and obstaculo.x+obstaculo.largura < self.passaro.x:
                obstaculo.passou = True
                self.pontos += 1
                self.tocar('ponto')
        self.obstaculos = [o for o in self.obstaculos if o.x+o.largura >= 0]
        if self.estado == 'JOGO' and (self.passaro.y < 30 or
                                     self.passaro.retangulo().bottom >= self.chao.y):
            self.perder_vida(agora_ms)

    def texto(self, mensagem, x, y, cor=(255,255,255), grande=False, centro=False):
        """Renderiza texto; centro=True centraliza horizontalmente em x."""
        fonte = self.fonte_grande if grande else self.fonte
        img = fonte.render(str(mensagem),True,cor)
        self.tela.blit(img, (x-img.get_width()//2 if centro else x,y))

    # Renderiza a pontuação com imagens PNG em vez de caracteres de uma fonte.
    # O argumento centralizar controla se x representa o centro ou a borda esquerda.
    def numero(self, valor, x, y, fator=1.0, centralizar=False):
        """Desenha pontuação com sprites PNG; fator=0.5 reduz à metade."""
        """Desenha os algarismos; x indica o centro quando centralizar=True."""
        # Primeiro preparamos todos os dígitos, inclusive a escala desejada.
        # Isso permite conhecer a largura total antes de desenhar qualquer sprite.
        sprites = []
        for digito in str(max(0, valor)):
            sprite = self.recursos.numeros[digito]
            if fator != 1:
                sprite = pygame.transform.smoothscale(
                    sprite, (max(1, int(sprite.get_width() * fator)),
                             max(1, int(sprite.get_height() * fator))))
            sprites.append(sprite)

        # A largura depende da quantidade e do tamanho dos algarismos.
        largura_total = sum(sprite.get_width() for sprite in sprites)
        if centralizar:
            # A posição inicial fica metade da largura à esquerda do centro.
            # O resultado permanece centralizado para 1, 2 ou mais dígitos.
            x -= largura_total // 2
        for sprite in sprites:
            self.tela.blit(sprite, (x, y))
            x += sprite.get_width()

    def medalha(self):
        """Retorna a maior medalha atingida ou None se não houver.

        Ajuste os limiares abaixo para testar a dificuldade da premiação.
        A ordem importa: primeiro ouro, depois prata e bronze.
        """
        if self.pontos >= 150: return 'ouro'
        if self.pontos >= 100: return 'prata'
        if self.pontos >= 50: return 'bronze'
        return None

    def desenhar(self):
        """Desenha o estado atual e apresenta o quadro na janela."""
        # Todas as posições abaixo usam a superfície lógica de 575 x 860.
        # Só ao final redimensionamos a imagem para a janela do usuário.
        fundo = self.recursos.fundos[self.tema if self.estado!='MENU' else 'bg']
        self.tela.blit(pygame.transform.scale(fundo,(LARGURA,ALTURA)),(0,0))
        if self.estado == 'MENU':
            self.chao.desenhar(self.tela)
            logo = self.recursos.logo
            self.tela.blit(logo,logo.get_rect(center=(LARGURA//2,300)))
            oscilacao = int(12*__import__('math').sin(time.monotonic()*3))
            sprite = self.recursos.passaros['dia'][1]
            self.tela.blit(sprite,sprite.get_rect(center=(LARGURA//2,408+oscilacao)))
            self.texto(f'RECORDE: {self.recorde} - {self.nome_recorde}',
                       LARGURA//2,170,centro=True)
            self.texto('ESPACO ou clique para iniciar',LARGURA//2,650,centro=True)
        elif self.estado == 'JOGO':
            for obstaculo in self.obstaculos:
                obstaculo.desenhar(self.tela)
            self.chao.desenhar(self.tela)
            self.passaro.desenhar(self.tela)
            self.numero(self.pontos,20,45)
            vida_sprite = self.recursos.passaros[self.passaro.familia][0]
            for i in range(self.vidas):
                mini = pygame.transform.scale(vida_sprite,(26,20))
                self.tela.blit(mini,(LARGURA-35-i*30,50))
            medalha = self.medalha()
            if medalha:
                self.tela.blit(self.recursos.medalhas[medalha],(15,120))
            if self.especial:
                self.texto('FASE ESPECIAL!',LARGURA//2,95,(255,220,90),centro=True)
            if self.pausado:
                camada = pygame.Surface((LARGURA,ALTURA),pygame.SRCALPHA)
                camada.fill((0,0,0,155))
                self.tela.blit(camada,(0,0))
                self.texto('PAUSADO',LARGURA//2,360,grande=True,centro=True)
                self.texto('Pressione P para continuar',LARGURA//2,420,centro=True)
        else:  # GAMEOVER
            # Nesta tela, os elementos são posicionados em camadas:
            # chão, identificação do recordista, logotipo, moldura e placar.
            self.chao.desenhar(self.tela)
            # Recordista centralizado acima da imagem GAME OVER.
            # Durante a digitação, identifica a nova marca ainda não salva.
            if self.digitando:
                # Ainda não houve confirmação com Enter; não anunciamos
                # o nome do recordista anterior como dono da nova marca.
                titulo_recorde = 'NOVO RECORDE!'
                detalhe_recorde = f'{self.pontos} pontos - digite seu nome abaixo'
            else:
                # Após salvar (ou quando não há novo recorde), mostramos
                # os dados já registrados na memória do jogo.
                titulo_recorde = f'RECORDISTA: {self.nome_recorde}'
                detalhe_recorde = f'{self.recorde} pontos'
            # O parâmetro centro=True alinha o texto no eixo médio da tela.
            # Coordenadas verticais escolhidas para ficar acima de GAME OVER.
            self.texto(titulo_recorde, LARGURA // 2, 105,
                       (255, 215, 0), centro=True)
            self.texto(detalhe_recorde, LARGURA // 2, 135,
                       (255, 255, 255), centro=True)
            # Pisca a cada 0,5 s durante os primeiros 10 s.
            decorrido = time.monotonic()-self.fim_iniciado
            if decorrido >= 10 or int(decorrido*2)%2 == 0:
                img = self.recursos.gameover
                self.tela.blit(img,img.get_rect(center=(LARGURA//2,245)))
            # A moldura deve ser desenhada antes dos títulos e dos números,
            # caso contrário cobriria o conteúdo do placar.
            moldura = self.recursos.moldura
            self.tela.blit(moldura,moldura.get_rect(center=(LARGURA//2,450)))
            # Posicionamento do placar conforme as coordenadas escolhidas.
            # Os textos usam x=270 como ponto inicial (não centralizado).
            # Os algarismos começam em x=380 e usam metade do tamanho original.
            # PONTOS: texto (270, 375); valor (380, 410).
            # RECORDE: texto (270, 460); valor (380, 490).
            self.texto('PONTOS', 270, 375)
            self.numero(self.pontos, 380, 410, 0.5)
            self.texto('RECORDE', 270, 460)
            # Durante a digitação, a tela já mostra a pontuação candidata
            # ao novo recorde; a gravação efetiva ocorre apenas com Enter.
            self.numero(max(self.recorde, self.pontos), 380, 490, 0.5)
            # A medalha é posicionada dentro da moldura do GAME OVER.
            # Valores aprovados para esta tela: x=106, y=420.
            medalha = self.medalha()
            if medalha:
                self.tela.blit(self.recursos.medalhas[medalha], (106, 420))
            if self.digitando:
                # Campo de entrada simples: o nome é tratado por KEYDOWN.
                # O sublinhado funciona como cursor visual.
                self.texto('NOVO RECORDE! Digite seu nome:',
                           LARGURA//2,580,(255,225,90),centro=True)
                self.texto(self.nome_digitado+'_',LARGURA//2,615,centro=True)
                self.texto('ENTER para salvar',LARGURA//2,650,centro=True)
            else:
                self.texto('ESPACO ou clique para reiniciar',
                           LARGURA//2,630,centro=True)
        # A barra superior pertence a todos os estados do jogo; por isso,
        # está fora do if/elif/else de MENU, JOGO e GAMEOVER.
        pygame.draw.rect(self.tela,(45,50,60),(0,0,LARGURA,30))
        self.texto('S: Som '+('ON' if self.som_ativo else 'OFF'),8,5)
        self.texto('P: Pausa | ESC: Sair',LARGURA-220,5)
        self.texto(('FASE ESPECIAL' if self.especial else 'Tema: '+self.tema),
                   165,5,(255,225,90))
        # Renderização lógica 575x860 -> janela física sem alterar colisões.
        # A escala visual não altera a geometria lógica nem as colisões.
        ajustada = pygame.transform.scale(self.tela,self.janela.get_size())
        self.janela.blit(ajustada,(0,0))
        pygame.display.flip()

    def tratar_evento(self, evento):
        """Processa teclado, mouse, redimensionamento e saída.

        Retorna False para encerrar o loop principal do programa.
        """
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.VIDEORESIZE:
            self.janela = pygame.display.set_mode(
                (max(250,evento.w),max(350,evento.h)),pygame.RESIZABLE)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False
            if evento.key == pygame.K_s:
                self.som_ativo = not self.som_ativo
                if pygame.mixer.get_init():
                    if self.som_ativo: pygame.mixer.unpause()
                    else: pygame.mixer.pause()
            if evento.key == pygame.K_p and self.estado == 'JOGO':
                self.pausado = not self.pausado
            # Entrada de nome só ocorre quando a pontuação supera
            # o recorde anterior; Enter confirma a gravação em JSON.
            if self.estado == 'GAMEOVER' and self.digitando:
                if evento.key == pygame.K_RETURN:
                    # Só o Enter confirma o nome e dispara a escrita do JSON.
                    nome = self.nome_digitado.strip() or 'Anônimo'
                    if salvar_recorde(self.pontos,nome):
                        # Atualiza o recordista exibido apenas após gravar.
                        self.recorde,self.nome_recorde = self.pontos,nome
                    self.digitando = False
                elif evento.key == pygame.K_BACKSPACE:
                    self.nome_digitado = self.nome_digitado[:-1]
                elif len(self.nome_digitado)<20 and evento.unicode.isprintable():
                    self.nome_digitado += evento.unicode
                return True
            if evento.key == pygame.K_SPACE:
                self.acao_principal()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button in (1,3):
            # Clique na barra superior não é comando de pulo.
            y_logico = evento.pos[1]*ALTURA/max(1,self.janela.get_height())
            if y_logico > 30 and not self.digitando:
                self.acao_principal()
        return True

    def acao_principal(self):
        """Interpreta espaço/clique de acordo com o estado do jogo."""
        if self.estado == 'MENU': self.iniciar()
        elif self.estado == 'JOGO' and not self.pausado:
            self.passaro.pular()
            self.tocar('pulo')
        elif self.estado == 'GAMEOVER' and not self.digitando:
            self.reiniciar()

    def executar(self):
        """Loop principal: eventos, atualização, áudio e renderização.

        tick(FPS) controla a taxa de quadros e devolve o tempo decorrido.
        """
        rodando = True
        while rodando:
            dt = min(self.relogio.tick(FPS)/1000,0.1)
            for evento in pygame.event.get():
                if not self.tratar_evento(evento):
                    rodando = False
                    break
            if not rodando: break
            self.atualizar(dt,pygame.time.get_ticks())
            if self.estado == 'GAMEOVER' and self.contador_arcade < 3:
                agora = time.monotonic()
                if agora-self.fim_iniciado >= 3.5 and (self.ultimo_arcade == 0 or
                                                         agora-self.ultimo_arcade >= 2):
                    self.tocar('arcade')
                    self.ultimo_arcade = agora
                    self.contador_arcade += 1
            self.desenhar()
        pygame.quit()

# Este bloco só é executado quando o arquivo é iniciado diretamente.
# Ao importar o módulo em outro programa, a partida não começa sozinha.
if __name__ == '__main__':
    Jogo().executar()
