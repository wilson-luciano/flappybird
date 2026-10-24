# Aula 04.0 — Recursos avançados e integração visual do Flappy Bird

**Disciplina:** Programação para Engenharia Mecânica — 2026.2  
**Projeto avaliativo 2:** Flappy Bird com Python e Pygame  
**Sprint:** 04 — Recursos avançados e identidade visual  
**Pré-requisito:** Aulas 03.0 e 03.1 concluídas

## 1. Objetivos de aprendizagem

Nesta etapa, o estudante dará continuidade ao jogo desenvolvido nas sprints anteriores, integrando novos recursos gráficos e sonoros e aperfeiçoando a interação com o jogador.

Ao concluir a aula, deverá ser capaz de:

- Organizar um programa em **classes**, atributos e métodos com responsabilidades bem definidas.
- Controlar os estados **MENU**, **JOGO** e **GAMEOVER**, incluindo o mecanismo de pausa.
- Implementar **seis vidas**, pontuação, medalhas e armazenamento do recorde em **JSON**.
- Alternar automaticamente os cenários e os sprites do pássaro nos períodos de dia, tarde e noite.
- Programar as fases normal e especial, com obstáculos representados por canos ou pássaros.
- Utilizar eventos do **teclado e do mouse**, efeitos sonoros e uma janela redimensionável.

A proposta é compreender como esses recursos se relacionam e como podem ser incorporados progressivamente a um projeto já existente.

## 2. Matriz de funcionalidades

| Recurso                             | Conceito de programação         | Implementação                      |
| ----------------------------------- | ------------------------------- | ---------------------------------- |
| 11 fundos, 13 posições na sequência | Listas, dicionários e conjuntos | `TEMAS`, `Recursos.fundos`         |
| Mudança de tema a cada 20 s         | Divisão inteira e resto         | `tema_por_tempo()`                 |
| Fases normal/especial de 260 s cada | Máquina de estados temporal     | `tempo_ativo % 520`                |
| 30 sprites de pássaros especiais    | Lista e amostragem aleatória    | `random.sample()`                  |
| Chão infinito                       | Aritmética modular e repetição  | `Chao.atualizar()`/`desenhar()`    |
| Menu, jogo e game over              | Máquina de estados              | `Jogo.estado`                      |
| Seis vidas e invulnerabilidade      | Condicionais e relógio          | `perder_vida()`                    |
| Colisão precisa                     | Retângulos e máscaras           | `Obstaculo.colide()`               |
| Placar gráfico e medalhas           | Dicionários e seleção           | `numero()`, `medalha()`            |
| Recorde com nome                    | JSON e tratamento de exceções   | `ler_recorde()`/`salvar_recorde()` |
| Pausa, áudio e mouse                | Eventos                         | `tratar_evento()`                  |
| Janela redimensionável              | Escala lógica/física            | `Jogo.desenhar()`                  |

## 3. Tempo, quadros e fases

O jogo opera em **30 FPS**. As posições dos obstáculos avançam **4 pixels lógicos por quadro**, mantendo a velocidade definida para o jogo. O tempo de fase, porém, é contado por `dt` (segundos decorridos por quadro), e não pela contagem simples de quadros. Quando a pausa está ativa, `tempo_ativo` não aumenta. Assim, a alternância de temas também para.

A fase normal dura **260 s**, seguida por **260 s de fase especial**. A cada **20 s**, muda o fundo. O ciclo completo é de **520 s**. Para descobrir a fase, calculamos `tempo_ativo % 520`; para descobrir o tema, `int((tempo_ativo % 260) // 20)`.

## 4. Classes e responsabilidade única

`Recursos` carrega imagens/sons; `Passaro` aplica gravidade e impulso; `Obstaculo` encapsula canos ou pares de pássaros especiais; `Chao` cria a rolagem infinita; `Jogo` coordena estados, eventos, placar e renderização. A organização separa dados, regras e apresentação, embora ainda usemos um único arquivo para facilitar o primeiro contato com orientação a objetos.

