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
