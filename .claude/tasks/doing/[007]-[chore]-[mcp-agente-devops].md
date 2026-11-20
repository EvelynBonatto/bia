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

aberta

---

## Checklist de Atividades (DevOps)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [ ] Criar o branch `chore/007-mcp-agente-devops` a partir de `ia-main`
- [ ] Declarar o `aws-mcp` (com `AWS_PROFILE=formacaoaws`, `us-east-1`) no cabeçalho de `.claude/agents/devops.md`
- [ ] Declarar o `postgres` (banco local do `compose.yml`) no cabeçalho de `.claude/agents/devops.md`
- [ ] Validar uma consulta de leitura em cada MCP (AWS e Postgres)
- [ ] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [ ] Validar rota `/api/versao` respondendo corretamente
- [ ] Aplicação buildando sem erros
- [ ] Registrar na task o que foi feito e as evidências
- [ ] Mudar o status para `pronta para aceite`
- [ ] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no branch da task (`git branch --show-current`)
- [ ] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [ ] Rodar a suíte de testes e registrar o resultado
- [ ] Remover os dados de teste criados durante a validação
- [ ] Testes no navegador: não aplicável (sem mudança de UI)
- [ ] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [ ] Mudar o status para `validada pelo QA` ou `com bugs`
- [ ] Fazer commit e push no branch da task
- [ ] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Validação QA

_(preenchido pelo QA)_

## Bugs

_(preenchido pelo QA, se houver)_

## Finalização (PO)

- [ ] Verificar se tudo foi implementado conforme o escopo técnico
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que o status da task é `validada pelo QA` (se estiver `com bugs`, devolver ao agent responsável)
- [ ] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, mudar o status para `recusada` com o motivo e devolver ao agent responsável (a task continua em `doing/`)
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada (resumo do que foi verificado) e **aguardar o OK do usuário** para continuar
  - [ ] Após o OK, confirmar que está no branch `chore/007-mcp-agente-devops` (não em `ia-main` nem em `main`)
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [ ] Fazer commit e push final no branch da task
  - [ ] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[007] - chore: MCP da AWS e do Postgres no agente devops` (rodar `git branch --show-current` imediatamente antes do `gh pr create`), conferindo se o check do workflow passou
  - [ ] Fazer o merge do PR em `ia-main` com **squash**
  - [ ] Voltar para `ia-main`, atualizar (`git pull`), limpar referências (`git fetch --prune`) e apagar o branch local da task
  - [ ] Enviar ao usuário o link do PR e o commit do merge