## 5. Colisão, máscaras e rotação

O teste por `pygame.Rect` é uma aproximação rápida. Quando `USAR_MASCARAS=True`, o programa só considera colisão se os pixels opacos se sobrepuserem. A rotação de **360° não inverte** uma imagem: equivale a nenhuma rotação. Para inverter o pássaro especial superior, utilizamos **180°**. O sprite do pássaro controlado é rotacionado apenas visualmente; a máscara é calculada sobre o sprite original, uma simplificação que deverá ser avaliada nos testes de colisão.

## 6. Interface, áudio e persistência

O menu possui logotipo e animação; durante o jogo aparecem pontos, vidas, medalhas e tema; no game over aparecem moldura, pontuação, recorde, medalha e entrada do nome do recordista. `S` ativa/desativa o áudio; `P` pausa; `ESC` fecha; `ESPAÇO` ou clique inicia/pula/reinicia. O recorde é persistido em `data/recorde.json` com as chaves `pontos` e `nome`. Não versionar dados pessoais de jogadores no repositório público.

## 7. Fundamentos de renderização: coordenadas, textos e sprites

No Pygame, a origem do sistema de coordenadas está no **canto superior esquerdo** da superfície. O eixo **x** aumenta para a direita e o eixo **y** aumenta para baixo. As posições são expressas em **pixels lógicos**, porque o jogo desenha primeiro na superfície `self.tela` de 575 × 860 e depois a ajusta ao tamanho da janela física.

O método `Surface.blit(imagem, (x, y))` desenha uma imagem sobre outra superfície. Quando recebe uma tupla `(x, y)`, ela identifica o **canto superior esquerdo** da imagem. Por exemplo:

```python
self.tela.blit(self.recursos.medalhas[medalha], (106, 420))
```

Nesse caso, a medalha começa em **x = 106** e **y = 420** na tela GAME OVER. Essa posição não interfere na medalha que aparece durante a partida.

### 7.1. Centralização e ponto inicial

Um texto pode ter larguras diferentes conforme o nome do recordista. Para centralizá-lo, o método `texto()` recebe `x = LARGURA // 2` e `centro=True`, subtraindo metade da largura renderizada do texto. O operador `//` realiza **divisão inteira**. Por isso, o título do recordista permanece centralizado independentemente do comprimento do nome.

A função `numero()` desenha algarismos a partir de sprites PNG. O parâmetro `fator=0.5` reduz as dimensões para metade. Embora essa função também aceite `centralizar=True`, o placar da tela GAME OVER **não utiliza centralização**: os números começam em coordenadas fixas e crescem para a direita conforme aumentam os dígitos.

### 7.2. Composição visual do GAME OVER

| Elemento                    | Posição lógica                | Regra de posicionamento                    |
| --------------------------- | ----------------------------- | ------------------------------------------ |
| Identificação do recordista | `x = LARGURA // 2`, `y = 105` | Texto centralizado                         |
| Pontuação do recordista     | `x = LARGURA // 2`, `y = 135` | Texto centralizado                         |
| Imagem GAME OVER            | centro `(LARGURA // 2, 245)`  | Retângulo centralizado                     |
| Moldura                     | centro `(LARGURA // 2, 450)`  | Retângulo centralizado                     |
| Título PONTOS               | `(270, 375)`                  | Início do texto                            |
| Número de pontos            | `(380, 410)`                  | Sprites em escala `0.5`, sem centralização |
| Título RECORDE              | `(270, 460)`                  | Início do texto                            |
| Número do recorde           | `(380, 490)`                  | Sprites em escala `0.5`, sem centralização |
| Medalha                     | `(106, 420)`                  | Canto superior esquerdo da imagem          |

