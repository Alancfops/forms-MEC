# forms-cesmac – Sistema Fabiana

Sistema do **CITEC / CESMAC** para a **Procuradoria Institucional** organizar a comprovação dos indicadores de qualidade exigidos pelo MEC: checklist por período (dimensões → indicadores → subindicadores → anexos), envio de documentos pelas coordenações de curso, validação, repositórios e histórico das avaliações. Chama-se **Fabiana** (antes “Mozart”).

Idioma de trabalho: **português do Brasil**.

## Situação (12/11/2026)

| Fase | Situação |
|---|---|
| Requisitos | **Concluídos – v5.1** (RF001–RF017). Aguardando validação da Fabiana (`docs/requisitos/pendencias.md`) |
| Arquitetura | **Definida** (ver “Decisões confirmadas” e `docs/README.md`) |
| Ambiente do Claude | Skills, agentes e comandos prontos (abaixo) |
| Código | **Não iniciado**; repositório criado (`main` e `develop`), sem código ainda |

O autor original (Alan) está saindo do projeto; este arquivo e a `docs/` foram preparados para quem assumir. Comece por `docs/README.md` (tem a ordem de leitura).

## Estrutura

```
docs/
├── README.md        # índice: situação, arquitetura (diagramas), fluxo Git, RFs, próximos passos, “para quem assume”
├── prd.md           # PRD: problema, objetivos, usuários, funcionalidades F1–F13 (RFs), MVP e fases
├── glossario.md     # termos MEC/INEP, instituição e sistema, com fonte
├── fontes/          # material recebido — não editar (transcrição, INEP 2017, esboço, fluxo da dupla, checklist de Medicina, prints do Miro)
└── requisitos/      # levantamento .docx/.pdf (oficial) e pendencias.md
.agents/ + AGENTS.md # mesma configuração no formato do Google Antigravity, para quem não usa Claude (ver “Manutenção”)
.claude/
├── agents/          # subagentes (tabela abaixo)
├── skills/          # skills e comandos (tabelas abaixo)
└── gerador-docx/    # gera o .docx do levantamento (modelo-tcc.docx = molde do TCC)
```

## Comandos (digitados pelo desenvolvedor)

| Comando | O que faz | Skill |
|---|---|---|
| `/ajuda [tema]` | Explica os comandos, os agentes e o fluxo típico; com tema, detalha um comando, agente ou tarefa | `.claude/skills/ajuda/` |
| `/git` | Pergunta o que fazer: abrir branch, commitar, abrir PR ou fechar branch (também entrega e hotfix pelo “Outro”) | `.claude/skills/git/` |
| `/commit [texto]` | Commita em Conventional Commits perguntando só o idioma (português ou inglês); não faz push; na `main`/`develop` só com motivo explicado | `.claude/skills/commit/` |
| `/revisar [PR\|branch\|caminho] [--publicar]` | Aciona o agente `code-reviewer`; com `--publicar`, comenta no PR (nunca aprova) | `.claude/skills/revisar/` |
| `/session [obs]` | Salva o registro da sessão (onde parou, o que foi feito, próximos passos) na memória do projeto | `.claude/skills/session/` |

`/revisar` e `/session` **só rodam quando digitados**. `/git` e `/commit` também são usados pelo Claude quando a tarefa pede (ex: abrir branch antes de implementar um RF).

## Agentes

| Agente | Quando usar | Skills que carrega |
|---|---|---|
| `backend-senior` | Implementar/alterar backend, decidir onde fica uma regra, investigar bug no backend | `backend`, `qualidade-codigo` (+ `commit`, `git`) |
| `frontend-senior` | Telas, templates, htmx, CSS, controllers web, acessibilidade e responsividade | `frontend`, `qualidade-codigo` (+ `backend`, `commit`, `git`) |
| `code-reviewer` | **Só via `/revisar`.** Revisão imparcial de back e front, somente leitura, relatório com veredito | `qualidade-codigo`, `backend`, `frontend` (+ `commit`, `git`) |
| `engenheiro-requisitos` | Levantamento ou atualização dos requisitos a partir de `docs/fontes/` | `especialista-requisitos-uml` |

Regras comuns aos agentes de desenvolvimento: imparciais e rigorosos (bloqueante × sugestão × preferência, críticas verificáveis), **nunca fazem merge** nem aprovam PR, e terminam com relatório. `backend-senior` e `frontend-senior` aceitam debate: devolvem “Ponto para debate” com opções e recomendação, e a palavra final é do desenvolvedor (salvo segurança, integridade de dados ou acessibilidade AA). **Subagentes não falam com o usuário:** repasse as perguntas e os pontos para debate e retome o mesmo agente (SendMessage) com a resposta.

