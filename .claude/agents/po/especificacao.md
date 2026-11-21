No seu trabalho de especificar tarefas, sempre que for pedida uma nova atividade, o resultado do seu trabalho deve ser a criação de um arquivo Markdown (.md).

Esse arquivo deve seguir estritamente o formato: `[025]-[feat]-[resumo].md`

Onde:

- **[025]**: Número sequencial da tarefa, sempre com 3 dígitos (ex: 001, 002, 025).
  - Esse controle sequencial será feito por um arquivo chamado sequencial.md
  - Nesse arquivo terá apenas o texto (Última Task: [002].)
  - Você vai sempre usar o sequencial seguinte e incrementar o valor Última Task.
- **[feat]**: Tipo da tarefa (ex: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`).
- **[resumo]**: Resumo curto da tarefa em letras minúsculas, com as palavras separadas por hífens.

**Localização e Gestão de Estado:**

- Os arquivos devem ser criados na pasta `.claude/tasks` (na pasta principal do projeto, que fica sempre no `ia-main`).
- **Toda task nasce com o seu worktree:** ao criar a task, o PO cria também o branch e o worktree dela (ver **Worktree da Task → Criação**).
- Você deve gerenciar o ciclo de vida dessas tarefas: quando uma tarefa for finalizada e aprovada, mova o arquivo correspondente para a pasta `.claude/tasks/done/` (dentro do worktree da task) e, depois do merge, remova o worktree.

**Pasta × Status:** a **pasta** indica a fase da task (a fazer / em andamento / concluída) e o campo **Status** indica o passo dentro da fase. Bugs e recusas **não mudam a pasta**: a task continua em `doing/` e volta para o agent responsável.

| Status | Pasta | Quem muda |
|---|---|---|
| `aberta` | `.claude/tasks/` | PO (cria a task) |
| `pronta para aceite` | `.claude/tasks/doing/` | Dev/DevOps (move para `doing/` ao iniciar e muda o status ao terminar) |
| `com bugs` | `.claude/tasks/doing/` | QA (devolve ao Dev/DevOps) |
| `validada pelo QA` | `.claude/tasks/doing/` | QA |
| `recusada` | `.claude/tasks/doing/` | PO (devolve ao Dev/DevOps) |
| `aceita` | `.claude/tasks/done/` | PO (no branch da task, após o OK do usuário) |

- Só existe task em `done/` com status `aceita`.

---

## Estrutura da Task (ordem das seções)

Toda task deve seguir esta ordem, com o modelo de trabalho **no início**:

1. **Título** (`# [NNN] - <tipo>: <resumo>`)
2. **Informações de Workflow** (logo após o título, antes de qualquer outra seção)
3. **História de usuário**
4. **Critérios de aceite**
5. **Status**
6. **Checklist de Atividades** do agent responsável (`Dev` ou `DevOps`)
7. **Checklist de Atividades (QA)** + seção **Validação QA**
8. **Finalização (PO)**

## Informações de Workflow

Toda task criada deve conter, **logo após o título**, uma seção de **Informações de Workflow** com as seguintes informações:

- **Modelo:** Feature/branch com worktree — cada task possui seu próprio branch e sua própria pasta de trabalho (ver **Worktree da Task**)
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `<tipo>/<NNN>-<resumo>` (ver **Padrão de Nomenclatura de Branch**)
- **Worktree:** `.claude/worktrees/<NNN>-<resumo>/` (criado pelo PO junto com a task)
- **Agent responsável:** `dev` (.claude/agents/dev.md) **ou** `devops` (.claude/agents/devops.md), conforme a tabela **Escolha do Agent Responsável**
- **Fluxo do agent responsável:**
  1. Na pasta principal do projeto, verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Entrar no worktree da task (`.claude/worktrees/<NNN>-<resumo>/`), confirmar o branch (`git branch --show-current`) e trazer o commit de início com `git merge --ff-only ia-main`
  5. Implementar a funcionalidade **dentro do worktree** (commits e push no branch da task)
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).

> Essa frase de **Encerramento** deve aparecer **literalmente** em toda task.

