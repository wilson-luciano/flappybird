# Aula 01.1 — Roteiro prático: Sprint 00 e Sprint 01

**Objetivo:** preparar o ambiente, executar a primeira janela do jogo e publicar o primeiro repositório individual no GitHub.

## Passo 1 — Obter o material do GitHub

Antes de iniciar, conclua a **Aula 00.0**. Ela explica como baixar o ZIP, extrair corretamente em `C:\Projetos\flappybird` ou clonar o repositório, evitando pastas duplicadas.

## Passo 2 — Abrir a pasta do projeto (PowerShell)

```powershell
cd C:\Projetos
cd flappybird
code .
```

Se a pasta `C:\Projetos` não existir, crie-a antes. O comando `code .` abre a pasta atual no VS Code.

## Passo 3 — Conferir a estrutura inicial do projeto

Antes de instalar ou configurar o Python, confira se os arquivos baixados estão na pasta correta. Neste momento, a pasta `.venv` **ainda não foi criada**.

```text
flappybird/
├── assets/
│   ├── audio/             # efeitos sonoros já fornecidos
│   └── imgs/              # sprites e figura didática já fornecidos
├── aulas/
│   ├── aula-00.0-obtencao-projeto-github.md
│   ├── aula-01.0-planejamento-ambiente.md
│   └── aula-01.1-roteiro-pratico.md
├── docs/
│   ├── sprints/
│   │   ├── sprint-00-preparacao-ambiente.md
│   │   ├── sprint-01-primeira-interface.md
│   │   ├── sprint-02-fisica-movimento.md
│   │   ├── sprint-03-obstaculos-colisoes-pontuacao.md
│   │   ├── sprint-04-recursos-avancados.md
│   │   └── sprint-05-testes-documentacao-entrega.md
│   └── roadmap.md
├── src/
│   └── main.py
├── tests/
│   └── .gitkeep
├── .gitignore
├── README.md
└── requirements.txt
```

No terminal integrado do VS Code, estando em `C:\Projetos\flappybird`, execute:

```powershell
tree /F /A
```

- `tree` exibe a hierarquia de pastas;
- `/F` inclui os nomes dos arquivos;
- `/A` usa caracteres simples na árvore.

**Observação:** a árvore acima segue a ordem visual do Explorador do VS Code (pastas primeiro e arquivos depois). O arquivo `.gitkeep` em `tests/` ajuda a preservar a pasta inicialmente vazia. As pastas `assets/imgs/` e `assets/audio/` já contêm recursos no pacote-base do professor. Como `docs/` já contém `roadmap.md` e os documentos das sprints, ela não precisa de `.gitkeep`. Para compreender o motivo e a diferença em relação ao `.gitignore`, consulte a **Aula 01.0 — seção 6**. O comando `tree /F /A` pode apresentar outra ordem e isso não é um erro. Confira também se não existe uma pasta `flappybird` dentro de outra por engano.

## Passo 4 — Verificar a instalação do Python 3.12.10

No terminal integrado do VS Code (PowerShell), execute:

```powershell
py -0p
py -3.12 --version
```

O primeiro comando lista as instalações encontradas pelo Python Launcher. O segundo verifica a versão selecionada. Para padronizar as atividades, utilizaremos **Python 3.12.10**.

Se o Python 3.12.10 ainda não estiver instalado, baixe o instalador oficial de 64 bits para Windows:

[Python 3.12.10 — instalador Windows (64 bits)](https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe)

Durante a instalação, quando disponíveis, habilite a inclusão do Python no PATH e mantenha os componentes **pip**, **venv** e **Python Launcher**. A série Python 3.12 teve o 3.12.10 como sua última versão com instaladores binários oficiais; atualizações posteriores da série são disponibilizadas como código-fonte.

> **Atenção:** o comando `py -3.12 --version` pode mostrar outra versão da série 3.12, se houver várias instalações. Confira o resultado e peça orientação ao professor antes de prosseguir se for diferente de `Python 3.12.10`.

