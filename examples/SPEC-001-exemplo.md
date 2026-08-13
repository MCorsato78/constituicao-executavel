# SPEC-001 — Relatório semanal de custo de tokens por área

```yaml
constituicao: v1.0.0        # ← Artigo 4: herança declarada. Sem isto, a spec é inválida.
classe_de_tarefa: producao  # ← Artigo 2: define teto (150k tokens) e roteamento (tier-intermediario)
autor: <tech lead>
data: 2026-08-13
```

## Objetivo

Gerar, toda sexta 08h00, um relatório em Markdown com o consumo de tokens
da semana por área, a partir de `telemetria_custo.jsonl`, com variação
contra a média das 4 semanas anteriores.

## Critérios de aceite

1. Todo número no relatório referencia o cálculo de origem (**herda E3** — verificado por `gate_evidencia.py`).
2. Execução consome ≤ 150.000 tokens (**herda C1**) e roteia no máximo para tier-intermediario (**herda C2**).
3. O relatório é salvo em `relatorios/` — nenhuma escrita fora deste diretório.
4. Se `telemetria_custo.jsonl` estiver vazio ou ausente, o agente reporta o gap e **para** — não estima, não inventa (herda E3).

## Restrições adicionais (mais restritivas que a constituição — permitido)

- Modelo máximo desta spec: `tier-economico` (mais apertado que o teto da classe — Artigo 4.2 permite).
- Sem acesso à rede: a tarefa é local.

## O que esta spec NÃO pode fazer

Relaxar qualquer invariante da constituição v1.0.0. Em conflito, a
constituição vence, a execução para e o conflito é registrado (Artigo 4.3).
