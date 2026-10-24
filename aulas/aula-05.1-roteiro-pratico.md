# Aula 05.1 — Roteiro prático: Sprint 05 — Executável e entrega final

**Disciplina:** Programação para Engenharia Mecânica — 2026.2  
**Projeto avaliativo 2:** Flappy Bird com Python e Pygame  
**Pré-requisito:** Aula 05.0 e Sprint 04 concluídas  
**Ambiente:** Windows, VSCode, PowerShell, Python 3.12 e `.venv`.

## Objetivo do roteiro

Ao final, o estudante deverá gerar e testar o arquivo **`FlappyBird.exe`**, preservando imagens, sons e recordes, registrar a Sprint 05 no GitHub e, quando houver autorização para redistribuição, publicar uma Release com o jogo pronto para download. Os comandos a seguir partem da estrutura real do projeto: `src/main.py`, `assets/imgs`, `assets/audio` e `data/recorde.json`.

> **Importante:** execute cada comando no terminal PowerShell do VSCode, a partir de `C:\Projetos\flappybird`, salvo indicação contrária. Não recrie o repositório Git nem substitua arquivos sem antes verificar o estado do projeto.

## Passo 1 — Abrir a pasta e ativar o ambiente virtual

```powershell
cd C:\Projetos\flappybird
.\.venv\Scripts\Activate.ps1
python --version
python -m pip --version
git status
```

**Explicação:** `cd` muda a pasta atual; `.venv` é o ambiente virtual do projeto; `git status` mostra arquivos modificados e evita perder alterações. Se o terminal já exibir `(.venv)`, não é necessário ativá-lo novamente.

## Passo 2 — Verificar se o jogo funciona no Python

```powershell
python -m py_compile src/main.py
python src/main.py
```

- `py_compile` verifica a sintaxe sem abrir a janela do jogo.
- `python src/main.py` inicia o jogo com Python e Pygame.

**Teste:** abra o menu, comece uma partida, pule, pause com **P**, alterne o som com **S**, encerre a partida e confira o GAME OVER. Não avance para o empacotamento se o jogo ainda apresentar erro na execução normal.

## Passo 3 — Instalar e verificar o PyInstaller

```powershell
python -m pip install pyinstaller
python -m PyInstaller --version
```

**Por que `python -m`?** O módulo será executado pelo Python do ambiente virtual ativo. Isso reduz a chance de chamar uma instalação de PyInstaller pertencente a outro interpretador.

## Passo 4 — Preparar o código para o executável

A versão da Sprint 04 define os caminhos assim:

```python
RAIZ = Path(__file__).resolve().parent.parent
IMAGENS = RAIZ / 'assets' / 'imgs'
AUDIOS = RAIZ / 'assets' / 'audio'
ARQUIVO_RECORDE = RAIZ / 'data' / 'recorde.json'
```

Esse cálculo é adequado quando `main.py` está em `src/`, mas precisa ser adaptado para o executável `--onefile`. Vamos **substituir somente o bloco de definição dos caminhos**, preservando as classes, a lógica do jogo e os comentários das aulas anteriores.

### 4.1. Acrescentar importações

No início de `src/main.py`, junto às demais importações, acrescente:

```python
import os   # Lê variáveis de ambiente, como LOCALAPPDATA no Windows.
import sys  # Permite identificar se o programa foi empacotado.
```

### 4.2. Substituir o bloco dos caminhos

Localize o trecho que começa com `RAIZ = Path(__file__).resolve().parent.parent` e termina em `ARQUIVO_RECORDE = ...`. Substitua-o por:

```python
# ================================================================
# CAMINHOS DE RECURSOS E DE DADOS PERSISTENTES
# ================================================================
# Recursos são imagens e sons: apenas lidos pelo jogo.
# Dados persistentes incluem o recorde: precisam ser graváveis.

if getattr(sys, 'frozen', False):
    # No executável PyInstaller, _MEIPASS é a pasta temporária
    # em que os recursos incorporados ao pacote são extraídos.
    RAIZ_RECURSOS = Path(sys._MEIPASS)

    # LOCALAPPDATA é uma pasta própria para dados de aplicativos
    # do usuário no Windows, independente da pasta do executável.
    pasta_local = os.environ.get('LOCALAPPDATA')
    if pasta_local:
        RAIZ_DADOS = Path(pasta_local) / 'FlappyBird'
    else:
        # Alternativa caso a variável não esteja definida.
        RAIZ_DADOS = Path.home() / 'AppData' / 'Local' / 'FlappyBird'
else:
    # No desenvolvimento, main.py está dentro da pasta src/.
    # parent.parent sobe até C:\Projetos\flappybird.
    RAIZ_RECURSOS = Path(__file__).resolve().parent.parent
    RAIZ_DADOS = RAIZ_RECURSOS

IMAGENS = RAIZ_RECURSOS / 'assets' / 'imgs'
AUDIOS = RAIZ_RECURSOS / 'assets' / 'audio'
ARQUIVO_RECORDE = RAIZ_DADOS / 'data' / 'recorde.json'
```

