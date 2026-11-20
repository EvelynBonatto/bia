# [007] - chore: MCP da AWS e do Postgres no agente devops

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `chore/007-mcp-agente-devops`
- **Agent responsável:** `devops` (.claude/agents/devops.md) — altera a configuração de ferramentas (MCP) do próprio agente
- **Fluxo do agent responsável:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch `chore/007-mcp-agente-devops` a partir de `ia-main`
  5. Implementar a funcionalidade
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).

## História de usuário

Como **aluna da Formação AWS**, quero **que o agente `devops` tenha os seus próprios servidores MCP (AWS e Postgres) declarados na definição dele**, para **que o acesso à infraestrutura e ao banco fique associado ao papel de DevOps, e não espalhado pelo projeto**.

## Critérios de aceite

1. **MCP da AWS no devops**
   - **Dado** que o agente `devops` foi acionado
   - **Quando** ele consulta a AWS pelo MCP `aws-mcp` (ex.: listar clusters ECS em `us-east-1`)
   - **Então** a consulta funciona usando o perfil `AWS_PROFILE=formacaoaws` e a região `us-east-1`

2. **MCP do Postgres no devops**
   - **Dado** que o agente `devops` foi acionado e o banco local do `compose.yml` está rodando
   - **Quando** ele consulta o banco `bia` pelo MCP `postgres` (ex.: listar as tabelas)
   - **Então** a consulta retorna as tabelas do banco local

3. **Configuração na definição do agente**
   - **Dado** o arquivo `.claude/agents/devops.md`
   - **Quando** leio o cabeçalho do agente
   - **Então** os servidores `aws-mcp` e `postgres` estão declarados ali

4. **Demais agentes e raiz sem alteração**
   - **Dado** que a task foi entregue
   - **Quando** comparo com o `ia-main` anterior
   - **Então** `.mcp.json` da raiz, `dev.md`, `qa.md` e `po.md` continuam iguais, e `.kiro/` não foi alterado

> **Referência técnica (Postgres local):** banco `bia`, usuário/senha `postgres`/`postgres`, porta `5433` no host (ver `compose.yml`). Uso apenas para o ambiente local.
>
> **Decisões do usuário:** `.kiro/` não é usado neste projeto (ignorar); manter `AWS_PROFILE=formacaoaws`; MCP apenas no `devops` por enquanto — os demais agentes e o `.mcp.json` da raiz serão definidos depois.

## Status

aceita

---

## Checklist de Atividades (DevOps)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch `chore/007-mcp-agente-devops` a partir de `ia-main`
- [x] Declarar o `aws-mcp` (com `AWS_PROFILE=formacaoaws`, `us-east-1`) no cabeçalho de `.claude/agents/devops.md`
- [x] Declarar o `postgres` (banco local do `compose.yml`) no cabeçalho de `.claude/agents/devops.md`
- [x] Validar uma consulta de leitura em cada MCP (AWS e Postgres)
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Registrar na task o que foi feito e as evidências
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch da task (`git branch --show-current`)
- [x] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [x] Rodar a suíte de testes e registrar o resultado
- [x] Remover os dados de teste criados durante a validação
- [x] Testes no navegador: não aplicável (sem mudança de UI)
- [x] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [x] Mudar o status para `validada pelo QA` ou `com bugs`
- [x] Fazer commit e push no branch da task
- [x] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Entrega DevOps

**Branch:** `chore/007-mcp-agente-devops`

### O que foi feito
- `.claude/agents/devops.md`: adicionado o campo `mcpServers` no frontmatter com dois servidores stdio definidos inline:
  - `aws-mcp`: `uvx mcp-proxy-for-aws@latest https://aws-mcp.us-east-1.api.aws/mcp --metadata AWS_REGION=us-east-1`, env `AWS_PROFILE=formacaoaws` (mesma configuração do `.mcp.json` da raiz).
  - `postgres`: `uvx --overrides .claude/mcp/postgres-overrides.txt --with "mcp<2" postgres-mcp --access-mode=unrestricted`, env `DATABASE_URI=postgresql://postgres:postgres@localhost:5433/bia` (banco local do `compose.yml`).
- `.claude/mcp/postgres-overrides.txt` (arquivo novo): override `pglast==7.24`.
  - **Por quê:** a configuração de referência (`.kiro/mcp-db.json`) não funciona mais. O `postgres-mcp` 0.3.0 (última versão no PyPI) fixa `pglast==7.2.0`, que foi removida do PyPI (hoje a série 7 só tem 7.20 a 7.24). Sem o override, o `uvx` não resolve a 0.3.0 e cai na 0.1.0, que não aceita `--access-mode` e trata o argumento como DSN (`invalid dsn: invalid connection option "--access-mode"`).
  - O caminho do override é relativo: o servidor precisa ser iniciado a partir da raiz do projeto (que é o comportamento padrão do Claude Code).

