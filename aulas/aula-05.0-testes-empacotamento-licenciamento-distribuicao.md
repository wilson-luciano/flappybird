# Aula 05.0 — Testes, empacotamento, licenciamento e distribuição do Flappy Bird

**Disciplina:** Programação para Engenharia Mecânica — 2026.2  
**Projeto avaliativo 2:** Flappy Bird com Python e Pygame  
**Sprint:** 05 — Testes funcionais, executável, licença MIT e entrega final  
**Pré-requisitos:** Aulas 04.0 e 04.1 concluídas; projeto funcionando em `C:\Projetos\flappybird`.

## 1. Objetivos de aprendizagem

Ao concluir esta aula, o estudante deverá ser capaz de:

- Diferenciar **script Python**, **ambiente virtual**, **bibliotecas** e **executável Windows**.
- Explicar a função do **PyInstaller** e dos parâmetros utilizados no empacotamento.
- Distinguir **recursos de leitura** (imagens e sons) de **dados persistentes** (recorde do jogador).
- Entender caminhos de arquivos no desenvolvimento e na execução de um `.exe`.
- Planejar testes funcionais e uma distribuição responsável pelo GitHub.
- Reconhecer licenças permissivas e copyleft e explicar a adoção da **MIT para o código original**.
- Diferenciar um commit/push de uma **Release** com executável para download.

## 2. Do código-fonte ao programa distribuível

Durante as sprints anteriores, o jogo foi iniciado com `python src/main.py`. Esse comando depende de um interpretador Python e das bibliotecas instaladas no ambiente de execução. O arquivo `src/main.py` contém **código-fonte**: instruções legíveis que são executadas pelo Python.

O **PyInstaller** analisa o programa, reúne o interpretador, dependências e recursos indicados e produz um pacote executável para o sistema operacional em que a compilação é realizada. **Não é um compilador que transforma automaticamente o programa em um aplicativo nativo independente de qualquer sistema operacional**: o pacote resultante é específico da plataforma. Para criar `FlappyBird.exe`, execute o processo no **Windows**.

O computador destinatário normalmente não precisa instalar Python ou Pygame separadamente, mas o executável ainda depende de compatibilidade com o Windows e de componentes do sistema.

## 3. Estrutura atual do projeto

```text
C:\Projetos\flappybird\
├── assets\
│   ├── imgs\                 # PNGs e, se disponível, arquivo .ico
│   └── audio\                # WAVs e MP3s
├── aulas\                    # teoria e roteiros práticos
├── data\
│   └── recorde.json          # dados locais: não enviar ao GitHub
├── docs\
├── src\
│   └── main.py               # entrada do programa
├── tests\
│   └── .gitkeep             # reserva a pasta para testes futuros
├── .gitignore
├── README.md
└── requirements.txt
```

O código da Sprint 04 utiliza `pathlib.Path` para localizar `assets/imgs`, `assets/audio` e `data/recorde.json`. Para a Sprint 05, precisamos diferenciar **a localização dos arquivos incorporados ao pacote** e **a localização dos arquivos que o jogador modifica**.

## 4. O que é o PyInstaller?

O PyInstaller é uma ferramenta de **empacotamento** (*packaging*). Ele examina importações, reúne dependências e constrói o aplicativo a partir do ponto de entrada, aqui `src/main.py`.

Instalação no ambiente virtual ativo:

```powershell
python -m pip install pyinstaller
```

Verificação:

```powershell
python -m PyInstaller --version
```

Usar `python -m` ajuda a empregar o PyInstaller instalado no mesmo ambiente Python utilizado pelo projeto.

### 4.1. Parâmetros principais

| Opção | Finalidade |
|---|---|
| `--onefile` | Produz um único executável; os recursos internos são extraídos temporariamente ao iniciar. |
| `--onedir` | Produz uma pasta com executável e arquivos de suporte; é útil para diagnóstico. |
| `--windowed` | No Windows, abre o aplicativo gráfico sem janela de console. |
| `--name FlappyBird` | Define o nome do executável e de artefatos de compilação. |
| `--add-data "assets;assets"` | Inclui a pasta `assets` no pacote, mantendo sua estrutura interna. |
| `--icon "assets/imgs/flappy_bird.ico"` | Define o ícone do `.exe`, **se o arquivo existir**. |
| `--clean` | Limpa cache de compilação do PyInstaller antes de gerar o pacote. |
| `--noconfirm` | Substitui artefatos anteriores de saída sem solicitar confirmação. |

No Windows, o separador tradicional entre origem e destino de `--add-data` é `;`. A sintaxe pode variar com a versão e o sistema; nesta aula adotamos **Windows e PowerShell**.

