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

aberta

---

## Checklist de Atividades (Dev)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [ ] Fazer commit e push no branch `ia-main` (task + sequencial)
- [ ] Criar o branch `feat/005-status-conexao-api-tela-versao` a partir de `ia-main`
- [ ] Exibir na tela `/versao` o status de conexão da API (verificando / online / offline)
- [ ] Manter a mensagem de erro existente no cenário de API indisponível
- [ ] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [ ] Validar rota `/api/versao` respondendo corretamente
- [ ] Aplicação buildando sem erros
- [ ] Mudar o status para `pronta para aceite`
- [ ] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

- [ ] Confirmar que está no branch da task (`git branch --show-current`)
- [ ] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [ ] Rodar a suíte de testes e registrar o resultado
- [ ] Remover os dados de teste criados durante a validação
- [ ] Testes no navegador: usar o navegador em container (`qa-browser`, ver `qa.md`) e encerrá-lo com `docker stop qa-browser` ao final, junto com qualquer servidor temporário
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
  - [ ] Após o OK, confirmar que está no branch `feat/005-status-conexao-api-tela-versao` (não em `ia-main` nem em `main`)
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [ ] Fazer commit e push final no branch da task
  - [ ] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[005] - feat: status de conexão da API na tela de versão` (rodar `git branch --show-current` imediatamente antes do `gh pr create`)
  - [ ] Fazer o merge do PR em `ia-main` com **squash**
  - [ ] Voltar para `ia-main`, atualizar (`git pull`), limpar referências (`git fetch --prune`) e apagar o branch local da task
  - [ ] Enviar ao usuário o link do PR e o commit do merge
