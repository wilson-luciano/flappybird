# Aula 02.1 — Roteiro prático: Sprint 02 — Física e movimento

**Objetivo:** implementar gravidade, salto, animação do pássaro e desenho em coordenadas lógicas.  
**Pré-requisito:** Aula 01.1 concluída, com Pygame instalado e ambiente `.venv` ativo.  
**Versão do material:** 0.2.2

## Passo 1 — Abrir o projeto e ativar o ambiente

No terminal integrado do VS Code (PowerShell):

```powershell
cd C:\Projetos\flappybird
.\.venv\Scripts\Activate.ps1
python --version
python -m pip show pygame
```

Confira se o interpretador selecionado no VS Code pertence à pasta `.venv`. Não é necessário recriar o ambiente virtual.

## Passo 2 — Conferir as imagens e os áudios do projeto-base

Os recursos já acompanham o projeto-base obtido do GitHub na Aula 00.0. **Não é necessário extrair um segundo ZIP nem copiar os sprites manualmente.** Confira os arquivos utilizados nesta sprint:

```text
assets/
├── audio/
│   └── wing.wav
└── imgs/
    ├── bird1.png
    ├── bird2.png
    ├── bird3.png
    └── coordenadas-pygame.png
```

A pasta `assets/` também contém outras imagens e sons que serão utilizados nas próximas sprints. No PowerShell, confira:

```powershell
Get-ChildItem .\assets\imgs\bird*.png
Get-ChildItem .\assets\audio\
```

Os sprites `bird1.png`, `bird2.png` e `bird3.png` medem 34 × 24 pixels. A superfície lógica será redimensionada apenas na apresentação. **Não copie o código do jogo original:** o aluno desenvolverá o próprio `src/main.py` nesta aula.

## Passo 3 — Compreender a arquitetura desta sprint

Nesta etapa, `src/main.py` terá três responsabilidades principais:

1. **Eventos:** identificar a tecla Espaço e o fechamento da janela.
2. **Física:** atualizar velocidade, posição e limites do pássaro.
3. **Desenho:** compor a cena lógica e apresentá-la na janela adaptada.

O desenho ocorrerá sempre em `575 × 860` pixels lógicos. Somente a imagem final será reduzida quando necessário.

## Passo 4 — Substituir o conteúdo de `src/main.py`

Digite ou cole o programa completo abaixo. Os comentários `#` foram organizados por seções para facilitar a leitura, a depuração e a associação com os conteúdos de programação.

