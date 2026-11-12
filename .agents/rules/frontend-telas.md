---
trigger: glob
globs: "frontend/**/*.html, frontend/**/*.css, frontend/**/*.js, frontend/**/*.java"
description: "Cores, acessibilidade WCAG 2 AA e mobile first nas telas Thymeleaf + htmx."
---

# Frontend: regras que não se negociam

Siga a skill `frontend` (`.agents/skills/frontend/SKILL.md`, com `assets/tokens.css` e `references/`). Resumo:

- **Cores:**
  - cores do projeto (identidade): **branco, azul e amarelo**;
  - cores **semafóricas** (verde = sucesso, amarelo = atenção, vermelho = erro) **só para estado**;
  - sempre pelos tokens de `tokens.css`.
- **Mudar uma cor exige perguntar ao usuário antes.** Isso vale para alterar um token, criar uma cor, usar cor fora dessas famílias ou usar uma cor semafórica como decoração. Na pergunta, explique o que muda, por quê, o impacto e o contraste.
- **WCAG 2 nível AA:**
  - contraste de 4,5:1 (texto) e 3:1 (componentes e foco);
  - tudo funciona pelo teclado, com o foco visível;
  - todo campo tem rótulo;
  - estado nunca é indicado só pela cor (sempre ícone + texto);
  - reordenação não depende só de arrastar;
  - confirmação de exclusão é uma janela do sistema, não o `confirm()` do navegador.
- **Mobile first:**
  - o estilo base é o do celular, e só cresce com `min-width`;
  - nada de rolagem horizontal da página em 320px;
  - alvos de toque com no mínimo 44px.
- **Controller é adaptador:** chama casos de uso e nunca repositório. Não há regra de negócio no template nem no JavaScript, e é `th:text` por padrão.
- **As mensagens dos RFs são texto exato.**
