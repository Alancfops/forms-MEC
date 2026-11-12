# Exemplo completo: criar período (RF004)

Mostra um caso de uso atravessando todas as camadas. Os nomes e as regras vêm do RF004 (“Usar modelo do ano anterior” / “Criar novo modelo”). Ajuste ao que o RF diz de fato e à stack em uso: o exemplo supõe Spring Boot + JPA.

> Regras usadas no exemplo:
> - não pode haver dois períodos com o mesmo código, ex: “2025.1” (regra 3);
> - o código segue o formato AAAA.S, com semestre 1 ou 2 (regra 2);
> - “Usar modelo do ano anterior” copia dimensões, indicadores, subindicadores, anexos e etiquetas do período escolhido, **sem os documentos enviados** (regra 4);
> - “Criar novo modelo” começa sem nenhuma dimensão (regra 6);
> - só o perfil Administrador cria períodos (perfis do RF002).

## 1. domain

```java
package br.cesmac.fabiana.estrutura.domain;

public record CodigoPeriodo(String valor) {
    private static final Pattern FORMATO = Pattern.compile("\\d{4}\\.[12]");

    public CodigoPeriodo {
        if (valor == null || !FORMATO.matcher(valor).matches()) {
            throw new CodigoPeriodoInvalidoException(valor);
        }
    }
}
```

```java
package br.cesmac.fabiana.estrutura.domain;

public class Periodo {
    private final PeriodoId id;
    private final CodigoPeriodo codigo;
    private final List<Dimensao> dimensoes;

    private Periodo(PeriodoId id, CodigoPeriodo codigo, List<Dimensao> dimensoes) {
        this.id = id;
        this.codigo = codigo;
        this.dimensoes = new ArrayList<>(dimensoes);
    }

    public static Periodo novoVazio(PeriodoId id, CodigoPeriodo codigo) {
        return new Periodo(id, codigo, List.of());
    }

    public static Periodo copiandoChecklistDe(PeriodoId id, CodigoPeriodo codigo, Periodo anterior) {
        return new Periodo(id, codigo, anterior.dimensoes.stream().map(Dimensao::copia).toList());
    }

    public List<Dimensao> dimensoes() {
        return List.copyOf(dimensoes);
    }
    // ...
}
```

Note: sem anotação de framework, regra de cópia dentro da entidade, lista protegida contra alteração de fora.

## 2. application

```java
package br.cesmac.fabiana.estrutura.application.port.in;

public record CriarPeriodoComando(String codigo, Optional<String> codigoPeriodoModelo) {}
```

```java
package br.cesmac.fabiana.estrutura.application.port.out;

public interface PeriodoRepository {
    boolean existeComCodigo(CodigoPeriodo codigo);
    Optional<Periodo> buscarPorCodigo(CodigoPeriodo codigo);
    PeriodoId proximoId();
    void salvar(Periodo periodo);
}
```

```java
package br.cesmac.fabiana.estrutura.application;

public class CriarPeriodo {
    private final PeriodoRepository periodos;
    private final UsuarioAtual usuarioAtual;

    public CriarPeriodo(PeriodoRepository periodos, UsuarioAtual usuarioAtual) {
        this.periodos = periodos;
        this.usuarioAtual = usuarioAtual;
    }

    @Transactional
    public PeriodoId executar(CriarPeriodoComando comando) {
        usuarioAtual.exigirPerfil(Perfil.ADMINISTRADOR);

        var codigo = new CodigoPeriodo(comando.codigo());
        if (periodos.existeComCodigo(codigo)) {
            throw new PeriodoJaExisteException(codigo);
        }

        var periodo = comando.codigoPeriodoModelo()
                .map(CodigoPeriodo::new)
                .map(modelo -> periodos.buscarPorCodigo(modelo)
                        .orElseThrow(() -> new PeriodoNaoEncontradoException(modelo)))
                .map(anterior -> Periodo.copiandoChecklistDe(periodos.proximoId(), codigo, anterior))
                .orElseGet(() -> Periodo.novoVazio(periodos.proximoId(), codigo));

        periodos.salvar(periodo);
        return periodo.id();
    }
}
```

O caso de uso só orquestra: permissão → validação de unicidade → domínio decide como criar → salva.

## 3. adapters/persistence

```java
package br.cesmac.fabiana.estrutura.adapters.persistence;

@Entity
@Table(name = "estrutura_periodo")
class PeriodoEntity {
    @Id UUID id;
    @Column(nullable = false, unique = true) String codigo;
    @OneToMany(mappedBy = "periodo", cascade = CascadeType.ALL, orphanRemoval = true)
    List<DimensaoEntity> dimensoes = new ArrayList<>();
    // construtor protegido para o JPA
}
```

```java
package br.cesmac.fabiana.estrutura.adapters.persistence;

@Repository
class PeriodoRepositoryJpa implements PeriodoRepository {
    private final PeriodoSpringData springData;
    private final PeriodoMapper mapper;

    // construtor

    @Override
    public boolean existeComCodigo(CodigoPeriodo codigo) {
        return springData.existsByCodigo(codigo.valor());
    }

    @Override
    public void salvar(Periodo periodo) {
        springData.save(mapper.paraEntidade(periodo));
    }
    // ...
}
```

As classes do adaptador são package-private: ninguém de fora precisa conhecê-las, só a porta.

Migração correspondente: `V2__cria_estrutura_periodo.sql`.

## 4. config

```java
package br.cesmac.fabiana.estrutura.config;

@Configuration
class EstruturaConfig {
    @Bean
    CriarPeriodo criarPeriodo(PeriodoRepository periodos, UsuarioAtual usuarioAtual) {
        return new CriarPeriodo(periodos, usuarioAtual);
    }
}
```

## 5. Testes

```java
class PeriodoTest {
    @Test
    @DisplayName("RF004 – usar modelo do ano anterior copia as dimensões")
    void deveCopiarDimensoesDoPeriodoAnterior() {
        var anterior = umPeriodo().comDimensoes(3).build();

        var novo = Periodo.copiandoChecklistDe(PeriodoId.novo(), new CodigoPeriodo("2026.1"), anterior);

        assertThat(novo.dimensoes()).hasSize(3);
    }
}
```

```java
class CriarPeriodoTest {
    private final PeriodoRepositoryEmMemoria periodos = new PeriodoRepositoryEmMemoria();

    @Test
    @DisplayName("RF004 – coordenação não cria período")
    void naoDevePermitirCoordenacaoCriarPeriodo() {
        var criarPeriodo = new CriarPeriodo(periodos, UsuarioAtualFalso.coordenacao());

        assertThatThrownBy(() -> criarPeriodo.executar(new CriarPeriodoComando("2026.1", Optional.empty())))
                .isInstanceOf(AcessoNegadoException.class);
    }

    @Test
    @DisplayName("RF004 – não permite dois períodos com o mesmo código")
    void naoDeveCriarPeriodoDuplicado() { /* ... */ }
}
```

O adaptador (`PeriodoRepositoryJpa`) ganha um teste de integração com PostgreSQL via Testcontainers, cobrindo o mapeamento de ida e volta.
