No seu trabalho de especificar tarefas, sempre que for pedida uma nova atividade, o resultado do seu trabalho deve ser a criação de um arquivo Markdown (.md).

Esse arquivo deve seguir estritamente o formato: `[025]-[feat]-[resumo].md`

Onde:

- **[025]**: Número sequencial da tarefa, sempre com 3 dígitos (ex: 001, 002, 025).
  - Esse controle sequencial será feito por um arquivo chamado sequencial.md
  - Nesse arquivo terá apenas o texto (Última Task: [002].)
  - Você vai sempre usar o sequencial seguinte e incrementar o valor Última Task.
- **[feat]**: Tipo da tarefa (ex: `feat`, `fix`, `test`, `chore`, `refactor`).
- **[resumo]**: Resumo curto da tarefa em letras minúsculas, com as palavras separadas por hífens.

**Localização e Gestão de Estado:**

- Os arquivos devem ser criados na pasta `.claude/tasks`.
- Você deve gerenciar o ciclo de vida dessas tarefas: quando uma tarefa for finalizada e aprovada, mova o arquivo correspondente para a pasta `.claude/tasks/done/`.

---

## Informações de Workflow

Toda task criada deve conter uma seção de **Informações de Workflow** com as seguintes informações:

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Nome do branch:** `<tipo>/<NNN>-<resumo>` (ver **Padrão de Nomenclatura de Branch**)
- **Agent responsável pelo início:** `dev` (.claude/agents/dev.md)
- **Fluxo do agent:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch da task a partir de `ia-main`, seguindo o padrão `<tipo>/<NNN>-<resumo>`
  5. Implementar a funcionalidade

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

## Checklist de Atividades (Agent dev)

Toda task deve conter um checklist para o agent dev marcar `[x]` conforme conclui cada etapa. É **obrigatório** que o dev marque as atividades **à medida que forem concluídas**, ou seja, durante o processo de implementação — e não apenas ao final.

O checklist deve incluir no mínimo:

- [ ] Confirmar que está no branch `ia-main` antes de iniciar
- [ ] Mover a task para `.claude/tasks/doing/`
- [ ] Fazer commit e push no branch `ia-main` (task + sequencial)
- [ ] Criar o branch da task a partir de `ia-main` (padrão `<tipo>/<NNN>-<resumo>`)
- [ ] Itens específicos da implementação (conforme escopo técnico)
- [ ] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [ ] Validar rota `/api/versao` respondendo corretamente
- [ ] Aplicação buildando sem erros
- [ ] Ao concluir, informar que a task precisa ser passada para o **PO** para encerramento

> **Importante:** Quando os agentes concluírem a implementação, eles devem avisar explicitamente que a task precisa ser passada para o **PO** para que possa ser encerrada.

## Finalização (Agent PO)

**SEMPRE** quem irá finalizar a task e movê-la para `done/` é o **PO**. Nenhum outro agent deve mover a task para `done/`.

### Regras de movimentação da task

- **Mover, nunca copiar:** sempre usar `git mv` para levar a task de uma pasta para outra (ex: `git mv ".claude/tasks/doing/[NNN]-[tipo]-[resumo].md" ".claude/tasks/done/"`). Depois de mover, a task **não pode** continuar existindo na pasta de origem.
- **Uma task, uma pasta:** antes do commit, conferir com `ls .claude/tasks/doing .claude/tasks/done` que a task aparece em **uma única** pasta.
- **Finalização SEMPRE no branch da task:** o movimento para `done/` e o commit de finalização são feitos **somente** no branch da task (ex: `feat/004-checkbox-importante-padrao`). **NUNCA** finalizar task diretamente no `ia-main` ou no `main`: a task só chega a `done/` no `ia-main` pelo merge do PR.

Toda task deve conter uma seção de Finalização executada apenas pelo PO após a implementação:

