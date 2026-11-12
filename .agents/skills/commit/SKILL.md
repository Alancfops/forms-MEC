---
name: commit
description: Faz o commit das mudanças atuais do sistema Fabiana no padrão Conventional Commits, perguntando só o idioma da mensagem (português ou inglês). Use quando o usuário digitar /commit, pedir "commita", "faz o commit", "salva isso num commit", ou quando outra skill (como /git) mandar commitar. Também define o formato de mensagem de commit do projeto. Consulte esta skill sempre que for escrever uma mensagem de commit aqui.
---

# /commit – commit direto

Quando chamada, **faça o commit com uma única pergunta: o idioma da mensagem** (português ou inglês). Fora isso, analise as mudanças, escreva a mensagem e commite. Só pare nos casos de bloqueio listados abaixo. O desenvolvedor escolheu este atalho para não ter um menu no meio do caminho. Se ele passou um texto junto (ex: `/commit corrige upload`), use-o como base da descrição.

## Passos

1. **Ver o estado:** `git status`, `git diff` e `git diff --staged`, e a branch atual (`git branch --show-current`).
2. **Checar bloqueios** (seção abaixo). Se houver um, pare e explique.
3. **Perguntar o idioma** numa pergunta curta no chat: “Mensagem do commit em português ou em inglês?”, com as opções **Português** e **Inglês**. Não pergunte se o desenvolvedor já indicou o idioma no próprio comando (ex: `/commit en corrige upload`, `/commit pt`) ou se já respondeu nesta mesma conversa: use a escolha dele. Vale o mesmo quando outra skill (como `/git`) manda commitar.
4. **Separar por assunto.** Se as mudanças tratam de coisas diferentes (ex: uma funcionalidade e uma correção sem relação), faça **um commit por assunto**, adicionando os arquivos de cada grupo com `git add <arquivos>`. Se o usuário já deixou arquivos no stage, respeite: commite o que está no stage.
5. **Não incluir lixo:** nada de `.env`, credenciais, chaves, arquivos de IDE, `target/`, logs ou dumps. Se aparecerem como não rastreados, deixe fora e avise. Se fizer sentido, sugira colocá-los no `.gitignore`.
6. **Escrever a mensagem** no formato abaixo e commitar com `git commit -m` (use um arquivo ou HEREDOC para mensagens com corpo).
7. **Mostrar o resultado:** `git log --oneline -n <quantidade de commits feitos>`.

**Não faça push.** Subir para o GitHub é outra etapa (`/git` → abrir PR).

## Bloqueios: pare e avise em vez de commitar

- **Está na `main` ou na `develop` e o desenvolvedor não explicou por que quer commitar direto.** Nessas branches o normal é entrar por PR: sugira `/git` → abrir branch (as mudanças vão junto). **Se ele explicou o motivo**, commite e registre-o no corpo (`Direto na main: <motivo>`); ver “Exceção” na skill `git`.
- **Não há nada para commitar.**
- **Há conflito de merge não resolvido.**
- **Há segredo no diff** (senha, token, chave privada).

## Formato da mensagem

Toda a mensagem no **idioma escolhido** (português ou inglês): descrição, corpo e rodapé. O **tipo** e o **escopo** não mudam: o tipo segue o Conventional Commits em inglês (`feat`, `fix`…), porque as ferramentas de CI e de changelog o reconhecem, e o escopo é o nome do módulo (`estrutura`, `documentos`…). O rodapé `Refs: RF00X` é igual nos dois idiomas.

```
<tipo>(<escopo>): <descrição>

<corpo opcional: o porquê da mudança>

Refs: RF004
```

- **Descrição:** no imperativo (“cria”, “corrige”, “remove”; em inglês, “add”, “fix”, “remove”), começando com minúscula, sem ponto final, até cerca de 72 caracteres. Diga o que muda para quem usa ou mantém, não “altera arquivo X”.
- **Corpo:** opcional. Explica o *porquê* quando não é óbvio: problema que resolve, decisão tomada. Linhas de até ~72 caracteres.
- **`Refs: RF00X`:** quando o commit implementa ou corrige um requisito do levantamento (`docs/requisitos/`). Liga o código ao requisito.
- **Quebra de compatibilidade:** `!` depois do tipo/escopo e o rodapé `BREAKING CHANGE: <o que muda>`.

**Tipos:**

| Tipo | Quando |
|---|---|
| `feat` | Funcionalidade nova para o usuário |
| `fix` | Correção de bug |
| `refactor` | Mudança de código sem alterar comportamento |
| `test` | Só testes |
| `docs` | Só documentação |
| `style` | Formatação, sem mudança de lógica |
| `perf` | Melhoria de desempenho |
| `build` | Build e dependências (ex: `pom.xml`) |
| `ci` | Pipeline de CI |
| `chore` | Manutenção que não se encaixa nos outros |

**Escopo:** o módulo afetado (`acesso`, `estrutura`, `documentos`, `avaliacoes`, `frontend`, `docs`, `ci`). Se a mudança atravessa vários módulos, omita o escopo.

## Exemplos

```
feat(estrutura): cria cadastro de períodos com cópia do período anterior

Refs: RF004
```

```
fix(documentos): impede envio de arquivo acima do limite configurado

O envio aceitava qualquer tamanho e estourava o armazenamento.

Refs: RF010
```

```
test(estrutura): cobre aplicação automática de NSA por modalidade

Refs: RF007
```

```
docs: adiciona glossário de termos do MEC e do sistema
```

Os mesmos commits em inglês:

```
feat(estrutura): add period registration with copy from the previous period

Refs: RF004
```

```
fix(documentos): reject uploads above the configured size limit

Uploads of any size were accepted and filled up the storage.

Refs: RF010
```

```
refactor(acesso)!: troca autenticação local pelo login do sistema acadêmico

BREAKING CHANGE: usuários passam a entrar só com as credenciais do sistema acadêmico.

Refs: RF001
```

## Autoria: só o desenvolvedor

O commit é do desenvolvedor. **Não** coloque Claude, Gemini nem nenhuma outra IA como autor ou coautor: nada de `Co-Authored-By` de IA, `Generated with …` ou link de sessão na mensagem. Use o `user.name`/`user.email` do git do desenvolvedor, sem alterar.

## Commits saudáveis

Um commit deve compilar e manter os testes passando. Assim dá para revisar commit a commit e usar `git bisect`. Se a mudança quebra algo de propósito (trabalho em andamento), avise o usuário em vez de esconder. A verificação completa antes do PR está na skill `qualidade-codigo`.