**Entenda o código:** `getattr(sys, 'frozen', False)` indica se a aplicação está empacotada. `Path(sys._MEIPASS)` localiza os arquivos incorporados. A pasta de recordes do `.exe` será `%LOCALAPPDATA%\FlappyBird\data\recorde.json`; no desenvolvimento, continuará sendo `C:\Projetos\flappybird\data\recorde.json`.

A função `salvar_recorde()` da Sprint 04 já utiliza `ARQUIVO_RECORDE.parent.mkdir(parents=True, exist_ok=True)`, portanto pode criar a pasta de dados quando necessário. **Não inclua `data/` no comando `--add-data`.**

### 4.3. Validar a alteração

```powershell
python -m py_compile src/main.py
python src/main.py
```

**Teste:** confirme que as imagens carregam e que o jogo continua funcionando no modo Python. A alteração dos caminhos não deve modificar física, pontuação, medalhas nem interface.

### 4.4. Código completo do `src/main.py` — copiar e colar

Para facilitar a execução do roteiro, apresentamos abaixo **o arquivo completo**, com os comentários didáticos, as classes e as funcionalidades da Sprint 04 preservadas. A única adaptação funcional em relação à versão congelada do código da Sprint 04 é o tratamento dos caminhos para o executável e para os recordes persistentes, explicado no Passo 4.2.

**Como utilizar:** no VSCode, abra `src/main.py`, faça uma cópia de segurança da versão atual, selecione todo o conteúdo (`Ctrl+A`), cole o código a seguir e salve (`Ctrl+S`). **Não é necessário executar as substituições dos Passos 4.1 e 4.2 separadamente se você optar por colar este código completo.**

```python
# ================================================================
# FLAPPY BIRD — SPRINT 04 AMPLIADA | Programação para Engenharia
# Código didático: classes, eventos, estados, sprites, áudio e JSON
# ================================================================
from pathlib import Path
import os   # Acessa LOCALAPPDATA para guardar dados persistentes no Windows.
import sys  # Detecta execução empacotada pelo PyInstaller.
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
# Os recursos (imagens/sons) são somente leitura; os recordes precisam
# de um diretório gravável e permanente, mesmo no modo --onefile.
if getattr(sys, 'frozen', False):
    # O PyInstaller extrai os recursos incorporados para esta pasta.
    RAIZ_RECURSOS = Path(sys._MEIPASS)
    # LOCALAPPDATA persiste entre execuções e não depende de onde o .exe está.
    pasta_local = os.environ.get('LOCALAPPDATA')
    RAIZ_DADOS = (Path(pasta_local) if pasta_local else Path.home() / 'AppData' / 'Local') / 'FlappyBird'
else:
    # main.py está em src/: subir duas pastas alcança a raiz do projeto.
    RAIZ_RECURSOS = Path(__file__).resolve().parent.parent
    RAIZ_DADOS = RAIZ_RECURSOS
IMAGENS = RAIZ_RECURSOS / 'assets' / 'imgs'
AUDIOS = RAIZ_RECURSOS / 'assets' / 'audio'
ARQUIVO_RECORDE = RAIZ_DADOS / 'data' / 'recorde.json'
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
```

**Conferência:** após colar, execute `python -m py_compile src/main.py` e `python src/main.py`. Confira o posicionamento aprovado do GAME OVER, as medalhas, os controles e a gravação dos recordes antes de gerar o `.exe`.

---

## Passo 5 — Conferir as pastas de recursos

```powershell
Test-Path .\assets\imgs\bg.png
Test-Path .\assets\imgs\Flappy_Bird_logo.png
Test-Path .\assets\audio
Test-Path .\src\main.py
```

Os caminhos essenciais devem existir. Os sons opcionais podem variar conforme o pacote didático. **O ícone `.ico` não é obrigatório.** Verifique sua existência antes de usá-lo:

```powershell
Test-Path .\assets\imgs\flappy_bird.ico
```

Se retornar `False`, use o comando de compilação **sem `--icon`**. Não basta renomear um PNG para `.ico`: é necessário um arquivo de ícone válido.

## Passo 6 — Gerar o executável do Windows

### 6.1. Comando principal, sem ícone opcional

Copie e execute **uma única linha**:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --name FlappyBird --add-data "assets;assets" src/main.py
```

### 6.2. Comando alternativo, se o arquivo `.ico` existir

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --icon "assets/imgs/flappy_bird.ico" --add-data "assets;assets" --name FlappyBird src/main.py
```

**Atenção:** os dois comandos são alternativas. Execute **apenas um deles**.

### 6.3. O que significa cada parâmetro?

| Parâmetro | Explicação |
|---|---|
| `python -m PyInstaller` | Executa o PyInstaller do Python ativo. |
| `--onefile` | Gera um único arquivo executável. |
| `--windowed` | Oculta a janela de console no aplicativo gráfico. |
| `--add-data "assets;assets"` | Inclui `assets/imgs` e `assets/audio` no pacote. |
| `--icon ...` | Define o ícone do executável, quando o `.ico` existe. |
| `--name FlappyBird` | Nomeia o executável `FlappyBird.exe`. |
| `--clean` | Limpa o cache de compilação. |
| `--noconfirm` | Permite substituir saídas anteriores. |
| `src/main.py` | Indica o arquivo Python que inicia o programa. |

A opção `--name FlappyBird` também define `build/FlappyBird/` e `FlappyBird.spec`. Sem essa opção, o nome seria baseado em `main.py`.

## Passo 7 — Encontrar o executável

Ao final da compilação, a estrutura esperada é:

```text
flappybird/
├── build/
│   └── FlappyBird/       # arquivos intermediários
├── dist/
│   └── FlappyBird.exe    # jogo empacotado
├── FlappyBird.spec       # configuração do PyInstaller
├── src/
│   └── main.py
└── ...
```

Verifique no PowerShell:

```powershell
Test-Path .\dist\FlappyBird.exe
Get-Item .\dist\FlappyBird.exe
```

`Test-Path` deverá retornar `True` se o arquivo foi gerado. `Get-Item` mostra informações do arquivo.

## Passo 8 — Testar o executável fora do VSCode

1. Abra a pasta `dist/` no Explorador de Arquivos.
2. Dê duplo clique em `FlappyBird.exe` e confirme que o jogo abre.
3. Copie **somente o `.exe`** para uma pasta de teste, por exemplo `C:\Projetos\TesteFlappyBird`, e execute-o novamente.
4. Confirme que o jogo não depende de `assets/` ao lado do `.exe`.
5. Teste menu, pulo, vidas, pausa, som, cenários, colisões, GAME OVER, medalha e reinício.
6. Supere o recorde, digite um nome e confirme com **Enter**.
7. Feche e reabra o executável para verificar se o recorde permanece.

Para verificar a pasta de recordes do executável:

```powershell
Test-Path "$env:LOCALAPPDATA\FlappyBird\data\recorde.json"
```

O resultado será `True` **depois que um recorde tiver sido salvo com sucesso**. O arquivo `data/recorde.json` da pasta do projeto permanece separado e ignorado pelo Git.

> **Observação:** o jogo só solicita o nome quando a pontuação supera o recorde atual. Para testar novamente sem apagar dados reais, utilize um usuário de teste ou faça uma cópia de segurança do JSON antes de modificá-lo.

## Passo 9 — Resolver possíveis erros de compilação

### 9.1. Diagnóstico: gerar temporariamente com console

