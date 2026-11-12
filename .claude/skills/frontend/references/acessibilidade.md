# Acessibilidade – WCAG 2, nível AA

Meta do projeto: **WCAG 2.2, nível AA** (que inclui os critérios da 2.0 e da 2.1). Abaixo, os critérios que mais aparecem nas telas do sistema Fabiana, com o que fazer em cada um. O número entre parênteses é o critério da WCAG.

## 1. Perceptível

**Contraste (1.4.3, 1.4.11)**
- Texto normal: no mínimo **4,5:1**. Texto grande (a partir de 24px, ou 18,66px em negrito): **3:1**.
- Bordas de campos, ícones que transmitem informação e anel de foco: **3:1** com o que está em volta.
- Use as combinações anotadas em `assets/tokens.css`. Para uma combinação nova, calcule o contraste antes. Se não passar, ajustar o tom é **mudança de cor**: pergunte ao usuário (SKILL.md, “Cores”).

**Cor não é a única pista (1.4.1)**
- A situação do documento ou do indicador sempre aparece com **ícone + texto** (“✓ Validado”, “✕ Devolvido para ajuste”). As cores semafóricas (verde, amarelo, vermelho) ajudam, mas quem não distingue verde de vermelho precisa entender só pelo ícone e pelo texto.
- Links no meio do texto são **sublinhados**.
- Campo com erro: borda + ícone + mensagem em texto, não só a borda colorida.

**Textos alternativos (1.1.1)**
- Imagem com informação → `alt` descrevendo a informação. Imagem decorativa → `alt=""`.
- Botão só com ícone (editar, excluir, mover) → texto acessível: `aria-label="Excluir indicador 1.3"`. Inclua o nome do item, porque “Excluir” repetido dez vezes na lista não ajuda quem usa leitor de tela.

**Estrutura (1.3.1, 1.3.2)**
- Títulos em ordem (`h1` único por página, depois `h2`, `h3`, sem pular nível).
- Tabelas de dados com `<caption>`, `<th scope="col">` e `<th scope="row">` quando houver.
- Grupos de campos relacionados em `<fieldset>` com `<legend>` (ex: opções de aplicabilidade do indicador).
- No celular, a lista de cards precisa manter os mesmos rótulos que a tabela tinha (ex: “Situação: Validado”).

**Redimensionar e refluir (1.4.4, 1.4.10, 1.4.12)**
- O texto aumenta até 200% sem perder conteúdo, e a tela funciona com 320px de largura sem rolagem horizontal da página.
- Não fixe altura de caixas com texto, porque o texto aumentado transborda.

## 2. Operável

**Teclado (2.1.1, 2.1.2)**
- Tudo que se faz com o mouse se faz com o teclado: abrir janela, escolher etiqueta, reordenar, enviar arquivo, trocar de aba.
- Nenhuma armadilha: o foco sempre consegue sair (exceto dentro da janela modal aberta, que fecha com Esc).

**Foco visível e não escondido (2.4.7, 2.4.11)**
- Use o anel de foco dos tokens (`--foco-anel` em fundo claro, `--foco-anel-escuro` no cabeçalho azul). **Nunca** `outline: none` sem substituto.
- Cabeçalho fixo ou barra fixa não pode cobrir o elemento focado (use `scroll-padding-top`).

**Ordem e navegação (2.4.1, 2.4.3, 2.4.2, 2.4.6)**
- O link “Pular para o conteúdo” é o primeiro elemento da página.
- A ordem de foco segue a ordem visual.
- Cada página tem um `<title>` próprio (“Checklist 2026.1 – Fabiana”).
- Rótulos e títulos descrevem o propósito.

**Arrastar (2.5.7)**
- A reordenação de indicadores (RF007) **não pode depender só de arrastar**: tenha botões “Mover para cima” e “Mover para baixo” (ou campo de posição). Arrastar pode existir como atalho.

**Tamanho do alvo (2.5.8)**
- A WCAG pede no mínimo 24×24px. Neste projeto, o padrão é **44×44px** (`--alvo-toque`), por causa do uso no celular.

**Tempo (2.2.1)**
- Se a sessão expirar, avise antes e permita continuar. Não perca o formulário preenchido sem aviso.

**Movimento (2.3.3)**
- Respeite `prefers-reduced-motion` (já está no `tokens.css`).

## 3. Compreensível

**Idioma (3.1.1)**
- `<html lang="pt-BR">`.

**Rótulos e instruções (3.3.2)**
- Todo campo tem `<label for>` visível. O placeholder **não** substitui o rótulo.
- Campo obrigatório: escreva “(obrigatório)” no rótulo, e não só um asterisco, e use o atributo `required`.
- Formato esperado no rótulo ou na dica ligada por `aria-describedby`. Ex: Período, “formato AAAA.S, ex: 2026.1” (RF004).

**Erros (3.3.1, 3.3.3, 3.3.4)**
- A mensagem de erro diz **qual campo** e **como corrigir**, em texto, ligada ao campo (`aria-describedby` + `aria-invalid="true"`).
- Com vários erros, um resumo no topo do formulário, com links para os campos, e o foco vai para ele.
- **Exclusões e ações que não se desfazem pedem confirmação** (todos os RFs pedem tela de confirmação antes de excluir). A confirmação é uma janela do próprio sistema, não o `confirm()` do navegador.

**Consistência (3.2.3, 3.2.4, 3.2.6)**
- O menu, o cabeçalho e o lugar da ajuda/contato são os mesmos em todas as telas.
- O mesmo ícone e o mesmo texto significam a mesma coisa em todo lugar.

**Sem mudança inesperada (3.2.1, 3.2.2)**
- Escolher um item numa lista não envia o formulário nem troca de página sozinho. A ação acontece no botão.
- Exceção: as abas de período (RF004) carregam o checklist ao clicar, porque esse é o comportamento esperado de uma aba.

## 4. Robusto

**Nome, função e estado (4.1.2)**
- Componentes personalizados informam o estado: `aria-expanded` (menu, acordeão), `aria-selected` (abas), `aria-pressed` (botão liga/desliga), `aria-current="page"` (item de menu atual).

**Mensagens de status (4.1.3)**
- Avisos que aparecem sem mover o foco (“Documento enviado”, “Indicador reordenado”) entram numa **região viva**: `<div role="status" aria-live="polite">` no layout, que o htmx atualiza. Erros urgentes usam `role="alert"`.

## Como verificar antes do PR

1. **Só teclado:** percorra a tela inteira com Tab, Shift+Tab, Enter, Espaço e Esc.
2. **Largura de 320px** (ferramentas do navegador) e **zoom de 200%**.
3. **Ferramenta automática:** axe DevTools, Lighthouse ou WAVE. Ela pega cerca de um terço dos problemas e não substitui os passos 1 e 2.
4. **Leitor de tela,** pelo menos uma vez por tela nova: NVDA no Windows, Orca no Linux ou TalkBack no Android. Veja se os rótulos, as situações e os avisos são lidos.
5. Se o projeto adotar testes de interface (ex: Playwright), inclua a verificação automática com axe-core nas telas principais.
