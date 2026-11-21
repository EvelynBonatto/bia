# [007] - chore: MCPs dos agentes (AWS e Postgres no devops, shadcn no dev, Playwright no qa)

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `chore/007-mcp-agentes`
- **Agent responsável:** `devops` (.claude/agents/devops.md) — configura as ferramentas (MCP) dos agentes. A parte do shadcn no `dev.md` foi feita pelo próprio `dev`
- **Fluxo do agent responsável:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch `chore/007-mcp-agentes` a partir de `ia-main`
  5. Implementar a funcionalidade
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).

> **Task reaberta (decisão da usuária, 20/11/2026):** a 1ª entrega (MCP da AWS e do Postgres no `devops`) já foi aceita e integrada no `ia-main` pelo PR #9 (`80d6d7c`). A usuária pediu que o MCP do shadcn no `dev` e o MCP do Playwright no `qa` (antes rascunhados como tasks 008 e 009) fossem incluídos nesta task, em vez de virarem tasks novas. O histórico do `ia-main` não é reescrito: a ampliação entra num segundo PR `[007]`.
>
> **Exceção ao fluxo (autorizada pela usuária):** a 2ª entrega foi implementada **só no working tree**, sem commit, push ou branch, para a usuária testar antes. O registro no `ia-main` e o branch `chore/007-mcp-agentes` só acontecem com o OK dela.

## História de usuário

Como **aluna da Formação AWS**, quero **que cada agente tenha os seus próprios servidores MCP declarados na definição dele** (`devops`: AWS e Postgres; `dev`: shadcn; `qa`: Playwright), para **que cada ferramenta fique associada ao papel que a usa, e não espalhada pelo projeto**.

## Critérios de aceite

### 1ª entrega — devops (aceita no PR #9)

1. **MCP da AWS no devops**
   - **Dado** que o agente `devops` foi acionado
   - **Quando** ele consulta a AWS pelo MCP `aws-mcp` (ex.: listar clusters ECS em `us-east-1`)
   - **Então** a consulta funciona usando o perfil `AWS_PROFILE=formacaoaws` e a região `us-east-1`

2. **MCP do Postgres no devops**
   - **Dado** que o agente `devops` foi acionado e o banco local do `compose.yml` está rodando
   - **Quando** ele consulta o banco `bia` pelo MCP `postgres` (ex.: listar as tabelas)
   - **Então** a consulta retorna as tabelas do banco local

3. **Configuração na definição do devops**
   - **Dado** o arquivo `.claude/agents/devops.md`
   - **Quando** leio o cabeçalho do agente
   - **Então** os servidores `aws-mcp` e `postgres` estão declarados ali

### 2ª entrega — dev e qa

4. **MCP do shadcn no dev**
   - **Dado** que o agente `dev` foi acionado
   - **Quando** ele consulta o registry do shadcn pelo MCP `shadcn` (ex.: buscar o componente `button`)
   - **Então** a consulta retorna as informações do componente

5. **Configuração na definição do dev**
   - **Dado** o arquivo `.claude/agents/dev.md`
   - **Quando** leio o cabeçalho do agente
   - **Então** o servidor `shadcn` está declarado ali

6. **MCP do Playwright no qa**
   - **Dado** que o agente `qa` foi acionado e a aplicação do `compose.yml` está rodando
   - **Quando** ele abre `http://localhost:3001` pelo MCP `playwright`
   - **Então** ele consegue ler o conteúdo da página inicial (ex.: título ou texto visível)

7. **Navegador encerrado ao final**
   - **Dado** que o `qa` terminou de usar o MCP do Playwright
   - **Quando** confiro os processos e containers da máquina
   - **Então** não fica nenhum navegador aberto pelo teste

8. **Configuração na definição do qa**
   - **Dado** o arquivo `.claude/agents/qa.md`
   - **Quando** leio o cabeçalho do agente
   - **Então** o servidor `playwright` está declarado ali, e o texto do `qa.md` explica quando usá-lo

### Geral

9. **Raiz, PO e aplicação sem alteração**
   - **Dado** que a task foi entregue
   - **Quando** comparo com o `ia-main` anterior
   - **Então** `.mcp.json` da raiz, `po.md`, `package.json`, `client/` e `.kiro/` continuam iguais

