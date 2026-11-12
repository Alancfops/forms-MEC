---
name: ajuda
description: Explica os comandos (/git, /commit, /revisar, /session, /ajuda), os agentes (backend-senior, frontend-senior, code-reviewer, engenheiro-requisitos) e as skills do sistema Fabiana, e qual usar em cada situação. Argumento opcional: comando, agente ou tarefa. Use quando o desenvolvedor digitar /ajuda ou parecer perdido no ambiente ("quais comandos tem?", "o que esse agente faz?", "como começo um RF?", "qual comando uso pra…").
---

# /ajuda – guia dos comandos e agentes

Explique ao desenvolvedor o que existe neste projeto e quando usar cada coisa. Ele pode ser novo aqui: escreva de forma direta, sem jargão desnecessário, em português.

## Como responder

1. **Confira o que existe de fato** antes de responder: liste `.agents/skills/*/SKILL.md` e `.agents/agents/*.md` e leia o `name` e a `description` de cada um. Se houver algo que não está nas tabelas abaixo (ou algo das tabelas que não existe mais), use o que está nos arquivos e avise que este guia está desatualizado.
2. **Sem argumento** (`/ajuda`): mostre a visão geral abaixo (comandos, agentes, fluxo típico), de forma resumida.
3. **Com argumento:**
   - **um comando ou agente** (`/ajuda commit`, `/ajuda code-reviewer`): leia o arquivo dele e explique o que faz, quando usar, o que pergunta, o que nunca faz e um exemplo de uso;
   - **uma tarefa** (`/ajuda como começo o RF004?`, `/ajuda subir pra revisão`): diga quais comandos/agentes usar, na ordem.
4. **Termine** com uma linha: “Para mais detalhes: `/ajuda <comando ou agente>`.”

Não execute nenhum comando nem acione agentes: `/ajuda` só explica.

## Visão geral

### Comandos (o desenvolvedor digita)

| Comando | O que faz |
|---|---|
| `/ajuda [tema]` | Este guia |
| `/git` | Menu do fluxo Git: abrir branch, commitar, abrir PR ou fechar branch (entrega para a `main` e hotfix pelo “Outro”) |
| `/commit [texto]` | Commita as mudanças em Conventional Commits. Pergunta só o idioma (português ou inglês). Não faz push |
| `/revisar [PR \| branch \| caminho] [--publicar]` | Revisão de código pelo agente `code-reviewer`. Com `--publicar`, comenta no PR (nunca aprova) |
| `/session [obs]` | Salva onde a sessão parou, o que foi feito e os próximos passos em `docs/sessoes/` |

`/revisar` e `/session` só rodam quando digitados. No Antigravity, os comandos são skills (`.agents/skills/`). `/git` e `/commit` também são usados pelo agente quando a tarefa pede.

### Subagentes (`.agents/agents/`; o agente aciona, ou você pede pelo nome)

| Agente | Para quê | Exemplo de pedido |
|---|---|---|
| `backend-senior` | Implementar ou alterar o backend Java (Clean Architecture), decidir onde fica uma regra, investigar bug | “Usa o backend-senior pra implementar o RF004” |
| `frontend-senior` | Telas Thymeleaf + htmx, CSS, acessibilidade (WCAG AA), celular primeiro | “Pede pro frontend-senior fazer a tela de períodos” |
| `code-reviewer` | Revisão imparcial de back e front. **Só via `/revisar`** | `/revisar 12` |
| `engenheiro-requisitos` | Levantamento ou atualização dos requisitos a partir de `docs/fontes/` | “Atualiza os requisitos com a resposta da Fabiana” |

Os agentes são rigorosos, separam **bloqueante × sugestão × preferência**, aceitam debate (devolvem um “Ponto para debate” com opções e recomendação) e **nunca aprovam nem fazem merge** de PR. A palavra final é sua, exceto em segurança, integridade de dados e acessibilidade.

### Skills de referência (o agente usa sozinho)

`backend`, `frontend`, `qualidade-codigo` e `especialista-requisitos-uml`: são os padrões do projeto. Você não precisa chamá-las.

### Fluxo típico para implementar um RF

1. `/git` → **Abrir branch** (ex: `feat/cadastro-de-periodos`, saindo da `develop`).
2. Peça a implementação (o agente aciona `backend-senior` e/ou `frontend-senior`).
3. `/commit` → escolha o idioma.
4. `/git` → **Abrir PR** para a `develop`.
5. Se quiser, `/revisar` antes de aprovar.
6. Aprovação e merge **por você**, no GitHub.
7. `/git` → **Fechar branch**.

### Regras que vale lembrar

- A `main` é protegida. Commit direto nela só se você explicar o motivo.
- Nenhuma IA aparece como autora ou coautora nos commits e PRs.
- Dúvida de regra de negócio vai para `docs/requisitos/pendencias.md`; ninguém inventa regra.
- Por onde começar a ler: `README.md` e depois `docs/README.md`.
