# Exercício 2: Gestão do Cronograma

Passado em aula em 25/09/2026 ([`enunciado.pdf`](enunciado.pdf)): elaborar o cronograma do projeto
semestral, a partir dos pacotes de trabalho da EAP do Exercício 1. A situação de cada item fica na
issue correspondente e no [GitHub Project](https://github.com/users/kaualimadesouza/projects/6).

| Item | Entrega | Issue |
| --- | --- | --- |
| 1. Atividades a partir dos pacotes de trabalho | Em aula | |
| 2. Duração das atividades (esboço) | Em aula | |
| 3. Precedências das atividades (esboço) | Em aula | |
| 2. Duração das atividades (versão final) | E-mail, até 06/10 às 12:00 | [#5](https://github.com/kaualimadesouza/GPTI/issues/5) |
| 3. Precedências das atividades (versão final) | E-mail, até 06/10 às 12:00 | [#4](https://github.com/kaualimadesouza/GPTI/issues/4) |
| 4. Rede de atividades do tipo AOA (versão final) | E-mail, até 06/10 às 12:00 | [#6](https://github.com/kaualimadesouza/GPTI/issues/6) |
| Revisão e envio | E-mail, até 06/10 às 12:00 | [#7](https://github.com/kaualimadesouza/GPTI/issues/7) |

A entrega final leva as referências, os outros materiais de pesquisa e o Registro de Uso de IA.
Vai para o e-mail do enunciado, com o assunto `ACH2027 – Turma T94 – Grupo 7 – Exercício 2`.

## Divisão

Em 28/09 o Victor sugeriu fazer de uma vez as entregas finais dos dois exercícios, com IA, e se
ofereceu para revisar.

## Arquivos

| Arquivo | O que é |
| --- | --- |
| `enunciado.pdf` | Enunciado da Juliana |
| `exercicio2_GPTI_2026.tex` / [`.pdf`](exercicio2_GPTI_2026.pdf) | Entrega inicial, cópia do Overleaf (Ex. 2). Fica como está, para comparar |
| `abcd.png` | EAP com as atividades no 4º nível (exportada do Overleaf) |
| `exercicio2_GPTI_2026_final.tex` / [`.pdf`](exercicio2_GPTI_2026_final.pdf) | Versão final: atividades da EAP final, durações, precedências, rede AOA com o caminho crítico e o Registro 02 de uso de IA |
| `gpti.sty` | Estilo do grupo, cópia idêntica à do Exercício 1 |
| `rede/aoa.py` | Gera a tabela de atividades, a rede AOA e os números citados no texto |
| `rede/*.tex` | Saída do `aoa.py`. Não edite à mão |

As atividades seguem os códigos da EAP final do Exercício 1: se a EAP mudar, a tabela e a rede
mudam junto.

## Mudar uma atividade

A tabela `ACTIVITIES` do `rede/aoa.py` é a única fonte das atividades, durações e precedências. O
programa monta a rede sem atividade fantasma desnecessária, calcula o caminho crítico e escreve
`rede/atividades.tex` (linhas da tabela), `rede/rede_aoa.tex` (a figura) e `rede/numeros.tex`
(duração total, semanas do desenvolvimento e atividades com folga zero).

```bash
cd exercicios/2-cronograma/rede
python3 aoa.py                                             # regenera os três .tex
uv run --no-project --with pytest --with pytest-cov pytest -q --cov=aoa test_aoa.py
```

Se a mudança criar ou remover eventos, ajuste `POSITIONS` (coluna e faixa de cada evento) e
confira a figura compilada. Os testes conferem a rede contra a tabela, então atualize os números
esperados junto.

No Overleaf, suba `gpti.sty` e a pasta `rede/` com os três `.tex` gerados. O Overleaf não roda o
`aoa.py`: mudanças na tabela passam por aqui.
