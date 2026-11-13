# [005] - Simplificar Tela de Versão

## Tipo
`refactor`

## Resumo
Simplificar a tela de versão mantendo apenas dois cards: **Versão da API** e **Status de Conexão**. Remover o card de Ambiente e o card de Endpoint da API.

---

## Informações de Workflow

- **Modelo:** Feature/branch — cada task possui seu próprio branch
- **Branch base:** `ia-main` (a task SEMPRE deriva deste branch)
- **Agent responsável pelo início:** `dev` (.claude/agents/dev.md)
- **Fluxo do agent:**
  1. Verificar se está no branch `ia-main`. Caso não esteja, informar e perguntar se pode retornar antes de iniciar
  2. Mover a task para `.claude/tasks/doing/`
  3. Fazer commit e push no branch `ia-main` (task + sequencial)
  4. Criar o branch da task a partir de `ia-main`
  5. Implementar a funcionalidade

---

## Checklist de Atividades (Agent dev)

> Marcar cada item com `[x]` à medida que for concluído durante a implementação.

- [x] Confirmar que está no branch `ia-main` antes de iniciar
- [x] Mover a task para `.claude/tasks/doing/`
- [x] Fazer commit e push no branch `ia-main` (task + sequencial)
- [x] Criar o branch da task a partir de `ia-main`
- [x] Remover o card "Ambiente" do JSX no `Versao.jsx` (bloco com `getEnvironmentInfo`)
- [x] Remover o card "Endpoint da API" do JSX no `Versao.jsx`
- [x] Remover a função `getEnvironmentInfo` e a constante `env` do `Versao.jsx` (código morto)
- [x] Manter o card "Versão da API" (hero) intacto
- [x] Manter o card "Status da Conexão" intacto (com ícone, badge e última verificação)
- [x] Manter os botões de ação (Atualizar / Tentar novamente) intactos
- [x] Executar deploy local (`docker compose down && docker compose build && docker compose up -d`)
- [x] Validar rota `/api/versao` respondendo corretamente
- [x] Aplicação buildando sem erros
- [x] Ao concluir, informar que a task precisa ser passada para o **PO** para encerramento

---

## Finalização (Agent PO)

> Esta etapa é executada **apenas pelo PO** após os agentes concluírem a implementação.

- [x] Verificar se tudo foi implementado conforme o escopo técnico
- [x] Verificar se todos os itens do checklist foram marcados como concluídos
- [x] Confirmar que a aplicação está buildando e funcionando corretamente
- [x] Se tudo estiver ok:
  - [x] Informar ao usuário que a task está finalizada
  - [x] Mover a task para `.claude/tasks/done/`
  - [x] Fazer commit e push final no repositório remoto

---

## Contexto

A tela de versão atual (`Versao.jsx`) exibe três cards além do hero:

1. **Status da Conexão** — mostra ícone (🟢/🔴/🟡), texto (Online/Offline/Verificando) e última verificação
2. **Ambiente** — detecta o tipo de ambiente (Local, IP Direto, ALB HTTP, Produção, Outro) com base no `window.location`
3. **Endpoint da API** — exibe a URL do endpoint (`apiUrl/api/versao`)

O usuário solicitou a simplificação da tela, mantendo apenas a **Versão da API** (hero) e o **Status de Conexão**. Os cards de Ambiente e Endpoint devem ser removidos.

---

## História de Usuário

> **Como** usuário do projeto BIA,  
> **quando** acesso a tela de versão,  
> **quero** ver apenas a versão da API e o status de conexão,  
> **para que** a tela seja mais limpa e direta, sem informações de ambiente e endpoint que não são relevantes no dia a dia.

---

## Critérios de Aceitação

### Cenário 1 — Tela exibe apenas versão e status
```
Given que o usuário acessa a rota /versao
When a tela é carregada
Then deve exibir o hero com a versão da API
And deve exibir o card de Status da Conexão
And NÃO deve exibir o card de Ambiente
And NÃO deve exibir o card de Endpoint da API
```

### Cenário 2 — Status da conexão continua funcional
```
Given que a API está online
When a tela carrega e a requisição é concluída
Then o card de Status da Conexão deve mostrar "🟢 Online"
And deve mostrar o horário da última verificação
```

### Cenário 3 — Botão de atualizar permanece
```
Given que o status da conexão é "online"
When o usuário visualiza a tela
Then o botão "🔄 Atualizar" deve estar visível e funcional
```

### Cenário 4 — Sem código morto
```
Given que a refatoração foi concluída
When o código do Versao.jsx é analisado
Then a função getEnvironmentInfo não deve existir
And a constante env não deve existir
And nenhuma referência a ambiente ou endpoint deve permanecer no JSX
```

---

## Escopo Técnico

### Arquivo a modificar
- `client/src/components/Versao.jsx`

### Alterações necessárias

1. **Remover do JSX** — O card "Ambiente" (segundo `feature-card` dentro de `feature-grid`):
   ```jsx
   {/* Ambiente detectado */}
   <div className="feature-card">
     <h3>Ambiente</h3>
     ...
   </div>
   ```

2. **Remover do JSX** — O card "Endpoint da API" (terceiro `feature-card` dentro de `feature-grid`):
   ```jsx
   {/* Endpoint da API */}
   <div className="feature-card">
     <h3>Endpoint da API</h3>
     <p className="versao-endpoint">{apiUrl}/api/versao</p>
   </div>
   ```

3. **Remover código morto** — A função `getEnvironmentInfo` (aproximadamente linhas 57-90) e a constante `env` que a invoca:
   ```jsx
   const env = getEnvironmentInfo();
   ```

4. **Manter intactos:**
   - O hero com a versão da API
   - O card "Status da Conexão" (com badge, ícone e última verificação)
   - Os botões de ação (Atualizar / Tentar novamente)
   - O link "← Voltar"
   - Toda a lógica de `fetchVersion`, `status`, `lastCheck`, `getStatusIcon`, `getStatusText`, `getStatusClass`, `formatTime`
   - O uso do `LogContext` (`logApiRequest`, `logApiResponse`, `logApiError`)

### Observações
- Nenhuma alteração no backend é necessária.
- Nenhuma alteração no CSS é estritamente necessária — o `feature-grid` pode ficar com apenas um card, mas se houver regras CSS que assumem múltiplos cards (ex: grid-template-columns), o dev pode ajustar para uma coluna única se ficar visualmente melhor. Fica a critério do dev avaliar.
- A importação de `Link` do `react-router-dom` deve ser mantida (usada no botão "← Voltar").

---

## Definition of Ready
- [x] História de usuário escrita e compreendida
- [x] Critérios de aceitação definidos
- [x] Arquivo de referência identificado (`Versao.jsx`)
- [x] Escopo técnico delimitado (alteração em um único arquivo)
- [x] Sem dependências externas bloqueantes

## Definition of Done
- [x] Card "Ambiente" removido do JSX
- [x] Card "Endpoint da API" removido do JSX
- [x] Função `getEnvironmentInfo` removida
- [x] Constante `env` removida
- [x] Hero com versão da API permanece intacto
- [x] Card de Status da Conexão permanece intacto e funcional
- [x] Botões de ação permanecem intactos
- [x] Sem código morto remanescente
- [x] Aplicação buildando sem erros
- [x] Deploy local validado com `docker compose down && docker compose build && docker compose up -d`
- [x] Rota `/api/versao` respondendo corretamente após deploy
- [x] Task revisada e encerrada pelo PO
