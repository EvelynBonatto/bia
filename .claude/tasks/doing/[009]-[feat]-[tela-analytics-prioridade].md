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
   - **Então** aparece, entre o formulário de cadastro e a lista de tarefas, uma box clicável com ícone de gráfico (📊), o título "Ver Analytics", o subtítulo "Visualize suas tarefas por prioridade" e uma seta (→) à direita

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

validada pelo QA

---

## Implementação (Dev)

**O que foi feito (somente `client/`):**
- Base do shadcn/ui: Tailwind CSS v4 (`@tailwindcss/vite`) **sem o preflight** (para não mudar o visual atual), alias `@/` → `src/` (`vite.config.js` + `jsconfig.json`), `components.json`, `src/lib/utils.js` (`cn`) e `src/tailwind.css` (cores do shadcn ligadas às variáveis de tema da BIA).
- Componente de gráfico do shadcn/ui adicionado via CLI (`npx shadcn add chart`) → `src/components/ui/chart.jsx` (usa `recharts`; `react-is` instalado como peer dependency).
- `src/components/AnalyticsBox.jsx`: box clicável 📊 "Ver Analytics" / "Visualize suas tarefas por prioridade" / →, colocada em `App.jsx` entre o `AddTask` e a lista.
- `src/components/Analytics.jsx` + rota `/analytics`: busca `/api/tarefas` toda vez que a tela abre e mostra o gráfico de barras ("Importantes" × "Não importantes") com `ChartContainer`/`ChartTooltip`; mensagem "Não há tarefas para exibir" quando a lista está vazia; mensagem de erro se a API falhar; link "← Voltar" para a home.
- Estilos novos em `src/index.css` (`.analytics-*`), seguindo as variáveis de tema existentes (claro/escuro).

**Evidências:**
- `npm run build` (client): ok (apenas o aviso de tamanho de chunk do Vite).
- `npm test`: 2 suites, 16 testes passando.
- Deploy local (`docker compose down && build && up -d`, de dentro do worktree): `curl /api/versao` → `Bia 4.3.0`; `GET /analytics` → HTTP 200.
- `git diff ia-main -- api database config`: vazio (sem backend nem migration).
- Teste no navegador (Playwright headless, script temporário):
  - Home: box com o texto "📊 Ver Analytics Visualize suas tarefas por prioridade →", logo depois do formulário (`.add-form`) e antes da lista.
  - Clique na box → `http://localhost:3001/analytics`; eixo X "Importantes" e "Não importantes".
  - `/api/tarefas` com 2 importantes; criada 1 não importante via API → barras com alturas proporcionais 2:1 (101px / 51px). Tarefa de teste removida em seguida.
  - `/api/tarefas` simulada vazia → "Não há tarefas para exibir 📊", sem erros de JavaScript.
  - "← Voltar" → volta para `/` com o formulário carregado; nenhum erro de JavaScript.

**Ajuste pedido pelo usuário (após a validação do QA):** barra "Importantes" na cor alaranjada (`#f97316`); "Não importantes" continua na cor de destaque do tema (azul). Cores definidas no `chartConfig` do shadcn/ui (`importantes` / `naoImportantes`) e aplicadas por barra via `fill` nos dados.
- Evidência (Playwright headless): cor computada das barras — tema claro `rgb(249, 115, 22)` / `rgb(59, 130, 246)`; tema escuro `rgb(249, 115, 22)` / `rgb(96, 165, 250)`. Deploy local ok (`/api/versao` → `Bia 4.3.0`).
- Barras mais finas: `maxBarSize={90}` no `<Bar>` (antes ~144px de largura, agora 90px — medido no Playwright headless).
- Status voltou para `pronta para aceite` para o QA reconferir os ajustes visuais (cor e largura).

## Checklist de Atividades (Dev)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Entrar no worktree da task, confirmar o branch e rodar `git merge --ff-only ia-main`
- [x] Adicionar o componente de gráfico do shadcn/ui em `client/` (pode usar o MCP do shadcn)
- [x] Criar a box "Ver Analytics" na home, entre o formulário e a lista
- [x] Criar a tela/rota de Analytics com o gráfico de barras por prioridade
- [x] Tratar o caso sem tarefas e incluir o link de voltar para a home
- [x] Garantir que backend e banco não foram alterados
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no worktree da task e no branch dela (`git branch --show-current` dentro de `.claude/worktrees/009-tela-analytics-prioridade/`)
- [x] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [x] Rodar a suíte de testes e registrar o resultado
- [x] Remover os dados de teste criados durante a validação
- [x] Testes no navegador: usar o MCP do Playwright (preferencial) ou o navegador em container (`qa-browser`), conforme o `qa.md`, e confirmar ao final que nenhum navegador ou servidor temporário ficou aberto
- [x] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [x] Mudar o status para `validada pelo QA` ou `com bugs`
- [x] Fazer commit e push no branch da task
- [x] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Validação QA

