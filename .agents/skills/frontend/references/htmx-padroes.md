# Padrões htmx do sistema Fabiana

Receitas para as interações que os RFs pedem. Elas seguem a regra: **o servidor decide e gera o HTML; o htmx só busca e troca o pedaço certo.** Os exemplos supõem Spring MVC + Thymeleaf. Ajuste ao que o projeto usa.

## Configuração base (layout/base.html)

```html
<!DOCTYPE html>
<html lang="pt-BR" xmlns:th="http://www.thymeleaf.org">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title th:text="${tituloPagina} + ' – Fabiana'">Fabiana</title>
  <meta name="_csrf" th:content="${_csrf.token}">
  <meta name="_csrf_header" th:content="${_csrf.headerName}">
  <link rel="stylesheet" th:href="@{/css/tokens.css}">
  <link rel="stylesheet" th:href="@{/css/app.css}">
  <script th:src="@{/js/htmx.min.js}" defer></script>
  <script th:src="@{/js/app.js}" defer></script>
</head>
<body>
  <a class="pular-conteudo" href="#conteudo">Pular para o conteúdo</a>
  <header th:replace="~{fragmentos/cabecalho :: cabecalho}"></header>
  <main id="conteudo" tabindex="-1" th:insert="~{::conteudo}"></main>
  <div id="avisos" role="status" aria-live="polite"></div>
  <dialog id="janela" aria-labelledby="janela-titulo"></dialog>
</body>
</html>
```

`app.js` envia o token CSRF em toda requisição htmx:

```js
document.addEventListener("htmx:configRequest", (e) => {
  const token = document.querySelector('meta[name="_csrf"]').content;
  const header = document.querySelector('meta[name="_csrf_header"]').content;
  e.detail.headers[header] = token;
});
```

## Página inteira × fragmento

```java
@GetMapping("/periodos/{codigo}/checklist")
String checklist(@PathVariable String codigo, Model model,
                 @RequestHeader(value = "HX-Request", required = false) String htmx) {
    model.addAttribute("checklist", consultarChecklist.executar(new ConsultarChecklistComando(codigo)));
    return htmx != null ? "estrutura/checklist :: conteudo-checklist" : "estrutura/checklist";
}
```

## Abas de período (RF004)

```html
<nav aria-label="Períodos">
  <ul class="abas" role="tablist">
    <li th:each="p : ${periodos}">
      <a role="tab"
         th:href="@{/periodos/{c}/checklist(c=${p.codigo})}"
         th:attr="aria-selected=${p.codigo == periodoAtual},
                  hx-get=@{/periodos/{c}/checklist(c=${p.codigo})}"
         th:text="${p.codigo}"
         hx-target="#conteudo-checklist" hx-push-url="true">2026.1</a>
    </li>
  </ul>
</nav>
```

O `href` faz o link funcionar sem JavaScript. O `hx-push-url` mantém o botão “voltar” do navegador funcionando.

## Janela de criação (RF006, RF007)

Botão que abre:

```html
<button type="button" class="botao-primario"
        hx-get="/dimensoes/nova" hx-target="#janela" hx-swap="innerHTML">
  Nova dimensão
</button>
```

Fragmento devolvido (`fragmentos/janela.html` + conteúdo):

```html
<div th:fragment="janela-dimensao">
  <h2 id="janela-titulo">Nova dimensão</h2>
  <form hx-post="/dimensoes" hx-target="#janela" hx-swap="innerHTML">
    <!-- campos com o fragmento de campo -->
    <div class="acoes">
      <button type="button" class="botao-secundario" data-fechar-janela>Cancelar</button>
      <button type="submit" class="botao-primario">Confirmar</button>
    </div>
  </form>
</div>
```

`app.js` cuida do comportamento acessível da janela:

```js
const janela = document.getElementById("janela");
let origemDoFoco = null;

document.body.addEventListener("htmx:afterSwap", (e) => {
  if (e.detail.target === janela && !janela.open) {
    origemDoFoco = document.activeElement;
    janela.showModal();                          // <dialog> nativo: prende o foco e fecha com Esc
    janela.querySelector("input, select, textarea, button")?.focus();
  }
});
janela.addEventListener("close", () => { janela.innerHTML = ""; origemDoFoco?.focus(); });
document.addEventListener("click", (e) => {
  if (e.target.matches("[data-fechar-janela]")) janela.close();
});
document.body.addEventListener("fecharJanela", () => janela.close());
```

