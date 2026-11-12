---
trigger: model_decision
description: "Aplicar ao alterar o levantamento de requisitos (RFs), as pendências ou o documento .docx do projeto."
---

# Documento de requisitos

- O documento oficial é `docs/requisitos/Levantamento de requisitos - Projeto Fabiana.docx`. Ele é **gerado**, nunca editado à mão: edite `.claude/gerador-docx/conteudo.py` e rode `.claude/gerador-docx/gerar.sh`. O gerador fica na pasta `.claude/`, mas é só um script Python e independe de ferramenta.
- **Formato:**
  - segue o modelo do TCC, com as mesmas seções e a fonte Calibri, sem seções extras e sem linha de prioridade nos RFs;
  - as seções 4 (RNF), 5 (Segurança), 6 (Matriz de Risco) e 8 (Ponto de função) ficam só com os títulos;
  - os RFs não citam tecnologia.
- **Estilo de cada RF:**
  - título “Requisito funcional que trata do/da …”;
  - “Campos do formulário:” ou “Campos do requisito:”, com cada campo como `Nome (Obrigatório|Opcional|Automático)` + o número das regras + o tipo;
  - “Regras e observações dos campos:” numeradas, no formato “O sistema deve …”, com as mensagens entre aspas curvas.
- **IDs:** são estáveis e nunca renumerados. Um RF novo entra no fim, e um removido fica marcado `[CANCELADO]`.
- **Fontes:** todo requisito cita a fonte. Inferências são marcadas `[SUPOSIÇÃO]`.
- **Diagramas:** só de arquitetura, em Mermaid, no `docs/README.md`.
