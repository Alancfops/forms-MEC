# Clean code no sistema Fabiana

A ideia central: **quem chegar depois tem que entender o código sem perguntar a quem escreveu.** O projeto já troca de responsável, então legibilidade não é luxo.

## 1. Nomes

- **Termos do domínio em português, igual ao glossário** (`docs/glossario.md`): `Periodo`, `Dimensao`, `Indicador`, `Subindicador`, `Anexo`, `EtiquetaDeCurso`, `DocumentoEnviado`, `SituacaoDocumento.DEVOLVIDO_PARA_AJUSTE`. Assim, o código, os RFs e a conversa com a Procuradoria usam as mesmas palavras.
- **Termos técnicos em inglês**, como é o costume no ecossistema Java: `PeriodoRepository`, `IndicadorService`, `ChecklistController`, `findBy…`.
- Sem acento nem `ç` em identificadores (`Dimensao`, não `Dimensão`). Nos textos de tela e nas mensagens, use a forma correta com acento.
- O nome diz a intenção: `aplicarNsaAutomatico(curso)`, não `processa(c)`. Booleanos como pergunta: `isAplicavelAoCurso`, `temEtiqueta`.
- Sem abreviações obscuras nem números mágicos: `QUANTIDADE_MINIMA_DOCUMENTOS = 1`, `PESO_DIMENSAO_CORPO_DOCENTE = 40`.

## 2. Arquitetura: módulos e camadas

A estrutura do backend (Clean Architecture dentro do monolito modular: `domain`, `application`, `adapters`, regra de dependência, comunicação entre módulos) está na skill **`backend`**. Em resumo:
- as regras de negócio ficam no `domain`, em Java puro;
- os casos de uso ficam no `application` e só orquestram;
- banco, arquivos e integrações ficam nos `adapters`;
- os controllers (frontend) chamam casos de uso, nunca repositórios;
- um módulo só usa outro pelo contrato público ou por eventos.

Essas regras são verificadas por testes de arquitetura. Se o teste reclamar, a solução é corrigir a dependência, não liberar a regra.

## 3. Funções e classes

- Uma função faz uma coisa. Se precisa de “e” para descrever, provavelmente são duas.
- Funções curtas (como referência, cabem na tela sem rolar). Poucos parâmetros: mais de 3 pede um objeto (`record NovoIndicador(...)`).
- Retorno cedo em vez de `if` aninhado.
- Sem efeito colateral escondido: um `buscar…` não altera nada.
- Classes pequenas e coesas. Injeção de dependência **pelo construtor** (campos `final`), nunca `@Autowired` em campo: deixa as dependências explícitas e facilita o teste.
- Use `record` para dados imutáveis (comandos, DTOs, valores) e `enum` para conjuntos fechados (perfis, situações, modalidade).
- Não retorne `null`: use `Optional` para “pode não existir” e coleção vazia para “nenhum”.

## 4. Erros e validação

- Valide **na entrada** (formulário e serviço) com Bean Validation (`@NotBlank`, `@Size`…) e mensagens em português.
- Exceções de negócio com nome do problema: `PeriodoJaExisteException`, `AcessoNegadoAoCursoException`. Um handler central transforma cada uma na mensagem de tela do RF.
- As **mensagens de tela dos RFs são texto exato** (ex: “Você não possui permissão para acessar o sistema”). Centralize-as (ex: `messages.properties`) para não haver variação.
- Nunca engula exceção (`catch` vazio). Ou trate, ou deixe subir.
- Logs com contexto e **sem dados sensíveis** (senha, token, conteúdo de documento).

## 5. Segurança no código

O sistema guarda documentos institucionais e tem perfis com acesso diferente. Erros aqui viram vazamento.

- **Toda operação checa permissão no backend**, não só escondendo o botão na tela. A Coordenação só lê e envia documentos dos cursos a que está vinculada (RF002, RF009, RF010, RF017).
- Uploads: valide tipo e tamanho, gere o nome do arquivo no servidor (nunca use o nome enviado como caminho) e guarde no armazenamento de objetos, não no disco da aplicação.
- Consultas sempre parametrizadas (JPA/Spring Data já fazem isso; não concatene SQL).
- Thymeleaf: use `th:text` (escapa HTML). `th:utext` só com conteúdo confiável e com justificativa no código.
- Formulários com proteção CSRF ligada (padrão do Spring Security; com htmx, envie o token no cabeçalho).

## 6. Thymeleaf e htmx

Os padrões de tela (paleta, acessibilidade WCAG 2 AA, mobile first, fragmentos, receitas htmx) estão na skill **`frontend`**. Em resumo: nenhum template com regra de negócio, `th:text` por padrão e nenhuma regra de negócio no JavaScript.

## 7. Banco de dados e migrações

- Toda mudança de esquema é uma migração versionada nova (ex: Flyway `V3__cria_tabela_anexo.sql`).
- **Nunca edite uma migração que já foi para a `develop`**: outros ambientes já a aplicaram. Crie uma nova.
- Cuidado com consultas N+1 em listas (checklist com dimensões → indicadores → anexos): use `JOIN FETCH` ou projeções.

## 8. Comentários

- O código explica o *quê*; o comentário explica o *porquê* que o código não mostra. Por exemplo: “Peso 40 conforme o instrumento do INEP 2017 (D2 – Corpo Docente)”.
- Referencie o requisito quando a regra vem dele: `// RF007, regra 8: NSA automático pela aplicabilidade`.
- Sem código comentado: o histórico está no Git.
- Sem `TODO` órfão: ou vira issue, ou tem dono e motivo.
