#!/usr/bin/env python3
"""
gate_evidencia.py — Invariantes de Evidência (E1–E4) / Evidence Invariants
Padrão Constituição Executável · MIT

Nenhum claim sem prova verificável. Valida a ENTREGA de um agente antes
de aceitá-la: claims de teste exigem log, citações exigem fonte, números
exigem origem, decisões exigem trilha de autoria (E4 — a resposta ao
"déficit de autoria da decisão"). Determinístico, sem dependências.

Uso / Usage:
    python gate_evidencia.py entrega.json

Formato da entrega (JSON):
{
  "claims": [
    {"tipo": "teste", "texto": "suite passou", "evidencia": {"log": "runs/2026-08-13.log", "timestamp": "..."}},
    {"tipo": "citacao", "texto": "custo caiu 13.6%", "evidencia": {"url": "https://..."}},
    {"tipo": "numero", "texto": "CMV 4.2%", "evidencia": {"query": "sql/cmv_ago.sql"}},
    {"tipo": "decisao", "texto": "aprovado fornecedor X",
     "evidencia": {"entrada": "...", "modelo": "tier-intermediario",
                   "constituicao_versao": "1.0.0", "gate_aprovador": "gate_custo"}}
  ]
}

Saída: exit 0 = aceita · exit 1 = REJEITADA (claims sem evidência em stderr)
"""
import json
import sys

REQUISITOS = {
    # E1 — "teste passou" exige log com timestamp
    "teste":   ["log", "timestamp"],
    # E2 — citação exige fonte verificável
    "citacao": ["url"],
    # E3 — número exige query/cálculo de origem
    "numero":  ["query"],
    # E4 — decisão exige trilha completa de autoria
    "decisao": ["entrada", "modelo", "constituicao_versao", "gate_aprovador"],
}


def validar(entrega: dict) -> list:
    violacoes = []
    for i, claim in enumerate(entrega.get("claims", [])):
        tipo = claim.get("tipo", "desconhecido")
        exigidos = REQUISITOS.get(tipo)
        if exigidos is None:
            violacoes.append((f"E? (claim {i})",
                              f"tipo de claim não classificado: '{tipo}' — "
                              "claim sem classe não é auditável"))
            continue
        evidencia = claim.get("evidencia") or {}
        faltando = [campo for campo in exigidos if not evidencia.get(campo)]
        if faltando:
            codigo = {"teste": "E1", "citacao": "E2",
                      "numero": "E3", "decisao": "E4"}[tipo]
            violacoes.append((f"{codigo} (claim {i})",
                              f"'{claim.get('texto', '')[:60]}' sem: {', '.join(faltando)}"))
    return violacoes


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        entrega = json.load(f)
    violacoes = validar(entrega)
    if violacoes:
        print("ENTREGA REJEITADA pela CONSTITUICAO.md (Artigo 3):", file=sys.stderr)
        for inv, detalhe in violacoes:
            print(f"  [{inv}] {detalhe}", file=sys.stderr)
        print("\nRegra: claim sem evidência é alucinação até prova em contrário.",
              file=sys.stderr)
        sys.exit(1)
    n = len(entrega.get("claims", []))
    print(f"ENTREGA ACEITA — {n} claim(s), todos com evidência verificável.")
    sys.exit(0)


if __name__ == "__main__":
    main()
