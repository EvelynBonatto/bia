# Regras de Deploy Local - Projeto BIA

## Atualização da Aplicação

Sempre que uma alteração for feita no código da aplicação (frontend ou backend), o fluxo de deploy local deve ser executado **automaticamente**, sem necessidade de autorização ou solicitação do usuário.

### Fluxo Obrigatório

```bash
docker compose down && docker compose build && docker compose up -d
```

### Quando Executar
- Após qualquer alteração em arquivos do frontend (`client/`)
- Após qualquer alteração em arquivos do backend (`api/`, `config/`, raiz)
- Após qualquer alteração no `Dockerfile` ou `compose.yml`

### Validação Pós-Deploy
Após subir os containers, verificar se a aplicação está respondendo:

```bash
curl -s http://localhost:3001/api/versao
```

A rota deve retornar a versão da aplicação (ex: `"Bia 4.2.0"`).

### Observações
- **Não usar** `npm run dev` ou `vite` diretamente — sempre passar pelo Docker Compose
- **Não solicitar** permissão do usuário para executar o fluxo — é automático
- Caso o `curl` falhe, aguardar alguns segundos e tentar novamente (o container pode ainda estar subindo)
