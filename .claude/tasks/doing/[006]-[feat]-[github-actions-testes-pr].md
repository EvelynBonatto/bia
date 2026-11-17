# [006] - feat: GitHub Actions rodando os testes em todo PR contra ia-main

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `feat/006-github-actions-testes-pr`
- **Agent responsável:** `devops` (.claude/agents/devops.md) — cria `.github/workflows/`; os testes em `tests/` já existem e não são alterados
- **Fluxo do agent responsável:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch `feat/006-github-actions-testes-pr` a partir de `ia-main`
  5. Implementar a funcionalidade
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).

## História de usuário

Como **aluna da Formação AWS que entrega tasks por PR**, quero **que os testes da BIA rodem automaticamente em todo PR aberto contra `ia-main`**, para **saber, antes do merge, se a entrega quebrou algo, sem depender de rodar os testes na mão**.

## Critérios de aceite

1. **Executa em PR contra ia-main**
   - **Dado** um PR aberto contra `ia-main` no repositório `EvelynBonatto/bia`
   - **Quando** o PR é aberto ou recebe um novo push
   - **Então** o workflow roda automaticamente e executa `npm test` (suíte em `tests/unit`)

2. **Resultado visível no PR (sucesso)**
   - **Dado** que todos os testes passam
   - **Quando** o workflow termina
   - **Então** o PR mostra o check do workflow como ✅ sucesso, e o log exibe o resumo do Jest (ex: `Tests: 16 passed`)

3. **Resultado visível no PR (falha)**
   - **Dado** que algum teste falha
   - **Quando** o workflow termina
   - **Então** o PR mostra o check como ❌ falha, e o log indica qual teste falhou

4. **Não executa fora do escopo**
   - **Dado** um PR contra outro branch que não seja `ia-main`
   - **Quando** o PR é aberto
   - **Então** o workflow não é executado

5. **Simples e seguro**
   - **Dado** o arquivo do workflow em `.github/workflows/`
   - **Quando** leio o conteúdo
   - **Então** ele usa Node.js 24 (o mesmo do `Dockerfile`), não usa credenciais AWS nem segredos, e não altera `tests/`, `api/` nem `package.json`

> **Fora do escopo:** bloquear o merge quando os testes falham (regra de proteção de branch) e build do frontend. Podem virar tasks futuras.

## Status

pronta para aceite

---

## Checklist de Atividades (DevOps)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch `feat/006-github-actions-testes-pr` a partir de `ia-main`
- [x] Criar o workflow em `.github/workflows/` disparado por `pull_request` contra `ia-main`
- [x] Instalar dependências e executar `npm test` com Node.js 24
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Validar a execução do workflow no GitHub (`gh run list` / `gh run view`), abrindo um PR de teste do branch da task contra `ia-main` se necessário (o PR oficial continua sendo aberto pelo PO; não fazer merge)
- [x] Registrar na task o que foi feito e as evidências (link/ID da execução)
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no branch da task (`git branch --show-current`)
- [ ] Validar cada critério de aceite (Given/When/Then) com evidência objetiva (IDs/links das execuções no GitHub)
- [ ] Para o critério 3, provocar uma falha de forma temporária e desfazê-la em seguida, sem deixar alteração em `tests/` ou `api/` no branch ao final
- [ ] Rodar a suíte de testes e registrar o resultado
- [ ] Remover os dados de teste criados durante a validação (branches/PRs temporários, commits de falha)
- [ ] Testes no navegador: usar o navegador em container (`qa-browser`, ver `qa.md`) e encerrá-lo com `docker stop qa-browser` ao final, junto com qualquer servidor temporário
- [ ] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [ ] Mudar o status para `validada pelo QA` ou `com bugs`
- [ ] Fazer commit e push no branch da task
- [ ] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

## Implementação (DevOps)

**O que foi feito**
- Criado `.github/workflows/testes-pr.yml` (workflow `Testes da BIA`):
  - Gatilho: `pull_request` com `branches: [ia-main]` (eventos padrão `opened`, `synchronize`, `reopened`) — PRs contra outros branches não disparam (critério 4)
  - Job `testes` em `ubuntu-latest`: `actions/checkout@v4` → `actions/setup-node@v4` com `node-version: 24` → `npm ci --loglevel=error` → `npm test`
  - Sem credenciais AWS, sem `secrets`, sem alteração em `tests/`, `api/` ou `package.json`
- Falha de qualquer teste faz o `jest` sair com código != 0, o step `Executar os testes` falha e o check fica ❌ com o teste falho no log (critério 3, a ser provocado pelo QA)

**Evidências**
- Testes locais com Node.js 24 (`node:24.18.0-slim`, `npm ci` + `npm test`): `Test Suites: 2 passed` / `Tests: 16 passed, 16 total`
- Deploy local (`docker compose down && docker compose build && docker compose up -d`): build sem erros; `curl http://localhost:3001/api/versao` → `Bia 4.3.0`
- PR de validação: https://github.com/EvelynBonatto/bia/pull/6 (contra `ia-main`, sem merge — reaproveitado pelo PO)
- Execução do workflow: run `44175043004` — https://github.com/EvelynBonatto/bia/actions/runs/44175043004 — evento `pull_request`, `completed / success`, 24s
  - Node usado: `24.22.2` (cache do runner)
  - Log do step `Executar os testes`: `Test Suites: 2 passed, 2 total` / `Tests: 16 passed, 16 total`
  - `gh pr checks 6`: `testes pass`

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
  - [ ] Após o OK, confirmar que está no branch `feat/006-github-actions-testes-pr` (não em `ia-main` nem em `main`)
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [ ] Fazer commit e push final no branch da task
  - [ ] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[006] - feat: GitHub Actions rodando os testes em todo PR contra ia-main` (rodar `git branch --show-current` imediatamente antes do `gh pr create`), conferindo se o check do workflow passou
  - [ ] Fazer o merge do PR em `ia-main` com **squash**
  - [ ] Voltar para `ia-main`, atualizar (`git pull`), limpar referências (`git fetch --prune`) e apagar o branch local da task
  - [ ] Enviar ao usuário o link do PR e o commit do merge
