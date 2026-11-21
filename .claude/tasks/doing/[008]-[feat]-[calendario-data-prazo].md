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

validada pelo QA

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

### Ajuste pedido pelo usuário: calendário com as cores da BIA

Depois da primeira validação do QA, a usuária pediu que o calendário combinasse com as cores da aplicação. O popup do calendário nativo do navegador (`showPicker()`) não aceita estilo por CSS, então ele foi trocado por um componente próprio, sem nova dependência:
- **Novo `client/src/components/Calendario.jsx`:** mostra mês e ano, com setas ‹ › para trocar de mês. A grade vai de Dom a Sáb. Clicar num dia devolve a string `DD/MM/AAAA` e fecha o calendário. Também fecha ao clicar fora ou apertar Esc. O dia de hoje fica com borda, e o dia escolhido fica preenchido.
- **`AddTask.jsx`:** o input `type="date"` invisível e o `showPicker()` saíram. Clicar no campo (ou apertar Enter/Espaço) abre e fecha o `<Calendario>`. O campo continua `readOnly` e volta vazio após o cadastro.
- **`index.css`:** as classes `.date-picker-hidden` saíram e entraram as classes `.calendario*`. Todas usam as variáveis do tema (`--bg-card`, `--bg-secondary`, `--border-color`, `--text-primary`, `--text-secondary`, `--accent-primary`), então o calendário acompanha o modo claro e o escuro.

**Evidências do ajuste:**
- Teste num container temporário só com o código da 008, na porta 3008. Os containers da porta 3001 estavam com a task 009, então não foram derrubados. O teste foi feito em Chromium headless com idioma `en-US`:
  - ao clicar no campo, `.calendario` aparece com o título `Novembro 2026`
  - clicar no dia 20 faz o campo mostrar `20/11/2026` e o calendário fecha
  - ao reabrir, o dia selecionado é o `20`; a seta › leva para `Dezembro 2026`
  - o calendário fecha ao clicar fora e ao apertar Esc
- Capturas de tela nos temas claro e escuro conferidas: fundo, borda, texto e destaque em azul seguem o tema da BIA.
- O container e a imagem temporários foram removidos.

**Para o QA (revalidação):** a validação abaixo vale para o commit `20d1197`, a versão com o calendário nativo. É preciso revalidar os critérios 1, 2, 3 e 5 com o calendário novo. No Playwright, o dia agora é escolhido clicando no botão de verdade, por exemplo `page.locator('.calendario-dia', { hasText: /^20$/ }).click()`. Não é mais preciso usar `force`.

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no worktree da task e no branch dela (`git branch --show-current` dentro de `.claude/worktrees/008-calendario-data-prazo/`)
- [x] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [x] Rodar a suíte de testes e registrar o resultado
- [x] Remover os dados de teste criados durante a validação
- [x] Testes no navegador: usar o MCP do Playwright (preferencial) ou o navegador em container (`qa-browser`), conforme o `qa.md`, e confirmar ao final que nenhum navegador ou servidor temporário ficou aberto
- [x] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [x] Mudar o status para `validada pelo QA` ou `com bugs`
- [x] Fazer commit e push no branch da task
- [x] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Validação QA

### Revalidação: commit `e60f66e` (calendário próprio com as cores da BIA)

**Ambiente:** worktree `.claude/worktrees/008-calendario-data-prazo/`, branch `feat/008-calendario-data-prazo`, `git pull --ff-only` até `e60f66e`. Os containers da porta 3001 continuavam com a task 009 (`docker inspect bia` → `working_dir` = `.../009-tela-analytics-prioridade`), então não foram derrubados. O QA rodou de novo um container temporário só com o código da 008 (`bia-qa-008`, porta **3008**, rede `bia-multi-agentic_default`, mesmo banco; `/api/versao` → `Bia 4.3.0`). O bundle chama a API em `localhost:3001`; a 008 não muda o backend. O container e a imagem temporários foram removidos ao final.