```python
# ============================================================
# PROJETO: FLAPPY BIRD
# DISCIPLINA: Programação para Engenharia Mecânica
# SPRINT 02: Física, salto e animação do pássaro
# ============================================================

# pathlib permite montar caminhos sem depender da pasta do terminal.
from pathlib import Path

# Biblioteca utilizada para janelas, eventos, imagens e desenho 2D.
import pygame


# ------------------------------------------------------------
# 1. CONFIGURAÇÕES DO JOGO
# ------------------------------------------------------------

# Resolução lógica de referência (independente do monitor).
LARGURA = 575
ALTURA = 860

# Limite de quadros por segundo.
FPS = 30

# Ocupa, no máximo, 85% das dimensões informadas pelo monitor.
FATOR_TELA = 0.85

# Parâmetros de movimento por quadro, em pixels lógicos.
GRAVIDADE = 1.1         # Incremento de velocidade a cada quadro.
IMPULSO = -8           # Velocidade vertical aplicada ao saltar.

# Coordenada vertical do topo do solo lógico.
ALTURA_SOLO = 760

# Número de quadros entre mudanças de sprite.
QUADROS_ANIMACAO = 5

# Localiza a raiz do projeto a partir deste arquivo (src/main.py).
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_IMAGENS = RAIZ_PROJETO / "assets" / "imgs"


# ------------------------------------------------------------
# 2. CLASSE RESPONSÁVEL PELO PÁSSARO
# ------------------------------------------------------------

class Passaro:
    """Armazena o estado e implementa o movimento do pássaro."""

    def __init__(self, imagens):
        # Lista de sprites que representam o bater de asas.
        self.imagens = imagens

        # Define posição inicial, usando números reais (float).
        self.x = 150.0
        self.y = 300.0

        # Começa em repouso vertical.
        self.velocidade_y = 0.0

        # Controla qual imagem será desenhada.
        self.indice_imagem = 0
        self.contador_animacao = 0

        # Obtém dimensões do sprite para tratar os limites.
        self.largura = imagens[0].get_width()
        self.altura = imagens[0].get_height()

    def pular(self):
        # No Pygame, velocidade negativa significa subir.
        self.velocidade_y = IMPULSO

    def atualizar(self):
        # Atualiza primeiro a velocidade e depois a posição.
        # Esse procedimento é um Euler semiexplícito simplificado.
        self.velocidade_y += GRAVIDADE
        self.y += self.velocidade_y

        # Impede que o pássaro ultrapasse o topo do cenário.
        if self.y < 0:
            self.y = 0
            self.velocidade_y = 0

        # Impede que a parte inferior atravesse o solo lógico.
        limite_inferior = ALTURA_SOLO - self.altura
        if self.y > limite_inferior:
            self.y = limite_inferior
            self.velocidade_y = 0

        # Conta os quadros para alternar os sprites.
        self.contador_animacao += 1
        if self.contador_animacao >= QUADROS_ANIMACAO:
            self.contador_animacao = 0
            self.indice_imagem = (
                self.indice_imagem + 1
            ) % len(self.imagens)

    def desenhar(self, superficie):
        # Escolhe a imagem correspondente ao quadro da animação.
        imagem = self.imagens[self.indice_imagem]

        # O desenho usa coordenadas inteiras em pixels lógicos.
        superficie.blit(imagem, (int(self.x), int(self.y)))


# ------------------------------------------------------------
# 3. CARREGAMENTO DAS IMAGENS
# ------------------------------------------------------------

def carregar_imagens():
    """Carrega os três sprites e preserva a transparência PNG."""

    imagens = []

    # Percorre os nomes dos três arquivos enviados.
    for numero in (1, 2, 3):
        caminho = PASTA_IMAGENS / f"bird{numero}.png"

        # Informa claramente quando falta algum arquivo.
        if not caminho.is_file():
            raise FileNotFoundError(
                f"Sprite não encontrado: {caminho}\n"
                "Copie bird1.png, bird2.png e bird3.png "
                "para assets/imgs/."
            )

        # convert_alpha() preserva transparência e otimiza desenho.
        imagem = pygame.image.load(str(caminho)).convert_alpha()
        imagens.append(imagem)

    return imagens


# ------------------------------------------------------------
# 4. FUNÇÃO PRINCIPAL
# ------------------------------------------------------------

def main():
    # Inicializa os módulos do Pygame.
    pygame.init()

    # Consulta a resolução informada pelo monitor.
    info = pygame.display.Info()
    largura_monitor = info.current_w
    altura_monitor = info.current_h

    # Calcula o fator de escala sem ultrapassar o tamanho lógico.
    escala_largura = largura_monitor * FATOR_TELA / LARGURA
    escala_altura = altura_monitor * FATOR_TELA / ALTURA
    escala = min(escala_largura, escala_altura, 1.0)

    # Obtém as dimensões físicas da janela (em pixels inteiros).
    largura_janela = int(LARGURA * escala)
    altura_janela = int(ALTURA * escala)

    # Cria a janela física adaptada ao monitor.
    tela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Flappy Bird — Sprint 02")

    # Cria uma superfície com resolução lógica FIXA.
    cenario = pygame.Surface((LARGURA, ALTURA))

    # As imagens são carregadas após a criação da janela.
    imagens = carregar_imagens()
    passaro = Passaro(imagens)

    # Cria o relógio e a variável de controle do loop.
    relogio = pygame.time.Clock()
    executando = True

    # --------------------------------------------------------
    # 5. LOOP PRINCIPAL DO JOGO
    # --------------------------------------------------------

    while executando:
        # 5.1. Processamento dos eventos do sistema e do teclado.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            # Um evento KEYDOWN de Espaço produz um salto.
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    passaro.pular()

        # 5.2. Atualização da física e da animação.
        passaro.atualizar()

        # 5.3. Desenho em coordenadas lógicas.
        cenario.fill((135, 206, 235))  # Fundo azul-claro.

        # Representa o solo com um retângulo verde.
        pygame.draw.rect(
            cenario,
            (70, 160, 80),
            (0, ALTURA_SOLO, LARGURA, ALTURA - ALTURA_SOLO),
        )

        # Desenha o pássaro sobre o cenário lógico.
        passaro.desenhar(cenario)

        # 5.4. Escalonamento apenas da imagem final.
        imagem_final = pygame.transform.scale(
            cenario, (largura_janela, altura_janela)
        )
        tela.blit(imagem_final, (0, 0))
        pygame.display.flip()

        # Mantém o limite de até 30 quadros por segundo.
        relogio.tick(FPS)

    # Encerra o Pygame depois que o loop termina.
    pygame.quit()


# ------------------------------------------------------------
# 6. PONTO DE ENTRADA DO PROGRAMA
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
```

## Passo 5 — Executar o jogo

Com `.venv` ativo e estando na raiz do projeto:

```powershell
python src/main.py
```