**Ambiente:** worktree `.claude/worktrees/009-tela-analytics-prioridade` (branch `feat/009-tela-analytics-prioridade`, commit `8877b52`), containers subidos com `COMPOSE_PROJECT_NAME=bia-multi-agentic docker compose build && up -d`. `curl /api/versao` → `Bia 4.3.0`; `GET /analytics` → HTTP 200. Navegador: MCP do Playwright (Chromium headless, `--isolated`). Contagem das barras lida do SVG do gráfico (altura da barra ÷ pixels por unidade do eixo Y) e comparada com `importante=true/false` de `/api/tarefas` (`{ data: [...] }`).

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | Box "Ver Analytics" na home | ✅ | Snapshot da home: `link "📊 Ver Analytics Visualize suas tarefas por prioridade →"` (`/url: /analytics`), com `heading "Ver Analytics"`, `paragraph "Visualize suas tarefas por prioridade"` e `→`. Posição: fim do formulário y=354, box y=370–449, primeira tarefa da lista y=577 (entre o formulário e a lista). Seta à direita do texto (texto termina em x=798, seta começa em x=814). `cursor: pointer`. |
| 2 | Box leva para Analytics | ✅ | Clique na box → `Page URL: http://localhost:3001/analytics`. Acesso direto a `/analytics` → HTTP 200. |
| 3 | Gráfico de barras por prioridade (shadcn/ui) | ✅ | Gráfico renderizado dentro de `[data-slot="chart"]` (`ChartContainer` de `client/src/components/ui/chart.jsx`, componente chart do shadcn/ui), eixo X "Importantes" e "Não importantes". Carga inicial: gráfico `Importantes=2, Não importantes=0` × API `2/0`. Com tarefa não importante criada: gráfico `Importantes=1, Não importantes=1` × API `importantes=1, nao=1`. |
| 4 | Gráfico reflete mudanças | ✅ | Pela home: criada "QA 009 nao importante" (sem estrela) → Analytics `1/1` = API `1/1`; marcada a estrela → Analytics `2/0` = API `2/0`; excluída → Analytics `1/0` = API `1/0`. Os dados são buscados a cada abertura da tela (incluindo voltar/avançar do navegador). Nenhum erro de JavaScript. |
| 5 | Sem tarefas | ✅ | Validado **sem apagar dados**: `/api/tarefas` interceptada no Playwright (`page.route`) retornando `{ data: [] }` e também `[]`. Nos dois casos a tela mostra "Não há tarefas para exibir 📊 / Cadastre tarefas na tela inicial para ver o gráfico.", sem gráfico renderizado e sem erros (`pageerror` e `console.error` vazios). |
| 6 | Voltar para a home | ✅ | "← Voltar" → `http://localhost:3001/`, formulário (`.add-form`) presente e lista carregada ("Tarefa criada via Playwright"); em seguida cadastro/estrela/exclusão funcionando (ver critério 7). |
| 7 | Sem mudança no backend e no restante da home | ✅ | `git diff ia-main --name-only` só lista arquivos em `client/` e a própria task; `git diff ia-main -- api database config` vazio (sem migration). Regressão na home: criada "QA 009 regressao" (listada, title "Remover importante"), estrela alternada (title "Marcar importante"), exclusão com confirmação (tarefa some da lista). Nenhum erro de JavaScript. |

**Testes unitários:** `npm test` → `Test Suites: 2 passed, 2 total` / `Tests: 16 passed, 16 total`.

**Dados de teste:** as duas tarefas criadas pelo QA ("QA 009 nao importante" `10031090-…` e "QA 009 regressao" `2cb4f370-…`) foram excluídas pela própria UI ao final de cada teste (confirmado nos logs do container: `DELETE` dos dois uuids). Nenhuma tarefa existente foi apagada pelo QA e "Limpar tudo" não foi usado.

