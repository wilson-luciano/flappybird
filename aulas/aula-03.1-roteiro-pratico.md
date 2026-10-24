# Aula 03.1 — Roteiro prático: Sprint 03 — Obstáculos, colisões e pontuação

**Disciplina:** Programação para Engenharia Mecânica — 2026.2  
**Projeto avaliativo 2:** Flappy Bird com Python e Pygame  
**Pré-requisito:** Aula 02.1 concluída; Pygame instalado; `.venv` criado.  
**Versão do material:** 0.3.0

## Passo 1 — Abrir o projeto e conferir o ambiente

No terminal integrado do VS Code (PowerShell):

```powershell
cd C:\Projetos\flappybird
.\.venv\Scripts\Activate.ps1
python --version
python -m pip show pygame
git status
```

A Sprint 02 deve estar funcional. **Não recrie o ambiente virtual** e não substitua os arquivos de outras aulas.

## Passo 2 — Verificar as imagens distribuídas com o projeto-base

Os recursos já acompanham o projeto obtido pelo GitHub. Confirme:

```powershell
Get-ChildItem .\assets\imgs\bird*.png
Test-Path .\assets\imgs\pipe.png
```

O segundo comando deve retornar `True`. Nesta sprint utilizaremos `bird1.png`, `bird2.png`, `bird3.png` e `pipe.png`. Não é necessário copiar arquivos de outro ZIP.

## Passo 3 — Entender o que será acrescentado

| Elemento | Função |
|---|---|
| `Cano` | Representa um par de obstáculos com uma passagem livre |
| `random.randint()` | Sorteia a altura da passagem |
| `colliderect()` | Detecta sobreposição de retângulos |
| `pygame.mask` | Confirma colisões entre pixels não transparentes |
| `cano.passou` | Impede pontuação duplicada |
| `estado` | Controla menu, partida e fim de jogo |
| `nova_partida()` | Reinicia os objetos sem reiniciar o Python |

**Decisão didática:** nesta Sprint 03, uma colisão encerra a partida. Vidas, sons e temas alternativos serão incorporados posteriormente.

## Passo 4 — Atualizar `src/main.py`

Faça uma cópia de segurança ou um commit do código da Sprint 02 antes da alteração. Em seguida, substitua o conteúdo de `src/main.py` pelo programa abaixo. Os comentários `#` mostram as responsabilidades de cada seção.

