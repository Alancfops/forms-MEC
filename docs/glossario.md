# Glossário – Projeto Fabiana

Termos usados no levantamento de requisitos e nas fontes do projeto. Cada termo traz a fonte de onde veio.

**Fontes citadas:**
- **Transcrição:** `fontes/transcricao-reuniao-projeto-mozart.pdf`
- **INEP:** `fontes/instrumento-inep-2017-reconhecimento-curso.pdf` (glossário no fim do instrumento)
- **Checklist:** `fontes/checklist-medicina/`
- **Fluxo:** `fontes/fluxo-telas-sistema-fabiana.jpg` e `fontes/miro/`
- **RFxxx:** requisito do `requisitos/Levantamento de requisitos - Projeto Fabiana.docx`

---

## 1. Avaliação do MEC

| Termo | Significado | Fonte |
|---|---|---|
| **MEC** | Ministério da Educação. Faz a avaliação externa para abrir e para manter um curso. | Transcrição |
| **INEP** | Órgão do MEC responsável pelo instrumento de avaliação de cursos. O instrumento atual deve mudar de 3 para 5 dimensões (previsto para dezembro, com aplicação no ano seguinte). | Transcrição, INEP |
| **Sinaes** | Sistema Nacional de Avaliação da Educação Superior, criado em 2004 para melhorar a qualidade dos cursos de graduação e das instituições. | INEP |
| **Avaliação externa** | Avaliação feita pelo MEC, com visita *in loco* de uma comissão de avaliadores, que gera um relatório e o Conceito de Curso. | Transcrição, INEP |
| **Autorização / Reconhecimento / Renovação de reconhecimento** | Etapas do curso perante o MEC: o curso precisa de **autorização** para começar, de **reconhecimento** para emitir diplomas e de **renovação de reconhecimento**, periódica, para continuar sendo ofertado. | INEP (os três tipos de avaliação no RF012 são suposição, ver `pendencias.md`) |
| **Instrumento de avaliação** | Documento do INEP com as dimensões, os indicadores e os critérios usados pelos avaliadores. É a base dos checklists da Fabiana. O de 2017 vale para todos os cursos, exceto os tecnológicos. | Transcrição, INEP |
| **Dimensão** | Grande grupo de indicadores do instrumento. Hoje são 3: **1. Organização Didático-Pedagógica** (24 indicadores), **2. Corpo Docente e Tutorial** (16) e **3. Infraestrutura** (18). | INEP, Transcrição |
| **Indicador** | Item avaliado dentro de uma dimensão, numerado pelo INEP (ex: 1.1 Políticas institucionais no âmbito do curso). Recebe um conceito de 1 a 5 ou NSA. | INEP, RF007 |
| **Subindicador** | Desdobramento de um indicador feito pela própria Fabiana (ex: no currículo flexível, separar acessibilidade, Libras e estudos étnico-raciais). Não existe no instrumento do INEP. | Transcrição, RF015 |
| **Critérios de análise** | Texto do INEP que descreve o que é preciso para cada conceito (1 a 5) de um indicador. | INEP, RF007 |
| **Conceito** | Nota de 1 a 5 dada a cada indicador. 4 = atende a todas as exigências (excelência); 5 = atende com diferenciais de inovação. A Fabiana citou notas de 0 a 5 na reunião; o instrumento usa 1 a 5. | Transcrição, INEP |
| **CC – Conceito de Curso** | Nota final do curso, em cinco níveis, calculada com pesos por dimensão (D1 = 30, D2 = 40, D3 = 30). Valores a partir de 3 indicam qualidade satisfatória. As notas finais são fracionadas (ex: dimensão 1 de Medicina = 4,97). | INEP, Transcrição |
| **Diligência** | Situação do curso que tira nota 0, 1 ou 2: fica impedido de ofertar vestibular até corrigir o problema. | Transcrição |
| **NSA** | “Não se aplica”: o indicador não tem pertinência com o curso (ex: indicador de EaD para curso totalmente presencial). | INEP, RF007 |
| **Relatório do MEC (parecer)** | Documento que acompanha as notas e descreve as fragilidades encontradas (ex: adequar salas de aula multifuncionais). | Transcrição, RF012 |

## 2. Documentos e órgãos da instituição

