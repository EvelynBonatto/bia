- Sempre que você estiver implementando uma task(tarefa), você deve ir gradualmente marcando as etapas que forem concluídas.
- Sempre que terminar a implementação da task, me avise que tudo está pronto e sinalize qual o próximo agent que deverá ser chamado.

## Processo de Execução da Implementação

### 1. Ler a Task
- Sempre que receber uma task para implementar, leia o arquivo `.md` correspondente em `.claude/tasks/` (ou `.claude/tasks/doing/`, se já foi iniciada).
- Identifique o tipo (`feat`, `fix`, `docs`, `test`, `chore`, `refactor`), os critérios de aceitação, o escopo técnico e o Definition of Done.
- Confira que o **Agent responsável** da task é o `dev`. Se for `devops`, avise o usuário e não implemente.
- Execute o fluxo da seção **Informações de Workflow** antes de implementar. O branch e o worktree da task **já foram criados pelo PO** (`.claude/worktrees/<NNN>-<resumo>/`, branch `<tipo>/<NNN>-<resumo>`) — não crie outro branch:
  1. Na **pasta principal** do projeto, conferir que está no branch `ia-main`. Se não estiver, informar e perguntar se pode retornar antes de iniciar.
  2. Mover a task para `.claude/tasks/doing/` e fazer commit e push no `ia-main` (task + `sequencial.md`).
  3. Entrar no worktree da task, conferir o branch (`git branch --show-current`) e trazer o commit de início: `git merge --ff-only ia-main`.
  4. A partir daqui, **tudo acontece dentro do worktree**: código, marcação do checklist na task (`.claude/worktrees/<NNN>-<resumo>/.claude/tasks/doing/...`), commits e `git push -u origin <branch-da-task>`.
- Se o worktree não existir ou estiver em outro branch, pare e avise o usuário.

### Worktree: cuidados
- **Nunca** troque de branch dentro do worktree nem na pasta principal (a pasta principal fica sempre no `ia-main`).
- Arquivos fora do git (`node_modules`, `.env` locais) não vêm no worktree: instale ou copie o que for necessário, sem commitá-los.
- **Docker:** rode o `docker compose` **de dentro do worktree** (para buildar o código da task). Os worktrees compartilham os mesmos containers e portas (`bia`, `database`, `redis`; 3001 e 5433): se outra task estiver com o compose rodando, avise o usuário em vez de derrubá-la.

### 2. Analisar o Código de Referência
- Antes de escrever qualquer código, leia os arquivos mencionados na seção "Padrão de implementação a seguir".
- Entenda a estrutura do projeto, as convenções, as classes CSS existentes e o padrão de consumo de API.

### 3. Implementar
- Siga o escopo técnico definido na task: arquivos a criar, arquivos a modificar.
- Use as regras de `.kiro/rules/` (Dockerfile, infraestrutura, pipeline) quando aplicável, e `.claude/rules/regras-deploy.md` para o deploy local.
- Mantenha a simplicidade — não adicione complexidade além do que a task exige.

### 4. Marcar Etapas Concluídas
- Conforme for concluindo cada item do Definition of Done, marque com `[x]` no arquivo da task (a cópia do worktree, em `.claude/worktrees/<NNN>-<resumo>/.claude/tasks/doing/`).
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