### 4.2. Um comando-base

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --name FlappyBird --add-data "assets;assets" src/main.py
```

Esse comando **só deve ser executado depois da adaptação dos caminhos do código** descrita na Aula 05.1. O ícone `.ico` é opcional e será acrescentado quando existir.

## 5. Caminhos de arquivos: desenvolvimento × executável

No projeto Python, `__file__` indica a localização do arquivo `main.py`. Como ele está em `src/`, a expressão `Path(__file__).resolve().parent.parent` encontra a raiz do repositório.

No modo `--onefile`, o PyInstaller extrai os arquivos incorporados para um diretório temporário. A variável `sys._MEIPASS` identifica esse diretório quando a aplicação está empacotada. **Não é adequado presumir que `parent.parent` continuará apontando para a raiz do projeto.**

Conceitualmente, teremos duas bases:

- **`RAIZ_RECURSOS`**: pasta de onde o jogo **lê** imagens e sons. No desenvolvimento, é a raiz do repositório; no `.exe`, é o diretório temporário do PyInstaller.
- **`RAIZ_DADOS`**: pasta onde o jogo **grava** o recorde. Deve ser persistente e gravável; no Windows distribuído, podemos usar `%LOCALAPPDATA%\FlappyBird\data\recorde.json`.

A Aula 05.1 apresenta o trecho exato de código que implementa essa distinção.

## 6. Persistência: por que o recorde não deve ser empacotado?

`assets/imgs` e `assets/audio` são **recursos de leitura**. O jogo consulta esses arquivos, mas não precisa modificá-los. Já `recorde.json` armazena o nome e a pontuação do jogador, sendo **dado de escrita**.

No modo `--onefile`, arquivos extraídos temporariamente não são o lugar correto para gravar dados persistentes. A pasta temporária pode ser eliminada ao encerrar o jogo. Além disso, o diretório do executável pode não permitir gravação.

**Estratégia adotada:** durante o desenvolvimento, preservar `data/recorde.json` na raiz do projeto; no executável Windows, usar a pasta de dados locais do usuário. A pasta `data/` do repositório continuará ignorada pelo Git.

## 7. Entendendo os resultados do empacotamento

```text
flappybird/
├── build/
│   └── FlappyBird/        # arquivos intermediários
├── dist/
│   └── FlappyBird.exe     # executável gerado com --onefile
├── FlappyBird.spec        # configuração de compilação
└── ...
```

- **`dist/FlappyBird.exe`**: produto distribuível.
- **`build/`**: arquivos intermediários que podem ser recriados.
- **`FlappyBird.spec`**: arquivo Python com a configuração da compilação; pode ser útil em builds avançados. **Não é um erro nem um arquivo descartável obrigatório.**

`--name FlappyBird` determina também o nome da pasta intermediária `build/FlappyBird/` e do arquivo `FlappyBird.spec`. Sem `--name`, os nomes derivam do script de entrada (`main.py`).

## 8. Testes e validação

**Teste sintático** verifica se o código pode ser interpretado:

```powershell
python -m py_compile src/main.py
```

**Teste funcional** exige executar e observar o jogo: menu, pulo, obstáculos, vidas, pausa, áudio, temas, GAME OVER, medalha, digitação e persistência do recorde.

**Testes automatizados** podem executar verificações repetitivas com ferramentas como `pytest`. Nesta etapa, **não implementaremos testes automatizados**: manteremos `tests/.gitkeep` para evolução futura e concentraremos a avaliação nos testes funcionais manuais.

**Teste de distribuição** verifica se o executável abre fora do VSCode e sem depender da pasta `assets` do projeto. É útil copiá-lo para uma pasta temporária separada e executá-lo ali.

A aprovação do teste sintático **não comprova** que o jogo funciona visualmente, nem que os recursos foram incorporados corretamente.

## 9. Solução de problemas e segurança

Erros comuns incluem: arquivo de imagem ausente, caminho incorreto, ícone `.ico` inexistente, biblioteca não instalada no ambiente ativo, bloqueio por permissões e falha de gravação do recorde.

Para diagnosticar erros ocultos pelo `--windowed`, gere temporariamente uma versão **com console**, omitindo `--windowed`, e execute pelo PowerShell. Não desative mecanismos de proteção do Windows como solução genérica.

Os diretórios `build/` e `dist/` podem ser recriados. O arquivo `.spec` também pode ser recriado, mas deve ser preservado se tiver sido personalizado.

## 10. Licenciamento: autoria, uso e compartilhamento

Publicar um repositório no GitHub não significa, por si só, que qualquer pessoa possa copiar e redistribuir todos os arquivos. Uma **licença** esclarece quais usos o titular dos direitos autoriza e sob quais condições.

### 10.1. Tipos comuns de licença

| Licença | Característica principal | Exemplo de aplicação |
|---|---|---|
| **MIT** | Permissiva: autoriza uso, modificação e redistribuição, inclusive comercial, com preservação dos avisos exigidos. | Código-fonte de projetos didáticos. |
| **Apache 2.0** | Permissiva; inclui condições expressas relativas a patentes. | Bibliotecas e aplicações. |
| **BSD 3-Clause** | Permissiva, com restrição de uso de nomes para endosso. | Projetos de software. |
| **GPL v3** | Copyleft: distribuições de versões derivadas estão sujeitas a obrigações de disponibilização de código, conforme a licença. | Software livre com reciprocidade. |
| **CC BY 4.0** | Licença voltada a obras criativas; exige atribuição. | Textos e materiais autorais, não como licença principal de software. |

### 10.2. Licença escolhida para o projeto

**Decisão do projeto:** o **código-fonte original** do Flappy Bird será disponibilizado sob a **licença MIT**, com aviso de copyright **© 2026 Wilson Luciano** e arquivo `LICENSE` na raiz do repositório. A Aula 05.1 ensina a criar e enviar esse arquivo.

A MIT não transfere automaticamente direitos sobre **imagens, músicas, efeitos sonoros, personagens ou outros materiais de terceiros**. Esses recursos podem estar sujeitos a termos próprios, mesmo quando obtidos gratuitamente. Por isso, a nota de licenciamento no README deve distinguir o código original dos recursos externos. Não é necessário elaborar uma auditoria extensa como atividade da aula; para uma distribuição pública, entretanto, devem ser utilizados apenas recursos cuja redistribuição seja permitida.

## 11. Git, GitHub e Releases

O repositório oficial do projeto é **https://github.com/wilson-luciano/flappybird**. Os alunos podem acessar **Code → Download ZIP** para obter o código e os materiais; quem já utiliza Git pode executar:

```powershell
git clone https://github.com/wilson-luciano/flappybird.git
```

**`git push`** envia os commits do repositório remoto, enquanto **GitHub Releases** organiza versões distribuíveis do programa e permite anexar arquivos binários, como `FlappyBird.exe`.

Após gerar e testar o executável, o arquivo local estará em:

```text
C:\Projetos\flappybird\dist\FlappyBird.exe
```

Quando uma versão pública estiver autorizada e publicada, o visitante poderá encontrá-la na **página de Releases**:

https://github.com/wilson-luciano/flappybird/releases

Se a Release mais recente elegível contiver um anexo denominado exatamente `FlappyBird.exe`, o endereço direto poderá ser:

```text
https://github.com/wilson-luciano/flappybird/releases/latest/download/FlappyBird.exe
```

Esse link só deve ser anunciado como download disponível depois de sua publicação e teste. O README poderá apresentar um botão em destaque no início da página, convidando o visitante a experimentar o jogo sem instalar Python ou Pygame.

O `.gitignore` continuará excluindo `.venv/`, `/data/`, `build/` e `dist/`; o executável deve ser anexado à Release, **não adicionado ao commit**. A pasta `tests/` permanecerá com `.gitkeep` nesta versão.

## 12. Critérios de aceitação da Sprint 05

- [ ] O jogo executa com `python src/main.py`.
- [ ] A sintaxe de `src/main.py` é válida.
- [ ] Os testes funcionais manuais foram realizados; `tests/.gitkeep` foi preservado.
- [ ] O código diferencia caminhos de recursos e dados persistentes.
- [ ] O PyInstaller gera `dist/FlappyBird.exe`.
- [ ] O executável abre sem o VSCode e apresenta imagens e áudio.
- [ ] Menu, jogo, pausa, GAME OVER e recordes funcionam.
- [ ] O recorde permanece após fechar e reabrir o `.exe`.
- [ ] O `.gitignore` impede o envio de dados locais e arquivos temporários.
- [ ] O código original tem arquivo `LICENSE` com a licença MIT.
- [ ] O README apresenta o roadmap final e o endereço oficial do repositório.
- [ ] A publicação via GitHub Releases foi compreendida e, quando autorizada, o link do executável foi testado.
- [ ] A documentação final e as condições de redistribuição dos recursos incorporados foram consideradas.

**Continuidade:** a Aula 05.1 transforma esses fundamentos em um roteiro prático executável no PowerShell.
---

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame**.
