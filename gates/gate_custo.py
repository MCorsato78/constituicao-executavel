#!/usr/bin/env python3
"""
gate_custo.py — Invariantes de Custo (C1–C3) / Cost Invariants
Padrão Constituição Executável · MIT

Token é o único OpEx variável sem unidade de medida gerencial.
Este gate transforma o teto em cláusula: valida ANTES de executar (C1, C2)
e registra telemetria DEPOIS (C3). Determinístico, sem dependências.

Uso / Usage:
    # antes da execução — valida classe, teto e roteamento
    python gate_custo.py --classe consulta --tokens-estimados 45000 --modelo tier-economico

    # depois da execução — registra telemetria (C3)
    python gate_custo.py --registrar --classe producao --tokens-consumidos 88000 \
        --tarefa SPEC-014 --modelo tier-intermediario

Saída: exit 0 = aprovado · exit 1 = VETADO
Telemetria: telemetria_custo.jsonl (append-only, uma linha por execução)
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

# ── Espelho do Artigo 2 da CONSTITUICAO.md (edite junto com ela) ───────
CLASSES = {
    "consulta":  {"teto": 20_000,  "modelo_maximo": "tier-economico"},
    "producao":  {"teto": 150_000, "modelo_maximo": "tier-intermediario"},
    "critica":   {"teto": 500_000, "modelo_maximo": "tier-fronteira",
                  "exige_aprovacao": True},
}
ORDEM_TIERS = ["tier-economico", "tier-intermediario", "tier-fronteira"]
ARQUIVO_TELEMETRIA = Path("telemetria_custo.jsonl")


def validar(classe: str, tokens: int, modelo: str, aprovacao: str | None) -> list:
    violacoes = []
    if classe not in CLASSES:
        return [("C1", f"classe desconhecida: '{classe}' — toda tarefa nasce classificada")]
    regra = CLASSES[classe]

    # C1 — teto por execução
    if tokens > regra["teto"] and not aprovacao:
        violacoes.append(("C1", f"{tokens:,} tokens excede o teto de {regra['teto']:,} "
                                f"da classe '{classe}' sem aprovação registrada"))
    # C2 — roteamento como invariante
    if modelo and modelo not in ORDEM_TIERS:
        violacoes.append(("C2", f"tier desconhecido: '{modelo}' — roteamento fora dos tiers "
                                f"declarados na constituição ({', '.join(ORDEM_TIERS)})"))
    elif modelo and ORDEM_TIERS.index(modelo) > ORDEM_TIERS.index(regra["modelo_maximo"]):
        violacoes.append(("C2", f"classe '{classe}' roteada para '{modelo}' — "
                                f"máximo constitucional: '{regra['modelo_maximo']}'"))
    # classe crítica sempre exige aprovação
    if regra.get("exige_aprovacao") and not aprovacao:
        violacoes.append(("C1", "classe 'critica' exige aprovação humana registrada"))
    return violacoes


def registrar(args) -> None:
    """C3 — telemetria obrigatória: sem registro, não houve execução válida."""
    linha = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tarefa": args.tarefa,
        "classe": args.classe,
        "modelo": args.modelo,
        "tokens_consumidos": args.tokens_consumidos,
        "constituicao_versao": args.constituicao,
    }
    with ARQUIVO_TELEMETRIA.open("a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    print(f"C3 registrado: {args.tarefa} · {args.tokens_consumidos:,} tokens · {args.modelo}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--classe", required=True)
    p.add_argument("--tokens-estimados", type=int, default=0)
    p.add_argument("--tokens-consumidos", type=int, default=0)
    p.add_argument("--modelo", default="")
    p.add_argument("--aprovacao-id", default=None)
    p.add_argument("--tarefa", default="sem-spec")
    p.add_argument("--constituicao", default="1.0.0")
    p.add_argument("--registrar", action="store_true")
    args = p.parse_args()

    if args.registrar:
        registrar(args)
        sys.exit(0)

    violacoes = validar(args.classe, args.tokens_estimados, args.modelo, args.aprovacao_id)
    if violacoes:
        print("VETADO pela CONSTITUICAO.md (Artigo 2):", file=sys.stderr)
        for inv, detalhe in violacoes:
            print(f"  [{inv}] {detalhe}", file=sys.stderr)
        sys.exit(1)
    print(f"APROVADO — classe '{args.classe}', {args.tokens_estimados:,} tokens estimados.")
    sys.exit(0)


if __name__ == "__main__":
    main()
