---
name: session
description: Salva um registro da sessão atual na memória do projeto — data/hora, onde parou, o que foi feito e próximos passos. Rodar só quando o usuário digitar /session.
disable-model-invocation: true
argument-hint: "[observação opcional]"
---

# /session — salvar a sessão na memória

Registra o estado desta sessão para que a próxima comece de onde esta parou.
Quem vai ler é você mesmo numa conversa nova, sem nenhum contexto desta: escreva
para essa pessoa.

## Passos

1. **Data e hora**: rode `date '+%Y-%m-%d %H:%M'` e use exatamente esse valor.
   Não deduza a data da conversa.

2. **Onde salvar**: na pasta de memória automática deste projeto, a que o
   prompt de sistema indica na seção "Memory" (algo como
   `~/.claude/projects/<projeto>/memory/`). Arquivo:
   `session-AAAA-MM-DD.md`. Se já existir um desse dia, **acrescente** uma nova
   seção `## HH:MM` no fim em vez de sobrescrever.

3. **Conteúdo**, a partir desta conversa e do estado real dos arquivos (rode
   `git status`/`git log -5` se for repositório git):

   ```markdown
   ---
   name: session-AAAA-MM-DD
   description: Sessão de AAAA-MM-DD — <resumo de uma linha do que foi feito>
   metadata:
     type: project
   ---

   ## HH:MM

   **Onde parou:** <a última coisa em andamento, com caminho de arquivo se houver,
   e qualquer pergunta que ficou sem resposta>

   **O que foi feito:**
   - <fato concreto: arquivo criado/alterado, decisão tomada e por quê>

   **Próximos passos:**
   1. <ação concreta, na ordem>

   **Observação:** <$ARGUMENTS, se o usuário passou algo; senão omita a linha>
   ```

   - Escreva no idioma da conversa.
   - Fatos, não narrativa. Caminhos de arquivo e nomes exatos.
   - Separe o que **o usuário decidiu** do que **você propôs e ele não confirmou**.
   - Não copie o que já está no código ou no git; aponte para onde está.
   - Nada de segredo (tokens, senhas, chaves).

4. **Índice**: em `MEMORY.md` da mesma pasta, mantenha **uma única linha** de
   sessão, sempre apontando para a mais recente, no formato:
   `- [Última sessão](session-AAAA-MM-DD.md) — AAAA-MM-DD HH:MM: <resumo>`
   Substitua a linha anterior de sessão se existir; não mexa nas outras linhas.

5. **Memórias permanentes**: se nesta sessão surgiu algo que vale para sempre
   (preferência do usuário, decisão de arquitetura), atualize ou crie também a
   memória própria disso, além do registro da sessão.

6. **Responda** em 2–3 linhas: caminho do arquivo salvo e os próximos passos.
