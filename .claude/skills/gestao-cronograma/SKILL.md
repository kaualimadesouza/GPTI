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
% gpti.sty loads tikz with the babel and quotes libraries: without babel, "A" breaks under brazil
\begin{tikzpicture}[x=1.26cm, y=1.9cm, >=Stealth,
    evento/.style={circle, draw, minimum size=6mm, font=\sffamily\scriptsize},
    ativ/.style={->, semithick}, fantasma/.style={->, dashed},
    every edge quotes/.style={font=\sffamily\scriptsize, auto, sloped}]
  \node[evento] (e1) at (0, 0) {1};  \node[evento] (e2) at (1, 0) {2};
  \node[evento] (e3) at (2, 1) {3};  \node[evento] (e4) at (2, 0) {4};
  \path (e1) edge[ativ, "A", "1"'] (e2);   % letter above, weeks below
  \path (e2) edge[ativ, "B", "2"'] (e3);
  \path (e2) edge[ativ, "C", "3"'] (e4);
  \path (e3) edge[fantasma] (e4);          % without it, B and C would both run from 2 to 4
\end{tikzpicture}
```

Exercício 2 does not draw by hand: `exercicios/2-cronograma/rede/aoa.py` builds the network with
no unneeded dummy from its `ACTIVITIES` table, runs the critical path, and writes the table rows,
the TikZ picture and the numbers the text quotes. Edit the table there and rerun it.

## 5. Caminho crítico

- **Ida** (forward pass): earliest time of each event = max over incoming arrows of (earliest
  time of the tail + duration).
- **Volta** (backward pass): latest time = min over outgoing arrows of (latest time of the
  head - duration).
- **Folga total** of an activity = latest time of its head - earliest time of its tail - duration.
- Activities with zero folga form the critical path; its length is the project duration.
  Highlight it in the network (`very thick, red`) and state the total duration in the text.
