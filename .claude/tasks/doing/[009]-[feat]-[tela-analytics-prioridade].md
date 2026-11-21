# [009] - feat: Tela de Analytics com gráfico de tarefas por prioridade

## Informações de Workflow

- **Modelo:** Feature/branch com worktree — cada task possui seu próprio branch e sua própria pasta de trabalho
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `feat/009-tela-analytics-prioridade`
- **Worktree:** `.claude/worktrees/009-tela-analytics-prioridade/` (criado pelo PO junto com a task)
- **Agent responsável:** `dev` (.claude/agents/dev.md) — altera apenas `client/`
- **Fluxo do agent responsável:**
  1. Na pasta principal do projeto, verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Entrar no worktree `.claude/worktrees/009-tela-analytics-prioridade/`, confirmar o branch `feat/009-tela-analytics-prioridade` e rodar `git merge --ff-only ia-main`
  5. Implementar a funcionalidade **dentro do worktree** (commits e push no branch `feat/009-tela-analytics-prioridade`)
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).

## História de usuário

Como **usuário da BIA**, quero **ver um gráfico com a quantidade de tarefas por prioridade**, para **entender rapidamente quantas das minhas tarefas são importantes**.

## Critérios de aceite

> "Prioridade" = campo **Importante** da tarefa: **Importantes** (`importante = true`) e **Não importantes** (`importante = false`).

1. **Box "Ver Analytics" na home**
   - **Dado** que estou na tela home da BIA
   - **Quando** a página carrega
   - **Então** aparece, entre o formulário de cadastro e a lista de tarefas, uma box clicável com ícone de gráfico, o título "Ver Analytics", o subtítulo "Visualize suas tarefas por prioridade" e uma seta à direita

2. **Box leva para a tela de Analytics**
   - **Dado** que estou na home
   - **Quando** clico na box "Ver Analytics"
   - **Então** sou levado para a tela de Analytics, com uma URL própria (ex: `/analytics`)

3. **Gráfico de barras agrupado por prioridade**
   - **Dado** que existem tarefas cadastradas, importantes e não importantes
   - **Quando** abro a tela de Analytics
   - **Então** vejo um gráfico de barras feito com o componente de gráfico do **shadcn/ui**, com uma barra "Importantes" e outra "Não importantes", cada uma com a mesma quantidade que aparece em `/api/tarefas`

4. **Gráfico reflete mudanças**
   - **Dado** que criei, excluí ou mudei a estrela (importante) de uma tarefa na home
   - **Quando** abro (ou volto para) a tela de Analytics
   - **Então** as quantidades do gráfico estão atualizadas

5. **Sem tarefas**
   - **Dado** que não há tarefas cadastradas
   - **Quando** abro a tela de Analytics
   - **Então** vejo uma mensagem informando que não há tarefas para exibir, sem erro na tela

6. **Voltar para a home**
   - **Dado** que estou na tela de Analytics
   - **Quando** clico no link de voltar
   - **Então** volto para a home, com o formulário e a lista de tarefas funcionando

7. **Sem mudança no backend e no restante da home**
   - **Dado** que a alteração foi entregue
   - **Quando** uso a aplicação
   - **Então** não há migration nem alteração no backend (os dados vêm de `/api/tarefas`), e o cadastro, a listagem, a edição e a exclusão de tarefas continuam como antes

## Status

aberta

---

## Checklist de Atividades (Dev)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no branch `ia-main` antes de iniciar
- [ ] Mover a task para `.claude/tasks/doing/`
- [ ] Fazer commit e push no branch `ia-main` (task + sequencial)
- [ ] Entrar no worktree da task, confirmar o branch e rodar `git merge --ff-only ia-main`
- [ ] Adicionar o componente de gráfico do shadcn/ui em `client/` (pode usar o MCP do shadcn)
- [ ] Criar a box "Ver Analytics" na home, entre o formulário e a lista
- [ ] Criar a tela/rota de Analytics com o gráfico de barras por prioridade
- [ ] Tratar o caso sem tarefas e incluir o link de voltar para a home
- [ ] Garantir que backend e banco não foram alterados
- [ ] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [ ] Validar rota `/api/versao` respondendo corretamente
- [ ] Aplicação buildando sem erros
- [ ] Mudar o status para `pronta para aceite`
- [ ] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no worktree da task e no branch dela (`git branch --show-current` dentro de `.claude/worktrees/009-tela-analytics-prioridade/`)
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
  - [ ] Após o OK, confirmar que o worktree está no branch `feat/009-tela-analytics-prioridade`
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/`, dentro do worktree
  - [ ] Fazer commit e push final no branch da task, dentro do worktree
  - [ ] Abrir o Pull Request contra `ia-main` em `EvelynBonatto/bia` (conferir o branch imediatamente antes do `gh pr create`)
  - [ ] Fazer o merge do PR em `ia-main` com **squash**
  - [ ] Voltar para `ia-main`, atualizar, limpar referências, remover o worktree e apagar o branch local
  - [ ] Enviar ao usuário o link do PR e o commit do merge
