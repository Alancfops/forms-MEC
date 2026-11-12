# Sintaxe UML — Mermaid e PlantUML

## Casos de uso (PlantUML — Mermaid não tem suporte nativo)

```plantuml
@startuml
left to right direction
actor Aluno
actor Coordenador
actor "Sistema Acadêmico" as SA <<sistema>>
rectangle "Sistema de Avaliação" {
  usecase "Responder avaliação" as UC1
  usecase "Manter questionário" as UC2
  usecase "Emitir relatório de indicadores" as UC3
  usecase "Autenticar" as UC0
  usecase "Exportar PDF" as UC4
}
Aluno --> UC1
Coordenador --> UC2
Coordenador --> UC3
UC1 ..> UC0 : <<include>>
UC4 ..> UC3 : <<extend>>
UC1 --> SA
@enduml
```

Alternativa em Mermaid (aproximação com flowchart, quando só Mermaid renderiza):

```mermaid
flowchart LR
  Aluno([👤 Aluno]) --- UC1((Responder avaliação))
  Coord([👤 Coordenador]) --- UC2((Manter questionário))
  UC1 -. include .-> UC0((Autenticar))
```

## Classes (domínio)

```mermaid
classDiagram
  class Questionario {
    titulo
    periodo
    ativo
    publicar()
  }
  class Pergunta {
    enunciado
    tipo
    obrigatoria
  }
  class Resposta {
    valor
    dataEnvio
  }
  Questionario "1" *-- "1..*" Pergunta : contém
  Pergunta "1" -- "0..*" Resposta : recebe
  Aluno "1" -- "0..*" Resposta : registra
  Usuario <|-- Aluno
  Usuario <|-- Coordenador
```

Relações: `<|--` herança, `*--` composição, `o--` agregação, `-->` associação dirigida, `..>` dependência, `..|>` realização.

## Sequência

```mermaid
sequenceDiagram
  actor A as Aluno
  participant UI as Interface
  participant S as ServicoAvaliacao
  participant BD as Repositório
  A->>UI: Envia respostas
  UI->>S: registrar(respostas)
  S->>BD: jaRespondeu(aluno, questionario)
  BD-->>S: false
  alt respostas válidas
    S->>BD: salvar(respostas)
    S-->>UI: ok
    UI-->>A: Confirmação
  else obrigatória vazia
    S-->>UI: erro de validação
  end
```

## Atividades (com raias)

```plantuml
@startuml
|Coordenador|
start
:Criar questionário;
:Publicar;
|Aluno|
:Responder;
|Sistema|
if (Todas obrigatórias?) then (sim)
  :Registrar respostas;
else (não)
  :Exibir erro;
endif
stop
@enduml
```

Em Mermaid use `flowchart TD` com `subgraph` por raia.

## Máquina de estados

```mermaid
stateDiagram-v2
  [*] --> Rascunho
  Rascunho --> Publicado : publicar
  Publicado --> Encerrado : fim do período
  Publicado --> Rascunho : despublicar [sem respostas]
  Encerrado --> [*]
```

## Entidade-Relacionamento

```mermaid
erDiagram
  QUESTIONARIO ||--|{ PERGUNTA : contem
  PERGUNTA ||--o{ RESPOSTA : recebe
  ALUNO ||--o{ RESPOSTA : registra
```

## Componentes / Implantação (PlantUML)

```plantuml
@startuml
node "Servidor Web" {
  [Frontend] --> [API]
}
database "PostgreSQL" as DB
[API] --> DB
@enduml
```

## Dicas
- Mermaid: evite acentos/espaços em identificadores; use rótulos entre aspas ou `id["Rótulo"]`.
- Mantenha cada diagrama focado (≤ ~15 elementos); divida por módulo se crescer.
- Legende decisões não óbvias logo abaixo do diagrama.
