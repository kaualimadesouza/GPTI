# Atividade extraclasse: AHP do trabalho semestral

Pedida pelo professor por e-mail em 05/10/2026, vale como presença da aula de 09/10: usar o AHP
(*Analytic Hierarchy Process*) para escolher a ferramenta que implementa o trabalho semestral, entre
Java, C#, Python e Go. A situação fica na [issue #14](https://github.com/kaualimadesouza/GPTI/issues/14)
e no [GitHub Project](https://github.com/users/kaualimadesouza/projects/6).

Entrega: até **15/10/2026 às 14:00**, para eprado@usp.br, com o assunto
`ACH2027 – T94 – G7 – AHP Trabalho Semestral`. O PDF leva as quatro saídas pedidas: o vetor de
prioridades dos critérios, os vetores das alternativas em cada critério, o ranking global e o CR de
cada matriz (consistente se for menor que 0,10).

## Decisões

| Decisão | Escolha |
| --- | --- |
| Quem julga | Os 30 julgamentos foram propostos com IA, a pedido do Kauã, a partir da `ficha.md`; o grupo revisa e pode mudar |
| Time | Bolsistas: 5 a 8 alunos de SI do último ano, com o Analista Sênior |
| Alternativas | Java/Spring Boot, C#/ASP.NET Core, Python/Django, Go/Gin |
| Critérios | Cada fator conta em um só critério (definições na `ficha.md`) |
| Método | Autovetor principal (Saaty), `CR = CI / RI` com RI = 0,90 para n = 4 (Vargas, 2010) |
| Registro de Uso de IA | Só entra o que o Kauã autorizar |

## Arquivos

| Arquivo | O que é |
| --- | --- |
| `ficha.md` | Leitura antes de julgar: critérios, escala de Saaty, como escrever um julgamento e fatos de cada linguagem, com fonte |
| `ahp.py` | Os julgamentos (fonte única), o cálculo e a geração das tabelas |
| `test_ahp.py` | Testes do cálculo, inclusive contra o exemplo publicado de Vargas (2010) |
| `tabelas/*.tex` | Saída do `ahp.py`: matrizes, ranking, sensibilidade e os números do texto. Não edite à mão |
| `ahp_GPTI_2026.tex` / `.pdf` | O documento a entregar |
| `gpti.sty` | Estilo do grupo, cópia idêntica à dos exercícios |

## Escrever ou mudar um julgamento

Os julgamentos ficam no `ahp.py`, agrupados por matriz. `Judgment("X", "Y", 5, "motivo")` quer dizer
"X é fortemente preferível a Y" naquela matriz; para favorecer Y, inverta os nomes, e 1 é empate.

```bash
cd atividades/ahp
python3 ahp.py                                             # confere e escreve tabelas/
uv run --no-project --with pytest --with pytest-cov pytest -q --cov=ahp test_ahp.py
```

O script recusa par faltando, repetido, nome fora da matriz e intensidade fora de 1 a 9. Se algum CR não
for menor que 0,10, ele não escreve nada e mostra os julgamentos que mais destoam dos pesos: revise esses
primeiro. Depois compile o documento duas vezes com `pdflatex`.

Os números do texto, as matrizes, o ranking e a tabela de sensibilidade vêm do `ahp.py`. O resto é escrito
à mão: os parágrafos das seções IV e V, que explicam cada matriz em palavras, a frase da seção VI que diz
por que o primeiro lugar vence, e as semanas de bolsa da seção IV, copiadas do Exercício 2. Depois de mudar
um julgamento, rode o `ahp.py` e releia o parágrafo daquela matriz e o começo da seção VI. Os testes
quebram se as tabelas commitadas não baterem com os julgamentos e fixam o ranking atual.

## Antes de enviar

- [ ] O grupo revisa os 30 julgamentos e os parágrafos; o que mudar no Overleaf volta para o `ahp.py`
- [ ] Conferir se a ACH2003 é obrigatória na grade em que vocês entraram (o texto cita só a de 2027)
- [ ] Conferir no PMBOK 6ª ed. a seção 9.3 citada na Tabela I (o livro não está em `docs/`)
- [ ] O Kauã decide o que entra no Registro de Uso de IA (o PDF ainda não tem a seção)
- [ ] Mandar o PDF no grupo antes de enviar
- [ ] Enviar para eprado@usp.br até 15/10 às 14:00

No Overleaf, suba `gpti.sty` e a pasta `tabelas/`. O Overleaf não roda o `ahp.py`: se o grupo mudar
um julgamento lá, a mudança precisa voltar para o `ahp.py`, senão as tabelas e o texto divergem.
