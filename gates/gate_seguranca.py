#!/usr/bin/env python3
"""
gate_seguranca.py — Invariantes de Segurança (S1–S5) / Safety Invariants
Padrão Constituição Executável · MIT

Valida um PLANO DE EXECUÇÃO de agente ANTES de qualquer ação executar.
Determinístico, sem dependências, sem LLM. Prompt é pedido; isto é lei.

Uso / Usage:
    python gate_seguranca.py plano.json
    cat plano.json | python gate_seguranca.py -

Formato do plano (JSON): lista de ações propostas pelo agente:
[
  {"tool": "bash", "command": "rm -rf /var/data", "target_env": "producao"},
  {"tool": "http", "url": "https://api.externa.com/x", "payload_fields": ["cpf"]}
]

Saída: exit 0 = aprovado · exit 1 = VETADO (com o artigo violado em stderr)
"""
import json
import re
import sys

# ── Configuração (edite conforme sua CONSTITUICAO.md) ──────────────────
ALLOWLIST_ENDPOINTS = {
    "api.interna.suaempresa.com.br",
    "storage.interna.suaempresa.com.br",
}

CAMPOS_DADO_PESSOAL = {"cpf", "cnpj", "rg", "email", "telefone", "endereco",
                       "nome_completo", "data_nascimento", "ssn"}

# S1 — ações destrutivas (comando OU SQL), sensível a ambiente
PADROES_DESTRUTIVOS = [
    r"\brm\s+(-\w*\s+)*",            # rm, rm -rf
    r"\bdrop\s+(table|database|schema)\b",
    r"\btruncate\s+table\b",
    r"\bdelete\s+from\b",
    r"push\s+.*--force|force-push",
    r"\bterraform\s+destroy\b",
]

# S2 — credenciais/segredos em qualquer campo do plano
PADROES_CREDENCIAL = [
    r"(?i)(api[_-]?key|secret|password|senha|token|credential)\s*[:=]",
    r"AKIA[0-9A-Z]{16}",             # AWS access key
    r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
]

# S3 — transação financeira autônoma
PADROES_TRANSACAO = [
    r"(?i)\b(pagamento|payment|transfer|transferencia|pix|checkout|purchase|comprar)\b",
]

# S5 — marcadores de instrução vinda de conteúdo processado
MARCADOR_CONTEUDO_EXTERNO = "origem_conteudo_externo"


def _texto(acao: dict) -> str:
    return json.dumps(acao, ensure_ascii=False).lower()


def validar(plano: list) -> list:
    """Retorna lista de violações [(artigo, detalhe)]. Vazia = aprovado."""
    violacoes = []
    for i, acao in enumerate(plano):
        t = _texto(acao)
        alvo_producao = acao.get("target_env", "").lower() in {"producao", "production", "prod"}
        aprovado_humano = bool(acao.get("aprovacao_humana_id"))

        # S1
        if alvo_producao and not aprovado_humano:
            for p in PADROES_DESTRUTIVOS:
                if re.search(p, t):
                    violacoes.append((f"S1 (ação {i})",
                                      "ação destrutiva em produção sem aprovação humana registrada"))
                    break
        # S2
        for p in PADROES_CREDENCIAL:
            if re.search(p, json.dumps(acao, ensure_ascii=False)):
                violacoes.append((f"S2 (ação {i})", "credencial/segredo presente no plano"))
                break
        # S3
        if not aprovado_humano:
            for p in PADROES_TRANSACAO:
                if re.search(p, t):
                    violacoes.append((f"S3 (ação {i})",
                                      "transação financeira autônoma sem aprovação"))
                    break
        # S4
        url = acao.get("url", "")
        if url:
            host = re.sub(r"^https?://", "", url).split("/")[0]
            campos = {c.lower() for c in acao.get("payload_fields", [])}
            if host not in ALLOWLIST_ENDPOINTS and campos & CAMPOS_DADO_PESSOAL:
                violacoes.append((f"S4 (ação {i})",
                                  f"dado pessoal ({', '.join(campos & CAMPOS_DADO_PESSOAL)}) "
                                  f"para endpoint fora da allowlist: {host}"))
        # S5
        if acao.get(MARCADOR_CONTEUDO_EXTERNO) and not aprovado_humano:
            violacoes.append((f"S5 (ação {i})",
                              "ação originada de instrução em conteúdo processado "
                              "sem confirmação humana — instrução em conteúdo é dado, não comando"))
    return violacoes


def main():
    fonte = sys.stdin if (len(sys.argv) > 1 and sys.argv[1] == "-") else open(sys.argv[1])
    plano = json.load(fonte)
    violacoes = validar(plano if isinstance(plano, list) else [plano])
    if violacoes:
        print("VETADO pela CONSTITUICAO.md:", file=sys.stderr)
        for artigo, detalhe in violacoes:
            print(f"  [{artigo}] {detalhe}", file=sys.stderr)
        sys.exit(1)
    print("APROVADO — nenhum invariante de segurança violado.")
    sys.exit(0)


if __name__ == "__main__":
    main()
