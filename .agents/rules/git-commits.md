---
trigger: model_decision
description: "Aplicar ao criar branch, fazer commit, abrir PR ou mexer no fluxo Git do projeto."
---

# Git: resumo

O fluxo completo está nas skills `git` e `commit`. Resumo:

- **Branches:** `main` = produção; `develop` = integração. As branches de trabalho seguem `tipo/descricao`, em kebab-case sem acento, e saem da `develop`. O `hotfix/` sai da `main`.
- **Commits:** em **português ou inglês**, à escolha do desenvolvedor (a skill `commit` pergunta), no padrão Conventional Commits, com o tipo em inglês: `feat(estrutura): cria cadastro de períodos`. O escopo é o módulo, e o rodapé `Refs: RF00X` liga o commit ao requisito.
- **PR:** vai para a `develop`, com o título no mesmo padrão. Só entra com o CI verde, por squash merge feito por um humano (aprovação de outra pessoa é opcional; o autor pode mergear o próprio PR). A entrega é um PR `develop → main`, por merge commit.
- **`main` protegida** no GitHub (admin pode passar por cima). Commit direto nela só com motivo explicado pelo desenvolvedor, registrado como `Direto na main: <motivo>` no corpo.
- **Autoria:** só o desenvolvedor. Nenhuma IA aparece como autora ou coautora em commit, PR ou comentário (sem `Co-Authored-By` de IA nem “Generated with …”).