> **Referência técnica (Postgres local):** banco `bia`, usuário/senha `postgres`/`postgres`, porta `5433` no host (ver `compose.yml`). Uso apenas para o ambiente local.
>
> **Decisões do usuário:** `.kiro/` não é usado neste projeto (ignorar); manter `AWS_PROFILE=formacaoaws`; `.mcp.json` da raiz não é alterado.
>
> **Fora do escopo:** instalar o shadcn/ui ou o Tailwind no `client/`; testes automatizados com Playwright guardados no projeto (ex.: `tests/e2e/`); mudanças no pipeline.
>
> **Decisão pendente:** a usuária ainda não definiu se o MCP do Playwright **substitui** o navegador em container (`qa-browser`, Selenium) ou se os **dois ficam**. Até essa definição, as instruções do `qa-browser` no `qa.md` são mantidas.

## Status

pronta para aceite

---

## Checklist de Atividades (DevOps)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

### 1ª entrega (PR #9)
- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch `chore/007-mcp-agente-devops` a partir de `ia-main`
- [x] Declarar o `aws-mcp` (com `AWS_PROFILE=formacaoaws`, `us-east-1`) no cabeçalho de `.claude/agents/devops.md`
- [x] Declarar o `postgres` (banco local do `compose.yml`) no cabeçalho de `.claude/agents/devops.md`
- [x] Validar uma consulta de leitura em cada MCP (AWS e Postgres)
- [x] Executar deploy local, validar `/api/versao` e build sem erros
- [x] Registrar na task o que foi feito e as evidências

