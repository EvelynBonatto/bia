# [001] - Tela de Versão da API

## Tipo
`feat`

## Resumo
Implementar uma tela dedicada no frontend do projeto BIA para exibir as informações retornadas pela rota `/api/versao`, seguindo o mesmo padrão visual e de estrutura da tela de tarefas.

---

## Contexto

Atualmente, a rota `/api/versao` já existe no backend e retorna uma string com a versão da aplicação (ex: `"Bia 4.2.0"`). Essa informação é consumida de forma secundária pelo componente `VersionInfo.jsx`, que exibe um tooltip no header.

O objetivo desta tarefa é criar uma **tela dedicada** acessível via rota de navegação, que apresente as informações de versão de forma clara, organizada e com a identidade visual já estabelecida pelo projeto.

---

## História de Usuário

> **Como** aluno ou desenvolvedor utilizando o projeto BIA,  
> **quero** acessar uma tela dedicada com as informações de versão da API,  
> **para que** eu possa verificar rapidamente qual versão está em execução e o status da API, sem precisar inspecionar o tooltip do header.

---

## Critérios de Aceitação

### Cenário 1 — Navegação até a tela de versão
```
Given que o usuário está em qualquer página da aplicação
When ele clica no link/botão de navegação para "Versão"
Then ele deve ser redirecionado para a rota /versao
And a tela de versão deve ser exibida
```

### Cenário 2 — Exibição das informações de versão
```
Given que o usuário está na tela /versao
When a página é carregada
Then deve ser feita uma requisição GET para /api/versao
And o resultado deve ser exibido na tela (ex: "Bia 4.2.0")
And o status da API (online/offline/verificando) deve ser exibido
```

### Cenário 3 — Estado de carregamento
```
Given que o usuário acabou de acessar a tela /versao
When a requisição para /api/versao ainda não foi concluída
Then um indicador visual de carregamento deve ser exibido
```

### Cenário 4 — Estado de erro (API offline)
```
Given que o usuário está na tela /versao
When a requisição para /api/versao falha ou retorna erro
Then uma mensagem de erro clara deve ser exibida
And um botão de "Tentar novamente" deve estar disponível
```

### Cenário 5 — Botão de retorno
```
Given que o usuário está na tela /versao
When ele clica no botão "Voltar"
Then deve ser redirecionado para a página inicial (/)
```

---

## Escopo Técnico

### Arquivos a criar
- `client/src/components/Versao.jsx` — Componente de tela da versão

### Arquivos a modificar
- `client/src/App.jsx` — Adicionar a rota `/versao` ao React Router
- `client/src/components/Header.jsx` — Adicionar link de navegação para `/versao` (seguindo o mesmo padrão do link `/about`)

### Padrão de implementação a seguir
- Estrutura de componente: seguir o mesmo padrão de `Tasks.jsx` e `About.jsx`
- Consumo de API: seguir o mesmo padrão de `fetchTasks` em `App.jsx` (uso de `VITE_API_URL`, `fetch`, tratamento de erros)
- Estilização: usar as classes CSS já existentes no projeto (`index.css`), sem adicionar arquivos CSS separados
- Roteamento: usar `React Router` com `<Route path="/versao" element={<Versao />} />`

### Dados exibidos na tela
- Versão da API (texto retornado por `/api/versao`)
- Status da conexão com a API (online / offline / verificando)
- URL da API sendo consultada
- Botão para atualizar/reconsultar manualmente
- Link/botão para voltar à página inicial

---

## Definition of Ready
- [x] História de usuário escrita e compreendida
- [x] Critérios de aceitação definidos
- [x] Padrão de código de referência identificado (`Tasks.jsx`, `App.jsx`)
- [x] Endpoint backend `/api/versao` já disponível e funcional
- [x] Sem dependências externas bloqueantes

## Definition of Done
- [x] Componente `Versao.jsx` criado seguindo o padrão existente
- [x] Rota `/versao` configurada no React Router (`App.jsx`)
- [x] Link de navegação adicionado ao `Header.jsx`
- [x] Requisição para `/api/versao` implementada com tratamento de erro
- [x] Estados de loading, sucesso e erro implementados
- [x] Layout consistente com o restante da aplicação (sem CSS externo adicional)
- [x] Aplicação buildando sem erros
- [x] Tela acessível via navegação e via URL direta

---

## Notas de Implementação
- **Não duplicar lógica** do `VersionInfo.jsx` — a tela é uma página, o `VersionInfo` é um widget do header; ambos podem coexistir consumindo o mesmo endpoint
- **Simplicidade:** não adicionar complexidade desnecessária; o padrão do projeto é prioridade
- Reaproveitar as classes CSS existentes para manter consistência visual