**Observação (ambiente, não é bug da entrega):** durante a validação, outro cliente acessou a mesma aplicação em `localhost:3001` ao mesmo tempo (provavelmente a sessão da task 008, que usa os mesmos containers/porta). Os logs do container `bia` mostram, fora das ações do QA, `INSERT`s às 23:34:03, `UPDATE` às 23:34:12, `DELETE` de `09131820-…`, `0925dcd0-…` e `345d34d0-…` ("teste ui dev 008") às 23:34:13 e `DELETE` de `3c233aa0-…` ("Tarefa criada via Playwright") às 23:35:10 UTC, quando o navegador do QA já estava sendo fechado. Em cada etapa o gráfico continuou igual à API naquele momento.

### Revalidação QA (após ajustes visuais `f6712f1` e `ed53b60`)

**Ambiente:** worktree da 009, branch `feat/009-tela-analytics-prioridade`, commit `ed53b60`. Containers `bia`, `database`, `redis` já em execução (não foram reiniciados): `docker inspect bia` → `working_dir` = worktree 009; `client/build/assets/index-BpT6a2OP.js` contém "Ver Analytics", `f97316` e `maxBarSize:90`. `curl /api/versao` → `Bia 4.3.0`. Navegador: MCP do Playwright (Chromium headless, `--isolated`), fechado ao final (`pgrep -af ms-playwright` sem processo do navegador).

| # | Item | Resultado | Evidência |
|---|------|-----------|-----------|
| A1 | Barra "Importantes" alaranjada, "Não importantes" na cor de destaque do tema | ✅ | `getComputedStyle(path).fill` das barras: tema claro (`data-theme="light"`) → `rgb(249, 115, 22)` / `rgb(59, 130, 246)`; tema escuro (`data-theme="dark"`) → `rgb(249, 115, 22)` / `rgb(96, 165, 250)`. |
| A2 | Barras mais finas (largura máx. 90px) | ✅ | Largura medida (`getBoundingClientRect`) das duas barras: `90px` em viewport 1280×720 e também em 1600×900 (não passa de 90px em tela mais larga). |
| 1 | Box "Ver Analytics" na home | ✅ | Texto do link: "📊 Ver Analytics Visualize suas tarefas por prioridade →". Posição: fim do formulário y=354, box y=370–449 (entre o formulário e a lista). |
| 2 | Box leva para Analytics | ✅ | Clique → `http://localhost:3001/analytics`. |
| 3 | Gráfico por prioridade (shadcn/ui) com contagens da API | ✅ | `[data-slot="chart"]` presente; eixo X "Importantes" e "Não importantes". `/api/tarefas` (`{ data: [...] }`): `importante=true` 3, `false` 2. Gráfico: topo de "Importantes" em y=241 (tick "3" em y=240) e de "Não importantes" em y=291 (tick "2" em y=291); alturas 151,5px / 101px (3:2) → `3/2`. |
| 4 | Gráfico reflete mudanças | ✅ | Criada pela home "QA 009 revalidacao" (`15f72000-…`, `importante=true`) → API `4/2`, gráfico `4/2`; excluída → API `3/2`, gráfico `3/2`. |
| 5 | Sem tarefas | ✅ | `/api/tarefas` interceptada (`page.route`) com `{ data: [] }` → "Não há tarefas para exibir 📊 Cadastre tarefas na tela inicial para ver o gráfico.", 0 barras, sem erros. Nenhum dado real apagado. |
| 6 | Voltar para a home | ✅ | "← Voltar" → `http://localhost:3001/`, `.add-form` presente. |
| 7 | Sem mudança no backend | ✅ | `git diff ia-main --stat -- api database config` vazio; `git diff ia-main --stat` só lista `client/` e a própria task. Cadastro/listagem/exclusão funcionando (item 4). |

**Erros de JavaScript:** nenhum (`pageerror` e `console.error` vazios em todos os fluxos).

**Testes unitários:** `npm test` → `Test Suites: 2 passed, 2 total` / `Tests: 16 passed, 16 total`.

**Dados de teste:** apenas "QA 009 revalidacao" (`15f72000-e608-11f1-a430-5138db05a659`) foi criada e removida em seguida (confirmado: não aparece mais em `/api/tarefas`, contagens voltaram a `3/2`). "Limpar tudo" não foi usado; containers mantidos em execução.

## Bugs

Nenhum bug encontrado.

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
