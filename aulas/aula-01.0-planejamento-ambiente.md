# Aula 01.0 — Planejamento, Ambiente e Primeira Interface do Flappy Bird

**Disciplina:** Programação para Engenharia Mecânica — 2026.2  
**Projeto avaliativo 2:** Flappy Bird com Python e Pygame  
**Local:** DMEC — Laboratório 26 (Informática)

## 1. Objetivos
Ao final, o estudante deverá: explicar o ciclo de execução de um jogo; distinguir FPS e tempo decorrido; criar um ambiente virtual; instalar Pygame; organizar um repositório; implementar uma janela e encerrá-la corretamente.

## 2. Contextualização
O jogo permite aplicar algoritmos, eventos, condicionais, laços, funções e classes. A simulação do movimento será aprofundada na Aula 02, com atenção à diferença entre modelos físicos e aproximações discretas.

## 3. Ferramentas
- Python 3.12 (preferencialmente 3.12.10)
- VS Code com extensão Python
- Git e conta GitHub
- Pygame instalado no ambiente virtual `.venv`

## 4. Conceitos
**Loop principal:** executa repetidamente leitura de eventos, atualização do estado e desenho.  
**Evento:** ação recebida do teclado, mouse ou sistema operacional.  
**FPS:** quadros por segundo; `clock.tick(30)` limita a frequência máxima, não garante duração exata de cada quadro.  
**Superfície:** região gráfica usada para desenhar elementos.  
**Ambiente virtual:** instalação isolada de dependências por projeto.

## 5. Roadmap
| Aula | Sprint | Entrega |
|---|---|---|
| 01 | 00 e 01 | Ambiente, estrutura, janela e loop |
| 02 | 02 | Pássaro, gravidade, salto e animação |
| 03 | 03 | Canos, colisões e pontuação |
| 04 | 04 e 05 | Recursos, testes, documentação e entrega |

## 6. Arquivos especiais do projeto: `.gitkeep` e `.gitignore`

Ao organizar o Flappy Bird, algumas pastas podem estar inicialmente vazias, como `assets/` e `tests/`. A pasta `docs/` já contém o roadmap e os documentos das sprints, portanto não precisa de `.gitkeep`. **O Git registra arquivos, mas não registra diretórios vazios isoladamente.** Para que a estrutura dessas pastas apareça no repositório e seja recuperada pelos alunos, podemos adicionar um arquivo vazio chamado `.gitkeep`.

Por exemplo:

```text
assets/
└── .gitkeep
tests/
└── .gitkeep
```

O nome `.gitkeep` é **uma convenção da comunidade**, não um recurso especial ou comando do Git. O arquivo não precisa conter texto e não é executado pelo Python. Quando a pasta passar a conter arquivos reais, ele poderá ser removido, desde que os novos arquivos sejam versionados.

**Não confunda `.gitkeep` com `.gitignore`:**

| Arquivo | Função | Exemplo no Flappy Bird |
|---|---|---|
| `.gitkeep` | Arquivo convencional para manter uma pasta inicialmente vazia no repositório. | `tests/.gitkeep` |
| `.gitignore` | Arquivo de regras que informa ao Git quais caminhos não devem ser rastreados, respeitadas as regras de arquivos já versionados. | `.venv/`, `__pycache__/` |

Ao publicar o projeto no GitHub, os arquivos `.gitkeep` versionados permitem que essas pastas apareçam no repositório. Quando o aluno baixar o ZIP ou usar `git clone`, a estrutura correspondente também será recuperada. Já a pasta `.venv`, ignorada pelo Git, deverá ser criada **localmente** por cada aluno.

**Questão de reflexão:** se removermos `assets/.gitkeep` e a pasta `assets/` não contiver outros arquivos versionados, o que acontecerá com ela após um novo clone do repositório?

## 7. Preparação do gerenciador de pacotes

Para instalar o Pygame no ambiente virtual, utilizamos o **pip**, gerenciador de pacotes do Python. O comando `python -m pip` executa o pip associado ao interpretador Python ativo, reduzindo a possibilidade de instalar pacotes no ambiente errado.

```powershell
python -m pip install --upgrade pip
```

Esse comando atualiza **somente o pip**, ferramenta responsável pela instalação e pelo gerenciamento de pacotes Python. As ferramentas `setuptools` (utilizada na construção e distribuição de pacotes) e `wheel` (utilizada na construção de pacotes no formato `.whl`) também podem ser instaladas ou atualizadas com:

```powershell
python -m pip install --upgrade pip setuptools wheel
```

