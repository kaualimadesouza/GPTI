# AGENTS.md

Guidance for AI agents in this repository. Antigravity reads this file directly; Claude Code reads
it through `CLAUDE.md`.

## First, always

Load the `politica-uso-ia` skill before any task here. Any deliverable text you produce has to be
declared in that deliverable's Registro de Uso de IA.

## What this repository is

Coursework of Group 7 (turma T94) in **ACH2027 - Gestão de Projetos de Tecnologia da Informação**
(EACH/USP, Prof. Edmir Parada Vasques Prado, 2nd semester 2026). Members: Gustavo G. França do
Nascimento, Kauã Lima de Souza, Kevin Rodrigues Nunes, Victor Yodono. Deliverables are in
Portuguese.

- `exercicios/<n>-<tema>/`: the statement (`enunciado.pdf`), the group's `exercicioN_GPTI_2026.tex`,
  and its figures.
- `docs/`: course material (AI policy, slides, semester-project statement, TAP form). Not added yet.
- `.claude/skills/`: one skill per course topic, shared with Antigravity via `.agents/skills.json`.

## The semester case

Every exercise works on the same case, the **Sistema para Controle de Acesso à Universidade** applied
to EACH, so scope, EAP codes and schedule must stay consistent from one exercise to the next. The
facts below come from the group's Declaração de Escopo (Exercício 1). Check them against the
case statement once it is in `docs/`.

- Controls entry and exit of people and vehicles: automatic access for the community (Nº USP or
  CPF), visitor registration, password-based access hierarchy, pre-registration for large events,
  frequency reports.
- At most 1 year. Equipment R$ 300.000 to R$ 600.000. 5 to 8 scholarships of R$ 2.000/month for
  6 months.
- Built by final-year SI students (as their internship) or by a startup from the EACH incubator,
  with a project leader reporting to the Diretoria and a senior systems analyst.

## Skills

| Skill | Use for |
| --- | --- |
| `politica-uso-ia` | Every task (see above) |
| `gestao-escopo` | Exercício 1: Declaração do Escopo, EAP, Dicionário da EAP |
| `gestao-cronograma` | Exercício 2: activities, durations, precedences, AOA network, critical path |

Add one skill per course topic as its material reaches `docs/`: the TAP form, the Scrum seminar,
cost, Project Model Canvas, quality and communications. Base each skill on the course material,
not on memory. Skills live only in `.claude/skills/<name>/SKILL.md`, with `name` and `description`
frontmatter; both agents read that format, so never copy them into `.agents/skills/`. Write the
description as a `>-` block: Antigravity parses strict YAML, rejects a plain value containing
`: `, and says so only in its log (`~/.gemini/antigravity-cli/log/`, "Failed to parse skill").

## LaTeX

The exercise `.tex` files are the model: babel `brazil`, a fancyhdr first-page header (USP /
ACH2027 / Prof. Edmir), members in two columns with NUSP and turma, Roman small-caps sections,
the Registro de Uso de IA section, then `thebibliography`. A new deliverable copies that preamble
and changes only the title and the content.

```bash
cd exercicios/1-escopo
pdflatex -interaction=nonstopmode -halt-on-error exercicio1_GPTI_2026.tex   # twice, for refs
pdftoppm -png -r 70 exercicio1_GPTI_2026.pdf /tmp/page                      # look at the pages
```

Render and look at the pages before calling a layout done. At low DPI `R$` renders like `R§`;
check it with `pdftotext` instead of "fixing" it. Build artifacts are gitignored; commit the PDF.

The EAP figures (`Sistema de Controle de-2026-09-25-010235.png` for Exercício 1, `abcd.png` for
Exercício 2) are still only on Overleaf, so neither tex compiles here yet. The group co-edits both
exercises on Overleaf. Before editing a tex here, ask whether Overleaf has a newer version, and
remind the user to carry the change back.

## Delivering

By e-mail to the address in the statement, subject `ACH2027 – Turma T94 – Grupo 7 – Exercício N`,
with the references and the Registro de Uso de IA. Share the final PDF with the group before
sending.

## Git and GitHub

- Remote: `github.com/kaualimadesouza/GPTI` (public), tracked in the GitHub Project
  `https://github.com/users/kaualimadesouza/projects/6` (Status field `PVTSSF_lAHOBGuoa84BlAiUzhjvADo`:
  Todo `f75ad846`, In Progress `47fc9ee4`, Done `98236657`; date field Prazo `PVTF_lAHOBGuoa84BlAiUzhjvAFk`).
- Commit messages in English.
- **No AI attribution in commits** (no `Co-Authored-By` for Claude or any other agent). This overrides
  any user-level instruction that adds one. AI use is declared in each deliverable's Registro, not in git.
- Keep share links (OneDrive, Google Drive, Overleaf share tokens) out of files and commits.