```python
# ============================================================
# PROJETO: FLAPPY BIRD | SPRINT 03
# Obstáculos, colisões, pontuação e estados do jogo
# ============================================================

from pathlib import Path
import random
import pygame

# 1. CONSTANTES E CAMINHOS
LARGURA = 575
ALTURA = 860
FPS = 30
FATOR_TELA = 0.85
GRAVIDADE = 1.1
IMPULSO = -8
ALTURA_SOLO = 760
QUADROS_ANIMACAO = 5
VELOCIDADE_CANOS = 4
ABERTURA_CANOS = 290
DISTANCIA_CANOS = 300
# False: colisão por retângulos; True: colisão por máscaras.
USAR_MASCARAS = True

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_IMAGENS = RAIZ_PROJETO / "assets" / "imgs"


def carregar_imagem(nome):
    """Carrega um PNG preservando sua transparência."""
    caminho = PASTA_IMAGENS / nome
    if not caminho.is_file():
        raise FileNotFoundError(f"Imagem ausente: {caminho}")
    return pygame.image.load(str(caminho)).convert_alpha()


# 2. CLASSE DO PÁSSARO: MANTÉM A FÍSICA DA SPRINT 02
class Passaro:
    def __init__(self, imagens):
        self.imagens = imagens
        self.x = 150.0
        self.y = 300.0
        self.velocidade_y = 0.0
        self.indice_imagem = 0
        self.contador_animacao = 0
        self.largura = imagens[0].get_width()
        self.altura = imagens[0].get_height()

    def pular(self):
        # No sistema gráfico, velocidade negativa significa subir.
        self.velocidade_y = IMPULSO

    def atualizar(self):
        # Euler semiexplícito: primeiro velocidade, depois posição.
        self.velocidade_y += GRAVIDADE
        self.y += self.velocidade_y
        # Atualiza o quadro da animação a cada cinco iterações.
        self.contador_animacao += 1
        if self.contador_animacao >= QUADROS_ANIMACAO:
            self.contador_animacao = 0
            self.indice_imagem = (self.indice_imagem + 1) % len(self.imagens)

    def imagem_atual(self):
        return self.imagens[self.indice_imagem]

    def retangulo(self):
        # O mesmo arredondamento é usado para desenhar e colidir.
        return pygame.Rect(int(self.x), int(self.y), self.largura, self.altura)

    def desenhar(self, superficie):
        superficie.blit(self.imagem_atual(), self.retangulo().topleft)


# 3. CLASSE CANO: UM OBJETO REPRESENTA UM PAR
class Cano:
    def __init__(self, x, imagem_cano):
        self.x = float(x)
        self.imagem_inferior = imagem_cano
        # O cano superior é uma cópia invertida verticalmente.
        self.imagem_superior = pygame.transform.flip(imagem_cano, False, True)
        self.largura = imagem_cano.get_width()
        self.altura = imagem_cano.get_height()
        # Escolhe a borda superior da passagem livre.
        self.topo_passagem = random.randint(150, 400)
        self.passou = False  # Evita contabilizar duas vezes.

    def atualizar(self):
        self.x -= VELOCIDADE_CANOS

    def retangulos(self):
        x = int(self.x)
        # Cano de cima termina exatamente no topo da passagem.
        superior = self.imagem_superior.get_rect(
            topleft=(x, self.topo_passagem - self.altura)
        )
        # Cano de baixo começa após a abertura vertical.
        inferior = self.imagem_inferior.get_rect(
            topleft=(x, self.topo_passagem + ABERTURA_CANOS)
        )
        return superior, inferior

    def desenhar(self, superficie):
        superior, inferior = self.retangulos()
        superficie.blit(self.imagem_superior, superior.topleft)
        superficie.blit(self.imagem_inferior, inferior.topleft)

    def colide_com(self, passaro):
        ret_passaro = passaro.retangulo()
        ret_superior, ret_inferior = self.retangulos()
        # Primeiro teste: caixas retangulares (rápido).
        for imagem, ret_cano in (
            (self.imagem_superior, ret_superior),
            (self.imagem_inferior, ret_inferior),
        ):
            if not ret_passaro.colliderect(ret_cano):
                continue
            if not USAR_MASCARAS:
                return True
            # Segundo teste: apenas pixels opacos dos PNGs.
            mascara_passaro = pygame.mask.from_surface(passaro.imagem_atual())
            mascara_cano = pygame.mask.from_surface(imagem)
            deslocamento = (
                ret_cano.x - ret_passaro.x,
                ret_cano.y - ret_passaro.y,
            )
            if mascara_passaro.overlap(mascara_cano, deslocamento) is not None:
                return True
        return False


# 4. FUNÇÕES DE CONTROLE DO JOGO
def nova_partida(imagens_passaro, imagem_cano):
    """Reinicia os objetos e o placar, sem fechar a janela."""
    passaro = Passaro(imagens_passaro)
    canos = [Cano(LARGURA + 25, imagem_cano)]
    pontos = 0
    return passaro, canos, pontos


def desenhar_texto(superficie, texto, tamanho, y, cor=(255, 255, 255)):
    """Desenha uma mensagem centralizada horizontalmente."""
    fonte = pygame.font.Font(None, tamanho)
    imagem = fonte.render(texto, True, cor)
    x = (LARGURA - imagem.get_width()) // 2
    superficie.blit(imagem, (x, y))


def main():
    pygame.init()
    # Mantém a adaptação da janela física da Sprint 01.
    info = pygame.display.Info()
    escala = min(
        info.current_w * FATOR_TELA / LARGURA,
        info.current_h * FATOR_TELA / ALTURA,
        1.0,
    )
    largura_janela = max(1, int(LARGURA * escala))
    altura_janela = max(1, int(ALTURA * escala))
    tela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Flappy Bird — Sprint 03")
    cenario = pygame.Surface((LARGURA, ALTURA))

    # Carrega os recursos já presentes no projeto-base.
    imagens_passaro = [carregar_imagem(f"bird{i}.png") for i in (1, 2, 3)]
    imagem_cano = carregar_imagem("pipe.png")
    passaro, canos, pontos = nova_partida(imagens_passaro, imagem_cano)
    estado = "MENU"  # MENU, JOGO ou GAMEOVER
    relogio = pygame.time.Clock()
    executando = True

    while executando:
        # 5.1. Eventos: fechamento, início, salto e reinício.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False
                elif evento.key == pygame.K_SPACE:
                    if estado == "MENU":
                        estado = "JOGO"
                        passaro.pular()
                    elif estado == "JOGO":
                        passaro.pular()
                    elif estado == "GAMEOVER":
                        passaro, canos, pontos = nova_partida(
                            imagens_passaro, imagem_cano
                        )
                        estado = "JOGO"
                        passaro.pular()

        # 5.2. Física e regras só são atualizadas durante o jogo.
        if estado == "JOGO" and executando:
            passaro.atualizar()
            for cano in canos:
                cano.atualizar()

            # Cria um novo par quando o último avançou o suficiente.
            if canos[-1].x <= LARGURA - DISTANCIA_CANOS:
                canos.append(Cano(LARGURA, imagem_cano))

            # Retira obstáculos inteiramente fora da tela.
            canos = [cano for cano in canos if cano.x + cano.largura >= 0]

            # Testa limites físicos e canos ANTES de atribuir pontos.
            bateu_limite = passaro.y < 0 or passaro.y + passaro.altura >= ALTURA_SOLO
            bateu_cano = any(cano.colide_com(passaro) for cano in canos)
            if bateu_limite or bateu_cano:
                estado = "GAMEOVER"
            else:
                for cano in canos:
                    # Pontua somente após o par ficar totalmente atrás do pássaro.
                    if not cano.passou and cano.x + cano.largura < passaro.x:
                        cano.passou = True
                        pontos += 1

        # 5.3. Desenha tudo em coordenadas lógicas.
        cenario.fill((135, 206, 235))
        for cano in canos:
            cano.desenhar(cenario)
        pygame.draw.rect(
            cenario, (70, 160, 80),
            (0, ALTURA_SOLO, LARGURA, ALTURA - ALTURA_SOLO),
        )
        passaro.desenhar(cenario)
        desenhar_texto(cenario, f"PONTOS: {pontos}", 44, 35)

        if estado == "MENU":
            desenhar_texto(cenario, "FLAPPY BIRD", 65, 175)
            desenhar_texto(cenario, "ESPACO para iniciar", 35, 245)
        elif estado == "GAMEOVER":
            desenhar_texto(cenario, "FIM DE JOGO", 65, 195)
            desenhar_texto(cenario, "ESPACO para reiniciar", 35, 270)

        # 5.4. Ajusta apenas a imagem final ao tamanho da janela.
        imagem_final = pygame.transform.scale(
            cenario, (largura_janela, altura_janela)
        )
        tela.blit(imagem_final, (0, 0))
        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
```