### Evidências
- **Critério 1 (aws-mcp):** servidor iniciado com a configuração lida do frontmatter do `devops.md`. Ferramentas expostas: `aws___run_script`, `aws___read_documentation`, `aws___search_documentation`, `aws___list_regions`, etc. Consulta de leitura via `aws___run_script` (ECS `ListClusters` + STS `GetCallerIdentity` em `us-east-1`):
  ```
  {"status": "success", "stdout": "[]\nuser/formacaoaws\n", ... "api_calls": [{"service": "ecs", "operation": "ListClusters", "status": "success", "n_items": {"clusterArns": 0}}, {"service": "sts", "operation": "GetCallerIdentity", "status": "success"}]}
  ```
  A chamada usou o perfil `formacaoaws`. Hoje não existe nenhum cluster ECS em `us-east-1`, por isso a lista vem vazia.
- **Critério 2 (postgres):** com o `compose.yml` rodando, `list_objects` (schema `public`, tipo `table`) retornou:
  ```
  [{'schema': 'public', 'name': 'SequelizeMeta', 'type': 'BASE TABLE'}, {'schema': 'public', 'name': 'Tarefas', 'type': 'BASE TABLE'}]
  ```
  Log do servidor: `Starting PostgreSQL MCP Server in UNRESTRICTED mode` / `Successfully connected to database`.
- **Critério 3:** `aws-mcp` e `postgres` estão declarados em `mcpServers` no frontmatter de `.claude/agents/devops.md` (YAML validado com `yaml.safe_load`).
- **Critério 4:** `git diff --stat ia-main -- .mcp.json .claude/agents/dev.md .claude/agents/qa.md .claude/agents/po.md .kiro/ .claude/settings.local.json` vazio.
- **Deploy local:** `docker compose down && docker compose build && docker compose up -d` sem erros; containers `bia`, `database` e `redis` em `Up`; `curl http://localhost:3001/api/versao` → `Bia 4.3.0` (igual ao `version` do `package.json`).

### Limitação da validação (registrada de forma explícita)
- Os MCPs **não foram carregados como ferramentas nativas nesta sessão do agente devops**: a definição do agente é lida quando ele é acionado, e a alteração foi feita durante a própria execução. A validação foi feita com um cliente MCP stdio (SDK Python `mcp<2`) que lê o frontmatter de `.claude/agents/devops.md` e sobe cada servidor com exatamente o `command`/`args`/`env` declarados ali (handshake `initialize`, `list_tools` e uma chamada de leitura).
- Para o QA: acionar o agente `devops` numa sessão nova e confirmar que as ferramentas `mcp__aws-mcp__*` e `mcp__postgres__*` aparecem e respondem.
- Esta máquina não é a `bia-dev`: o acesso à AWS foi pelo perfil `formacaoaws`, como a task pede.

## Validação QA

**Branch:** `chore/007-mcp-agente-devops` (`git branch --show-current`). Validação feita com um cliente MCP stdio próprio do QA (JSON-RPC puro, sem SDK, fora do repositório), que lê o frontmatter de `.claude/agents/devops.md` e sobe cada servidor com o `command`/`args`/`env` declarados ali, a partir da raiz do projeto (o script do DevOps não foi reaproveitado).

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | MCP da AWS no devops | ✅ | `aws-mcp` subiu como declarado (`uvx mcp-proxy-for-aws@latest https://aws-mcp.us-east-1.api.aws/mcp --metadata AWS_REGION=us-east-1`, env `AWS_PROFILE=formacaoaws`). `tools/list` → `aws___run_script`, `aws___list_regions`, `aws___read_documentation`, entre outras. `aws___run_script` com `call_boto3` ECS `ListClusters` + STS `GetCallerIdentity` → `{"status": "success", "stdout": "clusters: []\narn: user/formacaoaws\n", "api_calls": [{"service": "ecs", "operation": "ListClusters", "status": "success", ...}]}`. Conferência pela CLI: `AWS_PROFILE=formacaoaws aws ecs list-clusters --region us-east-1` também retorna a lista vazia, e o ARN é `user/formacaoaws`. |
| 2 | MCP do Postgres no devops | ✅ | Compose rodando (`bia`, `database` em `5433`, `redis`). `postgres` subiu como declarado; log: `Starting PostgreSQL MCP Server in UNRESTRICTED mode` / `Successfully connected to database`. `list_objects` (`public`, `table`) → `SequelizeMeta` e `Tarefas` (`BASE TABLE`), o mesmo resultado de `psql -U postgres -d bia -c '\dt'` direto no container `database`. |
| 3 | Configuração na definição do agente | ✅ | `yaml.safe_load` do frontmatter de `.claude/agents/devops.md` → `mcpServers` com `['aws-mcp', 'postgres']`, definidos inline (formato de lista `nome: config`). |
| 4 | Demais agentes e raiz sem alteração | ✅ | `git diff --stat ia-main -- .mcp.json .claude/agents/dev.md .claude/agents/qa.md .claude/agents/po.md .kiro/` vazio (igual contra `origin/ia-main`). O diff total contra `ia-main` mostra só `devops.md`, `.claude/mcp/postgres-overrides.txt` e a própria task. |