**Navegador:** MCP do Playwright (Chromium headless), contexto com locale `en-US`. O dia foi escolhido clicando no botão real (`.calendario-dia` com texto `20`), sem `force`.

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | Calendário ao clicar no campo | ✅ | Antes do clique, `.calendario` não existe. Depois do clique, fica visível com o título `Novembro 2026` e os cabeçalhos `Dom,Seg,Ter,Qua,Qui,Sex,Sáb`. Novembro tem 30 dias, o dia 1 cai no Domingo, e hoje (`21`) tem a classe `hoje`. O campo é `readOnly` e não há mais `input[type=date]` (0 na página). Também abre com Enter e com Espaço no campo |
| 2 | Data escolhida aparece no campo (DD/MM/AAAA) | ✅ | Clique no dia 20 → campo `20/11/2026` (navegador em `en-US`), e o calendário fecha. Ao reabrir, o dia `20` tem a classe `selecionado` |
| 3 | Data salva como string DD/MM/AAAA | ✅ | Body do POST: `{"titulo":"QA 008 r3 com data","dia_atividade":"20/11/2026","importante":true}`; `GET /api/tarefas` → `"dia_atividade":"20/11/2026"`; card na lista: `QA 008 r3 com data / 📅 20/11/2026` |
| 4 | Data continua opcional | ✅ | Só o título preenchido (Importante desmarcado) → POST `{"titulo":"QA 008 r3 sem data","dia_atividade":"21/11/2026","importante":false}` (data de hoje, mesmo comportamento anterior). Card: `📅 21/11/2026` |
| 5 | Formulário limpo após cadastrar | ✅ | Após o cadastro: campo Data/Prazo `""`, Tarefa `""`, Importante marcado, calendário fechado. Ao reabrir, nenhum dia está `selecionado` e o calendário volta para o mês atual (`Novembro 2026`) |
| 6 | Sem mudança no banco e no restante da tela | ✅ | `git diff ia-main -- api database config` → vazio (mudaram só `AddTask.jsx`, `Calendario.jsx` e `index.css`). As tarefas da usuária continuam com a data como antes (ex.: `Corrigir bug no login / 📅 24/11/2026`). O modal "Campo obrigatório" aparece ao enviar sem título. O toggle de prioridade funcionou nas duas direções numa tarefa do QA (`importante` false → true → false, conferido em `/api/tarefas`). A exclusão funcionou (`DELETE /api/tarefas/<uuid>`). A paginação (5 por página, que já existe em `ia-main`) segue funcionando |

**Comportamentos do calendário novo:**
- Troca de mês: › leva para `Dezembro 2026` e depois para `Janeiro 2027` (31 dias), virando o ano. ‹ volta até `Outubro 2026`.
- Esc fecha o calendário ✅. Clicar fora fecha ✅. Um segundo clique no campo fecha ✅. Ao reabrir, o calendário mostra o mês da data escolhida (ou o mês atual, se não houver data).
- Cores do tema (estilos computados × variáveis do tema):
  - **Claro:** fundo `rgb(255,255,255)` = `--bg-card #ffffff`, borda `rgb(229,231,235)` = `--border-color #e5e7eb`, texto `rgb(31,41,55)` = `--text-primary #1f2937`, dia escolhido com fundo `rgb(59,130,246)` = `--accent-primary #3b82f6` e texto branco, hoje com borda `#3b82f6`.
  - **Escuro** (pelo botão de tema do header): fundo `rgb(31,41,55)` = `--bg-card #1f2937`, borda `rgb(55,65,81)` = `#374151`, texto `rgb(249,250,251)` = `#f9fafb`, dia escolhido com fundo `rgb(96,165,250)` = `--accent-primary #60a5fa`, hoje com borda `#60a5fa`.
  - O tema foi restaurado para claro no final.
- Capturas de tela (fora do repositório): `/tmp/playwright-mcp/qa008-r2-claro.png` e `/tmp/playwright-mcp/qa008-r2-escuro.png`. As duas mostram o calendário aberto em Novembro 2026, com o dia 20 preenchido em azul e o dia 21 com borda azul, combinando com o tema.
- Observação (não é bug): clicar no botão de tema com o calendário aberto fecha o calendário, porque conta como clique fora. É o comportamento esperado.

**Testes unitários:** `npm test` → 2 suítes, 16 testes passando.