Se o executável fechar sem explicar o erro, compile uma versão **sem `--windowed`**:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --name FlappyBirdDebug --add-data "assets;assets" src/main.py
```

Depois execute:

```powershell
.\dist\FlappyBirdDebug.exe
```

O terminal poderá mostrar a mensagem de erro. Depois de corrigir o problema, gere novamente a versão final com `--windowed`.

### 9.2. Limpeza opcional de arquivos antigos

Primeiro confirme a pasta atual:

```powershell
Get-Location
```

**Somente se estiver na raiz correta do projeto**, remova as saídas antigas:

```powershell
if (Test-Path .\build) { Remove-Item .\build -Recurse -Force }
if (Test-Path .\dist) { Remove-Item .\dist -Recurse -Force }
if (Test-Path .\FlappyBird.spec) { Remove-Item .\FlappyBird.spec -Force }
```

**Cuidado:** esses comandos apagam os diretórios e o arquivo indicados. Não execute se houver arquivos importantes nessas pastas ou se o `.spec` tiver sido personalizado. A limpeza **não é obrigatória** em toda compilação; `--clean` e `--noconfirm` já resolvem muitos casos de recompilação.

**Diferença importante:** `rmdir /s /q` é sintaxe típica do **CMD**, não a forma recomendada no PowerShell. Para esta aula, usamos `Remove-Item`.

## Passo 10 — Ajustar o `.gitignore`

Abra o `.gitignore` na raiz do repositório. **Preserve as regras existentes**, especialmente `/data/`, e acrescente as que ainda não estiverem presentes:

```gitignore
# Ambiente virtual e caches Python
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/

# Configurações locais do VSCode
.vscode/

# Dados locais do jogador
/data/

# Saídas geradas pelo PyInstaller
/build/
/dist/
*.spec
```

**Por que ignorar `dist/`?** O executável poderá ser distribuído separadamente por um GitHub Release, sem entrar no histórico comum do código-fonte. Se a equipe decidir versionar um `.spec` personalizado, será necessário ajustar essa regra.

### 10.1 — Confirmar que o recorde está ignorado

Execute no PowerShell, na raiz do projeto:

```powershell
git check-ignore -v data/recorde.json
```

**Exemplo de saída esperada:**

```text
.gitignore:19:/data/    data/recorde.json
```

**Como interpretar:** `.gitignore` identifica o arquivo que contém a regra; `19` é o número da linha (pode ser outro, conforme o conteúdo do seu arquivo); `/data/` é a regra aplicada; `data/recorde.json` é o arquivo verificado. A saída confirma a correspondência com a regra de exclusão, **mas não garante que o arquivo nunca tenha sido rastreado pelo Git**.

### 10.2 — Verificar se a pasta `data/` já está rastreada

```powershell
git ls-files data/
```

- **Sem saída:** nenhum arquivo dessa pasta está rastreado no índice atual do Git. Não é necessário executar comandos de remoção.
- **Com saída**, por exemplo `data/recorde.json`: o arquivo está rastreado, apesar da regra no `.gitignore`. Nesse caso, siga o procedimento abaixo.

### 10.3 — Deixar de rastrear arquivos de `data/` sem apagá-los do computador

**Execute esta etapa somente se o comando anterior listar arquivos.** Antes, confira se a pasta `data/` contém exclusivamente dados locais que não devem ser versionados.

```powershell
git rm -r --cached -- data/
```

**Explicação:** `git rm` prepara a remoção do índice do Git; `-r` aplica-se recursivamente à pasta; `--cached` mantém os arquivos no disco local; `--` separa as opções do caminho. A remoção será registrada no próximo commit. Não use `git rm -r data/` sem `--cached`, pois isso também pode remover arquivos da pasta de trabalho.

Confira o resultado antes de confirmar:

```powershell
git status
```

Os arquivos anteriormente rastreados aparecerão como exclusões **preparadas para commit**, embora permaneçam fisicamente em `data/`. Se o resultado estiver correto, registre a mudança:

```powershell
git add .gitignore
git commit -m "Deixa de versionar dados locais do jogo"
git push origin main
```

**Atenção:** esse procedimento não elimina cópias que já tenham sido publicadas em commits anteriores. Caso existam dados sensíveis no histórico, será necessário um procedimento específico de limpeza do histórico, que não faz parte desta aula. Se o `git status` mostrar alterações inesperadas, revise-as antes de executar `git commit`.

> **Observação sobre `.pytest_cache/` e `.vscode/`:** a primeira pasta contém cache de testes e normalmente não deve ser versionada; a segunda contém configurações locais do VSCode. Se futuramente for necessário compartilhar configurações didáticas da pasta `.vscode/`, ajuste a regra para permitir somente os arquivos escolhidos.

## Passo 11 — Atualizar documentação e registrar a Sprint 05 no Git

No `README.md`, **confira** se o roadmap da Sprint 05 já indica **testes, empacotamento e entrega** e se a seção de download aponta para `https://github.com/wilson-luciano/flappybird/releases`. O botão de download direto deve ser ativado somente após testar a Release publicada. O código-fonte original será licenciado sob MIT; recursos de terceiros conservam suas condições de uso. A pasta `tests/.gitkeep` permanece como reserva didática, sem testes automatizados nesta sprint.