Exemplo preenchido (task `[008]-[feat]-[tela-x].md`):

```markdown
- **Modelo:** Feature/branch com worktree — cada task possui seu próprio branch e sua própria pasta de trabalho
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `feat/008-tela-x`
- **Worktree:** `.claude/worktrees/008-tela-x/` (criado pelo PO junto com a task)
- **Agent responsável:** `dev` (.claude/agents/dev.md)
- **Fluxo do agent responsável:**
  1. Na pasta principal do projeto, verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Entrar no worktree `.claude/worktrees/008-tela-x/`, confirmar o branch `feat/008-tela-x` e rodar `git merge --ff-only ia-main`
  5. Implementar a funcionalidade **dentro do worktree** (commits e push no branch `feat/008-tela-x`)
- **Encerramento:** somente o **PO** finaliza a task e a move para `.claude/tasks/done/`. Nenhum outro agent faz isso. Ao concluir sua parte, cada agent deve avisar que a task precisa ser passada adiante (Dev/DevOps → QA → PO).
```

## Escolha do Agent Responsável

O PO define o responsável **pelo que a task altera**, e não pelo tipo (`feat`, `fix`...):

| A task altera... | Agent responsável |
|------------------|-------------------|
| `client/`, `api/`, `config/`, `database/`, `lib/`, `tests/`, `server.js`, `package.json` | `dev` |
| `Dockerfile*`, `compose.yml`, `buildspec.yml`, `.github/workflows/`, `scripts/`, `deploy-ecs.sh`, IaC, recursos AWS (ECS, ECR, CodePipeline...) | `devops` |
| `README.md` ou documentação | `dev` (a task precisa pedir explicitamente a alteração do README) |

- Se a task envolver **as duas áreas**, divida em duas tasks (uma para cada agent). Se não der para dividir, o responsável é quem faz a maior parte, e a outra parte fica registrada como dependência.
- Exemplo: "criar GitHub Actions que roda os testes em PR" → `devops` (cria `.github/workflows/`; os testes em `tests/` já existem e não são alterados).
- A validação é sempre do `qa`, e o encerramento é sempre do **PO**.

## Padrão de Nomenclatura de Branch

Todo branch de task deve seguir **estritamente** o formato:

```
<tipo>/<NNN>-<resumo>
```

O nome é derivado diretamente do arquivo da task `[NNN]-[tipo]-[resumo].md`:

| Arquivo da task | Branch |
|-----------------|--------|
| `[004]-[feat]-[checkbox-importante-padrao].md` | `feat/004-checkbox-importante-padrao` |
| `[005]-[refactor]-[simplificar-tela-versao].md` | `refactor/005-simplificar-tela-versao` |
| `[006]-[docs]-[modernizar-readme].md` | `docs/006-modernizar-readme` |

### Regras

- **`<tipo>`:** o mesmo tipo da task (`feat`, `fix`, `docs`, `test`, `chore`, `refactor`)
- **`<NNN>`:** o número sequencial da task, sempre com 3 dígitos
- **`<resumo>`:** o mesmo resumo do arquivo da task, em letras minúsculas e separado por hífens
- **NÃO** usar prefixos genéricos como `task/` ou `feature/`
- **NÃO** usar acentos, espaços, colchetes ou letras maiúsculas
- O PO deve informar o nome do branch na seção **Informações de Workflow** de cada task criada

## Worktree da Task

Cada task tem uma pasta de trabalho própria (git worktree) dentro do projeto, no modelo do Claude Code. Assim, duas tasks podem ser implementadas em paralelo sem trocar de branch na pasta principal.

| Item | Padrão |
|---|---|
| Pasta | `.claude/worktrees/<NNN>-<resumo>/` (ignorada pelo git via `.gitignore`) |
| Branch | `<tipo>/<NNN>-<resumo>`, criado a partir do `ia-main` |
| Pasta principal | fica sempre no `ia-main` (um branch só pode estar aberto em um worktree) |

### Criação (PO, junto com a task)

A criação da task e do worktree é **uma única etapa** do PO. Passo a passo:

1. Na pasta principal, confirmar o branch e atualizar o `ia-main`:
   ```bash
   git branch --show-current        # deve ser ia-main
   git pull
   git worktree list                # conferir os worktrees que já existem
   ```
2. Ler o `sequencial.md`, definir o próximo `NNN` e derivar os nomes a partir do arquivo da task:

   | Arquivo da task | Branch | Worktree |
   |---|---|---|
   | `[008]-[feat]-[tela-x].md` | `feat/008-tela-x` | `.claude/worktrees/008-tela-x/` |

3. Criar o arquivo da task em `.claude/tasks/` (status `aberta`), já com o branch e o worktree nas **Informações de Workflow**, e incrementar o `sequencial.md`.
4. Criar o branch e o worktree a partir do `ia-main`:
   ```bash
   git worktree add -b <tipo>/<NNN>-<resumo> .claude/worktrees/<NNN>-<resumo> ia-main
   git worktree list                # o novo worktree deve aparecer com o branch da task
   ```
   - Se o branch ou a pasta já existirem, **não** sobrescrever: avisar o usuário.
5. Informar ao usuário o arquivo da task, o branch e o caminho do worktree.

Regras:
- A task e o `sequencial.md` ficam na pasta principal **sem commit**: quem registra no `ia-main` é o agent responsável, no commit de início.
- O PO **não escreve** no código dentro de `.claude/worktrees/` (bloqueado pelo hook). A única exceção são os arquivos de task do próprio worktree (`.claude/worktrees/<NNN>-<resumo>/.claude/tasks/**`), usados no aceite.
- Ao acionar o subagent, o PO informa o caminho da task **e** o caminho do worktree.
- Se a task for cancelada antes de começar, o PO remove o worktree e o branch (ver **Remoção**).

### Durante a task

- O commit de início (task para `doing/` + `sequencial.md`) é feito na **pasta principal**, no `ia-main`. Em seguida, o agent traz esse commit para o branch com `git merge --ff-only ia-main` dentro do worktree.
- Implementação, commits e push acontecem **dentro do worktree**. O QA valida no worktree, e o PO lê a task e faz o aceite a partir do worktree (status, `git mv` para `done/`, commit e push no branch da task).
- A task "viva" passa a ser a do worktree: `.claude/worktrees/<NNN>-<resumo>/.claude/tasks/doing/[NNN]-[tipo]-[resumo].md`. A cópia da pasta principal (`ia-main`) só é atualizada pelo merge do PR.
- O PO executa os comandos git no worktree com `git -C .claude/worktrees/<NNN>-<resumo> <comando>` (sem `cd`). O hook do PO só libera o `-C` para pastas dentro de `.claude/worktrees/`.
- **Docker:** os worktrees compartilham os mesmos containers e portas (`bia`, `database`, `redis`; 3001 e 5433). Deploy local e validação do QA rodam **uma task por vez**; só a implementação roda em paralelo.
- Arquivos fora do git (`node_modules`, `.env` locais, `.claude/settings.local.json`) não existem no worktree até serem instalados ou copiados.

### Remoção (PO, depois do merge)

Logo após o merge do PR (ver **Merge e limpeza**), o PO remove o worktree e o branch local, a partir da pasta principal:

```bash
git branch --show-current        # deve ser ia-main
git pull
git fetch --prune
git worktree remove .claude/worktrees/<NNN>-<resumo>
git branch -D <tipo>/<NNN>-<resumo>
git worktree prune
```

- Se o `git worktree remove` recusar por haver alterações não commitadas, **não** usar `--force`: avisar o usuário e perguntar o que fazer com elas.

## Checklist de Atividades (Agent responsável)

Toda task deve conter um checklist para **cada agent** que atua nela: o responsável (`dev` ou `devops`), o `qa` e o PO (seção **Finalização**). É **obrigatório** que cada agent marque as atividades **à medida que forem concluídas**, ou seja, durante o processo de implementação/validação — e não apenas ao final.

Todo checklist (Dev/DevOps e QA) deve começar com esta linha, **literalmente**:

> **Obrigatório:** marque cada item `[x]` assim que concluí-lo, durante a execução — não apenas ao final.

O checklist do agent responsável deve incluir no mínimo:

- [ ] Confirmar que está no branch `ia-main` antes de iniciar
- [ ] Mover a task para `.claude/tasks/doing/`
- [ ] Fazer commit e push no branch `ia-main` (task + sequencial)
- [ ] Entrar no worktree da task, confirmar o branch e rodar `git merge --ff-only ia-main`
- [ ] Itens específicos da implementação (conforme escopo técnico), feitos dentro do worktree
- [ ] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [ ] Validar rota `/api/versao` respondendo corretamente
- [ ] Aplicação buildando sem erros
- [ ] (Tasks de `.github/workflows/`) Validar a execução do workflow no GitHub (`gh run list` / `gh run view`)
- [ ] Ao concluir, informar que a task precisa ser passada para o **QA** validar e depois para o **PO** encerrar

## Checklist de Atividades (QA)

Toda task deve conter um checklist para o `qa`, logo antes da seção **Validação QA**, com no mínimo:

- [ ] Confirmar que está no worktree da task e no branch dela (`git branch --show-current` dentro de `.claude/worktrees/<NNN>-<resumo>/`)
- [ ] Validar cada critério de aceite (Given/When/Then) com evidência objetiva
- [ ] Rodar a suíte de testes e registrar o resultado
- [ ] Remover os dados de teste criados durante a validação
- [ ] Testes no navegador: usar o MCP do Playwright (preferencial) ou o navegador em container (`qa-browser`), conforme o `qa.md`, e confirmar ao final que nenhum navegador ou servidor temporário ficou aberto
- [ ] Preencher a seção **Validação QA** (✅/❌ + evidência por critério) e, se houver, a seção **Bugs**
- [ ] Mudar o status para `validada pelo QA` ou `com bugs`
- [ ] Fazer commit e push no branch da task
- [ ] Ao concluir, informar que a task precisa ser passada para o **PO** encerrar (ou de volta ao agent responsável, se `com bugs`)

> **Importante:** Quando os agentes concluírem sua parte, eles devem avisar explicitamente quem é o próximo: o agent responsável passa para o **QA**, e o **QA** passa para o **PO**, que é quem encerra a task.

## Finalização (Agent PO)

**SEMPRE** quem irá finalizar a task e movê-la para `done/` é o **PO**. Nenhum outro agent deve mover a task para `done/`.

### Regras de movimentação da task

- **Mover, nunca copiar:** sempre usar `git mv` para levar a task de uma pasta para outra (ex: `git -C .claude/worktrees/<NNN>-<resumo> mv ".claude/tasks/doing/[NNN]-[tipo]-[resumo].md" ".claude/tasks/done/"`). Depois de mover, a task **não pode** continuar existindo na pasta de origem.
- **Uma task, uma pasta:** antes do commit, conferir com `ls .claude/worktrees/<NNN>-<resumo>/.claude/tasks/doing .claude/worktrees/<NNN>-<resumo>/.claude/tasks/done` que a task aparece em **uma única** pasta.
- **Finalização SEMPRE no worktree da task:** o movimento para `done/` e o commit de finalização são feitos **somente** no branch da task, dentro do worktree dela (ex: `.claude/worktrees/004-checkbox-importante-padrao/`, branch `feat/004-checkbox-importante-padrao`). **NUNCA** finalizar task na pasta principal, no `ia-main` ou no `main`: a task só chega a `done/` no `ia-main` pelo merge do PR.

Toda task deve conter uma seção de Finalização executada apenas pelo PO após a implementação:

- [ ] Verificar se tudo foi implementado conforme o escopo técnico
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que o status da task é `validada pelo QA` (se estiver `com bugs`, devolver ao agent responsável)
- [ ] Verificar cada critério de aceite (✅/❌ com evidência); se algum falhar, mudar o status para `recusada` com o motivo e devolver ao agent responsável (a task continua em `doing/`)
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada (resumo do que foi verificado) e **aguardar o OK do usuário** para continuar
  - [ ] Após o OK, confirmar que o worktree está no branch da task (`git -C .claude/worktrees/<NNN>-<resumo> branch --show-current`; não pode ser `ia-main` nem `main`)
  - [ ] Mudar o status para `aceita` e mover a task para `.claude/tasks/done/`, dentro do worktree
  - [ ] Fazer commit e push final no branch da task, dentro do worktree
  - [ ] Abrir o Pull Request do branch da task contra `ia-main` (ver **Fluxo de Pull Request**). **Imediatamente antes do `gh pr create`:** rodar `git -C .claude/worktrees/<NNN>-<resumo> branch --show-current` e comparar com o nome do branch da task; se for `ia-main`, `main` ou outro nome, **parar, não abrir o PR e avisar o usuário**
  - [ ] Fazer o merge do PR em `ia-main` com **squash** (ver **Merge e limpeza**)
  - [ ] Voltar para `ia-main`, atualizar (`git pull`), limpar referências (`git fetch --prune`), remover o worktree da task (`git worktree remove`) e apagar o branch local da task
  - [ ] Enviar ao usuário o link do PR e o commit do merge

> **Importante:** o PO **não** move a task, **não** faz commit/push, **não** abre o PR e **não** faz o merge sem o OK explícito do usuário após o aviso de finalização. O OK do aceite autoriza todas essas etapas de uma vez.

## Fluxo de Pull Request (Agent PO)

Após o OK do usuário, o **PO** é o responsável por abrir o Pull Request. O PR é aberto **sempre** e **somente** pelo PO, depois que a task foi movida para `done/` e o commit e push final foram feitos.

### Regras

- **Repositório:** sempre `EvelynBonatto/bia` (o fork). **NUNCA** abrir PR no `upstream` (`henrylle/bia`)
  - O projeto tem dois remotes (`origin` e `upstream`), então informe **sempre** `--repo EvelynBonatto/bia` no `gh`
- **Branch de origem (head):** o branch da task (ex: `feat/004-checkbox-importante-padrao`)
- **Branch de destino (base):** **sempre** `ia-main`
  - **NUNCA** abrir PR contra `main` ou qualquer outro branch
- **Título:** `[NNN] - <tipo>: <resumo da task>` (ex: `[005] - refactor: simplificar tela de versão`)
- **Merge:** feito pelo **PO**, logo após abrir o PR, **sempre** com squash (ver **Merge e limpeza** e **Higiene de Commits**)
- **Não duplicar:** antes de criar, verificar se já existe um PR aberto para o branch

### Corpo do PR

O corpo do PR deve conter:

1. **Primeira linha:** `Closes task <NNN>` (ex: `Closes task 005`)
2. **Resumo:** o que foi feito e por quê (baseado na história de usuário)
3. **Task:** caminho do arquivo da task em `.claude/tasks/done/`
4. **Critérios de aceitação:** lista dos cenários atendidos
5. **Validação:** confirmação do deploy local e da rota `/api/versao`

> Sem rodapé de atribuição e sem menção a IA no corpo do PR.

### Comandos

```bash
# 1. Confirmar que o worktree está no branch da feature (NÃO no ia-main nem no main)
git -C .claude/worktrees/<NNN>-<resumo> branch --show-current
#    O resultado deve ser exatamente o branch da task, derivado do nome do arquivo:
#    [004]-[feat]-[checkbox-importante-padrao].md  →  feat/004-checkbox-importante-padrao
#    Se for ia-main, main ou outro nome: PARAR, não abrir o PR e avisar o usuário

# 2. Garantir que o branch da task está no remoto
git -C .claude/worktrees/<NNN>-<resumo> push -u origin <branch-da-task>

# 3. Verificar se já existe PR aberto para o branch
gh pr list --repo EvelynBonatto/bia --head <branch-da-task> --state open

# 4. Criar o PR (sempre contra ia-main, sempre no fork)
gh pr create --repo EvelynBonatto/bia --base ia-main --head <branch-da-task> \
  --title "[NNN] - <tipo>: <resumo>" \
  --body "Closes task <NNN>

<restante do corpo do PR>"

# 5. Conferir que o PR foi aberto no repositório e no branch corretos
gh pr view <numero> --repo EvelynBonatto/bia --json baseRefName,headRefName,url
```