## Skills de referência (o Claude usa sozinho)

| Skill | Conteúdo |
|---|---|
| `qualidade-codigo` | Clean code, testes (regra do RF → teste; permissão obrigatória; Testcontainers), portão de qualidade (`./mvnw verify`), roteiro de code review, `assets/ci-exemplo.yml` |
| `backend` | Clean Architecture por módulo (`domain` / `application` / `adapters` / `config`), regra de dependência testada, portas, eventos entre módulos, exemplo completo do RF004 |
| `frontend` | Thymeleaf + htmx, `assets/tokens.css` (cores do projeto + semafóricas, contrastes calculados), WCAG 2.2 AA, mobile first, receitas htmx |
| `especialista-requisitos-uml` | Elicitação, especificação e modelagem de requisitos |

## Como trabalhar aqui

- **Implementar um RF:** abrir branch (`/git`) → delegar ao `backend-senior` e/ou `frontend-senior` → `/commit` → `/git` abrir PR → o desenvolvedor pede `/revisar` se quiser → aprovação e merge **por um humano** → `/git` fechar branch.
- **Revisão de código:** só quando o desenvolvedor digitar `/revisar`. Não acione o `code-reviewer` por iniciativa própria.
- **Requisitos:** levantamento completo pelo agente `engenheiro-requisitos`; ajustes pontuais com a skill `especialista-requisitos-uml`. Dúvidas de negócio vão para `docs/requisitos/pendencias.md`, nunca são inventadas.
- **Alterar o documento de requisitos:** edite `.claude/gerador-docx/conteudo.py` e rode `.claude/gerador-docx/gerar.sh` (nunca editar o .docx à mão).
- **Leitura de fontes:** PDF e imagens com Read; `.docx` com `unzip -p "<arquivo>" word/document.xml | sed 's/<[^>]*>/ /g'` (`pandoc` não está instalado).

## Documento de requisitos: estilo (seguir sempre)

- `docs/requisitos/Levantamento de requisitos - Projeto Fabiana.docx` é o **documento oficial**: o .docx do TCC com o conteúdo substituído, **mesmas seções e formatação** (Calibri, sumário, cabeçalho). Seção 3 (RF001–RF017) e 7 (matriz de rastreabilidade) preenchidas; seções 4 RNF, 5 Segurança, 6 Matriz de Risco e 8 Ponto de função **só com títulos/tabelas vazias** (decisão do usuário). Sem seções extras nem linha de prioridade nos RFs.
- Tabela de 2 colunas `ID | Descrição`. Título da linha: "Requisito funcional que trata do/da …" (negrito).
- "Campos do formulário:" (entrada) ou "Campos do requisito:" (exibição). Cada campo: `Nome (Obrigatório|Opcional|Automático)` + números das regras em sobrescrito + `:` + quebra + `Tipo (detalhe). Regra curta.` Tipos: String, Integer, Enum (A / B), Lista, Lista/Card, Ação, Visual, Arquivo, Data(s), Texto, Decimal.
- "Regras e observações dos campos:" numeradas em sobrescrito, frases "O sistema deve …", mensagens de tela entre aspas curvas, "(RF00X)", exemplos com "(ex: …)". Exclusões sempre com tela de confirmação. RFs sem tecnologia.
- Gerado por script Python sobre o XML do modelo (sem python-docx/lxml); sumário calculado com `soffice --headless` + `pdftotext`. Novos RFs entram no fim.
- Diagramas: **só de arquitetura**, em Mermaid, no `docs/README.md` (o usuário não quer UML de casos de uso).

## Convenções

- IDs estáveis: `RF001`, `RNF001`, `RN001`. Nunca renumerar; removidos ficam `[CANCELADO]`.
- Todo requisito cita a fonte; inferências marcadas `[SUPOSIÇÃO]`; nada inventado.
- Código: domínio em português sem acento (igual ao glossário), termos técnicos em inglês; commits e PRs em português ou inglês, à escolha do desenvolvedor (o `/commit` pergunta; tipo do Conventional Commits sempre em inglês); branches `tipo/descricao` saindo da `develop`.
- **Autoria só do desenvolvedor:** nenhuma IA (Claude ou outra) aparece como autora ou coautora em commits, PRs ou comentários. `.claude/settings.json` desliga a atribuição automática (`attribution.commit`/`pr` vazios, `sessionUrl: false`).

