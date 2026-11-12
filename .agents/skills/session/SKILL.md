---
name: session
description: Salva um registro da sessão atual — data/hora, onde parou, o que foi feito e próximos passos — em docs/sessoes/. Rodar SOMENTE quando o usuário digitar /session (pode vir com uma observação opcional); nunca aplicar por iniciativa própria.
---

# /session — salvar a sessão

Registra o estado desta sessão para que a próxima comece de onde esta parou.
Quem vai ler é você mesmo, ou outra pessoa, numa conversa nova e sem nenhum
contexto desta: escreva para esse leitor.

> No Claude Code, o `/session` salva na memória local do Claude. Aqui, no
> Antigravity, o registro fica no próprio repositório, em `docs/sessoes/`,
> e fica visível para a equipe. Por isso, nada de dado pessoal nem segredo.

## Passos

1. **Data e hora:** rode `date '+%Y-%m-%d %H:%M'` e use exatamente esse valor.
   Não deduza a data da conversa.

2. **Onde salvar:** `docs/sessoes/AAAA-MM-DD.md`. Crie a pasta se não existir.
   Se já existir um arquivo desse dia, **acrescente** uma nova seção `## HH:MM`
   no fim em vez de sobrescrever.

3. **Conteúdo**, a partir desta conversa e do estado real dos arquivos (rode
   `git status` e `git log -5` se for repositório git):

   ```markdown
   # Sessão AAAA-MM-DD

   ## HH:MM

   **Onde parou:** <a última coisa em andamento, com caminho de arquivo se houver,
   e qualquer pergunta que ficou sem resposta>

   **O que foi feito:**
   - <fato concreto: arquivo criado/alterado, decisão tomada e por quê>

   **Próximos passos:**
   1. <ação concreta, na ordem>

   **Observação:** <o que o usuário escreveu depois de /session; se nada, omita a linha>
   ```

   - Escreva no idioma da conversa.
   - Fatos, não narrativa. Caminhos de arquivo e nomes exatos.
   - Separe o que **o usuário decidiu** do que **você propôs e ele não confirmou**.
   - Não copie o que já está no código ou no git; aponte para onde está.
   - Nada de segredo (tokens, senhas, chaves).

4. **Índice:** em `docs/sessoes/README.md`, mantenha a lista de sessões com a mais
   recente no topo, no formato
   `- [AAAA-MM-DD HH:MM](AAAA-MM-DD.md) — <resumo de uma linha>`.

5. **Decisões permanentes:** se nesta sessão surgiu algo que vale para sempre
   (decisão de arquitetura, convenção nova), atualize também o `AGENTS.md`
   (e avise que o `CLAUDE.md` precisa da mesma atualização).

6. **Responda** em 2–3 linhas: o caminho do arquivo salvo e os próximos passos.
