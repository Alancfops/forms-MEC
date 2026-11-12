# Modelos de especificação

## Requisito funcional

| Campo | Conteúdo |
|---|---|
| ID | RF001 |
| Nome | Registrar resposta de avaliação |
| Descrição | O sistema deve permitir que o **Aluno** registre respostas a um questionário de avaliação ativo dentro do período de aplicação. |
| Prioridade | Must |
| Fonte | Reunião 06/11/2026, min. 12:30 – Coordenação |
| Regras relacionadas | RN003, RN004 |
| Dependências | RF000 (autenticação) |
| Critérios de aceite | ver US001 |
| Status | Proposto / Aprovado / Implementado / Cancelado |

## Requisito não funcional

| ID | Categoria (ISO 25010) | Descrição | Métrica / critério de verificação | Prioridade | Fonte |
|---|---|---|---|---|---|
| RNF001 | Desempenho | Carregar o questionário | ≤ 2 s no p95 com 500 usuários simultâneos | Should | … |
| RNF002 | Segurança | Dados pessoais tratados conforme LGPD | Respostas anonimizadas nos relatórios agregados | Must | … |

## Regra de negócio

| ID | Regra | Exemplo | Fonte |
|---|---|---|---|
| RN001 | Cada aluno responde no máximo uma vez a cada questionário por período. | Segunda tentativa é bloqueada com mensagem. | … |

## História de usuário + critérios de aceite (Gherkin)

```
US001 – Responder avaliação
Como aluno matriculado,
quero responder o questionário de avaliação da disciplina,
para que minha opinião seja considerada na melhoria do curso.

Cenário: Resposta enviada com sucesso
  Dado que existe um questionário ativo para minha disciplina
  E que ainda não respondi este questionário
  Quando eu preencher todas as perguntas obrigatórias e enviar
  Então o sistema registra minhas respostas
  E exibe a confirmação de envio

Cenário: Tentativa de resposta duplicada (RN001)
  Dado que já respondi este questionário
  Quando eu tentar acessá-lo novamente
  Então o sistema informa que a resposta já foi registrada
```

Checagem INVEST: Independente, Negociável, Valiosa, Estimável, Small (pequena), Testável.

## Caso de uso expandido

```
UC001 – Responder Avaliação
Ator principal: Aluno
Atores secundários: —
Pré-condições: Aluno autenticado; questionário ativo (RN002).
Pós-condições (sucesso): Respostas persistidas e vinculadas ao período.
Requisitos: RF001, RF002 | Regras: RN001, RN002

Fluxo principal:
 1. Aluno seleciona a avaliação pendente.
 2. Sistema exibe as perguntas.
 3. Aluno responde e confirma envio.
 4. Sistema valida obrigatórias [FE01].
 5. Sistema registra e exibe confirmação.

Fluxos alternativos:
 FA01 – Salvar rascunho (passo 3): ...

Fluxos de exceção:
 FE01 – Pergunta obrigatória vazia: sistema destaca o campo e retorna ao passo 3.
```

## Glossário

| Termo | Definição | Sinônimos a evitar |
|---|---|---|

## Lista de dúvidas abertas

| # | Pergunta | Destinatário | Impacto se não respondida | Status |
|---|---|---|---|---|

## Matriz de rastreabilidade

| Fonte | RN | RF/RNF | UC/US | Classe/Diagrama | Teste |
|---|---|---|---|---|---|

## Documento de requisitos

Estrutura recomendada (baseada em ISO/IEC/IEEE 29148):

1. Introdução — propósito, escopo (dentro/fora), definições (glossário), referências, visão geral
2. Descrição geral — contexto e problema, stakeholders e usuários (perfis), restrições, premissas e dependências
3. Requisitos funcionais (agrupados por módulo/funcionalidade)
4. Requisitos não funcionais (por categoria ISO 25010)
5. Regras de negócio
6. Modelos — casos de uso (diagrama + expandidos), modelo de domínio, diagramas comportamentais
7. Protótipos / referências de telas (se houver)
8. Matriz de rastreabilidade
9. Dúvidas abertas e riscos
10. Histórico de versões
