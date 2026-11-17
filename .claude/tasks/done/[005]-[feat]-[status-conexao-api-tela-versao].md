# [005] - feat: Status de conexão da API na tela de versão

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `feat/005-status-conexao-api-tela-versao`
- **Agent responsável:** `dev` (.claude/agents/dev.md) — altera apenas `client/`
- **Fluxo do agent responsável:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch `feat/005-status-conexao-api-tela-versao` a partir de `ia-main`
  5. Implementar a funcionalidade
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).

## História de usuário

Como **aluno da Formação AWS**, quero **ver na tela de versão se a aplicação está conectada à API**, para **saber na hora se o backend do ambiente que estou testando está respondendo, sem precisar usar terminal**.

## Critérios de aceite

1. **API online**
   - **Dado** que a API está no ar
   - **Quando** acesso a rota `/versao`
   - **Então** vejo, junto da versão, o status "🟢 API online"

2. **API offline**
   - **Dado** que a API está fora do ar
   - **Quando** acesso a rota `/versao`
   - **Então** vejo o status "🔴 API offline" e a mensagem "Não foi possível obter a versão da API", sem a tela quebrar

3. **Verificação em andamento**
   - **Dado** que acabei de abrir a rota `/versao`
   - **Quando** a API ainda não respondeu
   - **Então** vejo o status "Verificando conexão..." até a resposta chegar ou falhar

4. **Status coerente com o cabeçalho**
   - **Dado** que estou na tela `/versao`
   - **Quando** a verificação termina
   - **Então** o status mostrado na tela é igual ao do indicador `VersionInfo` do cabeçalho (online/offline)

5. **Sem regressão**
   - **Dado** que a nova funcionalidade foi entregue
   - **Quando** navego para `/`, `/about` e `/versao`
   - **Então** as telas continuam funcionando como antes, incluindo a versão exibida (ex: `Bia 4.3.0`) e o `VersionInfo` do cabeçalho

> O status é verificado ao abrir a tela (sem atualização automática periódica).

## Status

aceita

---

## Checklist de Atividades (Dev)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch `feat/005-status-conexao-api-tela-versao` a partir de `ia-main`
- [x] Exibir na tela `/versao` o status de conexão da API (verificando / online / offline)
- [x] Manter a mensagem de erro existente no cenário de API indisponível
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Implementação (Dev)

**Arquivo alterado:** `client/src/components/Versao.jsx` (somente frontend, sem novas dependências)

- Novo estado `status` (`checking` / `online` / `offline`), começando em `checking`.
- A verificação usa o mesmo critério do `VersionInfo` do cabeçalho: `GET /api/versao` com timeout de 5s (`AbortController`); resposta OK = online, erro, timeout ou resposta não OK = offline. Com isso, o status da tela é coerente com o indicador do cabeçalho.
- Texto exibido abaixo da versão: "Verificando conexão..." → "🟢 API online" ou "🔴 API offline".
- No cenário offline, a mensagem existente "Não foi possível obter a versão da API" foi mantida, sem quebrar a tela.
- A verificação roda só ao abrir a tela (sem atualização periódica), como a task pede.

**Evidências:**
- Build do client (`npm run build` em `client/`): `✓ built in 1.55s`, sem erros.
- Deploy local: `docker compose down && docker compose build && docker compose up -d` subiu os containers `bia`, `database` e `redis`.
- `curl -s http://localhost:3001/api/versao` → `Bia 4.3.0`
- Rotas do frontend: `/` 200, `/about` 200, `/versao` 200.
- O bundle servido (`assets/index-B22yl77t.js`) contém "Verificando conexão...", "API online", "API offline" e "Não foi possível obter a versão da API".
- Testes (`docker compose exec -T server npm test`, porque o host não tem `node_modules` na raiz): `Test Suites: 2 passed, Tests: 16 passed`.

> Observação para o QA: o cenário offline pode ser simulado abrindo `/versao` e bloqueando `/api/versao` no navegador (ou parando o container depois de a página carregar e recarregando com o bundle em cache), porque o frontend é servido pelo mesmo container da API.

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch da task (`git branch --show-current`)
- [x] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [x] Rodar a suíte de testes e registrar o resultado
- [x] Remover os dados de teste criados durante a validação
- [x] Testes no navegador: usar o navegador em container (`qa-browser`, ver `qa.md`) e encerrá-lo com `docker stop qa-browser` ao final, junto com qualquer servidor temporário
- [x] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [x] Mudar o status para `validada pelo QA` ou `com bugs`
- [x] Fazer commit e push no branch da task
- [x] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Validação QA

**Ambiente:** branch `feat/005-status-conexao-api-tela-versao` (commit `47ffa0f`), containers `bia`, `database` e `redis` em execução, bundle `assets/index-B22yl77t.js`. Navegador real: Firefox no container `qa-browser` (`selenium/standalone-firefox`, `--network host`), controlado via WebDriver na porta 4444.

