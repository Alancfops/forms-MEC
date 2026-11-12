# Pendências – Levantamento de Requisitos (Projeto Fabiana)

Referente a: `Levantamento de requisitos - Projeto Fabiana.docx` (v5 – 10/11/2026, segue o fluxo de telas da equipe; modelo do TCC; RF001–RF017 preenchidos, demais seções só com títulos).
Fontes: transcrição da reunião, esboço de telas da Gerência de Checklist (06/11/2026), instrumento do INEP de 2017 (`docs/fontes/instrumento-inep-2017-reconhecimento-curso.pdf`) e checklist de Medicina da Procuradoria (`docs/fontes/checklist-medicina/`).

## Mudanças da v5 (fluxo de telas da equipe) – a Fabiana precisa aprovar

Se ela reprovar algum item, o protótipo deve seguir outro caminho.

| # | O que o fluxo propõe | Como estava antes | Requisitos |
|---|---|---|---|
| A | Três perfis: **Administrador Master** (cadastra usuários e define funções), **Administrador** (Pró-Reitores e Procuradoria: checklist, validação, histórico) e **Coordenação de Curso** (envia documentos) | Só a Procuradoria gerenciava; Pró-Reitores apenas consultavam | RF002, RF009, RF011, RF012, RF015, RF017 |
| B | Usuários cadastrados antes pelo **e-mail**; login continua com usuário e senha do sistema acadêmico | Whitelist pelo login do sistema acadêmico | RF001, RF002 |
| C | **Um checklist por período**, comum a todos os cursos, com **etiquetas de curso** em dimensões, indicadores e anexos; a coordenação só vê os itens sem etiqueta e os do seu curso | Modelo institucional + cópia do checklist para cada curso | RF005, RF006, RF007, RF008, RF009 |
| D | Mudanças no checklist valem **na hora** para todos os cursos (é a mesma estrutura) | O sistema avisava e a Procuradoria aplicava curso a curso | RF009 |
| E | Novo período: **“Usar modelo do ano anterior”** (copia tudo) ou **“Criar novo modelo”** (vazio) | Cópia opcional de um período anterior | RF004 |
| F | **Documento exemplo** no anexo, com checkbox para mostrar ou não à coordenação (a equipe ainda vai ver se dá) | Não existia | RF008, RF010 |
| G | Criação de dimensão e de indicador em **janela** (nome, curso, etiquetas, Confirmar/Cancelar) | O “+” criava direto | RF006, RF007 |

## Perguntas em aberto

| # | Pergunta | Para quem | Requisitos afetados | Recomendação |
|---|---|---|---|---|
| 1 | O checklist de Medicina mostra **documentos numerados por dimensão**, e um mesmo documento comprova vários indicadores (ex.: “1. PPC” vale para 1.1 a 1.5). O RF008 foi reescrito nesse modelo. Está certo? | Fabiana | RF008, RF010, RF016 | Confirmar, pois muda a hierarquia de “Indicador → Anexo” para “Dimensão → Anexo vinculado a indicadores”. |
| 1a | A numeração dos documentos (1, 2, … 169) corresponde à das **pastas físicas/digitais** de comprovação e precisa ficar fixa? | Fabiana | RF008 | Manter fixa (assim está no RF008). |
| 1b | Os documentos que não comprovam nenhum indicador (ex.: ouvidoria, egressos, alvará, plano de fuga) devem ficar no sistema? São cobrados em outra parte do instrumento (ex.: requisitos legais)? | Fabiana | RF008 | Mantê-los no grupo “Documentos sem indicador correspondente”. |
| 1c | Os avaliadores do MEC precisam acessar os repositórios direto no sistema, ou a Procuradoria baixa as pastas e entrega a eles (RF017)? A transcrição não diz. | Fabiana | RF001, RF002, RF017 | Baixar as pastas (assim está no RF017). |
| 1d | A Procuradoria quer **exportar** o checklist no mesmo formato do Word atual (RF016)? Em PDF basta ou precisa ser editável? | Fabiana | RF016 | PDF; editável se ela ainda for ajustar à mão. |
| 2 | O conceito de cada **indicador** é inteiro (1 a 5 ou NSA), como no instrumento do INEP, ou também pode ser fracionado? Hoje está decimal só na dimensão e no conceito final (CC). | Fabiana | RF012 | Manter assim, conforme o INEP. |
| 3 | O que representa o "período" (2025.1, 2025.2…) se a tela chama a área de "Anuais"? É semestre letivo, ciclo de avaliação ou versão do checklist? | Equipe do esboço (telas do Miro) | RF004, RF005 | Confirmar nas telas do Miro. |
| 4 | Ao excluir ou reordenar um indicador, a numeração deve mudar? O checklist de Medicina usa a numeração oficial do INEP (1.1–1.24, 2.1–2.16, 3.1–3.18). | Fabiana | RF006, RF007, RF015 | No RF007, a nova numeração só é aplicada após confirmação. |
| 5 | Os cursos serão cadastrados à mão ou virão do sistema acadêmico? | Fabiana / TI do sistema acadêmico | RF003 | Trazer do sistema acadêmico, se a integração permitir. |
| 6 | Quais formatos de arquivo e qual tamanho máximo podem ser enviados? | Fabiana | RF010, RF014 | PDF, imagens e documentos do Office, com tamanho a definir. |
| 7 | Os documentos que hoje estão na nuvem dos cursos serão migrados com envio em massa ou um por um? | Fabiana / Coordenações | RF010 | Tratar como requisito à parte, se for preciso. |