Entretanto, **não é necessário instalar ou atualizar explicitamente `setuptools` e `wheel` para a instalação usual do Pygame**, quando há um pacote binário compatível com a versão do Python e o sistema operacional. Por isso, neste projeto, atualizaremos apenas o `pip` antes de instalar o Pygame.

Depois, instalamos o Pygame com `python -m pip install pygame`. A execução e a verificação desses comandos estão detalhadas na **Aula 01.1 — Passo 7**.

## 8. Documentação das sprints e critérios de aceitação

O **roadmap** e as **Sprints 00 a 05** já estão documentados em arquivos próprios. Não é necessário preencher esses documentos do zero: eles são referências para acompanhamento das tarefas, evidências e critérios de aceitação. Os arquivos ficam em `docs/`, separados dos roteiros das aulas.

- [Roadmap completo](../docs/roadmap.md)
- [Sprint 00 — Preparacao ambiente](../docs/sprints/sprint-00-preparacao-ambiente.md)
- [Sprint 01 — Primeira interface](../docs/sprints/sprint-01-primeira-interface.md)
- [Sprint 02 — Fisica movimento](../docs/sprints/sprint-02-fisica-movimento.md)
- [Sprint 03 — Obstaculos colisoes pontuacao](../docs/sprints/sprint-03-obstaculos-colisoes-pontuacao.md)
- [Sprint 04 — Recursos avancados](../docs/sprints/sprint-04-recursos-avancados.md)
- [Sprint 05 — Testes documentacao entrega](../docs/sprints/sprint-05-testes-documentacao-entrega.md)

Nesta etapa, a **Sprint 00** valida o ambiente, as dependências, a organização e o versionamento inicial; a **Sprint 01** valida a janela de **575 × 860 pixels**, o loop de eventos, o encerramento e a execução no ambiente virtual. Os critérios detalhados e os checklists oficiais estão nos respectivos arquivos, evitando duplicações que possam ficar desatualizadas.

### Estrutura de referência do projeto

A árvore segue o padrão do Explorador do VS Code: **pastas primeiro, em ordem alfabética, seguidas dos arquivos da raiz**. Os documentos das aulas posteriores serão adicionados à medida que forem produzidos.

```text
flappybird/
├── assets/
│   └── .gitkeep
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

**Nota:** a pasta `docs/` já contém arquivos reais; portanto, não precisa mais de `docs/.gitkeep`. A pasta `.venv/` será criada localmente durante o roteiro prático e não deve ser enviada ao GitHub.

## 9. Avaliação do Projeto 2 (Aulas 01–04)
| Nº | Critério | Pontos |
|---|---|---:|
| 1 | Identificação de pasta e arquivos conforme padrão PPEM Python – Aluno1-Aluno2-Aluno3 – Projeto 2 – 26.2 | 0,5 |
| 2 | Relatório técnico completo | 1,0 |
| 3 | Ambiente Python, dependências e estrutura | 0,5 |
| 4 | Explicação dos parâmetros e funcionamento | 1,0 |
| 5 | Originalidade, complexidade e criatividade | 1,0 |
| 6 | Estrutura, legibilidade e qualidade do código | 1,0 |
| 7 | Controles, obstáculos e colisões funcionais | 1,0 |
| 8 | Pontuação, vidas, encerramento e reinício | 1,0 |
| 9 | Compreensão da física e programação | 0,5 |
| 10 | Testes, erros e limitações | 0,5 |
| 11 | README e Git/GitHub | 0,5 |
| 12 | Incrementos efetivamente implementados | 0,5 |
| 13 | Apresentação em PowerPoint | 0,5 |
| 14 | Bibliografia e créditos | 0,5 |
| **Total** | | **10,0** |

**Entregas:** relatório PDF, código e recursos, apresentação PowerPoint, link do GitHub, README e referências. Um executável não substitui o código-fonte.  
**Descontos:** 2,0 pontos por não apresentação/ausência; 0,5 ponto por arquivo enviado que não abre, adicionais à avaliação dos critérios.  
**Observação:** o item 5 avalia criatividade da proposta; o 12, incrementos implementados. O item 2 avalia o relatório; o 11, instruções de execução e versionamento.

## 10. Questões de fixação
1. Qual a diferença entre loop principal e evento?
2. Por que instalar Pygame dentro de `.venv`?
3. O que acontece quando o usuário fecha a janela?
4. Por que a pasta `.venv` não deve ser enviada ao GitHub?
5. Qual é a vantagem de concluir uma sprint antes da próxima?

---
© 2026 **Wilson Luciano** · **Programação para Engenharia Mecânica** · **Departamento de Engenharia Mecânica (DMEC)** · **Universidade Federal de Sergipe (UFS)**.  
Material didático do projeto **Flappy Bird com Python e Pygame** · **Versão 0.1.0**.
