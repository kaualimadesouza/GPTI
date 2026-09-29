---
name: politica-uso-ia
description: >-
  ACH2027 generative-AI policy as it applies to the agent's own work: what every deliverable must
  declare and how to write the "Registro de Uso de IA". Use before any task in this repository,
  and whenever an exercise, seminar or the semester project is written, edited, reviewed or sent.
---

# Política de Uso de IA (ACH2027)

Every final delivery must include (from the exercise statements):
- the bibliographic references and other material used in the research;
- the **Registro de Uso de IA** for that deliverable, as the course policy describes.

The policy PDF (`docs/ACH2027_Politica_Uso_IA_2026.pdf`) is not in the repo yet. Once it is, it
overrides this skill: read it and update this file to match.

## The agent's own use counts

Anything you (Claude, Gemini or any other agent) write or rewrite for a deliverable is AI use and
gets its own registro entry, in the same table as the group's entries. Add a column per registro
(`Registro 0N: <tema>`):

| Linha | What goes in it |
| --- | --- |
| Problema / Objetivo | What the group needed, in one sentence |
| Ferramenta de IA | The tool and model actually used, with month/year: `Claude Opus 5.5 (Setembro/2026)`, `Gemini 3.1 Pro (Setembro/2026)` |
| Comandos | The user's actual requests, each in `\enquote{}` and shortened with `...` |
| Revisão dos resultados | The group's critical review: what was wrong, changed or rejected, and why |
| Aplicação no trabalho | Which section used the result |

## Rules

1. **Never write "Revisão dos resultados" as if the group had reviewed.** Put
   `\textcolor{red}{[PREENCHER: revisão do grupo]}` there, and in the reply list what the group
   should check (claims, numbers, decisions you made on your own).
2. Never remove or reword earlier registros; add new ones.
3. Cite only sources that exist and were actually consulted. No invented page numbers,
   editions or URLs. If a claim has no source, say so instead of attaching one.
4. The group has to understand and defend the text. Explain non-obvious choices in the
   reply, keep the prose plain, and prefer short content the group can check over volume.
5. Exercises list the references and the other research material inside the deliverable
   (the statements require it). The seminar used a separate `Guia de pesquisa e Uso de IA`
   .docx for the research links and kept only the final bibliography in the slides.

## Registro table (group model, LaTeX)

```latex
\section{Registro de Uso de Inteligência Artificial}
\begin{table}[H]
    \centering
    \renewcommand{\arraystretch}{1.5}
    \small
    \begin{tabular}{|>{\raggedright\arraybackslash}p{3cm}|p{6cm}|p{6cm}|}
        \hline
        \rowcolor{eapC}
        \textbf{Registro de Uso de IA} & \textbf{Registro 01: ...} & \textbf{Registro 02: ...} \\
        \hline
        \textbf{Problema / Objetivo} & ... & ... \\ \hline
        \textbf{Ferramenta de IA} & ... & ... \\ \hline
        \textbf{Comandos} & ... & ... \\ \hline
        \textbf{Revisão dos resultados} & ... & ... \\ \hline
        \textbf{Aplicação no trabalho} & ... & ... \\ \hline
    \end{tabular}
    \caption{Registro de Uso de IA Generativa.}
\end{table}
```

`gpti.sty` loads what this needs (`float`, `array`, `colortbl`, `csquotes`). Two registros fill the
A4 width. A third one starts a continuation table with the same rows, and the numbering carries on.
Straight quotes break under babel `brazil`, so quote the prompts with `\enquote{}`.
