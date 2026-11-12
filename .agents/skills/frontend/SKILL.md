---
name: frontend
description: Como construir as telas do sistema Fabiana com Thymeleaf + htmx — cores do projeto branco/azul/amarelo e cores semafóricas (verde/amarelo/vermelho) para estados (tokens fixos; mudar cor exige perguntar ao usuário e explicar o porquê), acessibilidade WCAG 2 nível AA, mobile first, estrutura de templates e fragmentos, padrões htmx (janelas, formulários, confirmação de exclusão, reordenação, etiquetas) e controllers como adaptadores dos casos de uso. Use SEMPRE que for criar ou alterar tela, template, fragmento, CSS, JavaScript, controller web ou interação htmx deste projeto, implementar a parte visual de um RF ou revisar acessibilidade e responsividade — mesmo que o pedido seja só "faz a tela do RF006", "muda esse botão" ou "ajusta no celular".
---

# Frontend – Sistema Fabiana

As telas são feitas com **Thymeleaf + htmx**, no módulo `frontend`. O servidor gera o HTML e o htmx troca só o pedaço da tela que mudou. Três compromissos guiam todas as decisões:

1. **Cores do projeto: branco, azul e amarelo**, mais as **semafóricas** (verde, amarelo e vermelho) só para estados. Tudo vem dos tokens em `assets/tokens.css`.
2. **Acessibilidade WCAG 2, nível AA.** Pró-Reitores, Procuradoria e coordenações têm idades, aparelhos e necessidades diferentes. Uma tela que não funciona com teclado, leitor de tela ou zoom deixa alguém de fora.
3. **Mobile first.** O estilo base é o do celular, e a tela cresce para tablet e desktop. Coordenadores vão consultar e enviar documentos do celular.

Os prints do Miro (`docs/fontes/miro/`) **são só exemplos do fluxo, não o design**. O que define cada tela é o RF: campos, regras e mensagens.

## Arquivos desta skill

| Arquivo | Leia quando |
|---|---|
| `assets/tokens.css` | Antes de escrever qualquer CSS. Copie para `frontend/src/main/resources/static/css/tokens.css` na primeira vez |
| `references/acessibilidade.md` | Ao criar ou revisar qualquer tela: checklist WCAG 2 AA aplicado ao projeto |
| `references/htmx-padroes.md` | Ao criar interação: janela, formulário com erro, exclusão com confirmação, reordenação, etiquetas, abas, envio de arquivo |

## Cores

São duas famílias de cor. Todos os tons estão em `assets/tokens.css`, com o contraste de cada combinação anotado.

**1. Cores do projeto (identidade): branco, azul e amarelo**, em vários tons.
- **Use os papéis, não a cor crua:** `var(--cor-primaria)`, `var(--cor-texto)`, `var(--cor-destaque)`. Assim, um ajuste de tom muda o sistema todo de forma consistente.
- **Azul** é a cor principal: texto, títulos, botões, links, cabeçalho.
- **Amarelo** é o destaque: chips de etiqueta de curso (“Áreas”), item ou aba selecionada. Amarelo claro **nunca** leva texto branco nem fica como texto sobre branco, porque o contraste não passa. Use sempre texto azul-escuro sobre amarelo.
- **Branco** é o fundo. As superfícies (cards, cabeçalhos de tabela) usam azul bem claro.

**2. Cores semafóricas (estado):** verde = sucesso, amarelo = atenção, vermelho = erro ou problema. Elas **só comunicam estado**, nunca são usadas como decoração ou identidade.

| Estado | Cor | Exemplos |
|---|---|---|
| Sucesso | Verde | ✓ Validado, indicador Concluído, “salvo com sucesso” |
| Atenção | Amarelo | ⏳ Enviado (aguardando revisão), Em andamento, avisos |
| Erro / problema | Vermelho | ✕ Devolvido para ajuste, erro de formulário, nota em diligência (0 a 2, RF013) |
| Informação | Azul | ℹ avisos neutros |
| Neutro | Branco com contorno | Pendente, NSA |

A cor **nunca é a única pista**: todo estado aparece com **ícone + texto**. Quem não distingue verde de vermelho precisa entender do mesmo jeito (WCAG 1.4.1).

### Mudar uma cor: pergunte antes

Usar os tokens existentes é livre. **Alterar o valor de um token, criar uma cor nova, usar cor fora das duas famílias** (ex: roxo, laranja, cinza neutro) **ou usar uma cor semafórica como decoração** **exige perguntar ao usuário antes**, explicando:
- **o que** quer mudar (token, valor atual → valor proposto);
- **por quê**. Por exemplo, o contraste não passa na WCAG, falta uma cor para um estado novo ou um ícone precisa de mais destaque;
- **o impacto**: quais telas e componentes mudam, e o novo contraste calculado.

Só altere depois do “sim”. Se ele aprovar, atualize `tokens.css` com o contraste anotado e registre a mudança na seção de arquitetura do `docs/README.md`.

