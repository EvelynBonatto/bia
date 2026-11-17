# [001] - feat: Tela de versão da aplicação

## História de usuário

Como **aluno da Formação AWS**, quero **acessar uma tela no BIA que mostre a versão da aplicação**, para **confirmar, sem usar terminal, qual versão está publicada no ambiente que estou testando**.

## Critérios de aceite

1. **Acesso pela rota**
   - **Dado** que a aplicação está rodando
   - **Quando** acesso a rota `/versao` no navegador
   - **Então** vejo uma tela dedicada com o título "Versão" e o texto retornado por `/api/versao` (ex: `Bia 4.3.0`)

2. **Acesso pelo menu**
   - **Dado** que estou em qualquer tela da aplicação
   - **Quando** clico no link "Versão" do cabeçalho
   - **Então** sou levado para a rota `/versao`

3. **Versão igual à do projeto**
   - **Dado** que estou na tela `/versao`
   - **Quando** a API responde com sucesso
   - **Então** a versão exibida é igual ao campo `version` do `package.json` da raiz

4. **API indisponível**
   - **Dado** que a API está fora do ar
   - **Quando** acesso a rota `/versao`
   - **Então** vejo a mensagem "Não foi possível obter a versão da API", sem a tela quebrar

5. **Sem regressão**
   - **Dado** que a nova tela foi entregue
   - **Quando** navego para `/` e `/about`
   - **Então** as telas continuam funcionando como antes, incluindo o indicador de versão (`VersionInfo`) já existente

## Status

pronta para aceite

---

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main`
- **Nome do branch:** `feat/001-tela-versao`
- **Agent responsável:** `dev` (.claude/agents/dev.md) — altera apenas `client/`
- **Fluxo do agent responsável:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch `feat/001-tela-versao` a partir de `ia-main`
  5. Implementar a funcionalidade

## Checklist de Atividades (Dev)

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch `feat/001-tela-versao` a partir de `ia-main`
- [x] Criar a tela de versão consumindo `/api/versao`
- [x] Registrar a rota `/versao` no React Router
- [x] Adicionar o link "Versão" no cabeçalho
- [x] Tratar o cenário de API indisponível com a mensagem definida
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Mudar o status para `pronta para aceite`
- [x] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Implementação (Dev)

**Branch:** `feat/001-tela-versao`

**O que foi feito:**
- Criado `client/src/components/Versao.jsx`: tela com título "Versão" que busca `/api/versao` com a mesma lógica de URL da API do `VersionInfo` (`VITE_API_URL` → origin na porta 8080 → `http://localhost:8080`). Se a requisição falhar (erro de rede ou status não-OK), exibe "Não foi possível obter a versão da API". Reaproveita as classes CSS da tela About (`about-page`, `feature-card`, `back-button`), sem CSS novo.
- `client/src/App.jsx`: registrada a rota `/versao`.
- `client/src/components/Header.jsx`: adicionado o link "Versão" (`<Link to="/versao">`) ao lado do `VersionInfo`, que continua inalterado.

**Evidências:**
- Deploy local `docker compose down && docker compose build && docker compose up -d`: build do Vite ok (`✓ 58 modules transformed`, `✓ built`), containers `bia`, `database` e `redis` iniciados.
- `curl -s http://localhost:3001/api/versao` → `Bia 4.3.0` (igual ao `version` 4.3.0 do `package.json`).
- `curl` em `/`, `/about` e `/versao` → HTTP 200 (`/versao` serve o `index.html` do SPA).
- Mensagem "Não foi possível obter a versão da API" presente no bundle buildado.
- `npm test` (dentro do container `server`): 2 suítes, 16 testes passando.
- Observação para o QA: como frontend e API são servidos pelo mesmo container, o cenário "API indisponível" precisa ser simulado (ex.: frontend apontando para uma `VITE_API_URL` inválida ou bloqueando a requisição no DevTools).

## Validação QA

_(preenchido pelo QA)_

## Finalização (PO)

- [ ] Verificar se tudo foi implementado conforme o escopo
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que o status da task é `validada pelo QA` (se `com bugs`, devolver ao Dev)
- [ ] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, status `recusada` com motivo e devolver ao Dev
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada e **aguardar o OK**
  - [ ] Após o OK, confirmar que está no branch `feat/001-tela-versao`
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [ ] Fazer commit e push final no branch da task
  - [ ] Confirmar com `git branch --show-current` que está em `feat/001-tela-versao`
  - [ ] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[001] - feat: tela de versão`
  - [ ] Enviar ao usuário o link do PR
