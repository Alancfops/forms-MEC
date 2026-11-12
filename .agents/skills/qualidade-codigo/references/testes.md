# Testes no sistema Fabiana

Teste existe para dar **confiança de que o código faz o que o RF pede e continua fazendo depois de cada mudança**. Um teste que não falharia se a regra quebrasse não serve para nada.

## 1. Que testes escrever

| Tipo | O que cobre | Ferramenta sugerida | Velocidade |
|---|---|---|---|
| **Unitário de domínio** | Regras de negócio puras: NSA automático, numeração de indicadores, visibilidade por etiqueta, cálculo e validação de notas | JUnit 5 + AssertJ, **sem Spring** | Milissegundos |
| **Serviço** | Orquestração, transação, permissão por perfil | JUnit 5 + Mockito (só para dependências externas ao módulo) | Rápido |
| **Web (fatia)** | Controller + template Thymeleaf: status, view, mensagens exatas, fragmentos htmx, CSRF | `@WebMvcTest` + MockMvc + Spring Security Test | Rápido |
| **Persistência** | Consultas, mapeamentos, migrações | `@DataJpaTest` + **Testcontainers (PostgreSQL)** | Segundos |
| **Integração** | Fluxo completo: login → checklist → envio → validação, armazenamento de arquivos | `@SpringBootTest` + Testcontainers (PostgreSQL, MinIO) | Mais lento |
| **Arquitetura** | Fronteiras entre módulos; backend sem depender do frontend | Spring Modulith (`ApplicationModules.verify()`) ou ArchUnit | Rápido |

A base da pirâmide é larga: **a maioria das regras deve ser testada em unitários de domínio**, que são rápidos e precisos. Os testes de integração confirmam que as peças se encaixam, mas não precisam repetir todos os casos.

Use banco real em container, não H2: as diferenças de SQL entre bancos escondem bugs que só aparecem em produção.

## 2. De RF para teste

Cada RF tem campos e “Regras e observações” numeradas. Use-as como roteiro:

1. Para cada regra, escreva pelo menos um teste do caminho feliz e um do caminho que a regra proíbe.
2. Para cada campo obrigatório, teste a ausência.
3. Para cada mensagem entre aspas, verifique **o texto exato**.
4. Para cada perfil citado, teste quem pode e quem **não** pode.

Exemplo, a partir do RF001 (regra 3):

> Após a validação das credenciais, o sistema deve verificar se o e-mail do usuário foi previamente cadastrado na lista de usuários autorizados (RF002). Caso não conste, deve exibir a mensagem: “Você não possui permissão para acessar o sistema” e impedir o acesso.

Casos:
- usuário com credenciais válidas e na whitelist → entra e vai para a Gerência de Checklist;
- usuário com credenciais válidas fora da whitelist → vê exatamente “Você não possui permissão para acessar o sistema” e não recebe sessão.

Cite o RF no teste (`@DisplayName` ou nome da classe) para manter o rastreio requisito ↔ teste.

## 3. Nomes e estrutura

- Classe: `<ClasseTestada>Test` (unitário) e `<Fluxo>IT` (integração, roda no `verify`).
- Método em português, dizendo o comportamento: `deveAplicarNsaQuandoIndicadorForSoParaEad()`, `naoDevePermitirCoordenacaoVerDocumentoDeOutroCurso()`.
- Corpo em **dado / quando / então**:

```java
@Test
@DisplayName("RF007 regra 8 – indicador só para EaD fica NSA em curso presencial")
void deveAplicarNsaQuandoIndicadorForSoParaEad() {
    // dado
    var curso = umCurso().presencial().build();
    var indicador = umIndicador().aplicavelA(Aplicabilidade.A_DISTANCIA).build();

    // quando
    var situacao = indicador.situacaoPara(curso);

    // então
    assertThat(situacao).isEqualTo(SituacaoIndicador.NSA);
}
```

- Um comportamento por teste. Vários `assert` são permitidos se descrevem o mesmo comportamento.
- Para dados, use **builders de teste** (`umCurso()`, `umIndicador()`) em vez de construtores enormes repetidos.

## 4. Permissões: testes obrigatórios

Permissão errada é o bug mais grave deste sistema (documentos de um curso aparecendo para outro). Para cada tela ou operação, teste:
- o perfil que **pode** consegue;
- o perfil que **não pode** recebe acesso negado no backend, mesmo chamando a URL direto;
- a Coordenação **não vê nem envia** nada de curso a que não está vinculada;
- usuário fora da whitelist não entra.

## 5. O que evitar

- **Mock do que é seu**: não faça mock de entidades e regras do próprio módulo, use os objetos reais. Mock serve para fronteiras (outro módulo, sistema acadêmico, relógio).
- **Testar implementação em vez de comportamento**: verificar que um método privado foi chamado quebra a cada refatoração sem pegar bug.
- **Dependência de tempo e ordem**: nada de `Thread.sleep` nem de `LocalDate.now()` direto no domínio. Injete um `Clock`. Cada teste prepara e limpa os próprios dados.
- **Teste sem asserção** ou que só verifica “não lançou exceção” quando há resultado para conferir.
- **`@Disabled` para o CI passar.** Se um teste precisa ser desligado, explique o motivo no código e abra uma issue.

## 6. Cobertura

- Use a cobertura (JaCoCo) para **achar o que não foi testado**, não como meta em si.
- Sugestão inicial: falhar o build abaixo de **80% de linhas no código de domínio e serviços**. Controllers e configuração entram no relatório, mas sem meta.
- Código novo não pode baixar a cobertura do módulo.

## 7. Quando um teste quebra

1. Leia a mensagem: ela diz o esperado e o obtido.
2. Pergunte se é **o código** que está errado ou **o teste** (regra mudou no RF?). Se a regra mudou, atualize o teste junto e cite o RF no commit.
3. Nunca ajuste o valor esperado só para passar sem entender por que mudou.