| Termo | Significado | Fonte |
|---|---|---|
| **IES** | Instituição de Educação Superior, pública ou privada, que oferece cursos de graduação. | INEP |
| **DCN – Diretriz Curricular Nacional** | Regra pública que cada curso de graduação deve seguir. A Fabiana lê a DCN do curso, traduz em indicadores de qualidade e monta o checklist específico do curso. | Transcrição |
| **PPC – Projeto Pedagógico do Curso** | Documento do curso que precisa atender, no mínimo, à DCN. Tudo o que é avaliado precisa estar nele. Pode ser revisado quando o NDE e a coordenação acharem necessário, com aprovação da Pró-Reitoria Acadêmica. | Transcrição, INEP, RF014 |
| **PDI – Plano de Desenvolvimento Institucional** | Instrumento de planejamento e gestão da instituição (missão, metas, estrutura, cursos ofertados, infraestrutura). Muda a cada 5 anos. | Transcrição, INEP, RF014 |
| **NDE – Núcleo Docente Estruturante** | Grupo de professores do curso que acompanha a concepção e a atualização do PPC. | INEP, Transcrição |
| **Procuradoria Institucional** | Setor da Fabiana, responsável pela avaliação. Monta os checklists, revisa os documentos e alimenta o histórico de notas do MEC. | Transcrição |
| **Pró-Reitores / Pró-Reitoria Acadêmica** | Pró-Reitores Acadêmico, de Graduação e de Pesquisa e Extensão. Na reunião foram citados como quem terá acesso à plataforma. | Transcrição |
| **Coordenação de Curso** | Equipe do curso que reúne e envia os documentos que comprovam os indicadores. | Transcrição, RF010 |
| **CITEC** | Centro de Inovação Tecnológica do CESMAC, que desenvolve o sistema. | Transcrição |
| **Bacharelado / Modalidade (presencial ou EaD)** | A faculdade só tem bacharelados, com cursos presenciais e a distância (EaD). A modalidade decide se alguns indicadores são NSA. | Decisão do usuário, RF003 |

## 3. Termos do sistema Fabiana

| Termo | Significado | Fonte |
|---|---|---|
| **Fabiana** | Nome do sistema. Antes chamado Mozart (nome usado na transcrição) e Qualis5 (no esboço de telas). | Decisão do usuário |
| **Checklist** | Lista de tudo que precisa ser comprovado ao MEC, organizada em Dimensão → Indicador → Subindicador → Anexo. No sistema, há **um checklist por período**, comum a todos os cursos, com etiquetas de curso. | Transcrição, Fluxo, RF005, RF009 |
| **Período** | Ciclo do checklist (ex: “2025.1”). Ainda não se sabe se é semestre letivo, ciclo de avaliação ou versão do checklist (pendência 3). | Fluxo, RF004 |
| **Usar modelo do ano anterior / Criar novo modelo** | Opções ao abrir um período: copiar o checklist de um período anterior ou começar vazio. | Fluxo, RF004 |
| **Etiqueta de curso (campo “Áreas”)** | Marca de curso (ex: “Medicina”) em uma dimensão, um indicador ou um anexo. Sem etiqueta, o campo “Áreas” mostra “todos” e o item vale para todos os cursos. A coordenação vê só os itens sem etiqueta e os do seu curso. | Fluxo, RF006, RF007, RF009 |
| **Aplicabilidade** | Para quais cursos o indicador se aplica (Todos os cursos / A distância / Área da saúde), conforme as observações do INEP. Gera o NSA automático. | INEP, RF007 |
| **Anexo** | Documento exigido para comprovar um ou mais indicadores ou subindicadores. É numerado por dimensão (ex: “1. PPC”, que vale para os indicadores 1.1 a 1.5), pode ter subnível (ex: 16.1) e tem uma quantidade de documentos a enviar. | Checklist, RF008 |
| **Documentos sem indicador correspondente** | Grupo no fim de cada dimensão com documentos que não comprovam nenhum indicador (ex: alvará, plano de fuga). | Checklist, RF008 |
| **Outras referências** | Materiais de apoio da dimensão que não exigem envio de documento (ex: “Pasta do(s) coordenador(es) do curso”). | Checklist, RF008 |
| **Documento exemplo** | Modelo que o administrador anexa ao anexo para orientar a coordenação, com uma caixa de seleção para mostrá-lo ou não. | Fluxo, RF008, RF010 |
| **Repositório** | Local do sistema onde ficam os documentos enviados, organizado por dimensão e por indicador. Substitui a nuvem e as cerca de 300 pastas usadas hoje. | Transcrição, RF010, RF017 |
| **Situação do documento** | Enviado / Validado / Devolvido para ajuste. Devolver exige um parecer para quem enviou. | RF010, RF011 (suposição, ver `pendencias.md`) |
| **Validação** | Etapa única de revisão e aprovação dos documentos enviados pela coordenação. | Decisão do usuário, RF011 |
| **Whitelist (usuários autorizados)** | Lista de pessoas que podem entrar no sistema, cadastradas antes pelo e-mail. | Transcrição, Fluxo, RF002 |
| **Entrar com CESMAC** | Botão de login com a autenticação da instituição; ainda depende de confirmação da TI (pendência 5). | Fluxo, RF001 |
| **Administrador Master** | Perfil que cadastra os usuários e define a função de cada um. | Fluxo, RF002 |
| **Administrador** | Perfil dos Pró-Reitores e da Procuradoria (esta última por suposição): monta o checklist, valida documentos e registra o histórico. | Fluxo, RF002 |
| **Histórico de avaliações** | Registro das notas e dos relatórios do MEC por curso, por dimensão e por indicador, para acompanhar a evolução. | Transcrição, RF012, RF013 |
