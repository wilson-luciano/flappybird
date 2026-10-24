# Aula 00.0 — Preparação e obtenção do projeto no GitHub

**Projeto 2:** Flappy Bird com Python e Pygame  
**Disciplina:** Programação para Engenharia Mecânica — 2026.2  
**Objetivo:** baixar o material oficial, organizar as pastas no Windows e abrir o projeto no VS Code.

> **Repositório oficial:** [https://github.com/wilson-luciano/flappybird](https://github.com/wilson-luciano/flappybird). Utilize esse endereço para obter o projeto. O download do código-fonte é diferente do download do executável, quando este estiver disponível em **Releases**.

## 1. Preparação
Verifique se o computador possui VS Code, Python 3.12, Git e acesso ao GitHub. Abra o Explorador de Arquivos e confira a existência de `C:\Projetos`; crie a pasta se necessário.

## 2. Opção A — Baixar pelo navegador (Download ZIP)
1. Acesse **https://github.com/wilson-luciano/flappybird** no navegador.
2. Na página principal, clique em **Code** e depois em **Download ZIP**.
3. Aguarde o arquivo ser salvo na pasta **Downloads**.
4. Clique com o botão direito no ZIP e selecione **Extrair Tudo...**.
5. Abra a pasta extraída e identifique o diretório que contém `README.md`, `aulas`, `src` e `requirements.txt`.
6. Mova **esse diretório do projeto**, e não uma pasta externa adicional, para `C:\Projetos`.
7. Renomeie o diretório para `flappybird` se necessário. O caminho final deverá ser `C:\Projetos\flappybird\README.md`.

**Importante:** baixar ZIP não preserva o histórico de commits do Git. É adequado para obter uma cópia inicial, mas para versionamento posterior será necessário inicializar ou conectar um repositório.

## 3. Opção B — Clonar com Git (recomendado para versionamento)
Abra o terminal PowerShell e execute:

```powershell
cd C:\Projetos
git --version
git clone https://github.com/wilson-luciano/flappybird.git flappybird
cd flappybird
code .
```

O endereço acima já corresponde ao repositório oficial. O comando `git clone` cria a pasta `flappybird` e mantém o histórico Git. **Não execute o clone se já existir uma pasta `C:\Projetos\flappybird` com arquivos**; escolha um dos métodos ou consulte o professor para preservar o trabalho.

## 4. Conferência do download
No PowerShell:

```powershell
cd C:\Projetos\flappybird
dir
code .
```

Confirme que `README.md`, `aulas`, `src` e `requirements.txt` aparecem na raiz. Se o terminal disser que o caminho não existe, revise o local da extração e a grafia do nome da pasta. Se aparecer `flappybird\flappybird`, corrija o nível da pasta antes de continuar.

## 5. Atualizar uma cópia já clonada com `git pull`

Se o projeto já foi clonado e o professor publicou alterações, **não repita `git clone`**. No PowerShell, entre na pasta existente, confira suas modificações e atualize:

```powershell
cd C:\Projetos\flappybird
git status
git pull origin main
```

`git clone` obtém a primeira cópia do repositório e cria sua pasta; `git pull` busca e integra atualizações em uma cópia Git já existente. **Se houver alterações locais**, confira-as antes de atualizar: um `pull` pode exigir resolver conflitos. Quem baixou um ZIP não dispõe automaticamente do vínculo Git necessário ao `pull`.

## 6. ZIP ou clone: qual escolher?

| Download ZIP | git clone |
|---|---|
| Não exige comandos Git | Exige Git instalado |
| Não traz histórico de commits | Preserva histórico e vínculo remoto |
| Útil para primeiro acesso | Melhor para acompanhar atualizações |

## 7. Como baixar o executável (quando publicado)
O código-fonte pode ser baixado agora pelo botão **Code**. O jogo pronto para Windows, quando disponibilizado, será encontrado em [Releases](https://github.com/wilson-luciano/flappybird/releases): escolha uma versão publicada, expanda **Assets** e clique em `FlappyBird.exe`. Se não houver Release ou esse arquivo não estiver listado, o executável ainda não está disponível para download. Caso o Windows apresente um aviso do SmartScreen, verifique a procedência do arquivo e faça uma análise com o Microsoft Defender antes de decidir executá-lo; não desative as proteções do sistema.

## 8. Próximo passo
Abra a **Aula 01.0** para estudar o planejamento e siga a **Aula 01.1** para configurar `.venv`, instalar Pygame e executar a primeira janela.

## Checklist
- [ ] Material obtido do repositório oficial
- [ ] Arquivos extraídos sem duplicação de pastas
- [ ] Projeto localizado em `C:\Projetos\flappybird`
- [ ] `README.md` e `src/main.py` encontrados
- [ ] Pasta aberta no VS Code

---
© 2026 **Wilson Luciano** · Programação para Engenharia Mecânica · Universidade Federal de Sergipe (UFS/DMEC) · Material didático.
