# Técnicas de elicitação e banco de perguntas

## Quando usar cada técnica

| Técnica | Bom para | Cuidado |
|---|---|---|
| Entrevista | Entender objetivos e dores de um stakeholder | Viés do entrevistado; registre e valide |
| Workshop / JAD | Alinhar vários stakeholders, resolver conflitos | Precisa de facilitador e pauta |
| Observação / etnografia | Processos reais vs. descritos | Demorado |
| Questionário | Muitos usuários, dados quantitativos | Perguntas fechadas mal feitas enviesam |
| Análise de documentos | Regras, formulários, legislação, sistema legado | Documento pode estar desatualizado |
| Prototipação | Validar UI e fluxo cedo | Cliente confundir protótipo com produto |
| Brainstorming | Explorar soluções | Convergir depois com priorização |
| Cenários / storyboards | Tornar abstrações concretas | — |

## Roteiro de entrevista (base)

**Abertura / contexto**
- Qual é seu papel e como você se relaciona com este processo?
- Qual problema este sistema precisa resolver? O que acontece hoje sem ele?

**Processo atual**
- Descreva passo a passo como isso é feito hoje. Quem participa de cada etapa?
- Quais documentos, planilhas ou sistemas são usados?
- Onde ocorrem atrasos, retrabalho ou erros?

**Objetivos e sucesso**
- Como saberemos que o sistema deu certo? Que número deve mudar?
- O que é indispensável na primeira versão? O que pode esperar?

**Regras e exceções**
- Existem regras, normas ou legislação que se aplicam (ex.: LGPD, MEC/INEP, regimento interno)?
- E se…? (prazo vencido, dado faltando, usuário sem permissão, reenvio)
- Quem pode ver/alterar/aprovar cada informação?

**Qualidade**
- Quantos usuários simultâneos? Em que períodos há pico?
- Em quais dispositivos será usado? Precisa de acessibilidade específica?
- Quanto tempo os dados devem ser guardados? Há necessidade de auditoria?

**Integração**
- Com quais sistemas precisa trocar dados? Em que formato e com que frequência?

**Fechamento**
- Há algo que não perguntei e que é importante?
- Quem mais devemos ouvir?

## Sinais na transcrição que indicam requisito
- "precisa", "tem que", "deveria", "seria bom", "não pode" → RF/RN (mapear prioridade pela força do verbo)
- números, prazos, percentuais → RNF ou RN
- "sempre que", "quando", "se… então" → RN ou fluxo alternativo
- "hoje a gente faz no Excel/papel" → processo atual (modelar em atividades) e possível dado a migrar
- "depende", "ainda não sabemos", "vamos ver" → **dúvida aberta**
- "isso fica para depois" → fora de escopo / Won't