### Criar o arquivo `LICENSE` (licença MIT)

A licença informa sob quais condições outras pessoas podem utilizar, estudar, modificar e redistribuir o **código original** do projeto. Nesta sprint, adotaremos a **MIT License**. O arquivo será criado na **raiz do projeto**, ao lado do `README.md`.

**No PowerShell (na raiz do projeto):** o comando `mkdir` cria **pastas**, não arquivos. Para criar o arquivo `LICENSE`, use `New-Item`:

```powershell
cd C:\Projetos\flappybird
New-Item -Path . -Name "LICENSE" -ItemType File
code LICENSE
```

O comando `code LICENSE` abre o arquivo no VSCode para colar o conteúdo a seguir. **Se o arquivo já existir, não repita `New-Item`**: abra-o diretamente com `code LICENSE`. Alternativamente, no Explorador do VSCode, clique com o botão direito na pasta `flappybird`, escolha **New File (Novo Arquivo)** e digite `LICENSE` (sem `.txt` ou `.md`).

Copie **todo o conteúdo abaixo** e cole no arquivo `LICENSE`:

```text
MIT License

Copyright (c) 2026 Wilson Luciano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Salve com **Ctrl+S**. Em seguida, no PowerShell, confirme que o arquivo existe e contém o texto:

```powershell
Test-Path .\LICENSE
Get-Content .\LICENSE
```

`Test-Path` deverá retornar `True`. Se retornar `False`, confira se o arquivo foi criado na pasta correta e se não recebeu uma extensão adicional.

> **Limite da licença:** a MIT deste projeto cobre o código original. Imagens, músicas, efeitos sonoros e outros materiais de terceiros podem possuir condições próprias e não passam automaticamente a ser MIT.

### Atualizar e conferir o `requirements.txt`

Antes de conferir as alterações no Git, atualize a lista de dependências a partir do **ambiente virtual do Flappy Bird**, que deve estar ativo no PowerShell (`(.venv)` no início do prompt):

```powershell
python -m pip freeze > requirements.txt
```

**Explicação:** `pip freeze` lista os pacotes instalados com suas versões; `>` grava essa lista em `requirements.txt`, **substituindo o conteúdo anterior**. Execute o comando somente com o ambiente virtual correto ativado. O arquivo pode incluir ferramentas de desenvolvimento, como `pyinstaller`, além das bibliotecas necessárias para executar o jogo.

Confira o conteúdo gerado:

```powershell
Get-Content requirements.txt
```

Para instalar as dependências registradas em um ambiente virtual novo, ou verificar se já estão instaladas no ambiente atual, utilize:

```powershell
python -m pip install -r requirements.txt
```

**Atenção:** `pip freeze > requirements.txt` **gera/atualiza** a lista; `pip install -r requirements.txt` **instala** os pacotes da lista. Esse arquivo facilita a reprodução do ambiente, mas não garante sozinho compatibilidade entre diferentes versões do Python ou sistemas operacionais.

Confira as alterações **sem abrir o visualizador LESS**:

```powershell
git status
git --no-pager diff --stat
```

**Explicação:** `git diff --stat` resume linhas inseridas e removidas. `--no-pager` exibe a saída diretamente no terminal, sem abrir o LESS. Se algum comando abrir o LESS e mostrar `(END)`, pressione **Q** para sair.

Prepare os arquivos desta sprint. Este comando é **um único `git add`**, com vários caminhos separados por espaços:

```powershell
git add src/main.py aulas/aula-05.0-testes-empacotamento-licenciamento-distribuicao.md aulas/aula-05.1-roteiro-pratico.md README.md requirements.txt .gitignore LICENSE
```

**Atenção à nomenclatura:** os comandos acima utilizam os nomes dos arquivos sem sufixos de versão, conforme a pasta local do projeto. Se algum nome for diferente, confira com `Get-ChildItem .\aulas\*05*` e ajuste o comando. O Git não adiciona caminhos inexistentes.

Antes de confirmar o commit, confira o que está preparado:

```powershell
git diff --cached --stat
git status
```

Se estiver correto:

```powershell
git commit -m "Conclui Sprint 05 com executavel e documentacao"
git push origin main
```

**Importante:** `git add` prepara arquivos; `git commit` registra a versão local; `git push` envia commits ao repositório remoto. O executável ignorado em `dist/` **não é enviado por esses comandos**.

## Passo 12 — Publicar o jogo pronto no GitHub Releases

A publicação do executável é **diferente** do envio do código com `git push`. O código, as aulas e o `README.md` ficam no repositório; o arquivo compilado será anexado a uma **Release**, que é a área do GitHub destinada a distribuir versões prontas de programas.

> **Pré-condição obrigatória:** antes de publicar o `.exe` em uma Release pública, confirme que as imagens, sons, fontes e demais recursos incluídos permitem redistribuição. Se as permissões não estiverem verificadas, **não publique o executável publicamente**. É possível realizar os testes localmente enquanto essa análise é feita.

### 12.1 — Verificar o executável antes da publicação

No PowerShell, na raiz do projeto:

```powershell
Test-Path .\dist\FlappyBird.exe
Get-Item .\dist\FlappyBird.exe
```

O primeiro comando deve retornar `True`. Execute `dist\FlappyBird.exe` e confirme: menu, salto, colisões, pontuação, áudio, pausa, GAME OVER, medalhas e persistência do recorde. Quando possível, repita o teste em outro computador Windows, sem Python instalado. Um arquivo `.exe` desconhecido pode gerar alertas do Windows SmartScreen; não oriente usuários a desativar proteções de segurança.

### 12.2 — Criar a primeira Release pela interface do GitHub

1. Envie antes as alterações do projeto usando os comandos do **Passo 11**.
2. Abra [o repositório oficial](https://github.com/wilson-luciano/flappybird), entre em **Releases** e clique em **Draft a new release**.
3. Em **Tag: Select tag**, digite **`v0.5.0`** e **selecione a opção de criar a nova tag** (por exemplo, *Create new tag: v0.5.0 on publish*). **Apenas digitar o texto não basta**: o campo deve deixar de mostrar `Select tag`. Se a tag já existir, selecione-a.
4. Em **Target**, mantenha **`main`**, verificando que contém os commits finais da Sprint 05.
5. Em **Release title**, escreva **`Flappy Bird — Primeira versão jogável`**.
6. Em **Release notes**, copie e cole o texto completo a seguir (não é necessário clicar em *Generate release notes*). Antes de publicar, ajuste qualquer funcionalidade que não tenha sido validada:

```markdown
# 🎮 Flappy Bird — Primeira versão jogável