### 2ª entrega (local, aguardando OK da usuária para registrar)
- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Fazer commit e push no branch `ia-main` (task reaberta em `doing/` + sequencial)
- [x] Criar o branch `chore/007-mcp-agentes` a partir de `ia-main`
- [x] (dev) Declarar o `shadcn` no cabeçalho de `.claude/agents/dev.md`
- [x] (dev) Validar uma consulta ao registry do shadcn pelo MCP
- [x] Declarar o `playwright` no cabeçalho de `.claude/agents/qa.md`
- [x] Explicar no texto do `qa.md` quando usar o MCP do Playwright
- [x] Validar a abertura de `http://localhost:3001` pelo MCP e o encerramento do navegador
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Registrar na task o que foi feito e as evidências
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no branch da task (`git branch --show-current`)
- [ ] Validar cada critério de aceite da 2ª entrega (4 a 9) com evidência objetiva
- [ ] Rodar a suíte de testes e registrar o resultado
- [ ] Remover os dados de teste criados durante a validação
- [ ] Testes no navegador: usar o MCP do Playwright (objeto da task) e confirmar que nenhum navegador ficou aberto ao final
- [ ] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [ ] Mudar o status para `validada pelo QA` ou `com bugs`
- [ ] Fazer commit e push no branch da task
- [ ] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Entrega DevOps — 1ª entrega (PR #9)

**Branch:** `chore/007-mcp-agente-devops`

- `.claude/agents/devops.md`: campo `mcpServers` no frontmatter com dois servidores stdio:
  - `aws-mcp`: `uvx mcp-proxy-for-aws@latest https://aws-mcp.us-east-1.api.aws/mcp --metadata AWS_REGION=us-east-1`, env `AWS_PROFILE=formacaoaws`.
  - `postgres`: `uvx --overrides .claude/mcp/postgres-overrides.txt --with "mcp<2" postgres-mcp --access-mode=unrestricted`, env `DATABASE_URI=postgresql://postgres:postgres@localhost:5433/bia`.
- `.claude/mcp/postgres-overrides.txt`: override `pglast==7.24`. O `postgres-mcp` 0.3.0 fixa `pglast==7.2.0`, removida do PyPI; sem o override o `uvx` cai na 0.1.0, que não aceita `--access-mode`. Caminho relativo: o Claude Code precisa ser aberto na raiz do projeto.
- Evidências: `aws___run_script` com ECS `ListClusters` (`[]`) e STS `GetCallerIdentity` (`user/formacaoaws`) em `us-east-1`; `list_objects` no Postgres → `SequelizeMeta` e `Tarefas`; deploy local ok e `/api/versao` → `Bia 4.3.0`.

## Entrega Dev — shadcn no dev (2ª entrega, local)

**Branch:** `chore/007-mcp-agentes` (implementado antes só no working tree do `ia-main`, sem commit — exceção autorizada pela usuária).

### O que foi feito
- `.claude/agents/dev.md`, frontmatter: `mcpServers` com o servidor `shadcn` (stdio, sem `env`), no mesmo formato do `devops.md`:
  ```yaml
  mcpServers:
    - shadcn:
        type: stdio
        command: npx
        args:
          - "shadcn@latest"
          - "mcp"
  ```

### Evidências
Cliente MCP stdio (JSON-RPC puro, script no scratchpad) que lê o frontmatter do `dev.md` e sobe o servidor a partir da raiz do projeto. `shadcn` 4.23.0.
- **Handshake:** `initialize` → `{"name":"shadcn","version":"1.0.0"}`, protocolo `2024-11-05`.
- **tools/list:** 7 ferramentas: `get_project_registries`, `list_items_in_registries`, `search_items_in_registries`, `view_items_in_registries`, `get_item_examples_from_registries`, `get_add_command_for_items`, `get_audit_checklist`.
- **Critério 4:** `search_items_in_registries` (`@shadcn`, `"button"`) → 33 itens, o primeiro `button (registry:ui)`; `view_items_in_registries` (`@shadcn/button`) → `Type: registry:ui`, 1 arquivo, dependências `cn, radix-ui`; `get_add_command_for_items` → `npx shadcn@latest add @shadcn/button`.
- **Critério 5:** `shadcn` em `mcpServers` no frontmatter (YAML validado com `yaml.safe_load`).
- **Deploy local:** sem erros; `bia`, `database` e `redis` em `Up`; `/api/versao` → `Bia 4.3.0`; `npm test` no container `bia`: 2 suítes, 16 testes passando.
- Teste da usuária numa sessão nova: o `dev` recebeu as ferramentas nativas e usou `mcp__shadcn__search_items_in_registries` (busca 'button' em `@shadcn`, 33 itens) e `mcp__shadcn__view_items_in_registries` (`@shadcn/button`: `registry:ui`, 1 arquivo, deps `cn` e `radix-ui`).

### Limitações
- `components.json` **não é necessário** para consultar o registry e não foi criado (nem na raiz nem em `client/`). A consulta precisa citar o registry (`registries: ["@shadcn"]` ou o prefixo `@shadcn/`); sem o arquivo, `get_project_registries` volta vazio. Isso só muda se o shadcn/ui for instalado no `client/` (fora do escopo).
- As ferramentas `mcp__shadcn__*` não foram carregadas numa sessão do `dev` (a definição é lida quando o agente é acionado). Para o QA: acionar o `dev` numa sessão nova e confirmar.
- `shadcn@latest` baixa a versão mais recente a cada início (precisa de internet).

## Entrega DevOps — Playwright no qa (2ª entrega, local)

**Branch:** `chore/007-mcp-agentes` (implementado antes só no working tree do `ia-main`, sem commit — exceção autorizada pela usuária).

### O que foi feito
- `.claude/agents/qa.md`, frontmatter: `mcpServers` com o servidor `playwright` (stdio):
  `npx @playwright/mcp@latest --browser chromium --headless --isolated --output-dir /tmp/playwright-mcp`
- `.claude/agents/qa.md`, texto: nova subseção **MCP do Playwright** em "Testes no navegador" (quando usar, `browser_navigate`/`browser_snapshot`, `browser_install` se faltar o navegador, `browser_close` e conferência com `pgrep -af ms-playwright`). As instruções do `qa-browser` foram **mantidas** (decisão pendente).

### Por que essa configuração
- `--browser chromium`: Chromium baixado e gerenciado pelo Playwright (`~/.cache/ms-playwright`); **não usa o Firefox/`geckodriver` do snap**. É processo filho do servidor MCP e termina junto com ele.
- `--headless`: sem janela.
- `--isolated`: perfil em memória, sem estado entre execuções.
- `--output-dir /tmp/playwright-mcp`: tira os arquivos gerados da raiz do repositório (o padrão seria `.playwright-mcp/`, que o `.gitignore` também já ignora).
- Alternativa não escolhida: navegador em container (`--cdp-endpoint`), mais complexo para o aluno.

### Evidências
Cliente MCP stdio (JSON-RPC puro, script no scratchpad) que lê o frontmatter do `qa.md` e sobe o servidor a partir da raiz do projeto.
- **Handshake:** `serverInfo: {name: Playwright, version: 1.66.0-alpha-2026-11-18}` (`@playwright/mcp` 0.0.86), protocolo `2025-06-18`; 25 ferramentas, entre elas `browser_navigate`, `browser_snapshot`, `browser_close`.
- **Critério 6:** `browser_navigate` em `http://localhost:3001` → `Page Title: BIA + IA`; o snapshot mostra o heading "BIA", o campo "O que você precisa fazer?", o botão "Add New Task", a tarefa "Teste QA navegador" e o link "Sobre a BIA". Console: `API GET - 200 http://localhost:3001/api/tarefas`. Só leitura (a tarefa continua com o mesmo `uuid` e `updatedAt`).
- **Critério 7:** durante o teste, `pgrep -af ms-playwright` mostrava o `chrome --headless`; depois de `browser_close` e do fim do servidor (`exit 0`), `pgrep -af 'ms-playwright|playwright-mcp|playwright/mcp'` → nenhum processo. Encerrando o cliente sem `browser_close`, o navegador também terminou. `docker ps` → só `bia`, `database` e `redis`.
- **Critério 8:** `playwright` em `mcpServers` no frontmatter (YAML validado); o texto explica quando usar.
- **Deploy local:** sem erros; `/api/versao` → `Bia 4.3.0`.

### Limitações
- As ferramentas `mcp__playwright__*` não foram carregadas numa sessão do `qa`. Para o QA: acionar o `qa` numa sessão nova e confirmar.
- Numa máquina nova (ex.: `bia-dev`), o Chromium pode precisar de bibliotecas do sistema (`npx playwright install-deps chromium`, com sudo); não testado.
- Com `@latest`, uma versão futura pode pedir outra revisão do Chromium (resolver com `browser_install`).

## Validação QA

### 1ª entrega (PR #9)

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | MCP da AWS no devops | ✅ | `aws___run_script` com ECS `ListClusters` + STS `GetCallerIdentity` → `success`, `clusters: []`, `arn: user/formacaoaws` |
| 2 | MCP do Postgres no devops | ✅ | `list_objects` (`public`, `table`) → `SequelizeMeta` e `Tarefas`, igual ao `psql \dt` no container |
| 3 | Configuração na definição do devops | ✅ | `mcpServers` com `aws-mcp` e `postgres` no frontmatter de `devops.md` |

O override `.claude/mcp/postgres-overrides.txt` foi verificado como necessário. `npm test`: 2 suítes, 16 testes passando.

### 2ª entrega

_(preenchido pelo QA)_

## Bugs

_(preenchido pelo QA, se houver)_

## Finalização (PO)

### 1ª entrega — aceita (PR #9, `80d6d7c`)

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | MCP da AWS no devops | ✅ | `devops` numa sessão nova recebeu `mcp__aws-mcp__*`; `ListClusters` → `[]`, `GetCallerIdentity` → `user/formacaoaws` |
| 2 | MCP do Postgres no devops | ✅ | `devops` recebeu `mcp__postgres__*`; `list_objects` → `SequelizeMeta` e `Tarefas` |
| 3 | Configuração na definição do devops | ✅ | `mcpServers` com `aws-mcp` e `postgres` em `devops.md` |

### 2ª entrega

- [ ] Verificar se tudo foi implementado conforme o escopo técnico
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que o status da task é `validada pelo QA` (se estiver `com bugs`, devolver ao agent responsável)
- [ ] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, mudar o status para `recusada` com o motivo e devolver ao agent responsável (a task continua em `doing/`)
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada (resumo do que foi verificado) e **aguardar o OK do usuário** para continuar
  - [ ] Após o OK, confirmar que está no branch `chore/007-mcp-agentes` (não em `ia-main` nem em `main`)
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [ ] Fazer commit e push final no branch da task
  - [ ] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[007] - chore: MCPs dos agentes (shadcn no dev e Playwright no qa)` (rodar `git branch --show-current` imediatamente antes do `gh pr create`), conferindo se o check do workflow passou
  - [ ] Fazer o merge do PR em `ia-main` com **squash**
  - [ ] Voltar para `ia-main`, atualizar (`git pull`), limpar referências (`git fetch --prune`) e apagar o branch local da task
  - [ ] Enviar ao usuário o link do PR e o commit do merge
