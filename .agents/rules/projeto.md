---
trigger: always_on
description: "Regras gerais do projeto Fabiana que valem em toda tarefa."
---

# Regras gerais do projeto

- Trabalhe em **português do Brasil**.
- **Não invente regra de negócio.** Os requisitos estão em `docs/requisitos/` (RF001–RF017). Se algo for ambíguo, contraditório ou não estiver coberto, pergunte ao usuário e sugira registrar a dúvida em `docs/requisitos/pendencias.md`.
- **Não faça commit nem push direto na `main` ou na `develop`** sem o desenvolvedor explicar o motivo. O normal é branch `tipo/descricao` + PR; com motivo explicado, é permitido e o motivo vai no corpo do commit (skill `git`, “Exceção”).
- **Nenhuma IA aparece como autora ou coautora** em commit, PR ou comentário: só o desenvolvedor.
- **Nunca aprove nem faça merge de PR.** A aprovação e o merge são de um desenvolvedor humano.
- **Não declare que algo funciona sem ter verificado.** Diga o que rodou, o resultado e o que não deu para verificar.
- **Os prints do Miro (`docs/fontes/miro/`) são só exemplos do fluxo, não o design.**
- `docs/fontes/` é material recebido: não edite.
- Comandos do projeto: `/ajuda`, `/git`, `/commit`, `/revisar`, `/session` (skills em `.agents/skills/`). `/revisar` e `/session` só rodam quando o usuário digita.