## Respondidas (v2)

| Pergunta | Resposta | Onde entrou |
|---|---|---|
| Coordenação de Curso terá acesso? | Sim. Envia documentos só dos cursos a que está vinculada. | RF002, RF010, seção 2.2 |
| Revisão e validação são uma ou duas etapas? | Uma etapa só, feita pela Procuradoria. | RF011 (regra 7) |
| Quem gerencia o sistema? | ~~Só a Procuradoria Institucional~~ → **substituído na v5** pelos perfis Administrador Master / Administrador / Coordenação (item A). | RF002, RF009, RF015 |
| Precisa de nível de subindicador? | Sim, e continua mesmo com o checklist de Medicina (confirmado pelo usuário em 10/11). | **RF015**; RF005, RF007, RF008, RF016 e RF017 |
| Repositórios por quê? | A transcrição pede repositórios **por dimensão e por indicador**, que substituem a nuvem e as ~300 pastas, com fluxo de envio, revisão e validação. | Novo **RF017**; Abrangência (seção 2) |
| Alterações no modelo institucional chegam sozinhas nos cursos já criados? | ~~Não, aplica curso a curso~~ → **substituído na v5** pelo checklist único com etiquetas (itens C e D). | RF009 |
| Nome do sistema? | Fabiana (antes chamado Mozart; Qualis5 no esboço). | Capa, cabeçalho e seção 2 |
| Notas inteiras ou fracionadas? | Fracionadas. Aplicado a dimensões e conceito final; indicador segue o INEP (1–5 ou NSA). Confirmar na pergunta 3. | RF012, RF013 |

## Achados no checklist de Medicina que entraram no documento (v4)

- Documentos numerados por dimensão, com subnível (16.1) e itens sem número (ex.: programas dentro de “78. Política de extensão”) → RF008.
- Um documento comprova vários indicadores, sem reenvio → RF008 (regra 5) e RF010 (regra 7).
- Grupos “Outras referências” e “Documentos sem indicador correspondente” ao fim de cada dimensão → RF008.
- Anotações da Procuradoria nos documentos (“atualizar”, “falta 2019”) → campo “Observação” no RF008.
- NSA por tipo de curso (“Exclusivo para cursos de licenciatura”, “Não se aplica”) → campos “Modalidade” e “Área da saúde” no RF003 e “Aplicabilidade” no RF007, com NSA automático.
- O checklist é um documento Word que a Procuradoria monta à mão → novo **RF016** (exportação).
- Itens próprios de Medicina (eixos, manual do interno, ligas acadêmicas) confirmam o checklist específico do curso → exemplo no RF009.

## Achados no instrumento do INEP (2017) que entraram no documento

