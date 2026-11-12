---
name: git
description: Fluxo de trabalho Git do sistema Fabiana (/git) — pergunta o que fazer (abrir branch, commitar, abrir PR, fechar branch) e executa seguindo o fluxo main/develop, branches tipo/descricao saindo da develop, commits Conventional Commits em português, PR no GitHub com CI e aprovação de um desenvolvedor, e hotfix saindo da main. Use quando o usuário digitar /git e SEMPRE que for começar a implementar um requisito (RF), funcionalidade ou correção neste projeto, criar ou nomear branch, abrir PR, preparar entrega para a main, corrigir bug em produção, limpar branch depois do merge ou configurar o repositório/CI — mesmo que o pedido seja só "implementa o RF004" ou "sobe pra revisão".
---

# /git – fluxo de trabalho Git do sistema Fabiana

Este fluxo existe para que **todo código passe por revisão humana e pelo CI antes de chegar às branches compartilhadas**. A `main` e a `develop` são de todos: ninguém escreve nelas direto. Cada mudança nasce numa branch própria, vira um PR, passa no CI, é aprovada por um desenvolvedor e só então entra.

## Ao ser chamada

**Se o usuário digitou `/git` sem dizer o que quer**, pergunte com a ferramenta de perguntas (AskUserQuestion), com estas opções:

| Opção | Descrição curta | Seção |
|---|---|---|
| Abrir branch | Nova branch `tipo/descricao` a partir da develop atualizada | [Abrir branch](#abrir-branch) |
| Commitar | Commit das mudanças atuais (mesmo que `/commit`) | [Commitar](#commitar) |
| Abrir PR | Sobe a branch e abre o PR para a develop | [Abrir PR](#abrir-pr) |
| Fechar branch | Depois do merge: volta para a develop e apaga a branch | [Fechar branch](#fechar-branch) |

Antes de perguntar, rode `git status` e `git branch --show-current`. Inclua a branch atual no texto da pergunta e, se for óbvio, marque a opção mais provável como recomendada. Por exemplo: há mudanças não commitadas → Commitar; está na `develop` → Abrir branch. Entrega para a `main`, hotfix e configuração do repositório não estão no menu: o usuário pode pedir pelo campo “Outro”, e você segue a seção correspondente.

**Se o usuário já disse o que quer** (ex: `/git abrir pr`, “abre uma branch pro RF004”), vá direto para a seção, sem menu.

**Se esta skill foi acionada no meio de uma tarefa** (ex: “implementa o RF004”), não mostre o menu: aplique o passo que a tarefa pede. Antes de codar, abra a branch; ao terminar, commite e pergunte se pode abrir o PR.

## Branches

| Branch | Para que serve | Sai de | Volta para |
|---|---|---|---|
| `main` | Versão em produção. Só recebe entregas prontas | — | — |
| `develop` | Integração: onde as funcionalidades terminadas se juntam | `main` (uma vez, na criação) | `main`, por PR de entrega |
| `tipo/descricao` | Uma funcionalidade, correção ou ajuste | `develop` | `develop`, por PR |
| `hotfix/descricao` | Bug urgente em produção | `main` | `main` e `develop`, por PR |

O nome da branch usa **o mesmo tipo do commit** (ver skill `commit`) e uma descrição curta em português, em kebab-case e sem acento:

```
feat/cadastro-de-periodos
fix/upload-pdf-grande
refactor/modulo-estrutura
test/regras-nsa
docs/readme-arquitetura
chore/atualiza-dependencias
ci/pipeline-testes
hotfix/login-sistema-academico
```

Uma branch = um assunto. Se aparecer outra coisa no meio do trabalho, anote e faça em outra branch. PRs pequenos são revisados mais rápido e com mais cuidado.

## Abrir branch

1. `git status`. Se houver mudanças não commitadas:
   - se elas são do assunto da nova branch, podem ir junto (o `git switch -c` as leva);
   - se são de outro assunto, pergunte o que fazer (commitar antes, guardar com `git stash` ou descartar) em vez de levá-las.
2. Atualize a develop e crie a branch:

   ```bash
   git switch develop
   git pull --ff-only
   git switch -c <tipo>/<descricao>
   ```

3. Se o usuário não deu o nome, deduza pelo que vai ser feito (ex: “RF004 períodos” → `feat/cadastro-de-periodos`) e diga qual nome usou.

## Commitar

Siga a skill **`commit`** (`/commit`): ela analisa as mudanças, separa por assunto e escreve a mensagem em português no padrão Conventional Commits.

## Abrir PR

Push e PR publicam o trabalho para a equipe. Se o usuário escolheu “Abrir PR” ou pediu para subir, isso já é a confirmação. Se chegou aqui no meio de uma tarefa, pergunte antes.

1. **Pré-condições:**
   - não está na `main` nem na `develop`;
   - não há mudança sem commit (se houver, commite antes com `/commit` ou pergunte);
   - a verificação local passou (portão de qualidade da skill `qualidade-codigo`, em geral `./mvnw verify`). Se falhar, pare e mostre o erro: PR com CI vermelho só gasta o tempo do revisor.
2. **Autorrevisão rápida** do diff (`git diff develop...HEAD`), com o roteiro de `qualidade-codigo/references/code-review.md`.
3. **Subir e abrir:**

   ```bash
   git push -u origin <branch>
   gh pr create --base develop --title "<título>" --body-file <arquivo-com-o-corpo>
   ```

   - **Base:** `develop`. Só hotfix e entrega vão para a `main`.
   - **Título:** em português, no formato Conventional Commits (`feat(estrutura): cadastro de períodos`). O merge é com *squash*, então o título vira o commit que fica na `develop`.
   - **Corpo** (ou o `.github/pull_request_template.md`, se existir):

   ```markdown
   ## O que muda
   <resumo em 1–3 frases>

   ## Requisitos
   - RF004 – Gerenciamento dos períodos de avaliação

   ## Como testar
   1. <passo>
   2. <passo>

   ## Checklist
   - [ ] Testes cobrindo as regras novas
   - [ ] `verify` passando localmente
   - [ ] Documentação atualizada (README, glossário, pendências), se necessário
   ```

   O corpo **não** leva assinatura de IA (nada de “🤖 Generated with …”, `Co-Authored-By` ou link de sessão): o autor do PR é só o desenvolvedor.

4. **Mostre o link do PR e pare.** O PR só entra com **CI verde** e **aprovação de outro desenvolvedor**. **Quem faz o merge é o desenvolvedor que revisa, não o Claude.**

### Depois de aberto

- **CI falhou:** veja o log (`gh pr checks`, `gh run view --log-failed`), corrija na mesma branch e suba de novo.
- **Revisor pediu mudanças:** corrija na mesma branch com novos commits. Não reescreva o histórico de branch em revisão (sem `push --force`); se for inevitável, use `--force-with-lease` e avise no PR.
- **Conflito com a develop:** `git fetch && git merge origin/develop`, resolva, rode a verificação e suba.

## Fechar branch

Para depois que o PR foi **aprovado e mergeado** pelo revisor.

1. Confirme que o PR foi mergeado: `gh pr view <branch> --json state,mergedAt`. Se não foi, **não apague a branch**: avise o usuário e mostre o estado do PR.
2. Volte para a develop e limpe:

   ```bash
   git switch develop
   git pull --ff-only
   git branch -d <branch>
   git push origin --delete <branch>   # só se o GitHub não apagou sozinho
   ```

   Com squash merge, o `git branch -d` pode reclamar que a branch “não está mergeada”, porque os commits viraram um só. Se o passo 1 confirmou o merge, use `git branch -D`.

## Entrega para a main

Quando a `develop` tem um conjunto de funcionalidades prontas para produção:

```bash
gh pr create --base main --head develop --title "release: <resumo da entrega>"
```

No corpo, liste os PRs e RFs incluídos. O PR passa por CI e aprovação. Use **merge commit** (não squash) para preservar os commits da `develop`. Depois do merge, crie uma tag de versão se a equipe estiver versionando (ex: `v0.1.0`).

## Hotfix

Só para bug que afeta produção e não pode esperar a próxima entrega.

```bash
git switch main && git pull --ff-only
git switch -c hotfix/<descricao>
# corrige e commita como fix(...)
git push -u origin hotfix/<descricao>
gh pr create --base main --title "fix(<escopo>): <descrição>"
```

Depois do merge na `main`, leve a correção para a `develop` com um PR `main → develop`, para ela não sumir na próxima entrega.

## O que não fazer, e por quê

- **Commit ou push direto na `main` ou na `develop`:** pula a revisão e o CI, que são o motivo do fluxo existir. Se perceber que está numa delas com mudanças, crie a branch a partir dali antes de commitar.
- **Merge do próprio PR:** a aprovação tem que vir de outra pessoa.
- **`push --force` em `main` ou `develop`:** apaga o trabalho dos outros.
- **Misturar assuntos num PR:** dificulta a revisão e o rastreio de requisito.
- **Desligar ou pular testes para o CI passar:** esconde o problema em vez de resolver.
- **IA como autora ou coautora** (commit, PR, comentário de revisão): o projeto registra só o desenvolvedor. Sem `Co-Authored-By` de IA nem “Generated with …”.

## Configuração inicial do repositório (uma vez)

Se o repositório ainda não estiver configurado assim, ajude o usuário com estes passos. Todos mexem em configurações compartilhadas, então confirme antes de executar.

1. Criar a `develop` a partir da `main` e enviá-la: `git switch -c develop && git push -u origin develop`.
2. Definir a `develop` como branch padrão no GitHub, para os PRs já abrirem contra ela.
3. Proteger `main` e `develop` (*Settings → Branches* ou *Rulesets*): exigir PR, 1 aprovação e o CI passando, e bloquear push direto e force push.
4. Em *Settings → General → Pull Requests*: permitir *squash merge* (feature → develop) e *merge commit* (develop → main), e ativar *Automatically delete head branches*.
5. Criar o CI em `.github/workflows/` (exemplo em `qualidade-codigo/assets/ci-exemplo.yml`).
6. Opcional: `.github/pull_request_template.md` com o corpo do PR acima.