## Passo 5 — Criar o ambiente virtual `.venv`

Com o terminal na raiz do projeto (`C:\Projetos\flappybird`), execute:

```powershell
py -3.12 -m venv .venv
```

**Entendendo o comando:** `py -3.12` seleciona o Python 3.12; `-m venv` executa o módulo de criação de ambientes virtuais; `.venv` é o nome da pasta criada. O ambiente virtual isola as bibliotecas do projeto da instalação global do Windows.

## Passo 6 — Ativar o ambiente virtual

Escolha o comando correspondente ao terminal que estiver utilizando:

| Terminal       | Comando de ativação             |
| -------------- | ------------------------------- |
| **PowerShell** | `.\.venv\Scripts\Activate.ps1`  |
| **CMD**        | `.venv\Scripts\activate.bat`    |
| **Git Bash**   | `source .venv/Scripts/activate` |

No PowerShell, o prompt normalmente passa a mostrar `(.venv)` antes do caminho da pasta.

Se a ativação estiver bloqueada pela política de execução do PowerShell, utilize o **CMD** ou solicite orientação ao professor antes de alterar políticas de segurança. Não é necessário modificar configurações globais sem autorização.

Confirme a versão e o interpretador em uso:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

O primeiro resultado esperado é `Python 3.12.10`; o caminho do segundo comando deverá apontar para `.venv` dentro do projeto.

## Passo 7 — Atualizar o pip e instalar o Pygame

Com o ambiente virtual ativado, execute:

```powershell
python -m pip install --upgrade pip
python -m pip install pygame
python -m pip show pygame
```

**Por que utilizar `python -m pip`?** Essa forma executa o pip vinculado ao interpretador Python ativo, reduzindo o risco de instalar bibliotecas em outro ambiente. O primeiro comando atualiza apenas o `pip`; o segundo instala o Pygame; o terceiro mostra as informações da biblioteca instalada. Não é necessário instalar `setuptools` e `wheel` explicitamente para o procedimento habitual deste projeto. Consulte a **Aula 01.0 — seção 7**.

## Passo 8 — Selecionar o interpretador no VS Code

Pressione **Ctrl+Shift+P**, procure **Python: Select Interpreter** e selecione o interpretador localizado em `.venv\Scripts\python.exe`. Execute os programas pelo terminal integrado com o ambiente ativado.

## Passo 9 — Conferir estrutura após criar o ambiente virtual

Após baixar o material e configurar o ambiente, confira se a organização do projeto está semelhante à seguinte:

```text
flappybird/
├── .venv/                 # ambiente virtual local (não enviar ao GitHub)
├── assets/
│   ├── audio/             # efeitos sonoros já fornecidos
│   └── imgs/              # sprites e figura didática já fornecidos
├── aulas/
│   ├── aula-00.0-obtencao-projeto-github.md
│   ├── aula-01.0-planejamento-ambiente.md
│   └── aula-01.1-roteiro-pratico.md
├── docs/
│   ├── sprints/
│   │   ├── sprint-00-preparacao-ambiente.md
│   │   ├── sprint-01-primeira-interface.md
│   │   ├── sprint-02-fisica-movimento.md
│   │   ├── sprint-03-obstaculos-colisoes-pontuacao.md
│   │   ├── sprint-04-recursos-avancados.md
│   │   └── sprint-05-testes-documentacao-entrega.md
│   └── roadmap.md
├── src/
│   └── main.py
├── tests/
│   └── .gitkeep
├── .gitignore
├── README.md
└── requirements.txt
```

No terminal integrado do VS Code, a partir da pasta raiz `C:\Projetos\flappybird`, execute:

```powershell
tree /F /A
```

**Explicação do comando:**

