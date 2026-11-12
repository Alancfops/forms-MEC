# Fabiana – Indicadores de qualidade do MEC

Sistema do **CITEC / CESMAC** para a **Procuradoria Institucional** organizar a comprovação dos indicadores de qualidade exigidos pelo MEC. Ele cobre o checklist por período (dimensões → indicadores → subindicadores → anexos), o envio de documentos pelas coordenações de curso, a validação, os repositórios por dimensão e indicador e o histórico das avaliações.

> O sistema se chamava “Mozart” no início do projeto.

## Situação

| Fase | Situação |
|---|---|
| Requisitos | Concluídos – v5.1 (RF001–RF017), aguardando validação da Procuradoria |
| Arquitetura | Definida (ver `docs/README.md`) |
| Código | Não iniciado |

## Arquitetura

- **Definido:** Java, monolito modular com Clean Architecture em cada módulo, frontend Thymeleaf + htmx em módulo separado neste mesmo repositório, code review, clean code e testes no CI.
- **Sugestões iniciais** (podem ser trocadas): Java 21, Spring Boot + Maven, PostgreSQL (Flyway), MinIO (S3), JUnit + Testcontainers, Spring Modulith ou ArchUnit.

Diagramas e detalhes: [`docs/README.md`](docs/README.md#arquitetura-do-sistema).

## Documentação

| Arquivo | Conteúdo |
|---|---|
| [`docs/README.md`](docs/README.md) | Índice: situação, arquitetura, fluxo Git, requisitos, próximos passos |
| [`docs/prd.md`](docs/prd.md) | Visão de produto: problema, objetivos, usuários, MVP e fases |
| [`docs/glossario.md`](docs/glossario.md) | Termos do MEC/INEP, da instituição e do sistema |
| [`docs/requisitos/`](docs/requisitos/) | Levantamento oficial (.docx/.pdf) e `pendencias.md` |
| `docs/fontes/` | Material recebido (transcrição, instrumento INEP, checklist, fluxos). Não editar |

## Fluxo de trabalho

- `main` = produção; `develop` = integração.
- Toda mudança sai da `develop` numa branch `tipo/descricao` (ex: `feat/cadastro-periodos`) e volta por **pull request**, com CI verde e aprovação de outro desenvolvedor.
- Commits em **português ou inglês** (o `/commit` pergunta), no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/), com o tipo em inglês: `feat(estrutura): cria cadastro de períodos`.
- Hotfix sai da `main`. A entrega é um PR `develop → main`.

Detalhes nas skills `git` e `commit`.

## Assistentes de IA

O repositório já vem configurado para dois assistentes, com o mesmo conteúdo:

- **Claude Code:** `CLAUDE.md` + `.claude/` (agentes, skills e os comandos `/ajuda`, `/git`, `/commit`, `/revisar`, `/session`).

**Perdido? Digite `/ajuda`** para ver os comandos, os agentes e o fluxo de trabalho.
- **Google Antigravity:** `AGENTS.md` + `.agents/` (rules, skills e agents).

Toda mudança num lado deve ser repetida no outro.
