# Constituição Executável / Executable Constitution

> **PT-BR** · Um padrão aberto para governar sistemas com agentes de IA: um arquivo de invariantes — de segurança **e de custo** — imposto por código, não apenas escrito num prompt esperando que o modelo obedeça.
>
> **EN** · An open pattern for governing AI agent systems: a file of invariants — safety **and cost** — enforced by code, not just written in a prompt hoping the model complies.

*Determinístico primeiro. LLM só onde o determinístico não alcança. / Deterministic first. LLM only where deterministic doesn't reach.*

---

## 🇧🇷 Português

### O problema

Todos os incidentes documentados de agentes autônomos que causaram dano seguem o mesmo padrão: **a regra existia, escrita em prompt — o enforcement não existia**. Prompt é pedido, não é lei. Regras degradam em sessões longas, specs são negociáveis pelo modelo dentro da sessão, e limites de custo raramente são tratados como invariantes.

A maioria das empresas governa agentes hoje com regras críticas escritas onde o sistema pode ignorá-las. **Post-its colados na motosserra.**

### O padrão

Duas camadas de documento, uma camada de enforcement:

```
CONSTITUICAO.md          ← invariantes: o que NENHUMA tarefa pode fazer
   └── SPEC-<id>.md      ← por tarefa: o que ESTA tarefa deve fazer
gates/                   ← verificação determinística ANTES da ação executar
```

| Camada | Muda quando | Quem assina | Enforcement |
|---|---|---|---|
| `CONSTITUICAO.md` | Raramente (versionada, revisada como política de alçada) | CFO **e** CISO/CTO | Gates determinísticos + telemetria |
| `SPEC-<id>.md` | A cada tarefa/demanda | Tech lead | Critérios de aceite herdando a constituição |
| `gates/` | Junto com a constituição | Engenharia | Código, não prompt |

### As quatro classes de invariante

1. **Segurança** — o que o sistema nunca faz (deletar produção, tocar credencial, transacionar), independente de tarefa, sessão ou modelo.
2. **Custo** — quanto, no máximo, cada classe de tarefa pode consumir. Token é OpEx variável sem unidade de medida gerencial; o teto é cláusula constitucional, não sugestão.
3. **Evidência** — nenhuma afirmação sem prova verificável. "Teste passou" exige log anexado; citação exige fonte.
4. **Herança** — toda spec nasce subordinada à constituição e declara isso explicitamente.

### Comece aqui

1. Leia o template comentado: [`CONSTITUICAO.md`](CONSTITUICAO.md)
2. Veja a herança em prática: [`examples/SPEC-001-exemplo.md`](examples/SPEC-001-exemplo.md)
3. Rode os gates de referência: [`gates/`](gates/) (Python puro, sem dependências)

```bash
# exemplo: validar um plano de execução de agente contra a constituição
python gates/gate_seguranca.py examples/plano_exemplo.json
python gates/gate_custo.py --classe consulta --tokens-estimados 45000
```

### Maturidade: em que nível está a sua operação?

| Nível | Estado |
|---|---|
| **N0** | Regras em prompt / post-it. Nenhum enforcement. |
| **N1** | Regras documentadas por projeto, ainda dependentes do modelo obedecer. |
| **N2** | Constituição escrita e versionada; enforcement parcial/manual. |
| **N3** | Gates determinísticos bloqueando ações; specs herdam a constituição. |
| **N4** | N3 + telemetria de custo por tarefa + trilha de autoria de decisão auditável. |

---

## 🇬🇧 English

### The problem

Every documented incident of an autonomous agent causing damage follows the same pattern: **the rule existed, written in a prompt — the enforcement didn't**. A prompt is a request, not a law. Rules degrade over long sessions, specs are negotiable by the model mid-session, and cost limits are rarely treated as invariants.

Most companies govern agents today with critical rules written where the system can ignore them. **Post-it notes taped to a chainsaw.**

### The pattern

Two document layers, one enforcement layer:

```
CONSTITUTION.md          ← invariants: what NO task may ever do
   └── SPEC-<id>.md      ← per task: what THIS task must do
gates/                   ← deterministic checks BEFORE the action executes
```

### The four invariant classes

1. **Safety** — what the system never does (delete production, touch credentials, transact), regardless of task, session, or model.
2. **Cost** — the maximum each task class may consume. Tokens are the only variable OpEx without a management unit of measure; the ceiling is a constitutional clause, not a suggestion. This is the layer most harness discussions leave out — it's what puts the CFO and the CISO on the same document.
3. **Evidence** — no claim without verifiable proof. "Tests passed" requires the attached log; a citation requires the source.
4. **Inheritance** — every spec is born subordinate to the constitution and declares it explicitly.

### Start here

1. Read the annotated template: [`CONSTITUTION.md`](CONSTITUTION.md)
2. See inheritance in practice: [`examples/SPEC-001-exemplo.md`](examples/SPEC-001-exemplo.md)
3. Run the reference gates: [`gates/`](gates/) (pure Python, zero dependencies)

### Maturity ladder

**N0** rules in prompts → **N1** documented per project → **N2** versioned constitution, partial enforcement → **N3** deterministic gates + spec inheritance → **N4** N3 + per-task cost telemetry + auditable decision-authorship trail.

---

## Filosofia / Philosophy

- A constituição é **enxuta**: só invariantes. Se cabe discussão caso a caso, vai para a spec. / The constitution is **lean**: invariants only. If it's debatable case-by-case, it belongs in the spec.
- Constituição define **o quê**; arquitetura entrega **o como**. Prompt injection e a tríade letal exigem arquitetura — o documento sozinho é teatro. / The constitution defines the **what**; architecture delivers the **how**.
- Invariantes são **portáveis entre modelos**. Quem depende de API de fronteira precisa de regras que sobrevivem à troca de fornecedor. / Invariants are **portable across models**.

## Autor / Author

**Marcos Corsato** — 30 anos atravessando os dois lados do balanço: 10 em gestão financeira, 20 em dados e tecnologia. / 30 years across both sides of the balance sheet: 10 in financial management, 20 in data & technology.

- Newsletter: [CFO&IA — Radar](https://www.linkedin.com/in/marcos-corsato) · Consultoria: [Fulcria](https://fulcria.com.br) · YouTube: [@MyOpenClaw](https://youtube.com/@MyOpenClaw)

Artigo de referência / Reference article: *"CONSTITUIÇÃO.md — a camada que falta entre o seu agente de IA e o seu balanço"* (LinkedIn).

## Licença / License

MIT — use, adapte, imponha. / MIT — use it, adapt it, enforce it.

*Medido, não achado. / Measured, not assumed.*