- `tree`: apresenta a estrutura hierárquica das pastas.
- `/F`: inclui os arquivos na listagem.
- `/A`: utiliza caracteres simples para desenhar a árvore.

**Atenção:** a pasta `.venv` deverá aparecer se foi criada no Passo 5; ela contém muitos arquivos e pode tornar a saída de `tree /F /A` extensa. A árvore acima mostra apenas os itens principais e segue a ordem visual do VS Code; a ordem exibida pelo comando `tree` pode ser diferente. A explicação conceitual de `.gitkeep` e `.gitignore` está na **Aula 01.0 — seção 6**. O roteiro e os checklists das seis sprints estão em `docs/roadmap.md` e `docs/sprints/`.

## Passo 10 — Primeira janela com adaptação automática ao monitor

No arquivo `src/main.py`, implemente o código abaixo. A resolução **575 × 860 pixels** permanece como referência do projeto, mas a janela será reduzida automaticamente quando o monitor não tiver espaço suficiente. Isso evita que a barra de título e o botão **X** fiquem fora da tela.

O programa está dividido em seções e utiliza comentários `#` para explicar os comandos e conceitos novos.

```python
# ============================================================
# PROJETO: FLAPPY BIRD
# DISCIPLINA: Programação para Engenharia Mecânica
# SPRINT 01: Criação da janela e adaptação ao monitor
# ============================================================

# Importa a biblioteca Pygame, utilizada para criar jogos 2D.
import pygame


# ------------------------------------------------------------
# 1. CONFIGURAÇÕES INICIAIS DO JOGO
# ------------------------------------------------------------

# Dimensões de referência do cenário, em pixels.
LARGURA = 575
ALTURA = 860

# FPS (Frames Per Second): limite de quadros por segundo.
FPS = 30

# Utiliza no máximo 85% das dimensões informadas pelo monitor.
# A margem ajuda a manter visível a barra de título da janela.
FATOR_TELA = 0.85


# ------------------------------------------------------------
# 2. FUNÇÃO PRINCIPAL
# ------------------------------------------------------------

def main():
    # Inicializa os módulos do Pygame.
    pygame.init()

    # --------------------------------------------------------
    # 2.1. IDENTIFICAÇÃO DA RESOLUÇÃO DO MONITOR
    # --------------------------------------------------------

    # Consulta as dimensões da tela informadas pelo Pygame.
    info = pygame.display.Info()
    largura_monitor = info.current_w
    altura_monitor = info.current_h

    # --------------------------------------------------------
    # 2.2. CÁLCULO DO FATOR DE ESCALA
    # --------------------------------------------------------

    # Calcula o fator permitido pela largura do monitor.
    escala_largura = largura_monitor * FATOR_TELA / LARGURA

    # Calcula o fator permitido pela altura do monitor.
    escala_altura = altura_monitor * FATOR_TELA / ALTURA

    # min() escolhe o menor fator, preservando a proporção.
    # O limite 1.0 impede ampliar a janela além de 575 x 860.
    escala = min(escala_largura, escala_altura, 1.0)

    # --------------------------------------------------------
    # 2.3. CÁLCULO DAS DIMENSÕES DA JANELA
    # --------------------------------------------------------

    # int() converte os resultados para pixels inteiros.
    largura_janela = int(LARGURA * escala)
    altura_janela = int(ALTURA * escala)

    # --------------------------------------------------------
    # 2.4. CRIAÇÃO DA JANELA
    # --------------------------------------------------------

    # Cria a janela com as dimensões ajustadas ao monitor.
    tela = pygame.display.set_mode((largura_janela, altura_janela))

    # Define o título da barra superior da janela.
    pygame.display.set_caption("Flappy Bird — Sprint 01")

    # Cria o relógio que controla a taxa de atualização.
    relogio = pygame.time.Clock()

    # Variável booleana que controla o funcionamento do jogo.
    executando = True

    # --------------------------------------------------------
    # 3. LOOP PRINCIPAL DO JOGO
    # --------------------------------------------------------

    # Repete as instruções enquanto executando for True.
    while executando:

        # Percorre os eventos (teclado, mouse, fechar janela etc.).
        for evento in pygame.event.get():

            # Detecta o clique no botão X da janela.
            if evento.type == pygame.QUIT:
                executando = False

        # Pinta o fundo com azul-claro no padrão RGB.
        # Cada componente (vermelho, verde e azul) vai de 0 a 255.
        tela.fill((135, 206, 235))

        # Apresenta na janela o quadro desenhado.
        pygame.display.flip()

        # Limita a execução a, no máximo, FPS quadros por segundo.
        relogio.tick(FPS)

    # --------------------------------------------------------
    # 4. ENCERRAMENTO DO PYGAME
    # --------------------------------------------------------

    # Libera os recursos da biblioteca após sair do laço.
    pygame.quit()


# ------------------------------------------------------------
# 5. PONTO DE ENTRADA DO PROGRAMA
# ------------------------------------------------------------

# Executa main() somente quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()
```

