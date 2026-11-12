---
name: backend
description: Como construir o backend Java do sistema Fabiana com Clean Architecture e clean code — estrutura de pacotes por módulo (domain, application, adapters), regra de dependência, casos de uso, portas e adaptadores, persistência separada do domínio, permissões, eventos entre módulos e testes por camada. Use SEMPRE que for criar ou alterar código Java do backend deste projeto, implementar um RF no backend, criar entidade, caso de uso, repositório, migração, integração (sistema acadêmico, armazenamento de arquivos) ou decidir onde uma classe deve ficar — mesmo que o pedido seja só "implementa o RF004", "cria a entidade Indicador" ou "onde coloco essa regra?".
---

# Backend – Sistema Fabiana

O backend é em **Java** e segue **Clean Architecture** dentro de um **monolito modular**. O objetivo é que o código e a estrutura fiquem limpos com o tempo: a regra de negócio não depende de framework, banco ou tela, e cada coisa tem um lugar óbvio. Quem chegar ao projeto deve conseguir achar onde está uma regra só pelo nome do pacote.

As regras de código (nomes, funções, erros, segurança) estão em `qualidade-codigo/references/clean-code.md`, e os testes em `qualidade-codigo/references/testes.md`. Esta skill cuida da **arquitetura**: onde cada coisa fica e quem pode depender de quem.

Spring Boot, PostgreSQL e MinIO são **sugestões** do `docs/README.md` e podem ter mudado. Confira o `pom.xml` antes de usar os exemplos. A arquitetura vale com qualquer framework, porque o framework fica só nas bordas.

## A regra de dependência

```
        adapters  ──►  application  ──►  domain
 (web, banco, arquivos,   (casos de uso,      (entidades, regras,
  sistema acadêmico)       portas)             eventos)
```

**As dependências só apontam para dentro.** O `domain` não conhece ninguém. O `application` conhece só o `domain`. Os `adapters` conhecem os dois. Quando o caso de uso precisa de algo de fora (salvar, guardar arquivo, saber quem está logado), ele declara uma **porta** (interface) no `application`, e um adaptador a implementa.

Por que isso importa aqui:
- **O instrumento do MEC vai mudar** (de 3 para 5 dimensões). Regras isoladas no domínio mudam sem mexer em banco nem em tela.
- **A integração de login ainda não está definida** (pendência 5). Atrás de uma porta, trocar a forma de autenticar não toca no resto.
- **O domínio é testado em milissegundos**, sem subir Spring nem banco.

## Estrutura de pacotes

Cada módulo de negócio (ver `docs/README.md`) tem as mesmas camadas:

```
backend/src/main/java/br/cesmac/fabiana/
├── compartilhado/                  ← o mínimo comum a todos (tipos de ID, erro base, Clock). Sem regra de negócio
├── acesso/                         ← RF001–RF002
├── estrutura/                      ← RF003–RF009, RF015
│   ├── EstruturaApi.java           ← contrato público do módulo (interface + records + eventos publicados)
│   ├── domain/                     ← Java puro
│   │   ├── Periodo.java
│   │   ├── Indicador.java
│   │   ├── Aplicabilidade.java
│   │   ├── PeriodoJaExisteException.java
│   │   └── IndicadorReordenado.java        (evento de domínio)
│   ├── application/
│   │   ├── CriarPeriodo.java               (caso de uso)
│   │   ├── port/in/                        (comandos e consultas que entram: records)
│   │   └── port/out/                       (o que o caso de uso precisa: PeriodoRepository, UsuarioAtual…)
│   ├── adapters/
│   │   ├── persistence/                    (entidades JPA, mapeadores, implementações dos repositórios)
│   │   └── integration/                    (sistemas externos, se houver)
│   └── config/                             (monta os casos de uso como beans; único lugar com "cola" do framework)
├── documentos/                     ← RF010, RF011, RF014, RF017 (+ adapters/storage para os arquivos)
└── avaliacoes/                     ← RF012, RF013, RF016
```

As **telas** ficam no módulo `frontend` (skill de frontend). Os controllers de lá são **adaptadores de entrada**: chamam os casos de uso pelas portas de entrada e nunca acessam repositório ou entidade JPA.

