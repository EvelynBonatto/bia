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
