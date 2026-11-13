#!/usr/bin/env python3
"""
Hook PreToolUse do agente PO.

Regra: o PO altera livremente arquivos dentro de .claude/ (ex: criar tasks,
inclusive tasks sobre o README). Para alterar QUALQUER arquivo fora de .claude/
(ex: README.md), o PO precisa da permissão do usuário.
Exceção dentro de .claude/: alterar a configuração dos agentes
(.claude/agents/, .claude/hooks/, .claude/settings*.json) também pede
permissão — o PO não pode mudar as próprias regras sozinho.

- Write / Edit / NotebookEdit: dentro de .claude/ libera; fora pede permissão
- Bash: funciona por LISTA DE PERMISSÃO. Só passam os comandos listados abaixo;
  todo o resto é bloqueado. Comandos permitidos que alteram arquivos fora de
  .claude/ (mv, cp, rm, redirecionamento >...) pedem permissão ao usuário.

Exit 0 = libera | Exit 2 = bloqueia (a mensagem no stderr volta para o agente)
Exit 0 + JSON com permissionDecision "ask" = pergunta ao usuário.
"""
import json
import os
import re
import shlex
import sys

data = json.load(sys.stdin)
tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {}) or {}

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
CWD = data.get("cwd") or PROJECT_DIR
ALLOWED_DIR = os.path.realpath(os.path.join(PROJECT_DIR, ".claude"))


def bloquear(motivo):
    print(f"BLOQUEADO (agente PO): {motivo}.", file=sys.stderr)
    sys.exit(2)


def pedir_permissao(motivos):
    texto = "; ".join(motivos)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason":
                f"Agente PO quer alterar arquivo protegido ({texto}). "
                "Autorizar?",
        }
    }, ensure_ascii=False))
    sys.exit(0)


# Alterações fora de .claude/ encontradas no comando: viram pedido de permissão
FORA = []


def dentro_do_claude(caminho):
    alvo = os.path.realpath(os.path.join(CWD, os.path.expanduser(caminho)))
    return alvo == ALLOWED_DIR or alvo.startswith(ALLOWED_DIR + os.sep)


def protegido(caminho):
    """Configuração dos agentes: mesmo dentro de .claude/, exige permissão."""
    alvo = os.path.realpath(os.path.join(CWD, os.path.expanduser(caminho)))
    rel = os.path.relpath(alvo, ALLOWED_DIR)
    if rel.split(os.sep)[0] in ("agents", "hooks"):
        return True
    return re.fullmatch(r"settings[^/]*\.json", rel) is not None


def precisa_permissao(caminho):
    return not dentro_do_claude(caminho) or protegido(caminho)


def checar_caminhos(cmd_nome, args):
    """Todo argumento que não é flag precisa estar dentro de .claude/."""
    for arg in args:
        if arg.startswith("-"):
            if "=" in arg:                      # ex: --target-directory=/x
                arg = arg.split("=", 1)[1]
            else:
                continue
        if precisa_permissao(arg):
            FORA.append(f"'{cmd_nome}' em {arg}")


# ============================================================
# Write / Edit / NotebookEdit
# ============================================================
if tool in ("Write", "Edit", "NotebookEdit"):
    arquivo = tool_input.get("file_path") or tool_input.get("notebook_path")
    if arquivo and precisa_permissao(arquivo):
        pedir_permissao([f"{tool} em {arquivo}"])
    sys.exit(0)

if tool != "Bash":
    sys.exit(0)

# ============================================================
# Bash
# ============================================================
comando = tool_input.get("command", "")

# Construções que permitem esconder comandos dentro de outros
if re.search(r"\$\(|`|<<|[<>]\(", comando):
    bloquear("$(...), crases, heredoc (<<) e <(...) não são permitidos — "
             "para textos longos (ex: corpo do PR) crie um arquivo em .claude/ "
             "com a ferramenta Write e use --body-file")