## O que vai em cada camada

### domain – as regras

- **Entidades e objetos de valor** com comportamento: `indicador.situacaoPara(curso)`, `periodo.copiarChecklistDe(anterior)`. Nada de classe só com getter e setter e a regra espalhada nos serviços.
- **Invariantes no construtor ou na fábrica**: um objeto inválido não chega a existir. Ex: `Anexo` com quantidade de documentos menor que 1 lança exceção ao ser criado.
- **Objetos de valor** como `record` imutável: `NumeroIndicador("1.1")`, `Conceito` (1–5 ou NSA), `NotaFracionada`.
- **Exceções de domínio** com o nome do problema, e **eventos de domínio** no passado (`DocumentoValidado`).
- **Proibido aqui:** Spring, JPA (`jakarta.persistence`), Jackson, HTTP, `LocalDate.now()` direto (receba a data ou um `Clock`).

### application – os casos de uso

- **Um caso de uso por ação do usuário**, com nome de verbo: `CriarPeriodo`, `ReordenarIndicadores`, `EnviarDocumento`, `ValidarDocumento`, `DevolverDocumentoParaAjuste`. Classe pequena, um método público (`executar`).
- O caso de uso **orquestra**: carrega pelas portas, checa a permissão, chama o domínio, salva e publica eventos. **A regra em si fica no domínio.**
- **Portas de entrada** (`port/in`): records de comando e de resultado (`CriarPeriodoComando`). O frontend só conhece isso.
- **Portas de saída** (`port/out`): interfaces escritas na língua do negócio (`PeriodoRepository.buscarPorCodigo`, `ArmazenamentoDeArquivos.guardar`, `UsuarioAtual.cursosVinculados()`), não na do banco.
- **Permissão é regra de negócio e fica aqui.** Por exemplo, a Coordenação só envia e consulta documentos dos seus cursos (RF002, RF010, RF017). O caso de uso pergunta à porta `UsuarioAtual` e nega se for o caso. Esconder o botão na tela não é proteção.
- **Transação:** o caso de uso é a unidade de transação. A única anotação de framework permitida nesta camada é `@Transactional`. É uma concessão pragmática: as alternativas puras custam muito mais código para pouco ganho.
- **Proibido aqui:** entidades JPA, controllers, `HttpServletRequest`, SDK do MinIO, SQL.

### adapters – as bordas

| Adaptador | Implementa | Exemplo |
|---|---|---|
| `persistence` | Portas de repositório | `PeriodoJpaRepository` + `PeriodoEntity` + `PeriodoMapper` |
| `storage` (em `documentos`) | `ArmazenamentoDeArquivos` | Cliente S3/MinIO |
| `integration` (em `acesso`) | Autenticação no sistema acadêmico / “Entrar com CESMAC” | A definir com a TI |
| eventos | `PublicadorDeEventos` | Publica no mecanismo de eventos do framework |

- **Entidade JPA ≠ entidade de domínio.** `PeriodoEntity` (com anotações JPA) fica no adaptador e é convertida para `Periodo` (domínio) por um mapeador. É mais código, mas impede o banco de ditar o formato das regras, e o domínio continua puro e testável.
- O adaptador **não tem regra de negócio**: só traduz entre o mundo de fora e as portas.

### config – a montagem

Declara os casos de uso como beans (ex: `@Bean CriarPeriodo criarPeriodo(PeriodoRepository r, …)`). Assim, o `application` não precisa de `@Service`, e toda a dependência do framework fica visível num lugar só.

## Comunicação entre módulos

- Um módulo usa outro **só pelo contrato público na raiz do módulo** (ex: `EstruturaApi`, records e eventos ali declarados). Nunca importe `domain`, `application` ou `adapters` de outro módulo.
- **Para avisar que algo aconteceu, use eventos**. Por exemplo, `documentos` publica `DocumentoValidado` e `estrutura` atualiza a situação do indicador. Isso evita dependência nos dois sentidos.
- **Para perguntar algo, use o contrato público.** Por exemplo, `documentos` pergunta a `EstruturaApi` quais anexos um curso vê.
- **Não compartilhe entidades nem tabelas entre módulos.** Cada módulo é dono dos seus dados. Referencie o dado de outro módulo pelo ID.