### Verificação independente do override (`.claude/mcp/postgres-overrides.txt`)
- **Sem override** (mesma linha de comando, só sem o `--overrides`, com `--refresh`): o `uvx` resolve `postgres-mcp` **0.1.0**, e o servidor encerra sem responder ao `initialize`: `Error connecting to database: invalid dsn: invalid connection option "--access-mode"`.
- **Forçando a 0.3.0 sem override** (`uvx --refresh --with "mcp<2" postgres-mcp==0.3.0`): `No solution found ... there is no version of pglast==7.2.0 and postgres-mcp==0.3.0 depends on pglast==7.2.0`.
- **Com override**: resolve `postgres-mcp` **0.3.0** com `pglast` **7.24** e funciona (critério 2).
- Conclusão: o diagnóstico do DevOps está correto e o arquivo extra é necessário.

### Testes e aplicação
- `npm test` (dentro do container `bia`, porque o `jest` não está instalado no host): **2 suítes, 16 testes, todos passando**.
- `curl http://localhost:3001/api/versao` → `Bia 4.3.0`.
- Dados de teste: nenhum foi criado (só consultas de leitura na AWS e no banco).
- Navegador: não aplicável (sem mudança de UI); o container `qa-browser` não foi usado.

### Limitações
- **Não confirmei que as ferramentas `mcp__aws-mcp__*` e `mcp__postgres__*` aparecem quando o agente `devops` é acionado pelo Claude Code.** A sessão do QA não carrega os MCPs do `devops`, e não acionei o agente `devops` para conferir. O que está comprovado: os servidores sobem e respondem com a configuração exata do frontmatter. Fica para o PO (ou numa sessão nova) acionar o `devops` e confirmar que as ferramentas estão disponíveis.
- O caminho do override é relativo (`.claude/mcp/postgres-overrides.txt`): o servidor só sobe se o Claude Code for iniciado a partir da raiz do projeto. Não é bug, porque esse é o uso esperado, mas vale saber.
- Esta máquina não é a `bia-dev`; o acesso à AWS foi pelo perfil `formacaoaws`, como a task pede.

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
  - [x] Após o OK, confirmar que está no branch `chore/007-mcp-agente-devops` (não em `ia-main` nem em `main`)
  - [x] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [x] Fazer commit e push final no branch da task
  - [x] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[007] - chore: MCP da AWS e do Postgres no agente devops` (rodar `git branch --show-current` imediatamente antes do `gh pr create`), conferindo se o check do workflow passou
  - [x] Fazer o merge do PR em `ia-main` com **squash**
  - [x] Voltar para `ia-main`, atualizar (`git pull`), limpar referências (`git fetch --prune`) e apagar o branch local da task
  - [x] Enviar ao usuário o link do PR e o commit do merge

**Aceite do PO:**

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | MCP da AWS no devops | ✅ | Verificação do PO, autorizada pela usuária: o agente `devops`, acionado numa sessão nova, recebeu as ferramentas nativas `mcp__aws-mcp__*`. Com `aws___run_script`, ECS `ListClusters` em `us-east-1` → `clusterArns: []` (a conta não tem cluster) e STS `GetCallerIdentity` → `user/formacaoaws` |
| 2 | MCP do Postgres no devops | ✅ | Na mesma sessão, o `devops` recebeu as ferramentas nativas `mcp__postgres__*`. `list_objects` (`public`) → `SequelizeMeta` e `Tarefas`; `execute_sql` → banco `bia`, usuário `postgres`, servidor no container do compose |
| 3 | Configuração na definição do agente | ✅ | `mcpServers` com `aws-mcp` e `postgres` no frontmatter de `.claude/agents/devops.md` |
| 4 | Demais agentes e raiz sem alteração | ✅ | `git diff --stat ia-main` → só `devops.md`, `.claude/mcp/postgres-overrides.txt` e a própria task |

**Observações (não bloqueiam o aceite):**
- O acesso à AWS usa o usuário IAM `formacaoaws` (credenciais próprias), e não a role da instância `bia-dev`, por decisão da usuária registrada na task. Se o projeto passar a rodar na `bia-dev`, vale uma task para trocar o perfil pela role.
- `.claude/mcp/postgres-overrides.txt` é necessário (confirmado pelo QA) e tem caminho relativo: o MCP do Postgres só sobe com o Claude Code aberto na raiz do projeto.
- Todas as chamadas AWS feitas na entrega e na validação foram de leitura (relatado pelos agentes; não conferido no CloudTrail, por decisão da usuária).
