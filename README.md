# ACH2027: Gestão de Projetos de TI

Grupo 7, turma T94. EACH/USP, Prof. Edmir Parada Vasques Prado, 2º semestre de 2026.

Projeto semestral: **Sistema para Controle de Acesso à Universidade**, aplicado à EACH.

## Entregas

| Entrega | Pasta | Prazo final | Situação |
| --- | --- | --- | --- |
| Exercício 1: Gestão de Escopo | [`exercicios/1-escopo`](exercicios/1-escopo) | 01/10, 12:00 | Declaração do escopo e esboço da EAP feitos em aula. Faltam a EAP final e o dicionário |
| Exercício 2: Gestão do Cronograma | [`exercicios/2-cronograma`](exercicios/2-cronograma) | 06/10, 12:00 | Atividades e esboço das durações feitos em aula. Faltam as precedências, as durações finais e a rede AOA |
| Seminário: Elementos do Scrum | [`seminario-scrum`](seminario-scrum) | | Slides e registro de IA enviados ao professor em 15/09 |

Os exercícios vão por e-mail (o endereço está no enunciado), com o assunto
`ACH2027 – Turma T94 – Grupo 7 – Exercício N`. Toda entrega leva as referências e o
**Registro de Uso de IA**.

As tarefas estão no [GitHub Project](https://github.com/users/kaualimadesouza/projects/6). O grupo
edita os exercícios juntos no Overleaf ([Ex. 1](https://www.overleaf.com/project/6ab5c0a339166a2763ca23ae),
[Ex. 2](https://www.overleaf.com/project/6ab6f852cb131a410ba30055), com acesso por convite).

## Agentes de IA

As instruções para agentes ficam em [`AGENTS.md`](AGENTS.md). O Antigravity lê esse arquivo direto,
e o Claude Code lê pelo `CLAUDE.md`. As skills da disciplina ficam em [`.claude/skills/`](.claude/skills)
e valem para os dois (o Antigravity chega a elas pelo `.agents/skills.json`):

- `politica-uso-ia`: usada em toda tarefa. Diz como declarar o uso de IA na entrega.
- `gestao-escopo`: declaração do escopo, EAP e dicionário da EAP.
- `gestao-cronograma`: atividades, durações, precedências, rede AOA e caminho crítico.
- `scrum`: Scrum Guide 2020 e o seminário do grupo.

## Compilar

```bash
cd exercicios/1-escopo
pdflatex exercicio1_GPTI_2026.tex
pdflatex exercicio1_GPTI_2026.tex
```

As figuras da EAP ainda estão só no Overleaf. Sem elas, os `.tex` não compilam aqui.

## Integrantes

- Gustavo G. França do Nascimento
- Kauã Lima de Souza
- Kevin Rodrigues Nunes
- Victor Yodono