## Persistência e banco

- **Migrações versionadas** (Flyway, sugerido) em `backend/src/main/resources/db/migration`, com nome descritivo (`V3__cria_tabelas_de_anexo.sql`). Nunca edite uma migração já mergeada na `develop`: crie outra.
- **Tabelas com prefixo do módulo** (`estrutura_periodo`, `documentos_documento_enviado`), para deixar claro o dono de cada uma.
- **Consultas de lista** (checklist, repositórios) com cuidado para N+1: use projeções ou `JOIN FETCH` no adaptador.
- **Arquivos enviados** vão para o armazenamento de objetos pela porta `ArmazenamentoDeArquivos`. No banco, ficam só os metadados (nome original, chave no armazenamento, tamanho, tipo, quem enviou, quando).

## Configuração

- Perfis `dev`, `test` e `prod`. Segredos (senha do banco, chaves do armazenamento, credenciais de integração) **só por variável de ambiente**, nunca no repositório.
- Para rodar localmente, um `docker-compose.yml` na raiz sobe PostgreSQL e MinIO.

## Testes por camada

| Camada | Como testar |
|---|---|
| `domain` | Unitário puro, sem Spring e sem mock. A maior parte dos testes fica aqui |
| `application` | Caso de uso com **implementações falsas em memória** das portas (`PeriodoRepositoryEmMemoria`), preferidas a mocks. Incluir os testes de permissão |
| `adapters` | Integração real: Testcontainers com PostgreSQL e MinIO |
| Arquitetura | Teste automático da regra de dependência (abaixo) |

Detalhes, nomes e como transformar as regras do RF em testes estão em `qualidade-codigo/references/testes.md`.

### A regra de dependência é testada

A arquitetura só continua limpa se o build quebrar quando alguém a violar. Mantenha um teste de arquitetura (ArchUnit e/ou Spring Modulith) verificando:
- `..domain..` não depende de `..application..`, `..adapters..`, `org.springframework..`, `jakarta.persistence..`;
- `..application..` não depende de `..adapters..` nem de `jakarta.persistence..`;
- nenhum módulo acessa `domain`, `application` ou `adapters` de outro módulo;
- o backend não depende do módulo `frontend`.

Se o teste reclamar, corrija a dependência. **Não afrouxe a regra para o build passar.**

## Implementando um RF no backend, passo a passo

1. Leia o RF e veja a que módulo ele pertence (tabela de módulos no `docs/README.md`).
2. **Domínio:** modele as entidades e os valores e escreva os testes das regras do RF primeiro.
3. **Aplicação:** crie o caso de uso, os records de entrada e saída e as portas de saída de que ele precisa. Teste com portas em memória, incluindo os perfis sem permissão.
4. **Adaptadores:** migração, entidade JPA, mapeador e implementação da porta. Teste com Testcontainers.
5. **Config:** registre o caso de uso.
6. Exponha o caso de uso para o frontend pela porta de entrada.
7. Rode o portão de qualidade (`qualidade-codigo`) e siga o fluxo de commit e PR (`/commit`, `/git`).

Um exemplo completo de caso de uso, do domínio ao adaptador, está em `references/exemplo-caso-de-uso.md`. Leia-o na primeira vez que criar um caso de uso neste projeto.

## Sinais de que a arquitetura está se perdendo

- Um caso de uso com vários `if` de regra de negócio, enquanto a entidade só tem getters e setters → mova a regra para o domínio.
- A entidade de domínio com `@Entity` → separe a entidade JPA.
- O controller chamando repositório → ele deve chamar um caso de uso.
- Um módulo importando o `domain` de outro → use o contrato público ou um evento.
- Uma classe genérica de “utilidades” crescendo → a lógica tem dono, coloque-a no módulo certo.
- Um caso de uso “Gerenciar…” com dez métodos → quebre em um caso de uso por ação.
