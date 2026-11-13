# [004] - Checkbox "Importante" Marcado por Padrão

## Tipo
`feat`

## Resumo
Alterar o checkbox "Importante" no formulário de adição de tarefas para que venha marcado (`true`) por padrão ao carregar a tela e após cada nova adição de tarefa.

---

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Agent responsável pelo início:** `dev` (.claude/agents/dev.md)
- **Fluxo do agent:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch da task a partir de `ia-main`
  5. Implementar a funcionalidade

---

## Checklist de Atividades (Agent dev)

> Marcar cada item com `[x]` à medida que for concluído durante a implementação.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch da task a partir de `ia-main`
- [x] Alterar o estado inicial de `importante` de `useState(false)` para `useState(true)` no `AddTask.jsx` (linha 7)
- [x] Alterar o reset de `importante` após submit de `setImportante(false)` para `setImportante(true)` no `AddTask.jsx` (linha 26)
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Ao concluir, informar que a task precisa ser passada para o **PO** para encerramento

---

## Finalização (Agent PO)

> Esta etapa é executada **apenas pelo PO** após os agentes concluírem a implementação.

- [x] Verificar se tudo foi implementado conforme o escopo técnico
- [x] Verificar se todos os itens do checklist foram marcados como concluídos
- [x] Confirmar que a aplicação está buildando e funcionando corretamente
- [x] Se tudo estiver ok:
  - [x] Informar ao usuário que a task está finalizada
  - [x] Mover a task para `.claude/tasks/done/`
  - [x] Fazer commit e push final no repositório remoto

---

## Contexto

No formulário de adição de tarefas (`AddTask.jsx`), o checkbox "Importante" é inicializado como desmarcado (`false`). O usuário solicitou que ele venha marcado por padrão, para que toda nova tarefa já seja criada como importante sem que o usuário precise marcar manualmente.

Após o submit do formulário, o estado é resetado — também deve voltar para `true` para manter o comportamento padrão em adições consecutivas.

---

## História de Usuário

> **Como** usuário do projeto BIA,  
> **quando** abro o formulário de adição de tarefas,  
> **quero** que o checkbox "Importante" já esteja marcado por padrão,  
> **para que** as novas tarefas sejam criadas como importantes sem que eu precise marcar manualmente a cada vez.

---

## Critérios de Aceitação

### Cenário 1 — Checkbox marcado ao carregar a tela
```
Given que o usuário acessa a aplicação e visualiza o formulário de adição de tarefas
When a tela é carregada
Then o checkbox "Importante" deve estar marcado (checked)
```

### Cenário 2 — Checkbox marcado após adicionar uma tarefa
```
Given que o usuário preencheu o formulário e clicou em "Adicionar Tarefa"
When a tarefa é criada e o formulário é resetado
Then o checkbox "Importante" deve voltar a ficar marcado (checked)
```

### Cenário 3 — Usuário pode desmarcar manualmente
```
Given que o checkbox "Importante" está marcado por padrão
When o usuário clica no checkbox para desmarcá-lo
Then o checkbox deve ser desmarcado
And a tarefa enviada deve ser criada com importante = false
```

### Cenário 4 — Tarefa criada com importante = true por padrão
```
Given que o usuário não alterou o checkbox "Importante" (que está marcado por padrão)
When ele preenche o título e clica em "Adicionar Tarefa"
Then a tarefa deve ser criada com o campo importante = true no backend
And deve aparecer destacada na lista de tarefas (com indicador de importante)
```

---

## Escopo Técnico

### Arquivo a modificar
- `client/src/components/AddTask.jsx`

### Alterações necessárias

1. **Linha 7** — Alterar o estado inicial:
   ```jsx
   // De:
   const [importante, setImportante] = useState(false);
   // Para:
   const [importante, setImportante] = useState(true);
   ```

2. **Linha 26** — Alterar o reset após submit:
   ```jsx
   // De:
   setImportante(false);
   // Para:
   setImportante(true);
   ```

### Observações
- Nenhuma alteração no backend é necessária — o campo `importante` já é enviado no payload e tratado pelo controller `tarefas.js`.
- Nenhuma alteração de migração é necessária — o campo `importante` já existe na tabela `tarefas`.
- O comportamento de toggle (marcar/desmarcar manualmente) deve continuar funcionando normalmente via `onChange`.

---

## Definition of Ready
- [x] História de usuário escrita e compreendida
- [x] Critérios de aceitação definidos
- [x] Arquivo de referência identificado (`AddTask.jsx`)
- [x] Escopo técnico delimitado (alteração em um único arquivo, duas linhas)
- [x] Sem dependências externas bloqueantes

## Definition of Done
- [x] Estado inicial de `importante` alterado para `true` no `AddTask.jsx`
- [x] Reset pós-submit alterado para `true` no `AddTask.jsx`
- [x] Checkbox aparece marcado ao carregar a tela
- [x] Checkbox volta marcado após adicionar uma tarefa
- [x] Toggle manual continua funcionando (marcar/desmarcar)
- [x] Tarefa criada com `importante: true` reflete na lista (destaque visual)
- [x] Aplicação buildando sem erros
- [x] Deploy local validado com `docker compose down && docker compose build && docker compose up -d`
- [x] Rota `/api/versao` respondendo corretamente após deploy
- [x] Task revisada e encerrada pelo PO