## Manutenção deste arquivo

**Sempre atualize este CLAUDE.md quando algo novo for feito**: novo arquivo em `docs/`, novo agente, skill ou comando (atualize as tabelas acima), decisão tomada, convenção nova ou mudança de situação. Registre também no histórico.

**Estrutura espelhada para o Antigravity.** Quem não usa o Claude Code usa `AGENTS.md`, `.agents/rules/`, `.agents/skills/` e `.agents/agents/`, com o mesmo conteúdo adaptado ao formato do Antigravity:
- ferramentas `view_file`/`replace_file_content`/`run_command`;
- `skills: - skills/<nome>` nos agentes;
- `/session` salvando em `docs/sessoes/`;
- `/revisar` usando `invoke_subagent`.

**Toda mudança em skill, agente, comando ou decisão precisa ser repetida lá**, e o `AGENTS.md` atualizado. As regras de `.agents/rules/` resumem as skills `backend`, `frontend`, `git`/`commit` e o estilo do documento de requisitos: mantenha-as coerentes.

## Decisões confirmadas

- **Os requisitos seguem o fluxo de telas da dupla** (v5). Perfis: Administrador Master (usuários), Administrador (Pró-Reitores + Procuradoria [SUPOSIÇÃO]: checklist, validação, histórico), Coordenação de Curso (envia documentos dos cursos vinculados). Antes, só a Procuradoria gerenciava.
- Revisão + validação = uma etapa só.
- Hierarquia: Dimensão → Indicador → **Subindicador (manter sempre)** → Anexo. Desde a v4, o anexo é numerado por dimensão e vinculado a um ou mais indicadores ou subindicadores. **Ainda falta confirmar o vínculo com a Fabiana.**
- Repositórios **por dimensão e por indicador** (transcrição) → RF017.
- Nome do sistema: **Fabiana** (antes "Mozart"; "Qualis5" no esboço). Títulos de documentos-fonte (ex.: transcrição "Projeto Mozart") ficam com o nome original.
- Notas do MEC são fracionadas.
- Telas **definidas**: Thymeleaf + htmx, cores do projeto branco/azul/amarelo + **cores semafóricas valendo** para estados (verde sucesso, amarelo atenção, vermelho erro) (tons livres; **mudar cor exige perguntar ao usuário e explicar o porquê**), WCAG 2 AA, mobile first.
- Arquitetura **definida**: Java, monolito modular com **Clean Architecture** em cada módulo, um repositório, frontend Thymeleaf em módulo separado, code review + clean code + testes no CI. **Sugestões iniciais, que o próximo dev pode trocar**: Java 21, Spring Boot + Maven, PostgreSQL (Flyway), MinIO (S3), JUnit/Testcontainers/Modulith ou ArchUnit/Spotless/Checkstyle. Em aberto: login CESMAC (TI), hospedagem/CI.
- **Prints do Miro são só exemplo** para entender o fluxo, **não são o design** (usuário, 12/11/2026).
- Cursos: só bacharelado (sem licenciatura/tecnológico), há presencial e EaD; RF003 mantém Modalidade, Área da saúde e DCN.
- **`main` protegida no GitHub** (PR com 1 aprovação, sem force push/exclusão; administradores podem passar por cima). **Commit direto na `main` só se o desenvolvedor explicar o motivo** (vale para quem assumir o projeto, que precisa ser Admin no repositório); o motivo vai no corpo do commit (`Direto na main: …`). `develop` sem proteção, fluxo por PR por combinado (usuário, 12/11/2026).
- Checklist único por período com etiquetas de curso (v5, RF009). Substitui a regra anterior de modelo institucional aplicado curso a curso.

## Histórico

