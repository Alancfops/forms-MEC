# PRD – Sistema Fabiana

Documento de requisitos de produto. Resume **o que** será construído, **para quem** e **por quê**. Os detalhes de cada tela e regra estão no levantamento de requisitos (`requisitos/Levantamento de requisitos - Projeto Fabiana.pdf`). Os termos estão explicados em `glossario.md`, e a arquitetura está no `README.md`.

| | |
|---|---|
| **Produto** | Sistema Fabiana (antes chamado Mozart) |
| **Cliente** | Procuradoria Institucional do CESMAC (Fabiana) |
| **Desenvolvimento** | CITEC – Centro de Inovação Tecnológica |
| **Versão** | 1.0 – 12/11/2026, com base no levantamento v5.1 |
| **Situação** | Requisitos concluídos; aguardando validação da Fabiana; desenvolvimento não iniciado |

---

## 1. Problema

Para abrir e para manter cada curso de graduação, a instituição passa pela avaliação externa do MEC. O instrumento do INEP tem 3 dimensões com dezenas de indicadores, e cada indicador precisa ser **comprovado com documentos**.

Hoje esse trabalho é manual (fonte: transcrição):
- A Procuradoria lê a DCN de cada curso, traduz em indicadores e monta à mão um **checklist enorme** em Word.
- Os cursos montam **quase 300 pastas físicas e digitais** para apresentar ao MEC.
- Os documentos ficam numa **nuvem genérica**, e a Procuradoria revisa tudo fora de qualquer sistema.
- As notas e os relatórios das avaliações passadas não ficam reunidos num lugar só, o que dificulta acompanhar a evolução e as fragilidades de cada curso.

Se um curso tirar nota 0, 1 ou 2, ele entra em **diligência** e não pode ofertar vestibular. A instituição hoje tem cerca de 95% de nota máxima nos cursos avaliados desde 2017 (fonte: transcrição), e o objetivo é manter esse resultado com menos esforço.

## 2. Objetivos

1. **Substituir o checklist em Word e a nuvem genérica** por um checklist no sistema, com repositórios de documentos por dimensão e por indicador.
2. **Dar à coordenação de cada curso** um lugar único para saber o que enviar e para enviar os documentos.
3. **Ter um fluxo de revisão e validação** dos documentos, com parecer quando algo precisa de ajuste.
4. **Guardar o histórico das avaliações do MEC** (notas, relatórios e fragilidades) para acompanhar a evolução de cada curso.
5. **Aguentar mudanças no instrumento**: o MEC/INEP prevê passar de 3 para 5 dimensões, então a estrutura do checklist precisa ser editável.

### Fora do escopo
- Acesso direto dos avaliadores do MEC ao sistema. A Procuradoria exporta o checklist e baixa as pastas para entregar (pendência 1c).
- Cadastro e recuperação de senhas, que ficam com o sistema acadêmico (RF001).
- Cursos de licenciatura e tecnológicos, porque a instituição só tem bacharelado.
- Migração automática da nuvem atual. Se for preciso, vira um requisito à parte (pendência 7).

### Métricas de sucesso (sugestões, a validar com a Fabiana)
- Todos os cursos com avaliação no período com o checklist montado **no sistema**, sem cópia em Word.
- Nenhum documento de comprovação guardado fora do sistema (fim do uso da nuvem genérica).
- Todo documento enviado com situação final: validado ou devolvido com parecer.
- Histórico do MEC preenchido para os cursos já avaliados.

## 3. Usuários

| Perfil | Quem é | O que faz |
|---|---|---|
| **Administrador Master** | A definir (talvez o CITEC/TI) | Cadastra os usuários pelo e-mail e define o perfil de cada um |
| **Administrador** | Pró-Reitores e Procuradoria Institucional (esta última é suposição) | Monta o checklist do período, valida os documentos, registra o histórico do MEC e exporta o checklist |
| **Coordenação de Curso** | Coordenadores dos cursos | Vê o checklist do seu curso e envia os documentos dos cursos a que está vinculada; não administra nada |

São poucas dezenas de usuários, todos internos, que entram com o login do sistema acadêmico e precisam estar cadastrados antes (whitelist).

## 4. Funcionalidades

Prioridade: **Essencial** entra no MVP; **Importante** entra na fase 2.

| # | Funcionalidade | O que entrega | RFs | Prioridade |
|---|---|---|---|---|
| F1 | Acesso | Login com as credenciais do sistema acadêmico ou “Entrar com CESMAC”; só entra quem está na whitelist | RF001 | Essencial |
| F2 | Usuários e perfis | Cadastro por e-mail, perfil e cursos vinculados | RF002 | Essencial |
| F3 | Cursos | Cadastro com modalidade (presencial/EaD), área da saúde e DCN | RF003 | Essencial |
| F4 | Períodos | Novo período copiando o anterior ou começando vazio | RF004 | Essencial |
| F5 | Checklist | Dimensões, indicadores (com critérios do INEP e NSA), subindicadores e anexos, num checklist único por período | RF005–RF008, RF015 | Essencial |
| F6 | Etiquetas de curso | Itens específicos de um curso; sem etiqueta, valem para todos | RF009 | Essencial |
| F7 | Envio de documentos | A coordenação envia os documentos de cada anexo; um documento pode comprovar vários indicadores | RF010 | Essencial |
| F8 | Validação | Validar ou devolver com parecer obrigatório, em uma etapa só | RF011 | Essencial |
| F9 | Repositórios | Consulta por dimensão e por indicador e download das pastas por anexo | RF017 | Essencial |
| F10 | Histórico do MEC | Registro das notas (fracionadas), dos relatórios e das fragilidades | RF012 | Importante |
| F11 | Evolução | Comparativo das avaliações do curso e destaque das fragilidades | RF013 | Importante |
| F12 | PDI e PPC | Versões sem apagar as anteriores e reaproveitamento em novas avaliações | RF014 | Importante |
| F13 | Exportação | Checklist do curso em PDF | RF016 | Importante |

