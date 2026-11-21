# [008] - feat: Calendário no campo "Data/Prazo" da tela home

## Informações de Workflow

- **Modelo:** Feature/branch com worktree — cada task possui seu próprio branch e sua própria pasta de trabalho
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `feat/008-calendario-data-prazo`
- **Worktree:** `.claude/worktrees/008-calendario-data-prazo/` (criado pelo PO junto com a task)
- **Agent responsável:** `dev` (.claude/agents/dev.md) — altera apenas `client/`
- **Fluxo do agent responsável:**
  1. Na pasta principal do projeto, verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Entrar no worktree `.claude/worktrees/008-calendario-data-prazo/`, confirmar o branch `feat/008-calendario-data-prazo` e rodar `git merge --ff-only ia-main`
  5. Implementar a funcionalidade **dentro do worktree** (commits e push no branch `feat/008-calendario-data-prazo`)
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).

## História de usuário

Como **usuário da BIA**, quero **escolher a data/prazo da tarefa em um calendário**, para **não precisar digitar a data e evitar datas em formato errado**.

## Critérios de aceite

1. **Calendário ao interagir com o campo**
   - **Dado** que estou na tela home da BIA
   - **Quando** clico no campo "Data/Prazo"
   - **Então** um calendário é exibido para eu escolher o dia

2. **Data escolhida aparece no campo**
   - **Dado** que o calendário está aberto
   - **Quando** escolho um dia
   - **Então** o campo "Data/Prazo" mostra a data escolhida no formato `DD/MM/AAAA`

3. **Data salva como string no mesmo formato de hoje**
   - **Dado** que escolhi uma data no calendário e preenchi o campo "Tarefa"
   - **Quando** clico em "Add New Task"
   - **Então** a tarefa é criada com `dia_atividade` como string `DD/MM/AAAA` (ex: `"20/11/2026"`) em `/api/tarefas`, e a lista mostra essa data

4. **Data continua opcional**
   - **Dado** que estou no formulário de cadastro
   - **Quando** preencho só o campo "Tarefa", sem escolher data, e clico em "Add New Task"
   - **Então** a tarefa é criada normalmente, com o mesmo comportamento atual para tarefa sem data escolhida

5. **Formulário limpo após cadastrar**
   - **Dado** que acabei de cadastrar uma tarefa com data
   - **Quando** o formulário é limpo
   - **Então** o campo "Data/Prazo" volta vazio

6. **Sem mudança no banco e no restante da tela**
   - **Dado** que a alteração foi entregue
   - **Quando** uso a aplicação
   - **Então** não há migration nem alteração no backend, as tarefas já existentes continuam exibindo a data como antes, e o checkbox "Importante", a validação de campo obrigatório, a listagem, a edição e a exclusão não mudam

## Status

pronta para aceite

---

## Checklist de Atividades (Dev)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Entrar no worktree da task, confirmar o branch e rodar `git merge --ff-only ia-main`
- [x] Trocar o campo "Data/Prazo" por um seletor com calendário (em `client/`)
- [x] Converter a data escolhida para a string `DD/MM/AAAA` antes de enviar para a API
- [x] Manter o campo opcional e vazio após o cadastro
- [x] Garantir que backend e banco não foram alterados
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Implementação (Dev)

**O que foi feito** (só `client/`):
- `client/src/components/AddTask.jsx`: o campo "Data/Prazo" virou um input de texto `readOnly` (placeholder "Quando?"). Ao clicar nele (ou apertar Enter/Espaço), o calendário nativo do navegador abre (`showPicker()` de um `<input type="date">` invisível). O dia escolhido (`AAAA-MM-DD`) é convertido para a string `DD/MM/AAAA` e mostrado no campo; é essa string que vai em `dia_atividade`.
- `client/src/index.css`: classes `.form-control-date` e `.date-picker-hidden` (esconde o input date e deixa o cursor de clique no campo).
- Sem nova dependência. Sem migration e sem mudança em `api/`, `database/` e `config/`.
- Sem data escolhida, o comportamento é o mesmo de antes (envia a data de hoje, `toLocaleDateString('pt-BR')`). O campo volta vazio após o cadastro (`setDia("")`, já existente).
- Motivo do input date invisível: com o `<input type="date">` visível, o formato mostrado muda conforme o idioma do navegador (em inglês fica `MM/DD/AAAA`). Do jeito escolhido, o campo sempre mostra `DD/MM/AAAA`.

**Evidências:**
- Deploy local feito de dentro do worktree, com o mesmo nome de projeto compose da pasta principal (`docker compose -p bia-multi-agentic ...`) para reaproveitar o banco. `curl http://localhost:3001/api/versao` → `Bia 4.3.0`.
- `npm test` → 2 suítes, 16 testes passando.
- `git diff ia-main -- api database config` → vazio.
- Teste em navegador headless (Chromium, idioma `en-US`):
  - campo `readOnly: true`; o clique no campo chama `showPicker` (calendário aberto: `true`)
  - escolhido 2026-11-20 → campo mostra `20/11/2026`
  - body do POST: `{"titulo":"teste ui dev 008","dia_atividade":"20/11/2026","importante":true}`
  - campo depois do cadastro: `""`; a lista mostra `📅 20/11/2026`
- A tarefa que já existia (`"Tarefa criada via Playwright"`, `20/11/2026`) continua sendo listada igual. Os dados de teste foram removidos.

**Para o QA:** o input date fica invisível, então no Playwright a escolha do dia pode ser simulada com `locator('input[type=date]').fill('AAAA-MM-DD', { force: true })`. Também dá para clicar no campo e usar o calendário de verdade (modo headed).

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no worktree da task e no branch dela (`git branch --show-current` dentro de `.claude/worktrees/008-calendario-data-prazo/`)
- [ ] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [ ] Rodar a suíte de testes e registrar o resultado
- [ ] Remover os dados de teste criados durante a validação
- [ ] Testes no navegador: usar o MCP do Playwright (preferencial) ou o navegador em container (`qa-browser`), conforme o `qa.md`, e confirmar ao final que nenhum navegador ou servidor temporário ficou aberto
- [ ] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [ ] Mudar o status para `validada pelo QA` ou `com bugs`
- [ ] Fazer commit e push no branch da task
- [ ] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Validação QA

_(preenchida pelo QA)_

## Finalização (PO)

- [ ] Verificar se tudo foi implementado conforme o escopo técnico
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que o status da task é `validada pelo QA` (se estiver `com bugs`, devolver ao agent responsável)
- [ ] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, mudar o status para `recusada` com o motivo e devolver ao agent responsável (a task continua em `doing/`)
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada (resumo do que foi verificado) e **aguardar o OK do usuário** para continuar
  - [ ] Após o OK, confirmar que o worktree está no branch `feat/008-calendario-data-prazo`
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/`, dentro do worktree
  - [ ] Fazer commit e push final no branch da task, dentro do worktree
  - [ ] Abrir o Pull Request contra `ia-main` em `EvelynBonatto/bia` (conferir o branch imediatamente antes do `gh pr create`)
  - [ ] Fazer o merge do PR em `ia-main` com **squash**
  - [ ] Voltar para `ia-main`, atualizar, limpar referências, remover o worktree e apagar o branch local
  - [ ] Enviar ao usuário o link do PR e o commit do merge