Primeira versão jogável para Windows do projeto didático **Flappy Bird**, desenvolvido com **Python e Pygame**.

## Funcionalidades
- Controle do pássaro, obstáculos e colisões.
- Pontuação, vidas e recorde persistente.
- Pausa, efeitos sonoros e alternância de cenários.
- Tela de encerramento, medalhas e reinício da partida.

## Como jogar
1. Em **Assets**, clique em `FlappyBird.exe`.
2. Aguarde o download e verifique a procedência do arquivo.
3. Execute no Windows. Não é necessário instalar Python ou Pygame separadamente.

**Segurança:** o Windows pode apresentar um aviso do Microsoft Defender SmartScreen para aplicativos novos e sem assinatura digital. Verifique o arquivo com o antivírus e não desative as proteções do sistema.

## Licença e créditos
Código-fonte original sob licença MIT (arquivo `LICENSE`). Imagens e áudios de terceiros podem ter licenças próprias.

**Wilson Luciano** — Professor Titular e Pesquisador, Universidade Federal de Sergipe (UFS).  
Repositório: https://github.com/wilson-luciano/flappybird
```

7. Em **Attach binaries by dropping them here or selecting them**, clique para escolher o arquivo: no explorador do Windows, entre na pasta **`dist` do projeto**, selecione **`FlappyBird.exe`** e clique em **Abrir**. O caminho local do computador **não é publicado**: somente o arquivo anexado aparecerá na Release.
8. Aguarde o upload e confira que o anexo se chama exatamente **`FlappyBird.exe`**.
9. Em **Release label**, mantenha **None**; não selecione **Pre-release**.
10. Confira tag, branch, título, notas, arquivo anexado e permissões de redistribuição. Clique em **Publish release**.
11. Abra a página publicada e, em **Assets**, baixe o `.exe` para testar o arquivo distribuído, preferencialmente em outro computador Windows.

**Erro comum — "Make sure you have a valid tag" / "tag name can't be blank":** a tag não foi efetivamente selecionada. Volte ao campo **Select tag**, digite `v0.5.0` e **clique na opção de criação/seleção da tag**. É possível corrigir o rascunho sem descartá-lo.

**Atenção:** `v0.5.0` identifica a Release do jogo, não a versão dos documentos da aula. Para publicar outra versão do programa, utilize uma nova tag, por exemplo `v0.5.1`, em vez de sobrescrever silenciosamente a anterior.

### 12.2.1 — Aviso do Microsoft Defender SmartScreen

Ao executar um programa novo baixado da internet, o Windows pode mostrar **"O Windows protegeu o computador"**. Esse aviso pode estar relacionado à reputação ainda não estabelecida do aplicativo ou à ausência de assinatura digital; **não prova que o arquivo seja malicioso, mas também não garante que seja seguro**.

Antes de executar, confirme que o download veio da Release oficial e analise o arquivo com o **Microsoft Defender**. Se a procedência e a verificação forem satisfatórias, o Windows pode oferecer **Mais informações** e, conforme sua política de segurança, **Executar assim mesmo**. **Não desative o SmartScreen nem o antivírus**. Se houver detecção de ameaça ou dúvida sobre o arquivo, não o execute; procure orientação do professor.

### 12.3 — Criar o destaque de download no README

Após a Release estar publicada e o arquivo anexado com o nome exato `FlappyBird.exe`, **substitua o link provisório para Releases no início do `README.md` por este botão**, após testar o endereço:

```markdown
## 🎮 Baixe e jogue — Windows

