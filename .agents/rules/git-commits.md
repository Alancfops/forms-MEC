---
trigger: model_decision
description: "Aplicar ao criar branch, fazer commit, abrir PR ou mexer no fluxo Git do projeto."
---

# Git: resumo

O fluxo completo está nas skills `git` e `commit`. Resumo:

- **Branches:** `main` = produção; `develop` = integração. As branches de trabalho seguem `tipo/descricao`, em kebab-case sem acento, e saem da `develop`. O `hotfix/` sai da `main`.
- **Commits:** em **português**, no padrão Conventional Commits, com o tipo em inglês: `feat(estrutura): cria cadastro de períodos`. O escopo é o módulo, e o rodapé `Refs: RF00X` liga o commit ao requisito.
- **PR:** vai para a `develop`, com o título no mesmo padrão. Só entra com o CI verde e a aprovação de um humano, por squash merge. A entrega é um PR `develop → main`, por merge commit.
- **Autoria:** só o desenvolvedor. Nenhuma IA aparece como autora ou coautora em commit, PR ou comentário (sem `Co-Authored-By` de IA nem “Generated with …”).
