- Sempre que você estiver implementando uma task(tarefa), você deve ir gradualmente marcando as etapas que forem concluídas.
- Sempre que terminar a implementação da task, me avise que tudo está pronto e sinalize qual o próximo agent que deverá ser chamado.

## Processo de Execução da Implementação

### 1. Ler a Task
- Sempre que receber uma task para implementar, leia o arquivo `.md` correspondente em `.claude/tasks/` (ou `.claude/tasks/doing/`, se já foi iniciada).
- Identifique o tipo (`feat`, `fix`, `docs`, `test`, `chore`, `refactor`), os critérios de aceitação, o escopo técnico e o Definition of Done.
- Confira que o **Agent responsável** da task é o `dev`. Se for `devops`, avise o usuário e não implemente.
- Execute o fluxo da seção **Informações de Workflow** antes de implementar: conferir o branch `ia-main`, mover para `doing/`, commit e push, criar o branch `<tipo>/<NNN>-<resumo>`.

### 2. Analisar o Código de Referência
- Antes de escrever qualquer código, leia os arquivos mencionados na seção "Padrão de implementação a seguir".
- Entenda a estrutura do projeto, as convenções, as classes CSS existentes e o padrão de consumo de API.

### 3. Implementar
- Siga o escopo técnico definido na task: arquivos a criar, arquivos a modificar.
- Use as regras de `.kiro/rules/` (Dockerfile, infraestrutura, pipeline) quando aplicável, e `.claude/rules/regras-deploy.md` para o deploy local.
- Mantenha a simplicidade — não adicione complexidade além do que a task exige.

### 4. Marcar Etapas Concluídas
- Conforme for concluindo cada item do Definition of Done, marque com `[x]` no arquivo da task.
- Isso garante rastreabilidade do progresso.

### 5. Verificar o Build
- Após implementar, rode o build do projeto para confirmar que não há erros de compilação.
- Frontend: `npm run build` dentro de `client/` ou via Docker (`docker compose up --build`).
- Se houver testes configurados, rode-os também.

### 6. Rodar a Aplicação Localmente
- Suba a aplicação com o fluxo de `.claude/rules/regras-deploy.md`: `docker compose down && docker compose build && docker compose up -d` (sobe backend, banco PostgreSQL e frontend buildado).
- Aguarde os containers estarem saudáveis (`docker ps`).
- Rode as migrations se o banco foi recriado: `docker compose exec server bash -c 'npx sequelize db:migrate'`.
- Valide as rotas com `curl` (ex: `curl http://localhost:3001/api/versao`).
- Teste as funcionalidades implementadas acessando `http://localhost:3001` no navegador.

### 7. Avisar Conclusão e Próximo Agent
- Após validar que tudo está funcionando, avise o usuário que a implementação está pronta.
- Sinalize que o próximo passo é o **QA** validar a entrega e, depois, o **PO** encerrar a task. Se algo de infraestrutura ficou pendente, aponte que precisa de uma task para o **DevOps**.
- Pergunte se o usuário deseja parar os containers com `docker compose down` para liberar recursos.