- **2026-11-09** — Criada a skill `especialista-requisitos-uml` (com `referencias/`), o agente `engenheiro-requisitos` e este CLAUDE.md.
- **2026-11-09** — Levantamento v1 gerado: `docs/requisitos/Levantamento de requisitos - Projeto Fabiana.docx` com RF001–RF014 (login via sistema acadêmico, whitelist, cursos, períodos, gerência de checklist, dimensões, indicadores, anexos, modelo institucional × curso, envio de documentos, revisão/validação, histórico MEC, consulta de evolução, versões PDI/PPC) + `pendencias.md` (12 perguntas abertas). Aguardando respostas da Fabiana (Procuradoria) e o checklist que ela enviaria por WhatsApp.
- **2026-11-09** — v2 com respostas do usuário: Coordenação de Curso usa o sistema (só envia docs dos seus cursos); revisão/validação em etapa única; só a Procuradoria Institucional gerencia; novo **RF015 subindicadores**; notas de dimensão/CC fracionadas, conceito de indicador 1–5 ou NSA (conforme INEP). Adicionado `curso_reconhecimento.pdf` (INEP 2017) → critérios de análise e NSA no RF007. Próximos insumos: questionários da Fabiana (ela adapta o instrumento INEP por curso) e telas do Miro.

- **2026-11-09** — v3: documento refeito em cima do modelo do TCC (substituição de conteúdo, sem seções extras). Removidos "Termos e abreviações" e "Usuários do sistema" (usuário achou grande/diferente). Fonte corrigida para Calibri. Nome do sistema: Fabiana.

- **2026-11-10** — Recebido o checklist de Medicina da Fabiana (`~/Downloads/Check List MEDICINA.doc`: documentos que comprovam cada indicador INEP, Dimensões 1–3). Gerada versão corrigida `~/Downloads/Check List MEDICINA - corrigido.docx/.pdf`: uma linha por indicador (1.1–1.24, 2.1–2.16, 3.1–3.18), cada uma só com os seus documentos (os documentos compartilhados se repetem com o número original), tabelas das Dimensões 2 e 3 separadas (antes ficavam sobrepostas) e timbre fora do texto. Ainda não está em `docs/`. Distribuição dos documentos conferida com os critérios de análise do `curso_reconhecimento.pdf`; o que não se encaixa em nenhum indicador fica na linha "Documentos sem indicador correspondente" ao fim de cada dimensão (decisão do usuário).

- **2026-11-10** — v4 do levantamento com base no checklist de Medicina: RF008 reescrito (anexos numerados por dimensão, com subnível e itens, vinculados a vários indicadores; grupos “Documentos sem indicador correspondente” e “Outras referências”; observação), RF003 ganhou Modalidade e Área da saúde, RF007 ganhou Aplicabilidade + NSA automático e numeração só muda com confirmação, RF010 aceita documento único para vários indicadores, novo **RF016** (exportação do checklist em PDF). Pendências atualizadas (perguntas 1–1d). Usuário vai ler e depois validar com a Fabiana. Backup da v3 em scratchpad da sessão.

- **2026-11-10** — v4.1: usuário confirmou que o **subindicador continua** (RF015 mantido; incluído na exportação RF016). Novo **RF017**: consulta aos repositórios por dimensão e por indicador, conforme a transcrição (substitui a nuvem; download de pastas por anexo; Pró-Reitores veem todos os cursos, Coordenação só os seus). Abrangência ajustada.

- **2026-11-10** — v5: requisitos refeitos **em cima do fluxo de telas da dupla** (`Sistema Fabiana (1).jpg`). O usuário quer que a Fabiana aprove ou reprove o fluxo pelo documento antes do protótipo. Perfis Administrador Master / Administrador (Pró-Reitores + Procuradoria) / Coordenação; whitelist por e-mail; RF009 reescrito: checklist único por período com **etiquetas de curso**, no lugar de modelo institucional + cópia por curso; RF004 com “Usar modelo do ano anterior” / “Criar novo modelo”; RF008 com documento exemplo e checkbox; criação em janela (RF006/RF007). Tabela A–G de mudanças em `pendencias.md`. Backup da v4.1 do conteudo.py no scratchpad.

- **2026-11-12** — v5.1: a faculdade só tem **bacharelado** → campo Grau removido do RF003, regra do checklist separado para tecnológicos removida do RF009, “Licenciatura” saiu da Aplicabilidade do RF007. **Área da saúde mantida** (ainda não se sabe se os cursos vêm do sistema acadêmico ou se a Fabiana cadastra à mão — pendência 5). Usuário confirmou: **DCN fica** (a Fabiana monta o checklist do curso a partir da DCN, conforme a transcrição) e **Modalidade fica** (há cursos EaD). A transcrição não diz quem cadastra os cursos. Backup da v5 no scratchpad.