- Cada indicador tem um **critério de análise escrito para cada conceito (1 a 5)**. Entrou como campo "Critérios de análise" no RF007.
- Vários indicadores são **NSA** para certos cursos (ex.: 1.22 SUS, 1.24 licenciaturas, 2.10 EaD). Entrou como opção "Não se aplica" com justificativa no RF007.
- O **CC** é calculado com pesos por dimensão (D1 = 30, D2 = 40, D3 = 30). Entrou no glossário. O instrumento novo pode mudar esses pesos.
- O instrumento tem 24 indicadores na dimensão 1, 16 na dimensão 2 e 18 na dimensão 3. Dá para usar como carga inicial do modelo institucional.

## Recomendações de pesquisa e documentos a buscar

| # | O que buscar | Onde/como | Requisitos afetados |
|---|---|---|---|
| 1 | Checklists de outros cursos (de preferência um que não seja da saúde) | Fabiana | RF003, RF007, RF008, RF009 |
| 2 | Telas no Miro | Recebidas (`docs/fontes/miro/`, 12/11/2026). Nenhuma tem tela de cadastro de curso | RF001–RF009, RF015 |
| 3 | Novo instrumento do MEC/INEP (previsto para dezembro, com 5 dimensões) | Portal do INEP e Diário Oficial | RF006, RF009, RF012 |
| 4 | Um relatório de avaliação do MEC já recebido (ex.: Medicina, dimensão 1 = 4,97) | Procuradoria Institucional | RF012, RF013 |
| 5 | Como fazer o login usando as credenciais do sistema acadêmico e se a autenticação da instituição (“Entrar com CESMAC”, tela de login da dupla) pode ser usada | TI responsável pelo sistema acadêmico | RF001, RF002 |

## Suposições adotadas (confirmar)

| # | Suposição | Base | Requisitos |
|---|---|---|---|
| 1 | "Quantidade de documento" é o número de documentos exigidos para considerar o anexo atendido | Esboço de tela | RF008, RF010 |
| 2 | Situação do indicador: Pendente / Em andamento / Concluído / NSA | Fluxo de envio → validação | RF005 |
| 3 | Situações do documento: Enviado / Validado / Devolvido para ajuste | Fluxo de envio → validação | RF010, RF011 |
| 4 | Um novo período pode copiar a estrutura de um período anterior | Pedido de reaproveitar documentos | RF004 |
| 5 | Tipos de avaliação: Autorização / Reconhecimento / Renovação | Reunião + instrumento do INEP | RF012 |
| 6 | Um documento reaproveitado passa por nova revisão | Boa prática | RF014 |
| 7 | Recuperação de senha fica a cargo do sistema acadêmico | O login usa as credenciais do sistema acadêmico | RF001 |
| 8 | Anexos podem ficar direto no indicador ou nos subindicadores | Esboço (anexos no indicador) + pedido de subnível | RF008, RF015 |
| 9 | Pró-Reitores e Pró-Reitoria Acadêmica apenas consultam | "Só um perfil gerencia" | RF009 |
| 10 | NSA automático pela modalidade e pela área da saúde (a faculdade só tem bacharelado, então o grau saiu do RF003), com base nas observações do INEP; a Procuradoria pode desfazer | Notas “Obrigatório para…/NSA para…” do instrumento | RF003, RF007 |
| 11 | Exportação em PDF | Uso atual (documento impresso/enviado) | RF016 |
| 12 | Baixar o repositório gera uma pasta por anexo, nomeada com número e nome | Hoje as comprovações são entregues em pastas | RF017 |
| 13 | Pró-Reitores consultam repositórios de todos os cursos | Transcrição: Pró-Reitores têm acesso à plataforma | RF017 |
| 14 | Procuradoria Institucional tem perfil Administrador, igual aos Pró-Reitores | O fluxo só cita pró-reitores como admins, mas a Procuradoria monta o checklist | RF002 |
| 15 | Quem cuida do Administrador Master não foi definido (talvez o CITEC/TI) | “Pode-se pensar em deixar em alguma conta de Adm master” | RF002 |
| 16 | Subindicadores e anexos herdam as etiquetas do indicador; anexos também podem ter etiqueta própria | Fluxo mostra etiqueta só em dimensão e indicador; Medicina tem anexos próprios em indicadores comuns | RF007, RF008, RF009 |
| 17 | A Coordenação de Curso usa o sistema (envia documentos e consulta checklist e repositórios dos seus cursos), mas **não administra** nada | Usuário acredita que não; vai avisar se mudar | RF002, RF009, RF010, RF017 |
