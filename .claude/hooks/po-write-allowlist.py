#!/usr/bin/env python3
"""Hook PreToolUse (Write|Edit) do agente PO — escrita só em .claude/**, exceto .claude/worktrees/**
(nos worktrees, só os arquivos de task: .claude/worktrees/<nome>/.claude/tasks/**).

Qualquer erro no próprio hook também bloqueia (fail closed).
"""
import json
import os
import sys


def bloquear(motivo):
    print(f"Bloqueado pelo hook do PO: {motivo}", file=sys.stderr)
    sys.exit(2)


SUBAGENTS_LIBERADOS = {"dev", "qa", "devops"}


def main():
    dados = json.load(sys.stdin)
    if dados.get("agent_type") in SUBAGENTS_LIBERADOS:
        return  # chamada feita por um subagent (dev/qa/devops), não pelo PO
    caminho = (dados.get("tool_input") or {}).get("file_path", "")
    if not caminho:
        bloquear("caminho do arquivo não informado")

    projeto = os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or os.getcwd()
    permitido = os.path.realpath(os.path.join(projeto, ".claude"))
    worktrees = os.path.realpath(os.path.join(projeto, ".claude", "worktrees"))
    alvo = os.path.realpath(os.path.join(projeto, caminho))

    if os.path.commonpath([permitido, alvo]) != permitido:
        bloquear(f"o PO só pode escrever em .claude/** (tentou: {caminho})")

    # Os worktrees das tasks ficam em .claude/worktrees/ e contêm código da aplicação:
    # o PO não escreve neles (quem implementa é o dev/devops). Única exceção: os arquivos
    # de task do próprio worktree (.claude/worktrees/<nome>/.claude/tasks/**), para o aceite.
    if os.path.commonpath([worktrees, alvo]) == worktrees:
        partes = os.path.relpath(alvo, worktrees).split(os.sep)
        eh_task = len(partes) >= 4 and partes[1] == ".claude" and partes[2] == "tasks"
        if not eh_task:
            bloquear(
                "o PO não escreve em .claude/worktrees/** (código das tasks), "
                f"só em .claude/worktrees/<nome>/.claude/tasks/** (tentou: {caminho})"
            )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail closed
        bloquear(f"erro ao validar o caminho ({e})")
    sys.exit(0)