**Resultado esperado:** janela azul-clara adaptada ao monitor; um pássaro animado próximo da esquerda; uma faixa verde representando o solo. O pássaro começa a cair, sobe ao pressionar **Espaço** e volta a cair. Ele não atravessa o topo nem o solo. A janela fecha normalmente pelo botão **X** (ou **Alt+F4** no Windows).

**Se aparecer `FileNotFoundError`:** confira se os arquivos estão em `assets/imgs/` e não em `imgs/`, `assets/` ou em uma pasta duplicada `FlappyBird/FlappyBird/`.

## Passo 6 — Interpretar a física e o escalonamento

A atualização usa as equações discretas:

$$
v_{k+1}=v_k+1{,}1
$$

$$
y_{k+1}=y_k+v_{k+1}
$$

A velocidade negativa indica subida, pois o eixo `y` cresce para baixo. O salto altera a velocidade para `-8` pixels por quadro. A aceleração adotada é expressa em pixels por quadro ao quadrado, **não em m/s²**.

A superfície `cenario` permanece com `575 × 860` pixels, mesmo que a janela física seja menor. O redimensionamento da imagem final **não modifica os valores de `self.x`, `self.y` ou `self.velocidade_y`**.

## Passo 7 — Conferir a estrutura do projeto

A organização relevante nesta etapa é:

```text
flappybird/
├── .venv/                 # ambiente local, ignorado pelo Git
├── assets/
│   ├── audio/             # sons já disponíveis para as próximas etapas
│   └── imgs/
│       ├── bird1.png
│       ├── bird2.png
│       └── bird3.png
├── aulas/
│   ├── aula-00.0-obtencao-projeto-github.md
│   ├── aula-01.0-planejamento-ambiente.md
│   ├── aula-01.1-roteiro-pratico.md
│   ├── aula-02.0-fisica-movimento.md
│   └── aula-02.1-roteiro-pratico.md
├── docs/
│   ├── sprints/
│   │   └── sprint-02-fisica-movimento.md
│   └── roadmap.md
├── src/
│   └── main.py
├── tests/
│   └── .gitkeep
├── .gitignore
├── README.md
└── requirements.txt
```

_A árvore é resumida: outros arquivos das sprints e demais aulas continuam no projeto._ As pastas `assets/imgs/` e `assets/audio/` já possuem arquivos versionáveis; não precisam de `.gitkeep`.

## Passo 8 — Validar a Sprint 02

- [ ] O Pygame abre sem erro de importação.
- [ ] Os três sprites são carregados de `assets/imgs/`.
- [ ] O pássaro alterna visualmente as imagens das asas.
- [ ] Sem saltar, o pássaro acelera para baixo.
- [ ] A tecla **Espaço** aplica impulso de subida.
- [ ] O pássaro não ultrapassa o topo ou o solo.
- [ ] A janela permanece proporcional e o botão **X** funciona.
- [ ] O código separa eventos, física e desenho.

Consulte também [`Sprint 02 — Física e movimento`](../docs/sprints/sprint-02-fisica-movimento.md) para registrar evidências e pendências.

## Passo 9 — Registrar a evolução no Git

No terminal, após validar a execução:

```powershell
git status
git add src/main.py
git add aulas/aula-02.0-fisica-movimento.md aulas/aula-02.1-roteiro-pratico.md
git commit -m "Sprint 02: fisica, salto e animacao do passaro"
```

**Atenção:** os sprites já recebidos e versionados no projeto-base não precisam ser adicionados novamente se não sofreram alterações. Se o professor distribuir recursos com restrições de licença, **não publique esses arquivos no GitHub** antes de confirmar a autorização. Nesse caso, registre apenas o código e as instruções de obtenção dos recursos, conforme a orientação da turma.

## Passo 10 — Desafios de fixação

1. Altere `GRAVIDADE` de `1.1` para `0.8` e compare a trajetória.
2. Altere `IMPULSO` de `-8` para `-10` e observe a altura do salto.
3. Altere `QUADROS_ANIMACAO` de `5` para `3`. O que muda?
4. Identifique no código as funções, a classe, os métodos, os laços e as condicionais.
5. Explique por que não multiplicamos a gravidade pelo fator de escala da janela.

## Continuidade

Nesta Sprint 02, tocar o solo apenas limita a posição do pássaro; a condição de derrota será implementada posteriormente.

Na **Sprint 03**, adicionaremos os canos, o deslocamento horizontal dos obstáculos, colisões e pontuação. As imagens `pipe.png`, `background.png` e `base.png` do pacote original serão úteis nessa etapa. Os demais efeitos sonoros e cenários alternativos serão abordados na Sprint 04.

---

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame** · **Versão 0.2.2**.