- **2026-11-12** — Prints do Miro em boa resolução salvos em `docs/requisito/miro/`. RF001 ganhou o botão **“Entrar com CESMAC”** (possibilidade de usar a autenticação da instituição; a confirmar com a TI, pendência 5). O campo “Áreas” (chip “todos”) das janelas de dimensão e indicador = etiquetas de curso (Medicina, Odontologia…), confirmado pelo usuário; RF006/RF007 citam o nome “Áreas”.

- **2026-11-12** — **Construção dos requisitos finalizada**; início da organização do projeto. `docs/` reorganizada: `docs/requisito/` → `docs/fontes/` (arquivos renomeados), checklist de Medicina e fluxo da dupla copiados de `~/Downloads` para `docs/fontes/`. O .docx molde do TCC saiu de `docs/` e virou `.claude/gerador-docx/modelo-tcc.docx` (o gerador depende dele); documento regenerado idêntico.

- **2026-11-12** — Criados `docs/README.md` (índice: situação, fontes, RFs, como gerar o .docx, próximos passos) e `docs/glossario.md` (MEC/INEP, instituição, sistema; cada termo com fonte). Glossário fica fora do .docx (decisão anterior do usuário).

- **2026-11-12** — Seção “Arquitetura do sistema” no `docs/README.md`: diagramas Mermaid de contexto, módulos (com RFs) e caminho de um documento + tabela de módulos. Decisão do usuário: diagramas de arquitetura no README, não UML de casos de uso.

- **2026-11-12** — Arquitetura decidida pelo usuário: Java, monolito modular, monorepo com `backend/` e `frontend/` (Thymeleaf) separados, um executável; code review, clean code e testes. Microsserviços descartados. Registrado no `docs/README.md` (Decisões, estrutura do repositório, “Ainda a decidir”, “Para quem assume o projeto”). Não é mais trabalho em dupla; o usuário vai sair do projeto e está preparando o ambiente para o próximo responsável.

- **2026-11-12** — Stack: Spring Boot + Maven, PostgreSQL, MinIO (S3). Usuário esclareceu que o Miro é só exemplo, não o design.

- **2026-11-12** — htmx para a interatividade. Usuário: framework, banco, storage, htmx e ferramentas são **sugestões**, não decisões; o próximo desenvolvedor pode alterar. README separado em “Definido” × “Sugestões iniciais”.

- **2026-11-12** — Criado `docs/prd.md` (PRD v1.0): problema, objetivos, fora do escopo, métricas sugeridas, perfis, funcionalidades F1–F13 ligadas aos RFs (Essencial = MVP, Importante = fase 2), fluxo, RNFs conhecidos/a definir, riscos, fases 0–2.

- **2026-11-12** — Criada a skill `fluxo-git`: `main` (produção) e `develop` (integração), branches `tipo/descricao` (mesmo tipo do Conventional Commits) saindo da develop, commits com escopo = módulo e `Refs: RF00X`, PR para develop no GitHub com CI + 1 aprovação, squash merge, Claude não faz merge; entrega por PR develop→main (merge commit); hotfix sai da main. Resumo no `docs/README.md`.

- **2026-11-12** — Criada a skill `qualidade-codigo` (SKILL.md + references clean-code/testes/code-review + assets/ci-exemplo.yml). Convenções propostas: domínio em português sem acento (igual ao glossário), termos técnicos em inglês; regras de RF viram testes; testes de permissão obrigatórios; banco real com Testcontainers; cobertura sugerida 80% em domínio/serviços; Claude revisa mas não aprova/mergeia.

- **2026-11-12** — `fluxo-git` renomeada para `git` (`/git`, pergunta: abrir branch / commitar / abrir PR / fechar branch). Nova skill `commit` (`/commit`, commita direto, sem perguntas; bloqueia em main/develop). Commits em português (tipo do Conventional Commits continua em inglês).

- **2026-11-12** — Skill `session` (`/session`) copiada de `~/.claude/skills/session/` para `.claude/skills/session/`, para quem assumir também ter o comando.

- **2026-11-12** — Skill `backend` descrita pelo usuário: Java, clean code + Clean Architecture para manter código e estrutura limpos. Escrita com camadas domain/application/adapters/config por módulo, portas e adaptadores, entidade JPA separada do domínio, permissão no caso de uso, eventos entre módulos, testes por camada e de arquitetura; exemplo completo do RF004 em `references/`. `clean-code.md` passou a apontar para ela.

