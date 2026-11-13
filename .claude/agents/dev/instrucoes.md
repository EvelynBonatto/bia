- Sempre que você estiver implementando uma task(tarefa), você deve ir gradualmente marcando as etapas que forem concluídas.
- Sempre que terminar a implementação da task, me avise que tudo está pronto e sinalize qual o próximo agent que deverá ser chamado.

## Processo de Execução da Implementação

### 1. Ler a Task
- Sempre que receber uma task para implementar, leia o arquivo `.md` correspondente em `.claude/tasks/` (ou `.claude/tasks/done/`).
- Identifique o tipo (`feat`, `fix`, `test`, `chore`, `refactor`), os critérios de aceitação, o escopo técnico e o Definition of Done.

### 2. Analisar o Código de Referência
- Antes de escrever qualquer código, leia os arquivos mencionados na seção "Padrão de implementação a seguir".
- Entenda a estrutura do projeto, as convenções, as classes CSS existentes e o padrão de consumo de API.

### 3. Implementar
- Siga o escopo técnico definido na task: arquivos a criar, arquivos a modificar.
- Use as regras de `.claude/rules/` (Dockerfile, infraestrutura, pipeline) quando aplicável.
- Mantenha a simplicidade — não adicione complexidade além do que a task exige.

### 4. Marcar Etapas Concluídas
- Conforme for concluindo cada item do Definition of Done, marque com `[x]` no arquivo da task.
- Isso garante rastreabilidade do progresso.

### 5. Verificar o Build
- Após implementar, rode o build do projeto para confirmar que não há erros de compilação.
- Frontend: `npm run build` dentro de `client/` ou via Docker (`docker compose up --build`).
- Se houver testes configurados, rode-os também.

### 6. Rodar a Aplicação Localmente
- Suba a aplicação com `docker compose up --build -d` (sobe backend, banco PostgreSQL e frontend buildado).
- Aguarde os containers estarem saudáveis (`docker ps`).
- Rode as migrations se o banco foi recriado: `docker compose exec server bash -c 'npx sequelize db:migrate'`.
- Valide as rotas com `curl` (ex: `curl http://localhost:3001/api/versao`).
- Teste as funcionalidades implementadas acessando `http://localhost:3001` no navegador.

### 7. Avisar Conclusão e Próximo Agent
- Após validar que tudo está funcionando, avise o usuário que a implementação está pronta.
- Sinalize qual é o próximo agent que deve ser chamado (ex: QA para testes, DevOps para infraestrutura/pipeline).
- Pergunte se o usuário deseja parar os containers com `docker compose down` para liberar recursos.
