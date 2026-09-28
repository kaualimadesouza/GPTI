---
name: gestao-cronograma
description: >-
  Schedule management for ACH2027: defining activities from EAP work packages, estimating
  durations, setting precedences, drawing an AOA (activity-on-arrow) network and finding the
  critical path, with a TikZ template. Use for Exercício 2, or whenever the user mentions
  cronograma, atividades, duração, precedência, rede AOA/AON, PERT, CPM, caminho crítico or folga.
---

# Gestão do Cronograma

PMBOK 6th ed., chapter 6: planejar, definir as atividades, sequenciar, estimar as durações,
desenvolver e controlar o cronograma. Input: the EAP and its dictionary (see `gestao-escopo`).

## 1. Definir as atividades

- Break each **pacote de trabalho** into activities written as verb + object ("Configurar rede").
- Each activity belongs to exactly one work package. Its ID extends the package code
  (1.4.3 → 1.4.3.1, 1.4.3.2).
- **Marcos** (milestones) have zero duration: "Termo de aceite assinado".
- Leave level-of-effort work (weekly meetings, ongoing management) out of the network: it
  spans the whole project and would dominate the critical path.

## 2. Estimar as durações

Techniques: análoga, paramétrica, três pontos, bottom-up, opinião especializada.
- Três pontos, triangular: `tE = (O + M + P) / 3`
- Três pontos, beta (PERT): `tE = (O + 4M + P) / 6`, with `desvio = (P - O) / 6`

Duration is not effort: 80 hours of work by 2 people is 1 week, not 2. Use one unit
(semanas) throughout, and say which technique was used.

## 3. Definir as precedências

Relation types: **TI** (término-início, the default), II, TT, IT. Dependencies are
obrigatórias, arbitradas, externas or internas, and may carry antecipação (lead) or espera (lag).

| ID | Atividade | Duração | Predecessoras |
| --- | --- | --- | --- |
| A | Especificações | 1 sem | - |
| B | Cotação | 2 sem | A |

Check that there are no cycles, and that every activity starts from the project start and
leads to the project end, with no loose ends.

## 4. Rede AOA (atividade na seta)

- **Nodes are events** (numbered circles), **arrows are activities**, labelled `ID (duração)`.
- Only TI relations. One start event and one end event. Number events so each arrow goes from
  a lower to a higher number.
- **Atividade fantasma** (dummy): dashed arrow with zero duration. Needed when two activities
  would share both start and end events, or when an activity depends on only part of another's
  predecessors.
- AOA is not in PMBOK 6, which only describes the precedence diagram (AON). Cite the course
  material for it.

```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning}
\begin{tikzpicture}[>=Stealth, node distance=1.6cm and 2.4cm,
    ev/.style={circle, draw, minimum size=8mm, font=\small},
    act/.style={->, thick}, dum/.style={->, dashed}]
  \node[ev] (1) {1};
  \node[ev, right=of 1] (2) {2};
  \node[ev, above right=of 2] (3) {3};
  \node[ev, below right=of 3] (4) {4};
  \node[ev, right=of 4] (5) {5};
  \draw[act] (1) -- node[above] {A (1)} (2);
  \draw[act] (2) -- node[above left] {B (2)} (3);
  \draw[act] (2) -- node[below] {C (3)} (4);
  \draw[dum] (3) -- (4);  % B and C both precede D: B cannot also end at 4
  \draw[act] (4) -- node[above] {D (2)} (5);
\end{tikzpicture}
```

## 5. Caminho crítico

- **Ida** (forward pass): earliest time of each event = max over incoming arrows of (earliest
  time of the tail + duration).
- **Volta** (backward pass): latest time = min over outgoing arrows of (latest time of the
  head - duration).
- **Folga total** of an activity = latest time of its head - earliest time of its tail - duration.
- Activities with zero folga form the critical path; its length is the project duration.
  Highlight it in the network (`very thick, red`) and state the total duration in the text.