### Entendendo o dimensionamento

O fator de escala é calculado pela expressão:

$$
s = \min\left(\frac{0{,}85\,W_m}{575},\;\frac{0{,}85\,H_m}{860},\;1\right)
$$

Em que `W_m` e `H_m` representam a largura e a altura informadas pelo monitor. O menor valor faz a área desenhada da janela respeitar os limites adotados e manter aproximadamente a proporção original (com arredondamento para pixels inteiros). O valor `1` impede a ampliação acima da resolução de referência.

**Exemplo:** em um monitor de 1366 × 768 pixels, a janela terá aproximadamente **436 × 652 pixels**, em vez de 575 × 860.

**Atenção:** `pygame.display.Info()` não desconta necessariamente a barra de tarefas nem as bordas da janela. A margem de 15% é uma solução prática para os monitores usuais, mas não garante o encaixe em todas as configurações de escala do sistema operacional.

**Preparação para as próximas sprints:** nesta etapa, ajustamos somente as dimensões físicas da janela. Ao incluir o pássaro, os obstáculos e as colisões, manteremos coordenadas lógicas de referência em **575 × 860** e estudaremos como redimensionar o desenho sem alterar a física do jogo.

### Conceitos de programação praticados

| Conceito                          | Exemplo no código                           |
| --------------------------------- | ------------------------------------------- |
| Constantes de configuração        | `LARGURA`, `ALTURA`, `FPS`, `FATOR_TELA`    |
| Variáveis e operações aritméticas | `escala_largura`, `escala_altura`           |
| Funções nativas do Python         | `min()` e `int()`                           |
| Função definida pelo programador  | `main()`                                    |
| Estrutura de repetição            | `while` e `for`                             |
| Estrutura condicional             | `if`                                        |
| Variáveis booleanas               | `True` e `False`                            |
| Tuplas                            | `(largura_janela, altura_janela)` e cor RGB |

## Passo 11 — Executar e verificar a adaptação

Com o ambiente virtual ativo, execute:

```powershell
python src/main.py
```

A janela deve abrir com fundo azul-claro, respeitar a proporção de referência e permitir o fechamento pelo botão **X**, sem travamentos. Se necessário, use também o atalho **Alt+F4** para fechar a janela no Windows. Em monitores menores, a janela deverá aparecer reduzida automaticamente. Compare o resultado com a resolução do seu monitor.

## Passo 12 — Preparar o Git para o primeiro envio ao GitHub

Nesta etapa, cada aluno criará **seu próprio repositório**, independente do repositório do professor. A sequência abaixo utiliza o **terminal PowerShell do VS Code**, aberto em `C:\Projetos\flappybird`. Os comandos Git também funcionam no Git Bash; apenas a navegação entre pastas é diferente.

### 12.1 — Verificar Git e a pasta do projeto