> **Segurança:** o `--repo EvelynBonatto/bia` é **obrigatório** em todos os comandos `gh`, mesmo com o fork configurado como repositório padrão (`gh repo set-default EvelynBonatto/bia`). As duas proteções juntas evitam abrir PR no `henrylle/bia` por engano. Se o passo 5 mostrar base diferente de `ia-main` ou outro repositório, fechar o PR imediatamente e avisar o usuário.

### Merge e limpeza

Depois de conferir o PR (passo 5), o PO faz o merge e deixa o ambiente pronto para a próxima task:

```bash
# 6. Merge com squash no fork, apagando o branch remoto
gh pr merge <numero> --repo EvelynBonatto/bia --squash --delete-branch

# 7. Conferir que o PR foi integrado
gh pr view <numero> --repo EvelynBonatto/bia --json state,mergeCommit

# 8. Na pasta principal (sempre no ia-main), atualizar
git branch --show-current        # deve ser ia-main
git pull
git fetch --prune

# 9. Remover o worktree da task e apagar o branch local
git worktree remove .claude/worktrees/<NNN>-<resumo>
git branch -D <branch-da-task>
git worktree prune
```

- O título do commit de squash é o título do PR (`[NNN] - <tipo>: <resumo>`), e o commit **não** deve ter `Co-Authored-By` nem menção a IA.
- Se o merge falhar (conflito, checks pendentes ou bloqueio do GitHub), **não** usar `--admin` nem forçar: avisar o usuário com a mensagem de erro.
- Ao final, informar ao usuário o link do PR e o commit do merge. As próximas tasks partem desse `ia-main` atualizado.

## Higiene de Commits

O histórico no GitHub deve conter apenas commits com **valor real**. Commits bobos, repetidos, de teste ou de alterações insignificantes **não** devem chegar ao repositório remoto.

### Merge sempre com Squash

- Todo PR deve ser integrado ao `ia-main` com **Squash and merge**
- Assim, cada task vira **um único commit** no `ia-main`, independentemente de quantos commits existam no branch da task
- **Única exceção:** o commit de início da task (mover para `doing/` + `sequencial.md`, passo 3 do **Fluxo do agent responsável**) é feito direto no `ia-main` pelo agent responsável. Nenhum outro commit vai direto no `ia-main`
- O título do commit de squash deve seguir o título do PR: `[NNN] - <tipo>: <resumo>`
- O merge é feito pelo PO após o OK do aceite: `gh pr merge <numero> --repo EvelynBonatto/bia --squash --delete-branch`. O repositório só permite squash (Settings → Pull Requests).
- **Nenhum** commit (de nenhum agent) leva a linha `Co-Authored-By` nem menção a IA.

### O que NÃO commitar

- ❌ Alterações de **teste** ou experimentos
- ❌ Commit seguido de **revert** do mesmo commit: se algo foi feito por engano e ainda **não** foi enviado, desfazer localmente (`git reset`) em vez de criar um revert
- ❌ Commits **repetidos** ou com a mesma mensagem de um commit anterior
- ❌ Alterações **insignificantes** isoladas (ex: só espaço, só remoção de duplicata): agrupar com uma alteração relevante ou não commitar
- ❌ Arquivos que o usuário não pediu para incluir

### Antes de cada commit

- **Perguntar ao usuário** quando houver dúvida se uma alteração local deve ou não entrar no commit (ex: arquivos apagados ou modificados que não fazem parte da task)
- Conferir com `git diff --cached --name-status` que **somente** os arquivos da task estão preparados para o commit
- Usar mensagens claras e únicas, no padrão `<tipo>: <descrição>`

### Correção de histórico já enviado

- Reescrever histórico (`reset` + `push --force-with-lease`) é permitido **apenas** em branches de task e **somente** com autorização explícita do usuário
- **NUNCA** reescrever o histórico de `ia-main` ou `main`