## Mobile first

- **Estilo base para o celular** (a partir de 320px de largura). Use `@media (min-width: 40rem)` para tablet e `@media (min-width: 64rem)` para desktop, **nunca** `max-width` para “consertar” o celular depois.
- **Nada de rolagem horizontal da página** em 320px (WCAG 1.4.10). Tabelas largas (checklist, documentos, histórico) viram **lista de cards** no celular e tabela a partir do tablet. Outra opção é envolver a tabela num contêiner com rolagem própria e rótulo.
- **Alvos de toque com no mínimo 44×44px** (`--alvo-toque`), com espaço entre eles.
- **Navegação:** no celular, o menu fica recolhido num botão “Menu” (com `aria-expanded`). As abas de período (RF004) rolam na horizontal dentro do próprio contêiner.
- **Formulários:** um campo por linha no celular, rótulo acima do campo e `type`/`inputmode`/`autocomplete` corretos (e-mail, número).
- **Janelas** ocupam a tela inteira no celular e viram uma caixa central a partir do tablet.
- **Unidades relativas** (`rem`, `%`, `ch`) para o texto aumentar até 200% sem quebrar (WCAG 1.4.4).
- **Teste em largura de 320px e com zoom de 200%** antes de dar a tela como pronta.

## Estrutura do módulo frontend

```
frontend/src/main/
├── java/br/cesmac/fabiana/web/
│   ├── acesso/        LoginController, UsuariosController
│   ├── estrutura/     PeriodosController, ChecklistController, IndicadoresController…
│   ├── documentos/
│   ├── avaliacoes/
│   └── comum/         tratamento de erros, CSRF para htmx, dados do layout (usuário logado, menu por perfil)
└── resources/
    ├── templates/
    │   ├── layout/base.html          estrutura da página: <html lang="pt-BR">, cabeçalho, menu, <main>, região de avisos
    │   ├── fragmentos/               peças reutilizáveis: campo de formulário, janela, chip de etiqueta, situação, paginação
    │   └── <modulo>/                 páginas e fragmentos de cada módulo (ex: estrutura/checklist.html)
    ├── static/
    │   ├── css/tokens.css            (de assets/tokens.css)
    │   ├── css/app.css               componentes, sempre usando os tokens
    │   └── js/                       htmx (cópia local, versão fixa) e pequenos scripts de interface
    └── messages.properties           textos e mensagens de tela (as dos RFs com o texto exato)
```

### Controllers são adaptadores

Seguindo a Clean Architecture (skill `backend`):
- **Um controller chama casos de uso** pelas portas de entrada (records de comando e resultado). Ele nunca acessa repositório, entidade JPA ou regra de negócio.
- **O controller só traduz:** requisição → comando, resultado → modelo da view, exceção de domínio → mensagem na tela.
- **Requisição htmx** (cabeçalho `HX-Request`): devolva **só o fragmento** (`"estrutura/checklist :: lista-indicadores"`). Requisição normal: devolva a página inteira.
- **Permissão** é verificada no caso de uso, no backend. Esconder um botão por perfil (`th:if="${podeEditar}"`) é só conforto visual, não proteção.

## Regras dos templates

- **Sem regra de negócio no template.** Se precisa de um `th:if` complicado, calcule no controller (ex: `podeEditar`, `mostrarDocumentoExemplo`) e passe pronto.
- **`th:text` sempre.** `th:utext` só com conteúdo confiável e justificativa num comentário.
- **Textos de tela em `messages.properties`** (`#{periodo.erro.jaExiste}`). As mensagens que estão entre aspas nos RFs são **texto exato**.
- **Um fragmento por peça reutilizável:** campo com rótulo e erro, janela, chip de etiqueta, selo de situação, confirmação de exclusão. As telas montam peças; não copie HTML entre telas.
- **HTML semântico primeiro** (`<button>`, `<a>`, `<nav>`, `<main>`, `<table>`, `<dialog>`, `<label>`). ARIA só quando o HTML não resolve.
- **htmx em arquivo local com versão fixa** (não por CDN), para o sistema não depender de serviço externo nem mudar de versão sozinho.
- **JavaScript próprio só para comportamento de interface** (abrir menu, foco em janela). Nenhuma regra de negócio no navegador.

## Implementando a tela de um RF

1. Leia o RF: os campos (obrigatório, opcional, automático), as regras e as mensagens.
2. Monte a página no celular primeiro, com os fragmentos existentes e os tokens.
3. Ligue as interações com os padrões de `references/htmx-padroes.md`.
4. Passe o checklist de `references/acessibilidade.md`: teclado, leitor de tela, contraste, 320px, zoom de 200%.
5. Teste o controller e o template (`@WebMvcTest`): status, fragmento devolvido, mensagens exatas, perfil sem acesso. Ver `qualidade-codigo/references/testes.md`.
6. Portão de qualidade (`qualidade-codigo`) e fluxo de commit e PR (`/commit`, `/git`).
