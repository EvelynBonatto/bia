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
   - **Quando** preencho só o campo "Tarefa" e clico em "Add New Task"
   - **Então** a tarefa é criada sem data, como acontece hoje

5. **Formulário limpo após cadastrar**
   - **Dado** que acabei de cadastrar uma tarefa com data
   - **Quando** o formulário é limpo
   - **Então** o campo "Data/Prazo" volta vazio

6. **Sem mudança no banco e no restante da tela**
   - **Dado** que a alteração foi entregue
   - **Quando** uso a aplicação
   - **Então** não há migration nem alteração no backend, as tarefas já existentes continuam exibindo a data como antes, e o checkbox "Importante", a validação de campo obrigatório, a listagem, a edição e a exclusão não mudam

## Status

aberta

---

## Checklist de Atividades (Dev)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no branch `ia-main` antes de iniciar
- [ ] Mover a task para `.claude/tasks/doing/`
- [ ] Fazer commit e push no branch `ia-main` (task + sequencial)
- [ ] Entrar no worktree da task, confirmar o branch e rodar `git merge --ff-only ia-main`
- [ ] Trocar o campo "Data/Prazo" por um seletor com calendário (em `client/`)
- [ ] Converter a data escolhida para a string `DD/MM/AAAA` antes de enviar para a API
- [ ] Manter o campo opcional e vazio após o cadastro
- [ ] Garantir que backend e banco não foram alterados
- [ ] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [ ] Validar rota `/api/versao` respondendo corretamente
- [ ] Aplicação buildando sem erros
- [ ] Mudar o status para `pronta para aceite`
- [ ] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

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