[![Baixar Flappy Bird](https://img.shields.io/badge/Baixar-FlappyBird.exe-blue?style=for-the-badge)](https://github.com/wilson-luciano/flappybird/releases/latest/download/FlappyBird.exe)

O executável pode ser iniciado no Windows sem instalar Python ou Pygame.
Consulte a [página de versões](https://github.com/wilson-luciano/flappybird/releases) para informações e arquivos publicados.
```

O endereço utilizado acima corresponde ao repositório oficial do projeto. Para repositórios próprios dos alunos, adapte o endereço. O caminho `/releases/latest/download/FlappyBird.exe` funciona quando a Release mais recente elegível contém um arquivo com esse nome; Releases marcadas como *pre-release* não são necessariamente a versão `latest`. **Não divulgue o botão como download disponível antes de testar o link publicado.**

Para testar, abra a página inicial do repositório em uma janela anônima, clique no botão e confirme se o arquivo baixado é o esperado. Depois da alteração do README, registre-a:

```powershell
git add README.md
git commit -m "Destaca download do Flappy Bird no README"
git push origin main
```

### 12.4 — Por que não enviar `dist/` no commit?

A pasta `dist/` continua no `.gitignore`: ela contém artefatos gerados automaticamente. **GitHub Releases** permite disponibilizar o `FlappyBird.exe` para download sem colocar arquivos binários compilados no histórico do código-fonte. O visitante pode baixar o jogo pela página inicial e consultar o código e as aulas no mesmo repositório.

## Passo 13 — Preparar a entrega final

Entregue ao professor ou ao avaliador:

- Link do repositório GitHub, com o código-fonte e a documentação atualizados.
- Evidência de que o `FlappyBird.exe` abre e executa as funcionalidades principais.
- Resultado do teste de persistência do recorde.
- Executável em meio de entrega permitido, **somente após verificar a autorização para redistribuir os recursos incluídos**.

### Checklist de validação

- [ ] O jogo funciona com `python src/main.py`.
- [ ] O `src/main.py` passou no teste de sintaxe.
- [ ] Imagens e sons carregam no `.exe`.
- [ ] `dist/FlappyBird.exe` foi gerado.
- [ ] O `.exe` funciona fora da pasta do projeto.
- [ ] O recorde é salvo e permanece após reiniciar.
- [ ] A pasta `data/` está ignorada no Git.
- [ ] `README.md` e aulas estão atualizados.
- [ ] As permissões de distribuição dos recursos foram verificadas.
- [ ] Se autorizada, a Release foi publicada com `FlappyBird.exe` anexado.
- [ ] O botão do README foi testado e baixa o executável correto.

**Conclusão:** o projeto iniciado como script Python foi organizado, testado e empacotado como aplicação gráfica Windows. O aluno praticou desenvolvimento incremental, orientação a objetos, eventos, persistência, Git/GitHub e distribuição de software.
---

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame**.