```powershell
git --version
pwd
git rev-parse --show-toplevel
```

- `git --version` verifica a instalação do Git.
- `pwd` mostra a pasta atual; deve ser `C:\Projetos\flappybird`.
- `git rev-parse --show-toplevel` mostra a raiz do repositório Git, **quando ela existe**. Se aparecer `fatal: not a git repository`, isso é normal para um projeto obtido por ZIP.

**Atenção:** não execute `git init` dentro de `src/`, `aulas/` ou de uma segunda pasta `flappybird` criada por engano. O repositório deve abranger a **raiz inteira do projeto**.

### 12.2 — Verificar nome e e-mail dos commits

Se você já configurou o Git durante o projeto **EngConvert**, utilizando o mesmo usuário do Windows, **não é necessário repetir a configuração global**. Confira apenas os valores registrados:

```powershell
git config --global --get user.name
git config --global --get user.email
```

**Somente se algum dado estiver ausente ou incorreto**, configure-o com seus dados reais:

```powershell
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu-email-vinculado-ao-github@exemplo.com"
```

`user.name` identifica o autor dos commits e **não precisa ser igual** ao nome de usuário do GitHub. Para o GitHub associar os commits à sua conta, utilize um e-mail verificado na plataforma ou o endereço `noreply` disponibilizado nas configurações de e-mail do GitHub. Essas configurações identificam a autoria; **não autenticam** o acesso ao GitHub.

> A opção `--global` aplica os dados aos repositórios do mesmo usuário do computador. Caso utilize um computador compartilhado, peça orientação ao professor sobre o uso de `--local` em vez de `--global`.

### 12.3 — Identificar como o projeto foi obtido

**Situação A — Projeto obtido por ZIP (recomendada para o primeiro exercício):** o ZIP normalmente não contém a pasta oculta `.git`. Confirme que está na raiz e inicialize o repositório:

```powershell
git init
git branch -M main
```

`git init` cria a estrutura de controle de versões local; `git branch -M main` define o nome da branch principal. Ainda não houve publicação na internet.

**Situação B — Projeto obtido por `git clone`:** o repositório local já existe e normalmente aponta para o GitHub do professor. **Não execute `git init` novamente.** Confira:

```powershell
git remote -v
git branch --show-current
```

Depois de criar seu repositório individual no GitHub (Passo 13), substitua o endereço de `origin` pelo endereço do seu repositório usando `git remote set-url origin ...`. Essa operação muda o destino de `push`/`fetch`, **não apaga arquivos nem commits locais**. Atenção: o histórico do repositório clonado continuará presente; se o exercício exigir um histórico individual iniciado do zero, prefira a **Situação A (ZIP)**.

### 12.4 — Verificar o `.gitignore` antes de adicionar arquivos

Abra `.gitignore` e confira se ele exclui, pelo menos, o ambiente virtual e arquivos temporários:

```gitignore
.venv/
__pycache__/
*.py[cod]
.vscode/
```

Preserve outras regras úteis que já existirem. **Não exclua `assets/imgs/` nem `assets/audio/` automaticamente**: esses recursos são necessários ao jogo. Entretanto, a publicação pública dos recursos deve ocorrer **somente após confirmação de suas licenças de redistribuição**. Se ainda não houver essa autorização, use um repositório **privado** para o exercício e consulte o professor antes de torná-lo público.

### 12.5 — Preparar e realizar o primeiro commit local

```powershell
git status
git add .
git status
git commit -m "Sprint 01: ambiente e primeira janela Pygame"
git log -1 --oneline
```

- `git status`: identifica arquivos novos, alterados e preparados.
- `git add .`: coloca as alterações do projeto na área de preparação (_staging area_). **Não envia arquivos ao GitHub**.
- O segundo `git status`: permite conferir exatamente o que será incluído.
- `git commit -m "..."`: grava uma versão no **histórico local**.
- `git log -1 --oneline`: exibe o commit mais recente.

