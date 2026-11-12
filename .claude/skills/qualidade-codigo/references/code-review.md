# Code review no sistema Fabiana

A revisão existe para **pegar o que o autor não viu**: o requisito mal entendido, a permissão esquecida, o teste que não testa nada. Ela também espalha o conhecimento do código pela equipe. O foco é em bugs e riscos, não em gosto pessoal: estilo, o formatador e o lint já resolvem.

## 1. Como obter o PR

```bash
gh pr view <número>               # título, descrição, RFs citados
gh pr diff <número>               # o diff
gh pr checks <número>             # estado do CI
gh pr checkout <número>           # para rodar localmente, se precisar
```

Leia primeiro a descrição e o RF citado (`docs/requisitos/`). Sem saber o que o PR deveria fazer, não dá para dizer se ele faz.

## 2. Roteiro de revisão

Vá na ordem: os primeiros itens são os que mais custam se passarem.

**1. Faz o que o RF pede?**
- Todas as regras do RF citado foram tratadas? Alguma foi interpretada de outro jeito?
- As mensagens de tela batem com o texto exato do RF?
- Faz algo que o RF não pede? Escopo extra pede outro PR ou uma conversa.

**2. Segurança e permissões**
- Cada operação nova checa perfil e vínculo com o curso **no backend**?
- Upload: tipo, tamanho e nome gerado no servidor?
- Algum `th:utext`, SQL concatenado, dado sensível em log, segredo no código?

**3. Testes**
- Cada regra nova tem teste? Inclui o caminho proibido e o perfil sem acesso?
- Os testes falhariam se a regra quebrasse? (Asserção real, não só “não deu erro”.)
- Algum `@Disabled`, asserção removida ou limite de cobertura alterado?

**4. Arquitetura**
- Algum módulo usando classe interna de outro? Backend importando frontend?
- Regra de negócio no controller, no template ou no JavaScript?
- Migração de banco nova em vez de edição de uma antiga?

**5. Correção e robustez**
- Casos de borda: lista vazia, curso sem etiqueta, período sem checklist, arquivo vazio, valor nulo.
- Transação cobre tudo que precisa ser atômico?
- Consulta N+1 em listas grandes (checklist, repositórios)?

**6. Legibilidade** (`clean-code.md`)
- Nomes seguem o glossário? Funções com uma responsabilidade? Duplicação evitável?

**7. Fluxo** (skill `git`)
- Título do PR em português no formato Conventional Commits, base correta (`develop`, ou `main` só para entrega/hotfix), um assunto só.
- Documentação atualizada se a mudança afeta README, glossário ou pendências.

## 3. Como escrever os comentários

Cada comentário diz **onde**, **o quê**, **por quê** e, se possível, **como resolver**. Marque a gravidade para o autor saber o que é obrigatório:

| Marca | Significa |
|---|---|
| **[bloqueante]** | Bug, falha de segurança, regra do RF errada, teste ausente para regra nova. Precisa ser resolvido antes do merge |
| **[sugestão]** | Melhoria que vale a pena, mas o autor decide |
| **[dúvida]** | Não entendi; pode ser que esteja certo |
| **[detalhe]** | Coisa pequena, opcional |

Exemplo:

> **[bloqueante]** `DocumentoService.java:58` – `listarPorIndicador` não filtra pelos cursos da coordenação. Uma coordenação de Odontologia que chame a URL com o ID de um indicador de Medicina vê os documentos de Medicina (RF017). Sugestão: usar `cursosDoUsuario(usuario)` na consulta e adicionar um teste com coordenação de outro curso.

- Comente o código, não a pessoa.
- Seja específico: “está confuso” não ajuda; “o nome `processa` não diz que também envia o e-mail” ajuda.
- Se algo está bom e não é óbvio, diga também: ajuda a manter o padrão.

## 4. Fechando a revisão

- Resuma no fim: o que está bom, os bloqueantes e as sugestões.
- **O Claude não aprova nem faz merge.** Para registrar a revisão no GitHub (só se o usuário pedir para publicar):
  - `gh pr review <número> --comment --body-file <arquivo>` para comentários gerais;
  - `gh pr review <número> --request-changes --body-file <arquivo>` se houver bloqueante.
  
  A aprovação (`--approve`) e o merge ficam com o desenvolvedor humano.
- Se o usuário só pediu a revisão sem publicar, entregue o resultado na conversa.

## 5. Autorrevisão antes de abrir o PR

Antes de abrir o PR, passe o roteiro da seção 2 no próprio diff (`git diff develop...HEAD`). Quase sempre aparece alguma coisa: um log esquecido, um teste faltando, um nome ruim. É mais barato achar agora do que na revisão.
