---
trigger: glob
globs: "backend/**/*.java, backend/**/*.sql, **/pom.xml"
description: "Regra de dependência da Clean Architecture e qualidade no backend Java."
---

# Backend: regras que não se negociam

Siga a skill `backend` (`.agents/skills/backend/SKILL.md`) e a skill `qualidade-codigo`. Resumo do que é bloqueante:

- **Dependências só apontam para dentro:** `adapters → application → domain`.
  - O `domain` é Java puro: nada de Spring, JPA ou `LocalDate.now()` direto.
  - O `application` não usa adaptadores nem JPA; a única anotação de framework permitida é `@Transactional`.
- **Regra de negócio fica no domínio**, e os casos de uso só orquestram.
- **Permissão é verificada no caso de uso**, nunca só na tela. A Coordenação só acessa os seus cursos.
- **Um módulo só usa outro pelo contrato público ou por eventos.** Não há tabelas nem entidades compartilhadas.
- **Entidade JPA separada da entidade de domínio**, com um mapeador entre elas.
- **Migração já mergeada nunca é editada**: crie uma nova.
- **Toda regra do RF tem teste**, incluindo o perfil sem acesso. Não desligue testes para o build passar.