**Limpeza:** removidas pela tela só as tarefas criadas pelo QA ("QA 008 r2 com data", "QA 008 r2 debug", "QA 008 r3 com data", "QA 008 r3 sem data"). `GET /api/tarefas` final → apenas as 5 tarefas da usuária ("Corrigir bug no login", "Organizar a mesa de trabalho", "Ler artigo sobre AWS ECS", "Revisar pull request", "Preparar apresentação da sprint"). Navegador fechado (`browser_close`, sem processo Chromium restante). Container `bia-qa-008` parado e imagem removida.

### Primeira validação: commit `20d1197` (calendário nativo, substituído)

**Ambiente:** worktree `.claude/worktrees/008-calendario-data-prazo/`, branch `feat/008-calendario-data-prazo`, commit `20d1197`. Na hora do deploy, outra sessão (task 009) subiu os containers `bia`/`database`/`redis` a partir do worktree da 009 (`com.docker.compose.project.working_dir` = `.../009-tela-analytics-prioridade`). Para não derrubar o ambiente da outra task, o QA gerou uma imagem só do código da 008 (`docker build -t bia-qa-008 .`) e rodou um container temporário `bia-qa-008` na porta **3008**, ligado à mesma rede e ao mesmo banco (`curl localhost:3008/api/versao` → `Bia 4.3.0`). Obs.: o bundle do front tem `VITE_API_URL=http://localhost:3001` (Dockerfile), então a tela da 008 (porta 3008) chamou a API da porta 3001. Isso não afeta a validação: a 008 não mexe no backend (diff vazio) e o banco é o mesmo. O container e a imagem temporários foram removidos ao final.

**Navegador:** MCP do Playwright (Chromium headless), num contexto com locale `en-US` (`navigator.language` = `en-US`).

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | Calendário ao clicar no campo | ✅ | Campo "Data/Prazo" `readOnly: true`; o `input[type=date]` fica invisível (`isVisible: false`); ao clicar no campo, `showPicker()` foi chamado 1 vez, sem erro (`pickerCalls: 1`, `pickerErr: null`) |
| 2 | Data escolhida no formato DD/MM/AAAA | ✅ | Escolhido `2026-11-20` no calendário → campo mostra `20/11/2026`, mesmo com navegador em `en-US` |
| 3 | Data salva como string DD/MM/AAAA | ✅ | Body do POST: `{"titulo":"QA 008 com data","dia_atividade":"20/11/2026","importante":true}`; `GET /api/tarefas` → `"dia_atividade":"20/11/2026"`; a lista mostra `📅 20/11/2026` |
| 4 | Data continua opcional | ✅ | Só com o título preenchido (Importante desmarcado), a tarefa foi criada: POST `{"titulo":"QA 008 sem data","dia_atividade":"21/11/2026","importante":false}`. É a data de hoje, igual ao comportamento anterior (`toLocaleDateString('pt-BR')`) |
| 5 | Formulário limpo após cadastrar | ✅ | Depois do cadastro: campo Data/Prazo `""`, input date `""`, Tarefa `""`, Importante volta marcado (`true`) |
| 6 | Sem mudança no banco e no restante da tela | ✅ | `git diff ia-main -- api database config` → vazio (só mudaram `client/src/components/AddTask.jsx` e `client/src/index.css`). A tarefa que já existia ("Tarefa criada via Playwright") continua com `📅 20/11/2026`. Modal "Campo obrigatório / Por favor, adicione uma descrição para a tarefa" aparece ao enviar sem título. O toggle de prioridade (`PUT /api/tarefas/update_priority/<uuid>`) mudou a classe do card de `task` para `task reminder`. A exclusão (`DELETE /api/tarefas/<uuid>`) tirou os cards da lista. A tela não tem edição de título/data, só o toggle de importante, e ele segue funcionando |

**Testes unitários:** `npm test` → 2 suítes, 16 testes passando.

**Limpeza:** removidas pela tela (DELETE) as tarefas "QA 008 com data", "QA 008 sem data" e a pendente do dev "teste ui dev 008" (`345d34d0-e603-11f1-88e8-c3750aeb996a`). `GET /api/tarefas` final → só "Tarefa criada via Playwright". Navegador do QA fechado (`browser_close`); o Chromium que ainda aparece em `pgrep -af ms-playwright` é de outra instância do `playwright-mcp` (da outra sessão), não do QA. Container `bia-qa-008` parado e imagem removida.

## Bugs

Nenhum bug encontrado (validação de `20d1197` e revalidação de `e60f66e`).

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
