#!/usr/bin/env python3
"""
Hook PreToolUse do agente DEV.

O dev altera livremente o código do projeto e move tasks em .claude/tasks/.
Para alterar arquivos fora do escopo de implementação, precisa da permissão
do usuário:

- README.md (documentação: mudança precisa ser pedida pelo usuário/task)
- .claude/agents/, .claude/hooks/, .claude/rules/, .claude/settings*.json
  (configuração dos agentes: o dev não pode mudar as próprias regras)

Exit 0 = libera | Exit 0 + JSON com permissionDecision "ask" = pergunta ao usuário.
"""
import json
import os
import re
import sys

data = json.load(sys.stdin)
tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {}) or {}

PROJECT_DIR = os.path.realpath(
    os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
CWD = data.get("cwd") or PROJECT_DIR

# Caminhos protegidos, relativos à raiz do projeto
PROTEGIDOS = ["README.md", ".claude/agents", ".claude/hooks", ".claude/rules"]
PROTEGIDOS_PADRAO = [r"\.claude/settings[^/]*\.json"]


def pedir_permissao(motivo):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason":
                f"Agente DEV quer alterar arquivo protegido ({motivo}). Autorizar?",
        }
    }, ensure_ascii=False))
    sys.exit(0)


def protegido(caminho):
    alvo = os.path.realpath(os.path.join(CWD, os.path.expanduser(caminho)))
    rel = os.path.relpath(alvo, PROJECT_DIR)
    for p in PROTEGIDOS:
        if rel == p or rel.startswith(p + os.sep):
            return True
    return any(re.fullmatch(p, rel) for p in PROTEGIDOS_PADRAO)


# ============================================================
# Write / Edit / NotebookEdit
# ============================================================
if tool in ("Write", "Edit", "NotebookEdit"):
    arquivo = tool_input.get("file_path") or tool_input.get("notebook_path")
    if arquivo and protegido(arquivo):
        pedir_permissao(f"{tool} em {arquivo}")
    sys.exit(0)

# ============================================================
# Bash (verificação simples): comando que cita um caminho protegido
# e usa algo que escreve/move/apaga arquivos
# ============================================================
if tool == "Bash":
    comando = tool_input.get("command", "")
    cita_protegido = re.search(
        r"README\.md|\.claude/(agents|hooks|rules)|\.claude/settings", comando)
    escreve = re.search(
        r">|\btee\b|\bsed\s+(-\S*\s+)*-i|\b(mv|cp|rm|truncate|touch|chmod)\b",
        comando)
    if cita_protegido and escreve:
        pedir_permissao(f"comando: {comando[:200]}")

sys.exit(0)