- **2026-11-12** — Skill `frontend` descrita pelo usuário: Thymeleaf + htmx, paleta baseada em branco, azul e amarelo (mudança de cor só com pergunta e justificativa), WCAG 2, mobile first. Escrita com `assets/tokens.css` (contrastes calculados), `references/acessibilidade.md` (WCAG 2.2 AA aplicada) e `references/htmx-padroes.md` (janela, erro 422, exclusão, reordenação acessível, etiquetas, upload). htmx deixou de ser sugestão e virou definido.

- **2026-11-12** — Criado o agente `backend-senior`: usa as skills `backend` e `qualidade-codigo` (e `commit`/`git` quando preciso), imparcial e rigoroso (bloqueante × sugestão × preferência, críticas verificáveis), aceita debate (devolve “Ponto para debate” com opções e recomendação; muda de ideia com argumento melhor; palavra final do desenvolvedor, salvo segurança/integridade), nunca faz merge, e termina com relatório (o que foi feito, mudanças, decisões, testes, pontos).

- **2026-11-12** — Usuário: branco/azul/amarelo é a cor **do projeto**; as **semafóricas continuam valendo**. Tokens ganharam verde e vermelho (contraste AA calculado) e papéis sucesso/atenção/erro/info/neutro; Validado = verde, Enviado = amarelo, Devolvido para ajuste = vermelho.

- **2026-11-12** — Criado o agente `frontend-senior`, no mesmo formato do `backend-senior`: skills `frontend` + `qualidade-codigo` (e `backend`/`commit`/`git` quando preciso), bloqueantes de acessibilidade/cores/arquitetura listados, mudança de cor sempre devolvida para aprovação do usuário, debate com “Ponto para debate”, relatório com seção de acessibilidade e responsividade.

- **2026-11-12** — Criados o agente `code-reviewer` (imparcial com back e front, só leitura, não corrige/aprova/mergeia, publica no GitHub só com pedido e nunca `--approve`, relatório com veredito e gravidades) e a skill `review` (`/review`), única forma de acioná-lo. Descrições do `backend-senior`/`frontend-senior` deixam a revisão formal de PR para o comando.

- **2026-11-12** — `/review` renomeado para **`/revisar`** (skill `.claude/skills/revisar/`), para não colidir com um possível comando nativo do Claude Code. CLAUDE.md reorganizado com seções de comandos, agentes e skills.

- **2026-11-12** — Criada a estrutura do **Google Antigravity** para quem não usa Claude: `AGENTS.md` (equivalente a este arquivo), `.agents/rules/` (projeto = always_on; backend e frontend = glob; git e documento de requisitos = model_decision), `.agents/skills/` (cópia adaptada das 8 skills; no Antigravity, skill = comando `/nome`, não há pasta de comandos) e `.agents/agents/` (4 agentes com ferramentas `view_file`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `grep_search`, `run_command`). `/session` do Antigravity salva em `docs/sessoes/`.

- **2026-11-12** — Usuário: **nenhuma IA aparece como colaboradora**, só o desenvolvedor. Criado `.claude/settings.json` com a atribuição do Claude Code desligada; regra de autoria nas skills `commit` e `git` (Claude e Antigravity), em `.agents/rules/` e no `AGENTS.md`.

- **2026-11-12** — Repositório criado: `git@github.com:Alancfops/forms-MEC.git`. Commit inicial direto na `main` (exceção autorizada pelo usuário, sem PR) e `develop` criada a partir dela. README da raiz e `.gitignore` criados. Gerador do .docx sem caminhos absolutos (`build.py`/`gerar.sh` relativos à pasta), saída conferida idêntica.

- **2026-11-12** — Usuário decidiu **não proteger** `main`/`develop` no GitHub. Skill `git` (passo 3 da configuração inicial), `docs/README.md` e `docs/prd.md` ajustados; o fluxo por PR continua como combinado.

- **2026-11-12** — Usuário reconsiderou: **`main` protegida** no GitHub (aplicado via API, admin pode passar por cima), e o Claude permite commit direto na `main` quando o desenvolvedor explica o porquê. Seção “Exceção” na skill `git`, bloqueio da skill `commit` ajustado; `develop` segue sem proteção.

- **2026-11-12** — Novo comando **`/ajuda`** (Claude e Antigravity): explica comandos, agentes e fluxo típico, para quem assumir. `/commit` agora **pergunta o idioma** da mensagem (português ou inglês; pula se já indicado no comando, ex: `/commit en`, ou já respondido na conversa); tipo continua em inglês. Commit direto na `main` vale também para quem assumir, com motivo explicado e permissão Admin.
