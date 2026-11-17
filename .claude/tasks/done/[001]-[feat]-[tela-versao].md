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

aceita

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

**Branch/commit validado:** `feat/001-tela-versao` @ `81bdd76` — containers `bia`, `database` e `redis` rodando via `docker compose`.

**Como foi validado:** teste E2E em navegador real (Firefox headless controlado por WebDriver/`geckodriver`), clicando e lendo o DOM renderizado pelo React — não só o HTML estático devolvido pelo `curl`.

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | Acesso pela rota | ✅ | `GET http://localhost:3001/versao` no navegador → card com `h3` = `Versão` e `h4` = `Bia 4.3.0`, idêntico a `curl -s http://localhost:3001/api/versao` → `Bia 4.3.0` |
| 2 | Acesso pelo menu | ✅ | Clique no link `Versão` do `<header>` a partir de `/`, `/about` e da própria `/versao` → URL final `http://localhost:3001/versao` e título `Versão` nas três telas |
| 3 | Versão igual à do projeto | ✅ | Tela exibe `Bia 4.3.0`; `node -p "require('./package.json').version"` → `4.3.0` |
| 4 | API indisponível | ✅ | Falha simulada (ver abaixo): a tela mostra `Não foi possível obter a versão da API`; título `Versão`, cabeçalho e botão `← Voltar` continuam renderizados (sem tela branca). O `VersionInfo` mostra 🔴 offline, coerente com o cenário |
| 5 | Sem regressão | ✅ | `/`: `h1` `BIA`, formulário de nova tarefa e lista/empty-state renderizados; `VersionInfo` passa de `checking` para `online` e o tooltip mostra `Bia 4.3.0`. `/about`: conteúdo, `VersionInfo` e botão voltar presentes. `curl` em `/`, `/about`, `/versao` e `/api/tarefas` → HTTP 200 |

**Como o critério 4 foi simulado (reproduzível):**

```bash
# 1. Build do front apontando para uma API inalcançável (porta 9 não tem nada escutando)
cd client && VITE_API_URL=http://localhost:9 npx vite build --outDir /tmp/build-api-off --emptyOutDir
curl -s -m 2 http://localhost:9/api/versao   # exit 7 (conexão recusada) = API fora do ar

# 2. Servir esse build (com fallback de SPA) em outra porta
npx vite preview --outDir /tmp/build-api-off --port 4173

# 3. Abrir http://localhost:4173/versao no navegador
```

Resultado no DOM: `{"h3":"Versão","p":"Não foi possível obter a versão da API","header":true,"voltar":true}`.

**Saída do teste E2E:**

```
PASS - C1 titulo 'Versão' na tela /versao
PASS - C1 texto exibido == /api/versao ('Bia 4.3.0')
PASS - C3 versão exibida corresponde ao package.json (4.3.0)
PASS - C2 link 'Versão' a partir de /
PASS - C2 link 'Versão' a partir de /about
PASS - C2 link 'Versão' a partir de /versao
PASS - C5 / renderiza cabeçalho, formulário e lista/empty-state
PASS - C5 VersionInfo online e tooltip mostra a versão da API
PASS - C5 /about renderiza conteúdo, VersionInfo e botão voltar
PASS - C4 mensagem de erro exibida
PASS - C4 tela não quebra (título, cabeçalho e botão voltar presentes)
PASS - C4 VersionInfo indica API offline (coerente)
```

**Testes unitários:** `docker compose exec -T server npm test` → `Test Suites: 2 passed, 2 total` / `Tests: 16 passed, 16 total`.
Nenhum teste unitário novo: a suíte Jest do projeto (`tests/unit/`) cobre só o backend em CommonJS; testar o componente React com Jest exigiria configurar Babel/jsdom e tratar `import.meta.env`, o que foge da simplicidade do projeto. Por isso a validação do front foi feita em navegador real.

**Observações (não bloqueiam o aceite):**
- A versão retornada por `/api/versao` está fixa em `api/controllers/versao.js` (`"4.3.0"`, ou `VERSAO_API`), não é lida do `package.json`. Hoje bate com o `package.json`, mas se só o `package.json` for atualizado, o critério 3 deixa de valer. Fora do escopo desta task (backend não foi alterado); fica como sugestão de task futura.
- O link `Versão` no cabeçalho usa a classe CSS `footer-link`. Funciona, só vale considerar uma classe própria do header se o estilo precisar mudar.

## Bugs

Nenhum bug encontrado.

## Finalização (PO)

- [x] Verificar se tudo foi implementado conforme o escopo
- [x] Verificar se todos os itens do checklist foram marcados como concluídos
- [x] Confirmar que o status da task é `validada pelo QA` (se `com bugs`, devolver ao Dev)
- [x] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, status `recusada` com motivo e devolver ao Dev
- [x] Confirmar que a aplicação está buildando e funcionando corretamente
- [x] Se tudo estiver ok:
  - [x] Informar ao usuário que a task está finalizada e **aguardar o OK**
  - [x] Após o OK, confirmar que está no branch `feat/001-tela-versao`
  - [x] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/` com `git mv`
  - [x] Fazer commit e push final no branch da task
  - [x] Confirmar com `git branch --show-current` que está em `feat/001-tela-versao`
  - [x] Abrir o PR contra `ia-main` em `EvelynBonatto/bia` com título `[001] - feat: tela de versão`
  - [x] Enviar ao usuário o link do PR

**Aceite do PO:**

| # | Critério | Resultado | Evidência |
|---|----------|-----------|-----------|
| 1 | Acesso pela rota | ✅ | Rota `/versao` em `App.jsx`; `Versao.jsx` exibe título "Versão" e o texto de `/api/versao` (`Bia 4.3.0` no E2E do QA) |
| 2 | Acesso pelo menu | ✅ | Link "Versão" em `Header.jsx` (presente em todas as telas); E2E a partir de `/`, `/about` e `/versao` termina em `/versao` |
| 3 | Versão igual à do projeto | ✅ | Tela exibe `Bia 4.3.0`; `package.json` = `4.3.0` |
| 4 | API indisponível | ✅ | `catch` exibe "Não foi possível obter a versão da API"; falha simulada pelo QA sem quebrar a tela |
| 5 | Sem regressão | ✅ | `/` e `/about` funcionando, `VersionInfo` inalterado; 16 testes passando |