## 5. Fluxo principal

1. O **Administrador** abre o período (ex: 2025.1), copiando o checklist anterior ou criando um novo.
2. Ele ajusta as dimensões, os indicadores, os subindicadores e os anexos, e marca com **etiquetas** o que é de um curso só.
3. A **Coordenação** entra e vê só os itens sem etiqueta e os do seu curso.
4. A Coordenação **envia os documentos** de cada anexo.
5. O Administrador **valida** o documento ou **devolve com parecer**. Se devolveu, a coordenação corrige e reenvia.
6. Perto da avaliação, a Procuradoria **exporta o checklist** e **baixa as pastas** para entregar ao MEC.
7. Depois da avaliação, a Procuradoria **registra as notas, o relatório e as fragilidades** no histórico.

## 6. Requisitos não funcionais

O levantamento ainda não tem RNFs: a seção existe no documento, mas está vazia por decisão do autor. Os pontos abaixo saem das fontes e precisam ser detalhados:

| Tema | O que se sabe | Fonte |
|---|---|---|
| Acesso | Só usuários da whitelist, com as credenciais do sistema acadêmico | Transcrição, RF001, RF002 |
| Permissões | Cada perfil vê e faz só o que lhe cabe; a coordenação só vê os seus cursos | RF002, RF009, RF017 |
| Histórico | Versões de PDI e PPC nunca são apagadas; exclusões sempre pedem confirmação | RF014, padrão dos RFs |
| Volume | Centenas de documentos por curso (hoje cerca de 300 pastas) | Transcrição |
| Formatos e tamanho de arquivo | A definir | Pendência 6 |
| Flexibilidade | A estrutura do checklist precisa acompanhar a mudança do instrumento do INEP | Transcrição |
| Dados pessoais, desempenho, disponibilidade e backup | A definir | — |

## 7. Restrições e premissas

- **Arquitetura definida:** Java, monolito modular, um repositório, frontend Thymeleaf em módulo separado, code review, clean code e testes no CI. As ferramentas (Spring Boot, PostgreSQL, MinIO, htmx…) são sugestões e podem ser trocadas (`README.md`).
- **Os requisitos seguem o fluxo de telas da equipe anterior.** Os prints do Miro são exemplos do fluxo, não o design.
- **Instrumento do INEP de 2017** como base, até sair o novo.
- **Suposições** registradas em `requisitos/pendencias.md`. As principais: a Procuradoria tem perfil Administrador, e as situações dos documentos são Enviado / Validado / Devolvido para ajuste.

## 8. Dependências e riscos

| Risco ou dependência | Impacto | O que fazer |
|---|---|---|
| A Fabiana ainda não validou as mudanças A–G e o modelo de anexos | Retrabalho no checklist e nos repositórios | Validar antes de começar F5–F9 |
| Novo instrumento do MEC/INEP (de 3 para 5 dimensões) | Estrutura do checklist muda | Manter dimensões e indicadores editáveis (já previsto) |
| Integração com o sistema acadêmico depende da TI | Sem login, nada funciona | Conversar com a TI cedo (pendência 5) |
| Origem dos cursos: sistema acadêmico ou cadastro manual | Muda o RF003 | Pendência 5 |
| Troca de responsável pelo projeto | Perda de contexto | README, glossário, PRD e pendências mantidos em `docs/` |

## 9. Entregas sugeridas

| Fase | Conteúdo | Pronto quando |
|---|---|---|
| **0. Base** | Repositório, CI (build, testes, linter), `main` protegida, ambiente local | Um PR de exemplo passa no CI e na revisão |
| **1. MVP** | F1–F9 (RFs Essenciais) | Um curso consegue montar o checklist, enviar e validar todos os documentos de um período |
| **2. Histórico** | F10–F13 | Histórico do MEC registrado e checklist exportado em PDF |

## 10. Questões em aberto

As perguntas para a Fabiana e para a TI estão em `requisitos/pendencias.md`. As que mais afetam o MVP:
- **1:** confirmar os anexos numerados por dimensão e vinculados a vários indicadores.
- **3:** o que é o “período” (semestre letivo, ciclo de avaliação ou versão do checklist).
- **5:** como funciona o login com o sistema acadêmico e de onde vêm os cursos.
- **6:** formatos e tamanho máximo dos arquivos.