**Como os estados da API foram simulados:** o Firefox do container foi configurado para usar um proxy HTTP temporário (scratchpad, porta 3999, não comitado). O proxy repassa tudo para `http://localhost:3001` sem alterar nada e muda só o comportamento de `GET /api/versao`: `online` (repassa), `slow` (atraso de 3s), `offline` (fecha a conexão sem responder, ou seja, API inalcançável), `503` (responde HTTP 503) e `hang` (atraso de 8s, acima do timeout de 5s do front). Nem o código da aplicação nem o bundle foram alterados.

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | API online | ✅ | `/versao` com a API no ar mostra no card: `Versão / Bia 4.3.0 / 🟢 API online`. Log do proxy: `GET http://localhost:3001/api/versao 200`. |
| 2 | API offline | ✅ | Com a conexão de `/api/versao` fechada pelo proxy, o card mostra `Não foi possível obter a versão da API` e `🔴 API offline` (estado final em 0,24s). A tela não quebrou: título `BIA + IA`, cabeçalho e botão `← Voltar` continuam renderizados (screenshot `2-offline`). O mesmo resultado aparece com HTTP 503 e com timeout de 8s (o front aborta em cerca de 5s e mostra offline). |
| 3 | Verificação em andamento | ✅ | Com atraso de 3s, 0,8s depois de abrir a página o card mostra `Carregando... / Verificando conexão...` (screenshot `3-verificando`). Depois que a resposta chega, muda para `🟢 API online` (em cerca de 2,2s). Com atraso de 8s, aparece `Verificando conexão...` aos 2s e depois `🔴 API offline`, no tempo do timeout de 5s. |
| 4 | Status coerente com o cabeçalho | ✅ | Comparação do texto do card com a classe e o ícone do botão `.version-trigger` (`VersionInfo`) em todos os cenários. Online: card `🟢 API online`, cabeçalho `version-trigger online | 🟢`. Offline (conexão fechada, 503 e timeout): card `🔴 API offline`, cabeçalho `version-trigger offline | 🔴`. Verificando: card `Verificando conexão...`, cabeçalho `version-trigger checking | 🟡`. Os dois estados ficaram iguais em todas as medições. |
| 5 | Sem regressão | ✅ | `/`: lista de tarefas e formulário `Add New Task` renderizados, cabeçalho 🟢. `/about`: conteúdo do evento e links renderizados, cabeçalho 🟢. `/versao`: `Bia 4.3.0` + `🟢 API online`. Tooltip do `VersionInfo`: `Bia 4.3.0 / Status: Online / API: http://localhost:3001`. `curl http://localhost:3001/api/versao` → `Bia 4.3.0`. |

**Suíte de testes:** `docker compose exec -T server npm test` → `Test Suites: 2 passed, 2 total` / `Tests: 16 passed, 16 total`.

**Limpeza:** nenhum dado foi criado no banco (`/api/tarefas` → `{"data":[]}`). O container `qa-browser` foi encerrado com `docker stop qa-browser` e o proxy temporário foi finalizado. `docker ps` mostra só `bia`, `database` e `redis`.

## Bugs

Nenhum bug encontrado.

## Finalização (PO)

- [x] Verificar se tudo foi implementado conforme o escopo técnico
- [x] Verificar se todos os itens do checklist foram marcados como concluídos
- [x] Confirmar que o status da task é `validada pelo QA` (se estiver `com bugs`, devolver ao agent responsável)
- [x] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, mudar o status para `recusada` com o motivo e devolver ao agent responsável (a task continua em `doing/`)
- [x] Confirmar que a aplicação está buildando e funcionando corretamente
- [x] Se tudo estiver ok:
  - [x] Informar ao usuário que a task está finalizada (resumo do que foi verificado) e **aguardar o OK do usuário** para continuar
  - [x] Após o OK, confirmar que está no branch `feat/005-status-conexao-api-tela-versao` (não em `ia-main` nem em `main`)
  - [x] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [x] Fazer commit e push final no branch da task
  - [x] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[005] - feat: status de conexão da API na tela de versão` (rodar `git branch --show-current` imediatamente antes do `gh pr create`)
  - [x] Fazer o merge do PR em `ia-main` com **squash**
  - [x] Voltar para `ia-main`, atualizar (`git pull`), limpar referências (`git fetch --prune`) e apagar o branch local da task
  - [x] Enviar ao usuário o link do PR e o commit do merge

**Aceite do PO:**

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | API online | ✅ | `Versao.jsx` exibe "🟢 API online" com resposta OK; QA viu `Bia 4.3.0` + `🟢 API online` no navegador |
| 2 | API offline | ✅ | `catch` exibe "🔴 API offline" + "Não foi possível obter a versão da API"; QA validou conexão recusada, HTTP 503 e timeout, sem quebrar a tela |
| 3 | Verificação em andamento | ✅ | Estado inicial `checking` → "Verificando conexão..."; QA viu o texto com resposta atrasada |
| 4 | Status coerente com o cabeçalho | ✅ | Mesmo critério do `VersionInfo` (timeout 5s, resposta OK); QA comparou tela × cabeçalho em todos os cenários |
| 5 | Sem regressão | ✅ | `/`, `/about` e `/versao` funcionando, `VersionInfo` inalterado, 16 testes passando |
