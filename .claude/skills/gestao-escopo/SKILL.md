---
name: gestao-escopo
description: >-
  PMBOK scope management for ACH2027: the scope baseline (Declaração do Escopo, EAP/WBS,
  Dicionário da EAP), how to decompose an EAP and how to review one. Use for Exercício 1, or
  whenever the user mentions escopo, EAP, WBS, pacote de trabalho, dicionário da EAP or linha de
  base do escopo.
---

# Gestão do Escopo

Scope management makes the project do all the work it needs and nothing else. The detailed
processes are in PMBOK 6th ed., chapter 5: planejar, coletar requisitos, definir o escopo,
criar a EAP, validar e controlar o escopo.

**Linha de base do escopo** = Declaração do Escopo + EAP + Dicionário da EAP. Change it only
through change control.

## Declaração do Escopo

Sections, in the order the group uses (Exercício 1):
descrição do escopo do produto, critérios de aceitação, entregas, exclusões, restrições, premissas.
Every exclusion must be stated plainly ("fora do escopo: CFTV não integrado"), because anything
not excluded is open to interpretation.

## Building the EAP

1. **Level 1**: the project itself (`1 Sistema de Controle de Acesso`).
2. **Level 2**: phases of the life cycle *or* major deliverables. Pick one criterion per level.
3. **Decompose** each element until it reaches a **pacote de trabalho**, the lowest level, where
   cost, duration and resources can be estimated and one person owns it.
4. **Code** every element hierarchically (1, 1.1, 1.1.1). The same codes carry over to the
   dictionary and the schedule.
5. Write the **Dicionário da EAP** for every work package.

Review checklist:
- [ ] **Regra dos 100%**: the children add up to exactly the parent. No work is missing, and
      nothing from the exclusions sneaks in.
- [ ] **Substantivos**: elements are deliverables ("Módulo de Relatórios"), never actions
      ("Desenvolver relatórios"). Verbs belong to schedule activities.
- [ ] A **Gerenciamento do projeto** branch exists, since management work is part of the 100%.
- [ ] No element has a single child; decompose into two or more, or not at all.
- [ ] Work packages are sized to control: the 8/80 heuristic (8 to 80 hours of effort) is a
      rule of thumb, not a PMBOK rule.
- [ ] One owner per work package.
- [ ] No sequence, arrows or dates: the EAP is not a schedule.

## Dicionário da EAP

Fields per work package (PMBOK 6, 5.4.3.1): código, descrição do trabalho, premissas e
restrições, responsável, marcos, atividades associadas, recursos, estimativa de custo,
requisitos de qualidade, critérios de aceitação, referências técnicas, informações de acordos.
When a field is unknown, write "a definir" rather than inventing a value.

One compact table per work package reads better than one giant table:

```latex
\begin{tabular}{|p{4cm}|p{12cm}|}
  \hline \multicolumn{2}{|l|}{\textbf{1.4.3 Módulo de Rotinas Especiais}} \\ \hline
  \textbf{Descrição} & ... \\ \hline
  \textbf{Critérios de aceitação} & ... \\ \hline
  \textbf{Responsável} & ... \\ \hline
\end{tabular}
```

## Drawing the EAP

The group exports a Mermaid diagram as a PNG, using `flowchart LR` because top-down overflows
A4. The vector alternative is `forest`, with an indented tree that fits portrait:

```latex
\usepackage[edges]{forest}
\begin{forest}
  for tree={folder, grow'=0, draw, rounded corners, font=\small}
  [1 Sistema de Controle de Acesso
    [1.1 Gerenciamento do projeto [1.1.1 Plano do projeto]]
    [1.2 Requisitos [1.2.1 Documento de requisitos]]]
\end{forest}
```

## Citing

Chapter 5 is from PMBOK **6th ed.** (2017). The 7th ed. (2021) is organised by principles and
performance domains and has no scope chapter, so cite the edition the text actually follows:
PROJECT MANAGEMENT INSTITUTE. **Um guia do conhecimento em gerenciamento de projetos (Guia
PMBOK)**. 6. ed. Newtown Square, PA: Project Management Institute, 2017.
