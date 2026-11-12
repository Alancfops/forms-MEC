# AGENTS.md – Sistema Fabiana

Instruções para agentes de IA que **não** são o Claude Code (ex: Google Antigravity). Quem usa o Claude Code segue o `CLAUDE.md` e a pasta `.claude/`. As duas estruturas descrevem o mesmo projeto e as mesmas regras; **ao mudar uma, mude a outra** (veja “Manutenção”).

Sistema do **CITEC / CESMAC** para a **Procuradoria Institucional** organizar a comprovação dos indicadores de qualidade exigidos pelo MEC: checklist por período (dimensões → indicadores → subindicadores → anexos), envio de documentos pelas coordenações de curso, validação, repositórios e histórico das avaliações. Chama-se **Fabiana** (antes “Mozart”).

Idioma de trabalho: **português do Brasil**.

## Situação (12/11/2026)

| Fase | Situação |
|---|---|
| Requisitos | **Concluídos – v5.1** (RF001–RF017). Aguardando validação da Fabiana (`docs/requisitos/pendencias.md`) |
| Arquitetura | **Definida** (ver “Decisões confirmadas” e `docs/README.md`) |
| Ambiente dos agentes | Skills, agentes, regras e comandos prontos em `.agents/` (abaixo) |
| Código | **Não iniciado**; repositório criado (`main` e `develop`), sem código ainda |

Comece por `docs/README.md`, que tem a ordem de leitura.

## Estrutura

```
docs/
├── README.md        # índice: situação, arquitetura (diagramas), fluxo Git, RFs, próximos passos, “para quem assume”
├── prd.md           # PRD: problema, objetivos, usuários, funcionalidades F1–F13 (RFs), MVP e fases
├── glossario.md     # termos MEC/INEP, instituição e sistema, com fonte
├── fontes/          # material recebido — não editar
├── requisitos/      # levantamento .docx/.pdf (oficial) e pendencias.md
└── sessoes/         # registros do /session feitos fora do Claude Code
.agents/             # estrutura do Antigravity
├── rules/           # regras: projeto (sempre), backend e frontend (por arquivo), git e documento de requisitos (por assunto)
├── skills/          # skills; cada uma também vira comando /<nome>
└── agents/          # subagentes
.claude/             # estrutura equivalente para o Claude Code (+ gerador-docx/, o script que gera o .docx)
```

## Comandos

No Antigravity, os comandos são skills: digite `/<nome>`.

| Comando | O que faz |
|---|---|
| `/ajuda [tema]` | Explica os comandos, os subagentes e o fluxo típico |
| `/git` | Pergunta o que fazer: abrir branch, commitar, abrir PR ou fechar branch (também entrega e hotfix) |
| `/commit [texto]` | Commita em Conventional Commits perguntando só o idioma (português ou inglês); não faz push; na `main`/`develop` só com motivo explicado |
| `/revisar [PR\|branch\|caminho] [--publicar]` | Aciona o subagente `code-reviewer`; com `--publicar`, comenta no PR (nunca aprova) |
| `/session [obs]` | Salva o registro da sessão em `docs/sessoes/` |

`/revisar` e `/session` **só rodam quando o usuário digita**. As skills `git` e `commit` também são usadas pelo agente quando a tarefa pede.

## Subagentes (`.agents/agents/`)

| Agente | Quando usar | Skills |
|---|---|---|
| `backend-senior` | Implementar/alterar backend, decidir onde fica uma regra, investigar bug no backend | `backend`, `qualidade-codigo` |
| `frontend-senior` | Telas, templates, htmx, CSS, controllers web, acessibilidade e responsividade | `frontend`, `qualidade-codigo` |
| `code-reviewer` | **Só via `/revisar`.** Revisão imparcial de back e front, somente leitura | `qualidade-codigo`, `backend`, `frontend` |
| `engenheiro-requisitos` | Levantamento ou atualização dos requisitos a partir de `docs/fontes/` | `especialista-requisitos-uml` |

Regras comuns: imparciais e rigorosos (bloqueante × sugestão × preferência, críticas verificáveis), **nunca fazem merge** nem aprovam PR, e terminam com relatório. `backend-senior` e `frontend-senior` aceitam debate: devolvem “Ponto para debate” com opções e recomendação, e a palavra final é do desenvolvedor (salvo segurança, integridade de dados ou acessibilidade AA).

## Skills de referência

| Skill | Conteúdo |
|---|---|
| `qualidade-codigo` | Clean code, testes (regra do RF → teste; permissão obrigatória; Testcontainers), portão de qualidade (`./mvnw verify`), roteiro de code review, `assets/ci-exemplo.yml` |
| `backend` | Clean Architecture por módulo (`domain` / `application` / `adapters` / `config`), regra de dependência testada, portas, eventos, exemplo completo do RF004 |
| `frontend` | Thymeleaf + htmx, `assets/tokens.css` (cores do projeto + semafóricas), WCAG 2.2 AA, mobile first, receitas htmx |
| `especialista-requisitos-uml` | Elicitação, especificação e modelagem de requisitos |

## Como trabalhar aqui

- **Implementar um RF:** abrir branch (`/git`) → `backend-senior` e/ou `frontend-senior` → `/commit` → `/git` abrir PR → `/revisar` se o desenvolvedor quiser → aprovação e merge **por um humano** → `/git` fechar branch.
- **Revisão de código:** só quando o desenvolvedor digitar `/revisar`.
- **Requisitos:** dúvidas de negócio vão para `docs/requisitos/pendencias.md`, nunca são inventadas. Para mexer no documento, veja a regra `documento-requisitos`.
- **Leitura de fontes:** PDF com `pdftotext`; `.docx` com `unzip -p "<arquivo>" word/document.xml | sed 's/<[^>]*>/ /g'`.

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
- Checklist único por período com etiquetas de curso (v5, RF009). Substitui a regra anterior de modelo institucional aplicado curso a curso.

- **`main` protegida no GitHub** (administradores podem passar por cima). Commit direto na `main` só se o desenvolvedor (qualquer um, inclusive quem assumir; precisa ser Admin no repositório) explicar o motivo, registrado no corpo do commit. `develop` sem proteção; fluxo por PR por combinado.
- **Autoria só do desenvolvedor:** nenhuma IA (Gemini, Claude ou outra) aparece como autora ou coautora em commits, PRs ou comentários.

## Manutenção

O projeto tem **duas estruturas de agente com o mesmo conteúdo**:

| Claude Code | Antigravity e outros |
|---|---|
| `CLAUDE.md` | `AGENTS.md` (+ `.agents/rules/`) |
| `.claude/skills/<nome>/` | `.agents/skills/<nome>/` |
| `.claude/agents/<nome>.md` | `.agents/agents/<nome>.md` |

As diferenças são só de formato:
- **Frontmatter dos agentes:** o Claude usa as ferramentas `Read`/`Edit`/`Bash`; o Antigravity usa `view_file`/`replace_file_content`/`run_command` e `skills: - skills/<nome>`.
- **`/session`:** no Claude, salva na memória local; aqui, salva em `docs/sessoes/`.
- **`/revisar`:** no Claude, chama o agente com a ferramenta Agent; aqui, usa `invoke_subagent`.

**Ao mudar uma skill, um agente, uma regra ou uma decisão, faça a mesma mudança na outra estrutura** e atualize este arquivo e o `CLAUDE.md`.
