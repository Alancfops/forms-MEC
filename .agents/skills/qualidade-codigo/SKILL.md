---
name: qualidade-codigo
description: Padrões de qualidade do sistema Fabiana (Java, monolito modular, Thymeleaf) — clean code, testes (unitários, de integração, de arquitetura e de permissão) e code review de PRs. Use SEMPRE que for escrever, alterar ou refatorar código deste projeto, implementar um RF, escrever ou corrigir testes, investigar teste quebrado ou CI vermelho, fazer autorrevisão ou checar se uma mudança está pronta para subir — mesmo que o pedido seja só "implementa o RF007", "faz os testes disso" ou "tá pronto pra subir?" (revisão formal de PR é só via /revisar).
---

# Qualidade de código – Sistema Fabiana

O objetivo é que **nenhum código chegue à `develop` com erro conhecido**: cada mudança é legível, cada regra de negócio tem teste e cada PR é revisado. O fluxo de branches, commits e PRs está na skill `git` (`/git`); esta skill cuida do *conteúdo* do que entra.

A stack em `docs/README.md` é uma **sugestão inicial** (Spring Boot, Maven, PostgreSQL, MinIO, htmx, JUnit 5, Testcontainers…). Antes de aplicar um exemplo daqui, confira no README e no `pom.xml` o que o projeto usa de fato e adapte. Os princípios valem para qualquer ferramenta.

## Onde está cada coisa

| Arquivo | Leia quando |
|---|---|
| `references/clean-code.md` | For escrever ou refatorar código: nomes, módulos, camadas, Thymeleaf, erros |
| `references/testes.md` | For escrever testes ou investigar teste quebrado: tipos, nomes, como transformar regras de RF em testes |
| `references/code-review.md` | For revisar um PR ou diff, ou fazer a autorrevisão antes de abrir o PR |
| `assets/ci-exemplo.yml` | For criar ou ajustar o CI no GitHub Actions |

Leia o arquivo inteiro da tarefa em questão; eles são curtos.

## Ciclo de trabalho ao implementar um requisito

1. **Ler o RF** no levantamento (`docs/requisitos/`) e o termo no `docs/glossario.md`. Os campos e as “Regras e observações” do RF são a especificação. As mensagens entre aspas são o texto exato da tela.
2. **Escrever os testes a partir das regras** antes ou junto com o código. Cada regra numerada vira pelo menos um caso de teste (ver `references/testes.md`). Isso garante que o código faz o que o requisito pede, e não o que achamos que ele pede.
3. **Implementar o mínimo** para os testes passarem, seguindo `references/clean-code.md`.
4. **Refatorar** com os testes verdes: nomes, duplicação, métodos longos.
5. **Rodar a verificação completa** (o portão abaixo).
6. **Autorrevisão** com `references/code-review.md` antes de abrir o PR.

Se o RF for ambíguo ou contradizer outro, não invente a regra: pergunte ao usuário e, se for dúvida de negócio, registre em `docs/requisitos/pendencias.md`.

## Portão de qualidade (antes de todo commit que vai para PR)

A mudança só está pronta quando **tudo** abaixo passa. É o mesmo que o CI roda; rodar antes evita PR vermelho.

| Verificação | O que pega | Comando típico (Maven) |
|---|---|---|
| Compilação sem warnings novos | Erro de tipo, código morto | `./mvnw compile` |
| Formatação | Estilo inconsistente | `./mvnw spotless:check` (corrigir com `spotless:apply`) |
| Lint / análise estática | Más práticas, bugs comuns | `./mvnw checkstyle:check` |
| Testes unitários | Regra de negócio errada | `./mvnw test` |
| Testes de integração | Banco, armazenamento, telas | `./mvnw verify` |
| Testes de arquitetura | Módulo usando interno de outro | incluídos no `verify` |
| Cobertura | Regra sem teste | relatório do JaCoCo no `verify` |

Na prática, `./mvnw verify` roda tudo. Confira o comando real no README ou no workflow do CI.

**Nunca** faça o portão passar à força: sem `@Disabled`, sem apagar asserção, sem `-DskipTests` e sem baixar o limite de cobertura para caber. Se um teste falha, ou o código está errado, ou o teste está errado. Descubra qual e conserte. Se não der para resolver agora, pare e explique ao usuário em vez de esconder.

## Quando o CI fica vermelho

1. Leia o log da falha (`gh pr checks`, `gh run view --log-failed`).
2. Reproduza localmente com o mesmo comando.
3. Corrija a causa, não o sintoma. Um teste que falha só às vezes (*flaky*) também é um bug: resolva a dependência de ordem, tempo ou estado compartilhado.
4. Suba a correção na mesma branch.

## Code review

Todo PR é revisado por um desenvolvedor antes do merge (skill `git`). A revisão pelo agente de IA é feita pelo agente `code-reviewer`, acionado **só** quando o desenvolvedor digita `/revisar`, e segue `references/code-review.md`. Fora disso, use esse roteiro apenas para a autorrevisão antes de abrir o PR. O agente pode comentar e pedir mudanças, mas **não aprova nem faz merge**: a aprovação é de um humano.
