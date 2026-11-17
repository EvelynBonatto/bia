# [004] - feat: Checkbox "Importante" marcado por padrão no cadastro de tarefa

## História de usuário

Como **usuário da BIA**, quero **que o checkbox "Importante" já venha marcado ao cadastrar uma nova tarefa**, para **não precisar marcá-lo manualmente toda vez, já que a maioria das minhas tarefas é importante**.

## Critérios de aceite

1. **Checkbox marcado ao abrir o formulário**
   - **Dado** que a aplicação está rodando
   - **Quando** abro o formulário de cadastro de tarefa
   - **Então** o checkbox "Importante" aparece marcado

2. **Tarefa salva como importante por padrão**
   - **Dado** que estou no formulário de cadastro com o checkbox "Importante" marcado por padrão
   - **Quando** preencho o campo "Tarefa" e clico em "Add New Task" sem mexer no checkbox
   - **Então** a tarefa é criada como importante

3. **Usuário pode desmarcar**
   - **Dado** que estou no formulário de cadastro
   - **Quando** desmarco o checkbox "Importante", preencho o campo "Tarefa" e clico em "Add New Task"
   - **Então** a tarefa é criada como não importante

4. **Formulário volta com o checkbox marcado após cadastrar**
   - **Dado** que acabei de cadastrar uma tarefa (com ou sem o checkbox marcado)
   - **Quando** o formulário é limpo após o cadastro
   - **Então** o checkbox "Importante" volta a aparecer marcado

5. **Apenas o checkbox muda**
   - **Dado** que a alteração foi entregue
   - **Quando** abro o formulário de cadastro e uso o restante da aplicação
   - **Então** os campos "Tarefa" e "Data/Prazo" continuam vazios por padrão, a validação de campo obrigatório continua funcionando e a listagem, edição e exclusão de tarefas existentes não mudam

## Status

pronta para aceite

---

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main`
- **Nome do branch:** `feat/004-checkbox-importante-padrao`
- **Agent responsável:** `dev` (.claude/agents/dev.md) — altera apenas `client/`
- **Fluxo do agent responsável:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch `feat/004-checkbox-importante-padrao` a partir de `ia-main`
  5. Implementar a funcionalidade

## Checklist de Atividades (Dev)

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch `feat/004-checkbox-importante-padrao` a partir de `ia-main`
- [x] Deixar o checkbox "Importante" marcado por padrão no formulário de cadastro
- [x] Manter o checkbox marcado ao limpar o formulário após o cadastro
- [x] Garantir que o usuário ainda consegue desmarcar o checkbox
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Implementação (Dev)

**Arquivo alterado:** `client/src/components/AddTask.jsx`
- Estado inicial do checkbox: `useState(false)` → `useState(true)` (marcado ao abrir o formulário).
- Limpeza após o cadastro: `setImportante(false)` → `setImportante(true)` (volta marcado).
- O `onChange` do checkbox não mudou, então o usuário continua podendo desmarcar. Campos "Tarefa" e "Data/Prazo" seguem iniciando vazios e a validação de campo obrigatório (modal) não foi alterada. Nenhuma mudança em listagem, edição, exclusão ou backend.

**Evidências:**
- Deploy local (`docker compose down && docker compose build && docker compose up -d`) concluído sem erros; `vite build`: `✓ 58 modules transformed` / `✓ built in 1.20s`.
- `curl -s http://localhost:3001/api/versao` → `Bia 4.3.0`.
- Bundle gerado (`client/build/assets/index-*.js`) contém o estado do checkbox como `useState(!0)` (true).
- `POST /api/tarefas` com `importante: true` (payload que o formulário envia sem mexer no checkbox) → criado com `"importante":true`; registro de teste removido em seguida (`DELETE` → 200).
- `npm test` (no container `server`): 2 suites, 16 testes passando.

## Validação QA

_(preenchido pelo QA)_

## Finalização (PO)

- [ ] Verificar se tudo foi implementado conforme o escopo
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que o status da task é `validada pelo QA` (se `com bugs`, devolver ao Dev)
- [ ] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, status `recusada` com motivo e devolver ao Dev
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada e **aguardar o OK**
  - [ ] Após o OK, confirmar que está no branch `feat/004-checkbox-importante-padrao`
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [ ] Fazer commit e push final no branch da task
  - [ ] Confirmar com `git branch --show-current` que está em `feat/004-checkbox-importante-padrao`
  - [ ] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[004] - feat: checkbox importante marcado por padrão`
  - [ ] Enviar ao usuário o link do PR