Ao salvar com sucesso, o servidor responde com o cabeçalho `HX-Trigger: {"fecharJanela": true, "listaAtualizada": true}`, e a lista escuta o evento para se recarregar (`hx-trigger="listaAtualizada from:body"`).

## Formulário com erro de validação

- Em caso de erro, devolva **o mesmo fragmento do formulário**, com os valores digitados e as mensagens, e status **422**. Configure o htmx para fazer a troca também nesse status:

```html
<meta name="htmx-config" content='{"responseHandling":[{"code":"204","swap":false},{"code":"[23]..","swap":true},{"code":"422","swap":true},{"code":"[45]..","swap":false,"error":true}]}'>
```

- Fragmento de campo (`fragmentos/campos.html`):

```html
<div th:fragment="texto(nome, rotulo, dica, obrigatorio)" class="campo"
     th:classappend="${#fields.hasErrors(nome)} ? 'campo-com-erro'">
  <label th:for="${nome}">
    <span th:text="${rotulo}">Período</span>
    <span th:if="${obrigatorio}" class="obrigatorio">(obrigatório)</span>
  </label>
  <p th:if="${dica}" th:id="${nome} + '-dica'" class="dica" th:text="${dica}"></p>
  <input type="text" th:field="*{__${nome}__}" th:required="${obrigatorio}"
         th:attr="aria-describedby=${nome} + '-dica ' + ${nome} + '-erro',
                  aria-invalid=${#fields.hasErrors(nome)}">
  <p th:if="${#fields.hasErrors(nome)}" th:id="${nome} + '-erro'" class="erro">
    <span aria-hidden="true">⚠</span> <span th:errors="*{__${nome}__}"></span>
  </p>
</div>
```

- Depois da troca, mova o foco para o primeiro campo com erro (ou para o resumo de erros).

## Exclusão com confirmação

Todos os RFs pedem uma tela de confirmação antes de excluir. Não use `hx-confirm` (ele abre o `confirm()` do navegador): abra a janela do sistema.

```html
<button type="button" class="botao-icone"
        th:attr="aria-label='Excluir indicador ' + ${i.numero}, hx-get=@{/indicadores/{id}/excluir(id=${i.id})}"
        hx-target="#janela">
  <svg aria-hidden="true" focusable="false">…</svg>
</button>
```

A janela devolvida explica **o que será excluído e as consequências** (ex: “Os subindicadores e anexos deste indicador também serão excluídos”), com “Cancelar” (foco inicial) e “Excluir”.

## Reordenação de indicadores (RF007)

- **Botões “Mover para cima/para baixo”** em cada item, obrigatórios porque arrastar não pode ser a única forma (WCAG 2.5.7). Arrastar (ex: SortableJS) pode existir como atalho.
- A nova ordem fica **pendente** até o usuário confirmar, como o RF exige: mostre a numeração proposta e um botão “Confirmar nova numeração”.
- Depois de mover, mantenha o foco no botão do item movido e anuncie na região `#avisos`: “Indicador 1.3 movido para a posição 2”.

## Etiquetas de curso / “Áreas” (RF009)

- Os chips usam `--cor-destaque` (amarelo) com texto `--cor-destaque-texto` (azul-escuro).
- Sem etiqueta, o campo mostra “todos”.
- Para adicionar, use um `<select>` ou uma lista de checkboxes (`<fieldset>` com `<legend>Áreas</legend>`), e não um componente de digitação livre sem rótulo.
- Cada chip removível é um `<button>` com `aria-label="Remover etiqueta Medicina"`.

## Envio de arquivo (RF010)

```html
<form hx-post="/anexos/16/documentos" hx-encoding="multipart/form-data" hx-target="#documentos-anexo-16">
  <label for="arquivo">Documento (obrigatório)</label>
  <p id="arquivo-dica" class="dica">Formatos e tamanho máximo: …</p>
  <input type="file" id="arquivo" name="arquivo" required aria-describedby="arquivo-dica">
  <progress id="progresso" value="0" max="100" hidden></progress>
  <button type="submit" class="botao-primario">Enviar</button>
</form>
```

Os formatos e o tamanho máximo ainda são a pendência 6: mostre o texto vindo da configuração, não fixo no template. Use o evento `htmx:xhr:progress` para atualizar o `<progress>` e, no fim, anuncie o resultado na região `#avisos`.

## Indicador de carregamento

Use `hx-indicator` com um elemento que tenha texto (“Carregando…”) e, durante a requisição, `hx-disabled-elt="this"` no botão, para evitar envio duplicado.