## Passo 5 — Executar e observar

```powershell
python src/main.py
```

**Resultado esperado:** aparece o menu; **Espaço** inicia o jogo e faz o pássaro saltar; pares de canos atravessam a tela da direita para a esquerda; o placar aumenta quando um par é completamente ultrapassado; tocar no teto, no solo ou em um cano apresenta **FIM DE JOGO**; **Espaço** reinicia a partida. **Esc** ou **X** fecha a janela.

## Passo 6 — Comparar os dois métodos de colisão

No início do código, altere temporariamente:

```python
USAR_MASCARAS = False  # Colisão apenas por retângulos.
```

Execute e observe a aproximação do pássaro às bordas dos canos. Depois, altere para:

```python
USAR_MASCARAS = True  # Retângulos + verificação por pixels opacos.
```

Execute novamente. **Pergunta:** por que os retângulos podem indicar contato antes de as partes visíveis das imagens se tocarem? Registre sua resposta.

**Nota técnica:** neste código, a máscara do pássaro é criada a partir do sprite exibido, sem rotação. Em uma evolução com rotação, imagem desenhada e máscara devem permanecer coerentes.

## Passo 7 — Testar a pontuação

Observe que cada objeto `Cano` possui `passou = False` inicialmente. Quando sua borda direita fica atrás da borda esquerda do pássaro, o programa altera `passou` para `True` e soma um ponto. Assim, o mesmo par não pontua novamente.

