#!/usr/bin/env python3
"""Hook PreToolUse (Bash) do agente PO — equivalente ao denyByDefault do Kiro.

Só libera os comandos da lista abaixo. Todo o resto é bloqueado (exit 2).
Qualquer erro no próprio hook também bloqueia (fail closed).
"""
import json
import os
import shlex
import sys

# Comandos liberados: (programa, subcomando)
PERMITIDOS = {
    ("git", "add"), ("git", "commit"), ("git", "push"), ("git", "checkout"),
    ("git", "status"), ("git", "branch"), ("git", "log"), ("git", "worktree"),
    ("git", "mv"), ("git", "diff"),          # exigidos pela especificacao.md
    ("git", "pull"), ("git", "fetch"),       # atualizar ia-main após o merge
    ("gh", "pr"),                            # subcomando checado abaixo
    ("ls", None),                            # conferir doing/ e done/
}
GH_PR_PERMITIDOS = {"create", "list", "view", "merge"}
REPO_FORK = "EvelynBonatto/bia"
BRANCHES_PROTEGIDOS = {"main", "ia-main"}
# Subagents acionados pelo PO: o hook do PO não vale para eles
SUBAGENTS_LIBERADOS = {"dev", "qa", "devops"}


def bloquear(motivo):
    print(f"Bloqueado pelo hook do PO: {motivo}", file=sys.stderr)
    sys.exit(2)


def checar_metacaracteres(cmd):
    """Impede encadear comandos (;, &&, |, $(...), redirecionamento...)."""
    aspas = None
    i = 0
    while i < len(cmd):
        c = cmd[i]
        if aspas == "'":
            if c == "'":
                aspas = None
        elif aspas == '"':
            if c == "\\":
                i += 1
            elif c == '"':
                aspas = None
            elif c == "`" or cmd.startswith("$(", i):
                bloquear("substituição de comando não é permitida (use aspas simples)")
        else:
            if c == "\\":
                i += 1
            elif c in "'\"":
                aspas = c
            elif c in ";&|<>()`\n" or cmd.startswith("$(", i):
                bloquear(f"o caractere {c!r} fora de aspas não é permitido (um comando por vez)")
        i += 1
    if aspas:
        bloquear("aspas não fechadas")


def main():
    dados = json.load(sys.stdin)
    if dados.get("agent_type") in SUBAGENTS_LIBERADOS:
        return  # chamada feita por um subagent (dev/qa/devops), não pelo PO
    cmd =(dados.get("tool_input") or {}).get("command", "").strip()
    if not cmd:
        bloquear("comando vazio")

    checar_metacaracteres(cmd)
    tokens = shlex.split(cmd)
    prog = tokens[0]

    # git -C <pasta>: só para o worktree de uma task (.claude/worktrees/<nome>).
    # O resto do comando passa pelas mesmas regras abaixo.
    if prog == "git" and len(tokens) > 1 and tokens[1].startswith("-C"):
        if tokens[1] == "-C":          # git -C <pasta> <comando>
            pasta = tokens[2] if len(tokens) > 2 else ""
            resto = tokens[3:]
        else:                          # git -C<pasta> <comando>
            pasta = tokens[1][2:]
            resto = tokens[2:]
        if not pasta:
            bloquear("git -C sem pasta")
        projeto = os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or os.getcwd()
        worktrees = os.path.realpath(os.path.join(projeto, ".claude", "worktrees"))
        alvo = os.path.realpath(os.path.join(projeto, pasta))
        if os.path.dirname(alvo) != worktrees:
            bloquear("git -C só é permitido no worktree de uma task (.claude/worktrees/<nome>)")
        tokens = ["git"] + resto

    sub = tokens[1] if len(tokens) > 1 else None

    if (prog, None) in PERMITIDOS:
        return
    if (prog, sub) not in PERMITIDOS:
        nome = f"{prog} {sub or ''}".strip()
        bloquear(f"'{nome}' não está na lista de comandos permitidos")

    args = tokens[2:]
    if any(a.startswith("--output") for a in args):
        bloquear("--output grava arquivos fora de .claude/")

    if prog == "gh" and (not args or args[0] not in GH_PR_PERMITIDOS):
        bloquear("só 'gh pr create', 'gh pr list', 'gh pr view' e 'gh pr merge' são permitidos")

    if prog == "gh" and args[0] == "merge":
        # Merge só com squash, só no fork, sem passar por cima das proteções do GitHub
        if "--squash" not in args and "-s" not in args:
            bloquear("o merge do PO deve ser sempre com --squash")
        if any(a in ("--merge", "-m", "--rebase", "-r", "--admin") for a in args):
            bloquear("merge commit, rebase e --admin não são permitidos ao PO")
        repo = None
        for i, a in enumerate(args):
            if a in ("--repo", "-R") and i + 1 < len(args):
                repo = args[i + 1]
            elif a.startswith("--repo="):
                repo = a.split("=", 1)[1]
        if repo != REPO_FORK:
            bloquear(f"o merge deve informar --repo {REPO_FORK}")

    if prog == "git" and sub == "pull":
        if any(a.startswith("--force") or a in ("-f", "--rebase", "-r") for a in args):
            bloquear("git pull do PO só pode ser fast-forward simples")

    if prog == "git" and sub == "push":
        if any(a in ("-f", "--force", "--force-with-lease", "--mirror", "--delete", "-d")
               or a.startswith("--force") or a.startswith("+") for a in args):
            bloquear("push forçado ou de remoção não é permitido ao PO")
        destinos = {a.split(":")[-1] for a in args if not a.startswith("-")}
        if destinos & BRANCHES_PROTEGIDOS:
            bloquear("o PO não faz push em main/ia-main (só no branch da task)")

    if prog == "git" and sub == "checkout" and ("--" in args or "." in args):
        bloquear("'git checkout -- <arquivo>' descarta alterações; use só para trocar de branch")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail closed
        bloquear(f"erro ao validar o comando ({e})")
    sys.exit(0)