**Se você clonou o repositório do professor:** poderá já existir um histórico e nenhum arquivo novo para registrar. Nesse caso, `nothing to commit, working tree clean` não é erro. Faça um commit somente quando houver alterações reais; não crie commits vazios apenas para reproduzir a saída do exemplo.

## Passo 13 — Criar o repositório individual no GitHub

1. Entre em [github.com](https://github.com) com sua conta.
2. Clique em **+** (canto superior direito) e escolha **New repository**, ou acesse **Your repositories → New**.
3. Em **Repository name**, digite `flappybird` (ou outro nome indicado pelo professor).
4. Em **Description**, utilize, por exemplo: `Projeto didático de Flappy Bird com Python e Pygame — Programação para Engenharia Mecânica`.
5. Selecione **Private** enquanto as permissões dos recursos gráficos e sonoros não forem verificadas.
6. **Não marque** as opções para adicionar `README`, `.gitignore` ou `license` pela interface do GitHub: o projeto-base já possui os arquivos correspondentes ou terá a licença definida posteriormente.
7. Clique em **Create repository**.
8. Copie a URL **HTTPS** do repositório criado, no formato `https://github.com/SEU-USUARIO/flappybird.git`.

**Por que criar o repositório vazio?** Se o GitHub criar um README ou uma licença antes do primeiro `push`, o repositório remoto poderá ter commits que não existem no computador, gerando um conflito de históricos. Não é necessário enfrentar esse problema neste primeiro exercício.

## Passo 14 — Conectar o repositório local ao GitHub

Substitua `SEU-USUARIO` pelo seu nome de usuário real. **Não digite literalmente `SEU-USUARIO`.**

### 14.1 — Verificar se já existe `origin`

```powershell
git remote -v
```

`origin` é um **apelido convencional** para o repositório remoto. Ele não é o nome da sua conta nem da branch. A saída pode estar vazia (projeto obtido por ZIP) ou mostrar o endereço do professor (projeto clonado).

**Se não aparecer nenhum remoto `origin`:**

```powershell
git remote add origin https://github.com/SEU-USUARIO/flappybird.git
```

**Se `origin` já existir:** não execute `git remote add origin` novamente; atualize o endereço existente:

```powershell
git remote set-url origin https://github.com/SEU-USUARIO/flappybird.git
```

Confira:

```powershell
git remote -v
git branch -M main
```

Os endereços mostrados em `(fetch)` e `(push)` devem apontar para **o seu repositório individual**. O comando `git branch -M main` padroniza o nome da branch local; em um repositório clonado, verifique com o professor antes de renomear uma branch de trabalho diferente.

### 14.2 — Publicar o primeiro commit

```powershell
git push -u origin main
```

- `push`: envia os commits locais para o GitHub.
- `origin`: indica qual repositório remoto receberá os commits.
- `main`: indica qual branch será enviada.
- `-u`: estabelece o acompanhamento (_upstream_) entre a branch local e a remota, facilitando futuros `git push` e `git pull`.

O GitHub poderá solicitar autenticação no navegador ou por um gerenciador de credenciais. **Não utilize a senha comum da conta como senha Git HTTPS**; siga o fluxo de autenticação oferecido pelo Git Credential Manager ou as orientações atuais do GitHub.

### 14.3 — Confirmar a publicação

```powershell
git status
git branch -vv
git remote -v
```

Abra o repositório no navegador e confirme que `README.md`, `src/main.py`, `aulas/`, `docs/` e os demais arquivos permitidos estão presentes. A pasta `.venv/` **não deve** aparecer no GitHub.

## Passo 15 — Entender erros comuns de Git e GitHub

| Mensagem ou situação                    | Causa provável                                                             | Procedimento recomendado                                                                                                                          |
| --------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fatal: not a git repository`           | Projeto baixado por ZIP, sem Git inicializado, ou terminal na pasta errada | Confira `pwd`; na raiz do projeto obtido por ZIP, execute `git init`                                                                              |
| `remote origin already exists`          | Já existe um remoto chamado `origin`                                       | Verifique `git remote -v` e use `git remote set-url origin URL` quando precisar trocar o destino                                                  |
| `rejected (fetch first)`                | O remoto já possui commits que não estão no repositório local              | Confira se criou o repositório remoto vazio e se a URL está correta; peça orientação antes de integrar históricos. **Não use `git push --force`** |
| `nothing to commit, working tree clean` | Não existem alterações locais pendentes                                    | Continue se o commit já existir; caso contrário, confira se editou e salvou os arquivos                                                           |
| `Author identity unknown`               | Nome ou e-mail não configurado                                             | Configure `user.name` e `user.email` e repita o commit                                                                                            |
| `src refspec main does not match any`   | A branch `main` não existe ou ainda não há commit local                    | Confira `git branch --show-current`, `git status` e `git log -1`                                                                                  |
| A pasta `.venv` aparece em `git status` | `.gitignore` ausente ou incompleto                                         | Corrija `.gitignore` **antes** de executar `git add .`                                                                                            |
| `git branch` abre uma tela com `(END)`  | O Git abriu o paginador `less`                                             | Pressione `q` para sair; alternativamente, use `git --no-pager branch`                                                                            |

**Importante:** `git branch -a` lista branches locais **e** remotas conhecidas; `git --no-pager branch` lista apenas branches locais sem abrir o paginador. Portanto, os comandos não são equivalentes.

### Resumo visual do primeiro envio

```text
Pasta local C:\Projetos\flappybird
                |
                v
      git init (somente ZIP)
                |
                v
            git status
                |
                v
             git add .
                |
                v
            git commit
                |
                v
Criar repositório vazio no GitHub
                |
                v
  git remote add/set-url origin
                |
                v
     git push -u origin main
                |
                v
  Verificar arquivos no GitHub
```

**Nas próximas aulas**, o repositório já estará configurado. Para registrar novas alterações, normalmente bastará executar `git status`, `git add`, `git commit` e `git push`, sem repetir `git init` ou criar outro repositório.

## Documentos das Sprints 00 e 01

Depois de concluir os passos práticos, consulte os documentos de acompanhamento, que **já estão preenchidos**:

- [Sprint 00 — Preparação do ambiente](../docs/sprints/sprint-00-preparacao-ambiente.md): valide o ambiente Python, `.venv`, dependências, estrutura e arquivos do projeto.
- [Sprint 01 — Primeira interface](../docs/sprints/sprint-01-primeira-interface.md): valide a janela, o loop, o fechamento e a execução.
- [Roadmap geral das Sprints 00 a 05](../docs/roadmap.md): consulte a sequência completa do projeto.

Registre as evidências solicitadas nos documentos de sprint e compare os resultados com seus critérios de aceitação. As próximas sprints serão desenvolvidas nas aulas seguintes.

## Checklist da entrega

- [ ] Ambiente virtual ativado
- [ ] Pygame instalado no ambiente
- [ ] Interpretador correto selecionado
- [ ] Janela se adapta ao monitor, preserva a proporção e fecha normalmente
- [ ] Arquivos do projeto organizados
- [ ] Primeiro commit local registrado
- [ ] Repositório individual criado no GitHub (inicialmente privado)
- [ ] `origin` aponta para o repositório do aluno
- [ ] Primeiro `git push -u origin main` concluído e arquivos conferidos no navegador
- [ ] `.venv/` não foi publicada

## Desafio de fixação

Altere a cor de fundo, o título da janela e o FPS. Experimente também mudar `FATOR_TELA` de `0.85` para `0.75` e observe a diferença no tamanho da janela. Registre as alterações em um novo commit e explique os efeitos observados.

---

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame** · **Versão 0.1.3**.
