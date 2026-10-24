# Aula 03.0 — Obstáculos, colisões e pontuação

**Disciplina:** Programação para Engenharia Mecânica — 2026.2  
**Projeto avaliativo 2:** Flappy Bird com Python e Pygame  
**Sprint:** 03 — Obstáculos, colisões e pontuação  
**Versão do material:** 0.3.0

## 1. Objetivos de aprendizagem

Ao final desta aula, o estudante deverá ser capaz de:

1. Modelar obstáculos com classes, atributos e métodos.
2. Empregar geração pseudoaleatória para criar passagens de dificuldade controlada.
3. Descrever movimento horizontal em uma simulação por quadros.
4. Comparar colisão por retângulos (`pygame.Rect`) e por máscaras (`pygame.mask`).
5. Contabilizar pontos uma única vez por par de obstáculos ultrapassado.
6. Implementar estados de jogo: **MENU**, **JOGO** e **GAMEOVER**.
7. Validar os critérios da Sprint 03 e registrar alterações no Git.

## 2. Continuidade da Sprint 02

Na Sprint 02, implementamos a classe `Passaro`, a gravidade, o salto por **Espaço**, a animação com três sprites e o desenho em uma superfície lógica de **575 × 860 pixels**. Nesta sprint, preservaremos essa arquitetura e acrescentaremos pares de canos, colisões, pontuação e reinício.

**Decisão desta versão didática:** uma colisão encerra a partida. O sistema de seis vidas do gabarito ampliado será estudado em sprint posterior. Isso reduz o número de conceitos simultâneos e permite concentrar a aprendizagem em objetos, condições e estados.

Documento de acompanhamento: [`Sprint 03`](../docs/sprints/sprint-03-obstaculos-colisoes-pontuacao.md).

## 3. Representação de um par de canos

Cada obstáculo é composto por um cano superior e outro inferior. Os dois têm a mesma coordenada horizontal `x`; a passagem livre fica entre eles.

Definiremos:

```python
VELOCIDADE_CANOS = 4   # Deslocamento horizontal em pixels lógicos por quadro.
ABERTURA_CANOS = 290   # Espaço vertical livre entre os canos.
DISTANCIA_CANOS = 300 # Distância horizontal entre pares sucessivos.
```

A classe `Cano` terá os atributos `x`, `altura_passagem`, `passou` e as imagens dos canos. O atributo booleano `passou` impedirá que um mesmo obstáculo gere vários pontos.

### 3.1. Geração da passagem

A biblioteca `random` permite escolher uma posição vertical pseudoaleatória:

```python
import random

topo_passagem = random.randint(150, 400)
base_passagem = topo_passagem + ABERTURA_CANOS
```

Nesse exemplo, `topo_passagem` é a borda superior da abertura, **não** o topo do cano. Como `ALTURA_SOLO = 760`, a maior borda inferior será `400 + 290 = 690`, deixando 70 pixels antes do solo. O intervalo pode ser ajustado para aumentar ou reduzir a dificuldade.

## 4. Movimento dos obstáculos

A cada quadro, o par de canos desloca-se para a esquerda:

```python
self.x -= VELOCIDADE_CANOS
```

Um obstáculo pode ser removido quando sua borda direita estiver fora da tela:

```python
if cano.x + cano.largura < 0:
    canos.remove(cano)
```

**Atenção:** não é recomendável remover elementos de uma lista enquanto ela está sendo percorrida diretamente. Na prática, criaremos uma nova lista por compreensão:

```python
canos = [cano for cano in canos if cano.x + cano.largura >= 0]
```

Para gerar novos pares, verificaremos a posição do último obstáculo. O espaçamento será medido entre as coordenadas `x` dos pares consecutivos.

## 5. Colisões: retângulos e máscaras

### 5.1. Primeiro nível — `pygame.Rect`

Um retângulo delimita uma região de largura e altura definidas. A função `colliderect()` retorna `True` quando dois retângulos se sobrepõem:

```python
if retangulo_passaro.colliderect(retangulo_cano):
    print("Colisão detectada")
```

Esse método é simples, rápido e apropriado para introduzir **geometria computacional**. Entretanto, a caixa retangular pode incluir pixels transparentes do sprite, produzindo colisões visuais antecipadas.

### 5.2. Segundo nível — `pygame.mask`

Uma máscara representa os pixels não transparentes de uma superfície. O método `overlap()` verifica a sobreposição entre duas máscaras e retorna uma posição de contato ou `None`.

