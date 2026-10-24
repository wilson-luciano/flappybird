<div align="center">

# 🐤 Flappy Bird com Python e Pygame

**Projeto didático · Programação para Engenharia Mecânica · UFS/DMEC**

<img src="assets/imgs/Flappy_Bird_logo.png" alt="Ilustração do Flappy Bird incluída nos recursos do projeto" width="160">

*Da primeira janela à programação orientada a objetos, física, colisões e persistência de dados.*

</div>

> **Projeto de aprendizagem:** os alunos constroem o jogo progressivamente, seguindo aulas teóricas e roteiros práticos. Este repositório não pressupõe que todas as funcionalidades já estejam implementadas no `src/main.py` inicial.

## 🎮 Baixe e jogue — Windows

**Quer experimentar o jogo pronto?** Consulte as [versões e downloads do Flappy Bird](https://github.com/wilson-luciano/flappybird/releases). Em uma versão publicada que contenha o jogo, o arquivo `FlappyBird.exe` aparecerá nos **Assets** da respectiva Release.

**[📥 Ver versões disponíveis e baixar o jogo](https://github.com/wilson-luciano/flappybird/releases)**

> **Download direto:** a tag `v0.5.0` foi criada. Para evitar indicar um download não verificado, o acesso acima leva à página oficial de Releases. Depois de confirmar que o anexo `FlappyBird.exe` está disponível e testar seu download, o botão poderá apontar diretamente para `https://github.com/wilson-luciano/flappybird/releases/latest/download/FlappyBird.exe`.

O executável para Windows é preparado para funcionar sem instalar Python ou Pygame separadamente. Para estudar ou modificar o código, baixe o projeto na seção seguinte.

**Segurança no Windows:** executáveis novos e sem assinatura digital podem acionar o aviso do **Microsoft Defender SmartScreen**. Baixe apenas da Release oficial, confira a procedência, analise o arquivo com o Microsoft Defender e **não desative** as proteções do sistema. Se houver detecção de ameaça ou dúvida, não execute o arquivo.

## 🎯 Objetivos de aprendizagem

Praticar **Python**, estruturas condicionais e de repetição, funções, classes, listas, eventos, animação em tempo real, modelagem simplificada do movimento, colisões, leitura e gravação de arquivos, **Git** e **GitHub**.

## 🖼️ Visão dos recursos gráficos

<div align="center">
  <img src="assets/imgs/bg.png" alt="Cenário original usado como recurso didático" width="200">
</div>

*Imagens ilustrativas do conjunto de recursos do projeto; a aparência do jogo depende da sprint implementada.*

## 🚀 Como começar (Windows / VS Code)

Acesse o **[repositório oficial do Flappy Bird](https://github.com/wilson-luciano/flappybird)**. Clique em **Code → Download ZIP** ou clone com Git e abra a pasta `flappybird` no VS Code. Para clonar, use `git clone https://github.com/wilson-luciano/flappybird.git` a partir de `C:\Projetos`. Leia primeiro `aulas/aula-00.0-obtencao-projeto-github.md` e `aulas/aula-01.1-roteiro-pratico.md`.

No terminal PowerShell, na raiz do projeto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/main.py
```

Se o ambiente virtual já estiver criado, **não é necessário recriá-lo**. Se a ativação estiver bloqueada, consulte as alternativas indicadas na Aula 01.1.

## 🎮 Controles por etapa

| Etapa | Comandos |
|---|---|
| Sprint 01 | Fechar a janela pelo **X** |
| Sprint 02 | **Espaço**: salto |
| Sprint 03 | **Espaço**: iniciar, saltar ou reiniciar; **Esc**: sair |
| Sprint 04 (após implementação) | **P**: pausar/retomar; **S**: ativar/desativar som; **T**: alternar tema; **Espaço**: jogar |

## 🗺️ Roadmap

| Sprint | Conteúdo | Material |
|---|---|---|
| 00 | Preparação e obtenção do projeto | Aula 00.0 e Aula 01.1 |
| 01 | Primeira janela Pygame | Aulas 01.0 e 01.1 |
| 02 | Física, gravidade, salto e animação | Aulas 02.0 e 02.1 |
| 03 | Obstáculos, colisões e pontuação | Aulas 03.0 e 03.1 |
| 04 | Vidas, pausa, áudio, recorde e tema | Aulas 04.0 e 04.1 |
| 05 | Testes, empacotamento e entrega do executável | Aulas 05.0 e 05.1 |

Os documentos de acompanhamento ficam em [`docs/roadmap.md`](docs/roadmap.md) e [`docs/sprints/`](docs/sprints/).

## 📁 Estrutura principal

```text
flappybird/
├── assets/
│   ├── imgs/         # sprites e imagens didáticas
│   └── audio/        # efeitos sonoros
├── aulas/            # teoria e roteiros práticos
├── docs/sprints/     # planejamento e critérios de aceitação
├── src/main.py       # código evolutivo do jogo
├── tests/.gitkeep     # espaço reservado para testes futuros
├── .gitignore
├── LICENSE            # licença MIT do código original
├── README.md
└── requirements.txt
```

## 📦 Executável e distribuição

Na Sprint 05, o jogo é empacotado com o **PyInstaller** para Windows. Depois de executar o procedimento da **Aula 05.1**, o executável gerado estará em:

```text
flappybird/
└── dist/
    └── FlappyBird.exe
```

O arquivo `FlappyBird.exe` pode ser executado no Windows sem exigir a instalação separada de Python ou Pygame. A pasta `dist/` é uma saída local de compilação e **não precisa ser enviada ao repositório Git**. Para disponibilizar o programa, anexe o `.exe` à Release, conforme o Passo 12 da Aula 05.1. Para baixá-lo, abra [Releases](https://github.com/wilson-luciano/flappybird/releases), selecione uma versão publicada e, em **Assets**, clique em `FlappyBird.exe`.

**Distribuição:** o executável deve ser anexado à Release para ficar disponível ao público. Antes de redistribuir recursos gráficos e sonoros, confirme as permissões aplicáveis; o código original possui licença MIT, mas ela não abrange automaticamente recursos de terceiros.

## 🔐 Licenciamento e direitos de uso

O **código-fonte original** do projeto é disponibilizado sob a licença **MIT**, documentada no arquivo `LICENSE`. Imagens, áudios e outros materiais de terceiros não são automaticamente abrangidos por essa licença. A distribuição pública deve respeitar as permissões aplicáveis a esses recursos.

## 🔐 GitHub e direitos de uso

O projeto de referência está em [github.com/wilson-luciano/flappybird](https://github.com/wilson-luciano/flappybird). Cada estudante deve manter seu próprio repositório, conforme o primeiro envio explicado na **Aula 01.1**. **Antes de publicar este projeto em um repositório público, verifique as licenças e permissões de redistribuição das imagens e dos áudios de terceiros.** Enquanto essa verificação estiver pendente, utilize repositório privado e siga a orientação do professor. Não inclua a pasta `.venv/` nem dados pessoais de execução nos commits.

## 👨‍🏫 Créditos

© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame**.

## 🔄 Atualizar o projeto clonado

Para receber novas alterações do professor, dentro da pasta do projeto:

```powershell
cd C:\Projetos\flappybird
git status
git pull origin main
```

O `git clone` é usado para obter a primeira cópia com histórico Git; o `git pull` atualiza uma cópia já clonada. Verifique alterações locais antes de atualizar, pois podem ocorrer conflitos. Quem utilizou **Download ZIP** deverá baixar outro ZIP para obter uma nova versão ou configurar Git separadamente.