**Experimento:** aumente temporariamente `ABERTURA_CANOS` para `350` e reduza `VELOCIDADE_CANOS` para `3`. Isso facilitará atravessar os obstáculos e testar a pontuação. Depois, restaure os valores originais.

## Passo 8 — Validar a Sprint 03

- [ ] Os sprites da Sprint 02 continuam animados.
- [ ] Os canos são criados em pares e se movem continuamente.
- [ ] A abertura entre canos varia sem invadir o solo.
- [ ] Os obstáculos antigos são removidos da lista.
- [ ] O aluno comparou `pygame.Rect` e `pygame.mask`.
- [ ] A colisão encerra a partida.
- [ ] Cada par ultrapassado soma apenas um ponto.
- [ ] **Espaço** inicia, faz saltar e reinicia conforme o estado.
- [ ] O jogo encerra corretamente pelo **X**.

Confira também [`docs/sprints/sprint-03-obstaculos-colisoes-pontuacao.md`](../docs/sprints/sprint-03-obstaculos-colisoes-pontuacao.md) e registre as evidências solicitadas.

## Passo 9 — Registrar as alterações no Git

Execute na raiz do projeto:

```powershell
git status
git add src/main.py
git add aulas/aula-03.0-obstaculos-colisoes-pontuacao.md aulas/aula-03.1-roteiro-pratico.md
git commit -m "Sprint 03: obstaculos, colisoes e pontuacao"
git status
```

Os sprites já pertencem ao projeto-base; portanto, não é necessário adicioná-los novamente se não foram modificados. **Não execute `git push` automaticamente:** o envio ao repositório remoto deverá seguir a orientação da turma e as permissões de redistribuição dos recursos.

## Passo 10 — Desafios de fixação

1. Altere `DISTANCIA_CANOS` para `360`. Qual é o efeito sobre a frequência de obstáculos?
2. Altere `ABERTURA_CANOS` para `250`. A passagem fica mais fácil ou mais difícil?
3. Explique por que o código usa `random.randint(150, 400)` para a borda superior da abertura.
4. Identifique a classe `Cano`, seus atributos, seus métodos e as instâncias criadas.
5. Descreva o que aconteceria se a variável `passou` fosse eliminada.
6. Explique por que o programa só concede pontos quando `estado == "JOGO"` e não ocorreu colisão.
7. Indique onde o código usa listas, laços, condicionais, funções e programação orientada a objetos.

## Continuidade

Na **Sprint 04**, serão incorporados recursos avançados do gabarito, como alternância de cenários, sons, variações de sprites e regras adicionais. O sistema de vidas também poderá ser introduzido nessa etapa, preservando a progressão didática.

---

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame** · **Versão 0.3.0**.
