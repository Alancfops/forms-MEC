---
name: revisar
description: Revisão de código do sistema Fabiana pelo agente code-reviewer (backend e frontend). Rodar SOMENTE quando o desenvolvedor digitar /revisar; nunca aplicar por iniciativa própria. Argumentos opcionais: nº do PR, branch ou caminho, e --publicar.
---

# /revisar – revisão de código

Aciona o agente **`code-reviewer`**, um revisor imparcial de backend e frontend, sobre o alvo indicado. Esta é a **única** forma de acionar esse agente: ele não roda por iniciativa própria.

## Alvo

Interprete o que o desenvolvedor escreveu depois de `/revisar`:

| Argumento | Alvo |
|---|---|
| (vazio) | A branch atual comparada com a `develop`, incluindo mudanças não commitadas |
| número (ex: `42`) | O PR #42 no GitHub |
| nome de branch (ex: `feat/cadastro-de-periodos`) | Essa branch comparada com a `develop` |
| caminho (ex: `frontend/src/main/resources/templates/estrutura/`) | Só esses arquivos |
| `--publicar` (junto com um PR) | Depois da revisão, publica os comentários no PR |

Se o argumento for ambíguo, ou se estiver na `main`/`develop` sem alvo, pergunte ao desenvolvedor antes de acionar o agente.

## Passos

1. **Acione o subagente `code-reviewer`** (definido em `.agents/agents/code-reviewer.md`, chamado com `invoke_subagent`), passando:
   - o alvo exato (PR, branch ou caminho);
   - a branch atual e se há mudanças não commitadas (`git status --short`);
   - o que o desenvolvedor disse junto do comando, se disse algo (ex: “foca na permissão”).

   Não peça ao agente para publicar no GitHub: a publicação é o passo 3, depois de o desenvolvedor ver o resultado.
2. **Mostre o relatório do agente ao desenvolvedor**, sem resumir nem amenizar os bloqueantes. Se o relatório vier sem a estrutura esperada (veredito, bloqueantes, sugestões, verificação), peça ao agente para completá-lo.
3. **Publicar no GitHub (só com `--publicar`, ou se o desenvolvedor pedir depois):**
   - confirme o PR alvo;
   - grave o relatório num arquivo temporário;
   - se houver bloqueantes, use `gh pr review <n> --request-changes --body-file <arquivo>`; se não houver, use `gh pr review <n> --comment --body-file <arquivo>`.

   **Nunca** `--approve`: a aprovação é de um desenvolvedor humano.
4. **Ofereça os próximos passos:** corrigir os bloqueantes (o desenvolvedor, ou os agentes `backend-senior` / `frontend-senior`, se ele quiser) e rodar `/revisar` de novo depois.

## Se o desenvolvedor contestar um apontamento

Chame de novo o subagente `code-reviewer` (no CLI, dá para falar com ele em execução usando `@code-reviewer`), passando o relatório anterior e o argumento do desenvolvedor. O agente reavalia pelo mérito: ou retira o apontamento, ou explica o risco que o mantém.
