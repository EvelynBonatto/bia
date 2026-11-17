#!/usr/bin/env python3
"""Hook PreToolUse (Write|Edit) do agente PO — escrita só em .claude/**.

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
    alvo = os.path.realpath(os.path.join(projeto, caminho))

    if os.path.commonpath([permitido, alvo]) != permitido:
        bloquear(f"o PO só pode escrever em .claude/** (tentou: {caminho})")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail closed
        bloquear(f"erro ao validar o caminho ({e})")
    sys.exit(0)