Durante a entrada de um novo nome, a interface utiliza as alturas **580**, **615** e **650** para instruções e digitação. Quando não há nome pendente, a mensagem de reinício aparece em **y = 630**. Esses valores representam decisões de layout e podem ser estudados comparando a tabela com o método `Jogo.desenhar()`.

## 8. Recorde, estado do jogo e persistência em JSON

A pontuação obtida na partida (`self.pontos`) não é necessariamente igual ao recorde já salvo (`self.recorde`). Ao encerrar a partida, o jogo verifica se `self.pontos > self.recorde`. **Somente uma pontuação estritamente maior** inicia a digitação de um novo nome; empatar não basta.

Enquanto o nome está pendente, a tela informa **NOVO RECORDE!** e mostra a pontuação provisória acima da imagem GAME OVER. Ao pressionar **Enter**, o programa chama `salvar_recorde(pontos, nome)`. Essa função grava no arquivo `data/recorde.json` um objeto com as chaves `pontos` e `nome`, por exemplo:

```json
{
  "pontos": 15,
  "nome": "Aluno"
}
```

A função `ler_recorde()` consulta esse arquivo ao iniciar o jogo. O bloco `with` gerencia o fechamento do arquivo, enquanto `try/except` permite lidar com erros de leitura e escrita. A função de gravação devolve `True` quando consegue salvar; somente então o jogo atualiza o nome e a pontuação do recordista na memória. Se o arquivo ainda não existir, a leitura retorna valores iniciais seguros.

**Distinção importante:** desenhar uma pontuação na tela não significa gravá-la no disco. A persistência depende da confirmação por **Enter** e do sucesso da operação de escrita. O roteiro de execução e de teste dessa funcionalidade está na **Aula 04.1**.

## 9. Organização orientada a objetos e leitura do código

No projeto, `Jogo` coordena a renderização, mas delega responsabilidades a outros objetos. Por exemplo, `Recursos` concentra os sprites e sons; `Passaro` controla movimento e animação; `Obstaculo` controla obstáculos e colisões; e `Chao` desenha a faixa móvel. Isso ajuda a separar **dados**, **comportamentos** e **apresentação**.

Uma _docstring_ (texto entre aspas triplas no início de uma função ou método) explica sua finalidade. Os comentários iniciados por `#` esclarecem detalhes de implementação, como unidades, decisões de posicionamento e fórmulas. O decorador `@property` permite acessar `self.sprite` como uma propriedade, sem chamar `self.sprite()`: o valor é calculado a partir da família visual e do quadro atual da animação.

Na Aula 04.1, essas ideias aparecem diretamente no código completo. A leitura recomendada é identificar a responsabilidade de cada classe, acompanhar o fluxo **evento → atualização → desenho** e, por fim, executar os testes previstos.

## 10. Recursos externos e direitos de uso

Os sprites e sons devem permanecer em `assets/imgs/` e `assets/audio/`. A presença de um arquivo no pacote do professor não comprova autorização para redistribuição pública. Mantenha o repositório privado até conferir as licenças de cada recurso, inclusive imagens associadas a personagens e marcas de terceiros.

## 11. Critérios de aceitação para a Sprint 04

- [ ] Abrir menu e iniciar por espaço ou mouse.
- [ ] Jogar com seis vidas e reiniciar após game over.
- [ ] Pausar sem avançar o relógio de temas.
- [ ] Alternar tema automaticamente a cada 20 s.
- [ ] Alternar fases normal e especial a cada 260 s.
- [ ] Exibir pássaros especiais distintos nos obstáculos.
- [ ] Atualizar placar gráfico, medalhas e recorde com nome.
- [ ] Redimensionar a janela sem mudar a física lógica.
- [ ] Controlar som com S, pausa com P e saída com ESC.

**Atenção:** verificar a sintaxe é apenas o primeiro passo. Execute o jogo e confira a interface, o áudio, as colisões e a jogabilidade. Na próxima sprint, esses testes serão sistematizados e o projeto será preparado para distribuição.

---

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame** · **Versão 0.4.11**.
