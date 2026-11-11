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

- Os arquivos devem ser criados na pasta `.kiro/tasks`.
- Você deve gerenciar o ciclo de vida dessas tarefas: quando uma tarefa for finalizada e aprovada, mova o arquivo correspondente para a pasta `.kiro/tasks/done/`.

---

## Informações de Workflow

Toda task criada deve conter uma seção de **Informações de Workflow** com as seguintes informações:

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Agent responsável pelo início:** `dev` (.kiro/agents/dev.json)
- **Fluxo do agent:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.kiro/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch da task a partir de `ia-main`
  5. Implementar a funcionalidade

## Checklist de Atividades (Agent dev)

Toda task deve conter um checklist para o agent dev marcar `[x]` conforme conclui cada etapa. É **obrigatório** que o dev marque as atividades **à medida que forem concluídas**, ou seja, durante o processo de implementação — e não apenas ao final.

O checklist deve incluir no mínimo:

- [ ] Confirmar que está no branch `ia-main` antes de iniciar
- [ ] Mover a task para `.kiro/tasks/doing/`
- [ ] Fazer commit e push no branch `ia-main` (task + sequencial)
- [ ] Criar o branch da task a partir de `ia-main`
- [ ] Itens específicos da implementação (conforme escopo técnico)
- [ ] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [ ] Validar rota `/api/versao` respondendo corretamente
- [ ] Aplicação buildando sem erros
- [ ] Ao concluir, informar que a task precisa ser passada para o **PO** para encerramento

> **Importante:** Quando os agentes concluírem a implementação, eles devem avisar explicitamente que a task precisa ser passada para o **PO** para que possa ser encerrada.

## Finalização (Agent PO)

**SEMPRE** quem irá finalizar a task e movê-la para `done/` é o **PO**. Nenhum outro agent deve mover a task para `done/`.

Toda task deve conter uma seção de Finalização executada apenas pelo PO após a implementação:

- [ ] Verificar se tudo foi implementado conforme o escopo técnico
- [ ] Verificar se todos os itens do checklist foram marcados como concluídos
- [ ] Confirmar que a aplicação está buildando e funcionando corretamente
- [ ] Se tudo estiver ok:
  - [ ] Informar ao usuário que a task está finalizada
  - [ ] Mover a task para `.kiro/tasks/done/`
  - [ ] Fazer commit e push final no repositório remoto