```python
mascara_passaro = pygame.mask.from_surface(imagem_passaro)
mascara_cano = pygame.mask.from_surface(imagem_cano)

# O deslocamento deve ser calculado nas mesmas coordenadas das imagens.
offset = (x_cano - x_passaro, y_cano - y_passaro)
colidiu = mascara_passaro.overlap(mascara_cano, offset) is not None
```

**Importante:** se o sprite for rotacionado, a máscara deverá corresponder à **imagem efetivamente desenhada**, com sua posição real. Nesta sprint, o pássaro não será rotacionado, simplificando a correspondência entre imagem, máscara e posição.

**Progressão pedagógica:** primeiro testaremos os retângulos; depois utilizaremos máscaras como verificação mais precisa. A Aula 03.1 apresentará as duas abordagens, com uma opção para alternar entre elas.

## 6. Pontuação sem duplicidade

A pontuação aumenta quando o pássaro ultrapassa completamente um par de canos, sem colidir. A condição de passagem será:

```python
if not cano.passou and cano.x + cano.largura < passaro.x:
    cano.passou = True
    pontos += 1
```

A variável `cano.passou` muda de `False` para `True` no primeiro registro. Assim, mesmo que o jogo continue executando dezenas de quadros após a ultrapassagem, o ponto não será contabilizado novamente.

**Observação:** usamos a borda esquerda do pássaro como referência. É uma regra didática objetiva; outras versões podem considerar o centro ou a borda direita, desde que a regra seja documentada.

## 7. Estados do jogo

Uma variável `estado` determina o comportamento do programa:

| Estado | O que acontece | Ação do jogador |
|---|---|---|
| `MENU` | Exibe instruções; física e obstáculos ficam parados | Espaço inicia |
| `JOGO` | Atualiza física, canos, colisões e pontos | Espaço faz o pássaro saltar |
| `GAMEOVER` | Congela a partida e exibe a pontuação final | Espaço reinicia |

Esse mecanismo evita misturar condições de início, execução e encerramento no mesmo trecho de código. Na Aula 03.1, uma função `nova_partida()` concentrará a inicialização dos objetos e do placar.

## 8. Organização dos recursos

Os arquivos necessários já acompanham o projeto-base obtido pelo GitHub:

```text
flappybird/
├── assets/
│   └── imgs/
│       ├── bird1.png
│       ├── bird2.png
│       ├── bird3.png
│       ├── pipe.png
│       └── base.png
├── aulas/
│   ├── aula-03.0-obstaculos-colisoes-pontuacao.md
│   └── aula-03.1-roteiro-pratico.md
├── docs/
│   └── sprints/
│       └── sprint-03-obstaculos-colisoes-pontuacao.md
└── src/
    └── main.py
```

A imagem `pipe_night.png`, os cenários alternativos e os efeitos sonoros serão utilizados em evoluções posteriores. **Não é necessário extrair imagens de outro ZIP.** A publicação pública desses recursos depende da confirmação das respectivas licenças.

## 9. Critérios de aceitação da Sprint 03

- [ ] O pássaro mantém gravidade, salto e animação da Sprint 02.
- [ ] Os canos aparecem em pares com abertura livre controlada.
- [ ] Os obstáculos se deslocam para a esquerda e novos pares são gerados.
- [ ] Obstáculos fora da tela são removidos da lista.
- [ ] O aluno consegue demonstrar a diferença entre colisão retangular e por máscara.
- [ ] Colisão com canos, teto ou solo encerra a partida.
- [ ] Cada par superado concede exatamente um ponto.
- [ ] A partida inicia e reinicia sem reiniciar o processo Python.
- [ ] O programa fecha pelo botão **X** e o progresso foi registrado no Git.

## 10. Atividades de fixação

1. Explique a diferença entre `DISTANCIA_CANOS` e `ABERTURA_CANOS`.
2. Se `x = 500` e `VELOCIDADE_CANOS = 4`, determine `x` após cinco quadros.
3. Por que `pygame.Rect` pode acusar colisão em regiões transparentes?
4. Explique a função de `cano.passou` na contagem de pontos.
5. Compare o uso de uma lista de obstáculos com a criação de variáveis individuais para cada cano.
6. Discuta por que a velocidade em pixels/quadro depende da frequência efetiva de atualização.

## 11. Referências e continuidade

- Aula 02.0 — física, coordenadas e animação.
- Aula 02.1 — implementação do pássaro.
- Aula 03.1 — roteiro prático da Sprint 03.
- [`Roadmap do projeto`](../docs/roadmap.md).
- [Documentação oficial do Pygame](https://www.pygame.org/docs/).

---

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame** · **Versão 0.3.0**.