- [ ] Verificar se tudo foi implementado conforme o escopo técnico
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada (resumo do que foi verificado) e **aguardar o OK do usuário** para continuar
  - [ ] Após o OK, confirmar que está no branch da task (não em `ia-main` nem em `main`)
  - [ ] Mover a task para `.claude/tasks/done/`
  - [ ] Fazer commit e push final no branch da task
  - [ ] Antes de abrir o PR, confirmar com `git branch --show-current` que está no branch da feature e que o nome bate com a task (não pode ser `ia-main`)
  - [ ] Abrir o Pull Request do branch da task contra `ia-main` (ver **Fluxo de Pull Request**)
  - [ ] Enviar ao usuário o link do PR

> **Importante:** o PO **não** move a task, **não** faz commit/push e **não** abre o PR sem o OK explícito do usuário após o aviso de finalização.

## Fluxo de Pull Request (Agent PO)

Após o OK do usuário, o **PO** é o responsável por abrir o Pull Request. O PR é aberto **sempre** e **somente** pelo PO, depois que a task foi movida para `done/` e o commit e push final foram feitos.

### Regras

- **Repositório:** sempre `EvelynBonatto/bia` (o fork). **NUNCA** abrir PR no `upstream` (`henrylle/bia`)
  - O projeto tem dois remotes (`origin` e `upstream`), então informe **sempre** `--repo EvelynBonatto/bia` no `gh`
- **Branch de origem (head):** o branch da task (ex: `feat/004-checkbox-importante-padrao`)
- **Branch de destino (base):** **sempre** `ia-main`
  - **NUNCA** abrir PR contra `main` ou qualquer outro branch
- **Título:** `[NNN] - <tipo>: <resumo da task>` (ex: `[005] - refactor: simplificar tela de versão`)
- **Merge:** o PO **não** faz merge. O merge é feito pelo usuário após revisar o PR, **sempre** com **Squash and merge** (ver **Higiene de Commits**)
- **Não duplicar:** antes de criar, verificar se já existe um PR aberto para o branch

### Corpo do PR

O corpo do PR deve conter:

1. **Primeira linha:** `Closes task <NNN>` (ex: `Closes task 005`)
2. **Resumo:** o que foi feito e por quê (baseado na história de usuário)
3. **Task:** caminho do arquivo da task em `.claude/tasks/done/`
4. **Critérios de aceitação:** lista dos cenários atendidos
5. **Validação:** confirmação do deploy local e da rota `/api/versao`
6. **Rodapé de atribuição** do Claude Code

### Comandos

```bash
# 1. Confirmar que está no branch da feature (NÃO no ia-main nem no main)
git branch --show-current
#    O resultado deve ser exatamente o branch da task, derivado do nome do arquivo:
#    [004]-[feat]-[checkbox-importante-padrao].md  →  feat/004-checkbox-importante-padrao
#    Se for ia-main, main ou outro nome: PARAR, não abrir o PR e avisar o usuário

# 2. Garantir que o branch da task está no remoto
git push -u origin <branch-da-task>

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

### Após abrir o PR

- Informar ao usuário o link do PR
- Orientar que o próximo passo é o usuário revisar e fazer o merge em `ia-main` usando **Squash and merge**
- Após o merge, as próximas tasks continuam partindo de `ia-main` atualizado (`git pull` em `ia-main` antes de iniciar)

## Higiene de Commits

O histórico no GitHub deve conter apenas commits com **valor real**. Commits bobos, repetidos, de teste ou de alterações insignificantes **não** devem chegar ao repositório remoto.

### Merge sempre com Squash

- Todo PR deve ser integrado ao `ia-main` com **Squash and merge**
- Assim, cada task vira **um único commit** no `ia-main`, independentemente de quantos commits existam no branch da task
- O título do commit de squash deve seguir o título do PR: `[NNN] - <tipo>: <resumo>`
- Pelo terminal (quando o usuário pedir explicitamente): `gh pr merge <numero> --repo EvelynBonatto/bia --squash --delete-branch`

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