# Quebra o comando em tokens respeitando aspas.
# Quebra de linha conta como separador de comandos (igual ao ;)
try:
    lexer = shlex.shlex(comando, posix=True, punctuation_chars=";&|<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    tokens = list(lexer)
except ValueError:
    bloquear("não foi possível interpretar o comando (aspas não fechadas?)")


# Separa em subcomandos e trata redirecionamentos (> >> <)
subcomandos, atual, i = [], [], 0
while i < len(tokens):
    tok = tokens[i]
    if re.fullmatch(r"[;&|\n]+", tok):              # separador de comandos
        if atual:
            subcomandos.append(atual)
        atual = []
    elif re.fullmatch(r"[<>&|]+", tok):          # operador de redirecionamento
        alvo = tokens[i + 1] if i + 1 < len(tokens) else ""
        i += 1
        if ">" in tok and not (tok.endswith("&") or alvo.isdigit() or alvo == "/dev/null"):
            if precisa_permissao(alvo):
                FORA.append(f"redirecionamento para {alvo}")
        if atual and atual[-1].isdigit():         # descritor tipo 2>
            atual.pop()
    else:
        atual.append(tok)
    i += 1
if atual:
    subcomandos.append(atual)

# ------------------------------------------------------------
# Regras por comando
# ------------------------------------------------------------
LEITURA = {"ls", "cat", "head", "tail", "grep", "wc", "pwd", "echo", "date", "jq", "find"}
ESCRITA = {"mkdir", "mv", "cp", "rm", "rmdir", "touch"}
FIND_PROIBIDO = {"-exec", "-execdir", "-ok", "-okdir", "-delete",
                 "-fprint", "-fprint0", "-fprintf", "-fls"}


def checar_git(a):
    if len(a) < 2:
        bloquear("comando git incompleto")
    sub, resto = a[1], a[2:]

    if sub.startswith("-"):
        bloquear("opções globais do git (-c, -C, --git-dir...) não são permitidas")
    for x in a:
        if re.match(r"--(upload-pack|receive-pack|exec|output|ext-diff)", x):
            bloquear(f"opção do git não permitida: {x}")

    if sub in ("status", "log", "diff", "show", "fetch", "add", "commit", "rev-parse"):
        return
    if sub in ("mv", "rm"):
        return checar_caminhos(f"git {sub}", resto)
    if sub == "branch":
        if all(x in ("-a", "-r", "-v", "-vv", "--list", "--all",
                     "--remotes", "--show-current") for x in resto):
            return
        bloquear("git branch só é permitido para listar branches")
    if sub in ("checkout", "switch"):
        flag = "-b" if sub == "checkout" else "-c"
        if len(resto) == 2 and resto[0] == flag and not resto[1].startswith("-"):
            return
        bloquear(f"git {sub} só é permitido para criar branch nova: git {sub} {flag} <nome>")
    if sub == "push":
        for x in resto:
            if x in ("--force", "--force-with-lease", "--force-if-includes",
                     "--delete", "--mirror", "--all", "--prune"):
                bloquear(f"git push {x} não é permitido")
            if re.fullmatch(r"-[a-zA-Z]+", x) and re.search(r"[fd]", x):
                bloquear(f"git push {x} não é permitido (force/delete)")
            if not x.startswith("-") and (x.startswith("+") or ":" in x):
                bloquear(f"refspec não permitido no push: {x}")
        return
    if sub == "remote" and resto in ([], ["-v"]):
        return
    bloquear(f"'git {sub}' não está na lista de comandos permitidos do PO")


def checar_gh(a):
    if len(a) >= 3 and a[1] == "pr" and a[2] in (
            "create", "view", "list", "status", "diff", "checks", "comment", "edit"):
        return
    if a[1:3] in (["auth", "status"], ["repo", "view"]):
        return
    bloquear(f"'{' '.join(a[:3])}' não está na lista de comandos permitidos do PO")


for args in subcomandos:
    nome = args[0]

    if "/" in nome or "=" in nome:
        bloquear(f"executar '{nome}' não é permitido")

    if nome in LEITURA:
        if nome == "find" and FIND_PROIBIDO.intersection(args):
            bloquear("find com -exec/-delete/-fprint não é permitido")
        continue
    if nome in ESCRITA:
        checar_caminhos(nome, args[1:])
        continue
    if nome == "git":
        checar_git(args)
        continue
    if nome == "gh":
        checar_gh(args)
        continue

    bloquear(f"o comando '{nome}' não está na lista de comandos permitidos do PO")

if FORA:
    pedir_permissao(FORA)

sys.exit(0)
