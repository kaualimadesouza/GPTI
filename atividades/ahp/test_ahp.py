import re
from fractions import Fraction
from pathlib import Path

import pytest

import ahp
from ahp import ALTERNATIVE_JUDGMENTS, CRITERIA_JUDGMENTS, Comparison, Judgment

LETTERS = ("A", "B", "C", "D")
HERE = Path(ahp.__file__).parent


def comparison(*judgments: Judgment, elements: tuple[str, ...] = LETTERS, title: str = "Teste",
               slug: str = "Teste") -> Comparison:
    return Comparison(slug, title, elements, judgments)


# Weights 4:2:1:1, so every judgment agrees with every other one
CONSISTENT = (Judgment("A", "B", 2), Judgment("A", "C", 4), Judgment("A", "D", 4),
              Judgment("B", "C", 2), Judgment("B", "D", 2), Judgment("C", "D", 1))
EQUAL = (Judgment("A", "B", 1), Judgment("A", "C", 1), Judgment("A", "D", 1),
         Judgment("B", "C", 1), Judgment("B", "D", 1), Judgment("C", "D", 1))
# Vargas (2010), Tables 3 and 6: Stakeholders, Financial, Strategic, Other criteria
VARGAS = (Judgment("B", "A", 5), Judgment("C", "A", 9), Judgment("A", "D", 1),
          Judgment("B", "C", 1), Judgment("B", "D", 5), Judgment("C", "D", 5))
CYCLE = (Judgment("A", "B", 9), Judgment("B", "C", 9), Judgment("C", "A", 9),
         Judgment("A", "D", 1), Judgment("B", "D", 1), Judgment("C", "D", 1))


def test_consistent_judgments_give_their_exact_weights_and_zero_cr() -> None:
    result = ahp.evaluate(comparison(*CONSISTENT))
    assert result.weights == pytest.approx((0.5, 0.25, 0.125, 0.125))
    assert result.lambda_max == pytest.approx(4)
    assert result.consistency_ratio == 0
    assert result.consistent


def test_equal_judgments_give_equal_weights() -> None:
    result = ahp.evaluate(comparison(*EQUAL))
    assert result.weights == pytest.approx((0.25,) * 4)
    assert result.consistency_ratio == 0


def test_matrix_is_reciprocal_and_swapping_names_inverts_the_entry() -> None:
    matrix = ahp.reciprocal_matrix(comparison(*CONSISTENT[:2], Judgment("D", "A", 4), *CONSISTENT[3:]))
    assert [matrix[i][i] for i in range(4)] == [1] * 4
    assert matrix[0][1] == 2 and matrix[1][0] == Fraction(1, 2)
    assert matrix[0][3] == Fraction(1, 4) and matrix[3][0] == 4


def test_matches_the_published_example_of_vargas_2010() -> None:
    result = ahp.evaluate(comparison(*VARGAS))
    assert [round(w, 4) for w in result.weights] == [0.0684, 0.3927, 0.4604, 0.0785]
    assert round(result.lambda_max, 2) == 4.04
    assert result.consistency_ratio == pytest.approx((result.lambda_max - 4) / 3 / 0.90)
    assert result.consistent


def test_a_cycle_is_inconsistent_and_its_judgments_deviate_the_most() -> None:
    result = ahp.evaluate(comparison(*CYCLE))
    assert result.consistency_ratio > 0.10
    assert not result.consistent
    worst = ahp.deviations(result)
    assert {d.judgment for d in worst[:3]} == set(CYCLE[:3])
    assert [d.ratio for d in worst] == sorted((d.ratio for d in worst), reverse=True)
    assert all(d.ratio >= 1 for d in worst)


def test_complete_judgments_have_no_problems() -> None:
    assert ahp.judgment_problems(comparison(*CONSISTENT)) == ()


def test_missing_pairs_are_named() -> None:
    assert ahp.judgment_problems(comparison(*CONSISTENT[:4])) == (
        "Teste: falta comparar B com D", "Teste: falta comparar C com D")


@pytest.mark.parametrize(("bad", "message"), [
    (Judgment("B", "A", 1), "Teste: o par A e B aparece mais de uma vez"),
    (Judgment("A", "A", 1), "Teste: A aparece nos dois lados do julgamento"),
    (Judgment("A", "Z", 3), "Teste: Z não é um elemento desta matriz"),
    (Judgment("A", "B", 0), "Teste: A e B: a intensidade 0 não é um inteiro de 1 a 9"),
    (Judgment("A", "B", 10), "Teste: A e B: a intensidade 10 não é um inteiro de 1 a 9"),
    (Judgment("A", "B", 2.5), "Teste: A e B: a intensidade 2.5 não é um inteiro de 1 a 9"),  # type: ignore[arg-type]
    (Judgment("A", "B", True), "Teste: A e B: a intensidade True não é um inteiro de 1 a 9"),
])
def test_each_invalid_judgment_is_reported(bad: Judgment, message: str) -> None:
    assert message in ahp.judgment_problems(comparison(*CONSISTENT, bad))


def test_a_matrix_must_have_four_distinct_elements() -> None:
    assert ahp.judgment_problems(comparison(elements=("A", "B", "C"))) == (
        "Teste: a matriz precisa de 4 elementos distintos (RI = 0,90 vale para n = 4)",)
    assert ahp.judgment_problems(comparison(elements=("A", "B", "C", "C")))[0].endswith("(RI = 0,90 vale para n = 4)")


def test_the_real_hierarchy_is_well_formed() -> None:
    assert ahp.hierarchy_problems(CRITERIA_JUDGMENTS, ALTERNATIVE_JUDGMENTS) == ()
    assert CRITERIA_JUDGMENTS.elements == ahp.CRITERIA
    assert all(c.elements == ahp.ALTERNATIVES for c in ALTERNATIVE_JUDGMENTS)


def test_hierarchy_needs_one_alternative_matrix_per_criterion_with_the_same_alternatives() -> None:
    criteria = comparison(elements=("K1", "K2", "K3", "K4"))
    matrices = [comparison(title=k, elements=LETTERS) for k in ("K1", "K2", "K3")]
    assert ahp.hierarchy_problems(criteria, matrices) == (
        "as matrizes de alternativas precisam seguir os critérios, na ordem: K1, K2, K3, K4",)
    matrices.append(comparison(title="K4", elements=("A", "B", "C", "E")))
    assert ahp.hierarchy_problems(criteria, matrices) == (
        "K4: as alternativas precisam ser as mesmas de K1",)


CRITERIA_FOR_RANKING = comparison(*[Judgment(f"K{p.preferred}", f"K{p.over}", p.intensity) for p in CONSISTENT],
                                  elements=("KA", "KB", "KC", "KD"), title="Critérios", slug="Criterios")
ALTERNATIVES_FOR_RANKING = (
    comparison(*CONSISTENT, title="KA", slug="Ka"),
    comparison(*EQUAL, title="KB", slug="Kb"),
    comparison(*[Judgment(p.over, p.preferred, p.intensity) for p in CONSISTENT], title="KC", slug="Kc"),
    comparison(*EQUAL, title="KD", slug="Kd"),
)


def test_global_score_is_the_weighted_sum_and_the_ranking_is_sorted() -> None:
    criteria = ahp.evaluate(CRITERIA_FOR_RANKING)
    scores = ahp.rank(criteria, [ahp.evaluate(c) for c in ALTERNATIVES_FOR_RANKING])
    inverse = (1 / 11, 2 / 11, 4 / 11, 4 / 11)  # inverting 4:2:1:1 gives 1:2:4:4
    expected = {x: 0.5 * a + 0.25 * 0.25 + 0.125 * c + 0.125 * 0.25
                for x, a, c in zip(LETTERS, (0.5, 0.25, 0.125, 0.125), inverse)}
    assert [s.alternative for s in scores] == sorted(LETTERS, key=lambda x: -expected[x])
    assert {s.alternative: s.total for s in scores} == pytest.approx(expected)
    assert scores[0].by_criterion == pytest.approx((0.5, 0.25, 1 / 11, 0.25))
    assert sum(s.total for s in scores) == pytest.approx(1)


def test_numbers_are_written_with_a_decimal_comma_outside_math_mode() -> None:
    assert ahp.percent(0.3141) == r"31,4\%"
    assert ahp.comma(0.0321, 3) == "0,032"
    assert ahp.fraction(Fraction(1, 3)) == "1/3"
    assert ahp.fraction(Fraction(5)) == "5"
    assert ahp.escape("C#") == r"C\#"


def test_matrix_table_shows_the_fractions_and_the_priorities() -> None:
    table = ahp.matrix_table(ahp.evaluate(comparison(*CONSISTENT)))
    assert table.startswith(r"\begin{tabular}{|>{\raggedright\arraybackslash\nohyphens}p{2.7cm}|")
    assert r" & \textbf{A} & \textbf{B} & \textbf{C} & \textbf{D} & \textbf{Prioridade} \\" in table
    assert r"\textbf{A} & 1 & 2 & 4 & 4 & 50,0\% \\" in table
    assert r"\textbf{D} & 1/4 & 1/2 & 1 & 1 & 12,5\% \\" in table
    assert table.count(r"\hline") == 6
    assert table.endswith("\\end{tabular}\n")


def test_matrix_table_escapes_names() -> None:
    names = ("Java", "C#", "Python", "Go")
    renamed = [Judgment(names[LETTERS.index(j.preferred)], names[LETTERS.index(j.over)], j.intensity)
               for j in CONSISTENT]
    table = ahp.matrix_table(ahp.evaluate(comparison(*renamed, elements=names)))
    assert r"\textbf{C\#} & 1/2 & 1 & 2 & 2 & 25,0\% \\" in table


def test_ranking_table_lists_the_criteria_weights_and_the_ordered_totals() -> None:
    criteria = ahp.evaluate(CRITERIA_FOR_RANKING)
    scores = ahp.rank(criteria, [ahp.evaluate(c) for c in ALTERNATIVES_FOR_RANKING])
    table = ahp.ranking_table(criteria, scores)
    assert r"\textbf{KA} (50,0\%) & \textbf{KB} (25,0\%) & \textbf{KC} (12,5\%) & \textbf{KD} (12,5\%)" in table
    rows = [line for line in table.splitlines() if "º" in line]
    assert [row.split(" & ")[1] for row in rows] == [s.alternative for s in scores]
    assert rows[0].startswith("1º & ") and rows[-1].startswith("4º & ")
    assert rows[0] == r"1º & A & 50,0\% & 25,0\% & 9,1\% & 25,0\% & 35,5\% \\"


def test_numbers_write_each_cr_weight_the_top_two_and_the_sensitivity_counts() -> None:
    criteria = ahp.evaluate(CRITERIA_FOR_RANKING)
    matrices = (*ALTERNATIVES_FOR_RANKING[:3], comparison(*VARGAS, title="KD", slug="Kd"))
    alternatives = [ahp.evaluate(c) for c in matrices]
    scores = ahp.rank(criteria, alternatives)
    text = ahp.numbers(criteria, alternatives, scores, ahp.Sensitivity(48, ()))
    assert "\\newcommand{\\crCriterios}{0,000}\n" in text
    assert "\\newcommand{\\crKa}{0,000}\n" in text
    assert f"\\newcommand{{\\crKd}}{{{ahp.comma(alternatives[3].consistency_ratio, 3)}}}\n" in text
    assert alternatives[3].consistency_ratio > 0.01
    assert f"\\newcommand{{\\segundoLugar}}{{{scores[1].alternative}}}\n" in text
    assert "\\newcommand{\\pesoKa}{50,0\\%}\n" in text
    assert "\\newcommand{\\pesoKd}{12,5\\%}\n" in text
    assert f"\\newcommand{{\\primeiroLugar}}{{{scores[0].alternative}}}\n" in text
    assert f"\\newcommand{{\\pontuacaoSegundo}}{{{ahp.percent(scores[1].total)}}}\n" in text
    assert "\\newcommand{\\mudancasTestadas}{48}\n" in text
    assert "\\newcommand{\\mudancasQueTrocam}{0}\n" in text


def test_numbers_define_exactly_the_macros_the_document_falls_back_on() -> None:
    tex = (HERE / "ahp_GPTI_2026.tex").read_text()
    fallback = set(re.findall(r"\\newcommand\{\\(\w+)\}\{\\pendente\}", tex))
    criteria = ahp.evaluate(CRITERIA_JUDGMENTS)
    alternatives = [ahp.evaluate(c) for c in ALTERNATIVE_JUDGMENTS]
    text = ahp.numbers(criteria, alternatives, ahp.rank(criteria, alternatives), ahp.Sensitivity(60, ()))
    assert set(re.findall(r"\\newcommand\{\\(\w+)\}", text)) == fallback
    assert len(fallback) == 15


def test_run_stops_and_lists_what_is_missing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    incomplete = (*ALTERNATIVES_FOR_RANKING[:3], comparison(*EQUAL[:5], title="KD", slug="Kd"))
    assert ahp.run(CRITERIA_FOR_RANKING, incomplete, tmp_path / "tabelas") == 1
    assert "KD: falta comparar C com D" in capsys.readouterr().out
    assert not (tmp_path / "tabelas").exists()


def test_run_stops_on_an_inconsistent_matrix_and_shows_the_worst_judgments(
        tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    inconsistent = (*ALTERNATIVES_FOR_RANKING[:3], comparison(*CYCLE, title="KD", slug="Kd"))
    assert ahp.run(CRITERIA_FOR_RANKING, inconsistent, tmp_path / "tabelas") == 1
    out = capsys.readouterr().out
    assert "KD: CR = " in out and "não é menor que 0,10" in out
    worst = [line for line in out.splitlines() if line.startswith("  ")]
    assert len(worst) == 3 and all("com intensidade 9" in line for line in worst)
    assert "  A é preferível a B com intensidade 9, mas os pesos dão A/B = 1,00" in worst
    assert not (tmp_path / "tabelas").exists()


def test_run_writes_every_fragment_when_all_matrices_are_consistent(
        tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    out_dir = tmp_path / "tabelas"
    assert ahp.run(CRITERIA_FOR_RANKING, ALTERNATIVES_FOR_RANKING, out_dir) == 0
    assert sorted(p.name for p in out_dir.iterdir()) == [
        "matriz_criterios.tex", "matriz_ka.tex", "matriz_kb.tex", "matriz_kc.tex", "matriz_kd.tex",
        "numeros.tex", "ranking.tex", "sensibilidade.tex"]
    assert (out_dir / "matriz_ka.tex").read_text() == ahp.matrix_table(ahp.evaluate(ALTERNATIVES_FOR_RANKING[0]))
    out = capsys.readouterr().out
    assert "Critérios: CR = 0,000 (consistente)" in out
    assert not [line for line in out.splitlines() if line.startswith("  ")]
    assert "1º A: 35,5%" in out
    assert "Mudanças de um ponto que trocam o primeiro lugar: 0 de 60" in out
    assert "empatam no primeiro lugar" not in out


def test_cr_is_judged_on_the_printed_decimals() -> None:
    result = ahp.evaluate(comparison(Judgment("B", "A", 9), Judgment("C", "A", 9), Judgment("D", "A", 6),
                                     Judgment("C", "B", 4), Judgment("B", "D", 1), Judgment("C", "D", 1)))
    assert 0.0995 < result.consistency_ratio < 0.10
    assert ahp.comma(result.consistency_ratio, 3) == "0,100"
    assert not result.consistent


def test_floating_point_noise_never_makes_a_consistent_cr_negative() -> None:
    result = ahp.evaluate(comparison(Judgment("A", "B", 1), Judgment("A", "C", 3), Judgment("A", "D", 9),
                                     Judgment("B", "C", 3), Judgment("B", "D", 9), Judgment("C", "D", 3)))
    assert result.lambda_max < 4  # the noise the clamp exists for
    assert result.consistency_ratio == 0


def test_converges_on_a_matrix_with_close_eigenvalues() -> None:
    # |lambda2| / lambda1 = 0,83, close to the worst case; reference weights from numpy.linalg.eig
    result = ahp.evaluate(comparison(Judgment("A", "B", 9), Judgment("A", "C", 1), Judgment("D", "A", 9),
                                     Judgment("C", "B", 9), Judgment("B", "D", 9), Judgment("D", "C", 9)))
    reference = (0.2119959759180297, 0.25112135196739965, 0.21199597591802966, 0.324886696196541)
    assert result.weights == pytest.approx(reference, abs=1e-12)


def test_alternatives_in_another_order_are_rejected() -> None:
    criteria = comparison(elements=("K1", "K2"))
    matrices = [comparison(title="K1"), comparison(title="K2", elements=("B", "A", "C", "D"))]
    assert ahp.hierarchy_problems(criteria, matrices) == ("K2: as alternativas precisam ser as mesmas de K1",)
    assert ahp.hierarchy_problems(comparison(elements=()), ()) == (
        "as matrizes de alternativas precisam seguir os critérios, na ordem: ",)


def test_a_tie_is_described_as_a_tie() -> None:
    result = ahp.evaluate(comparison(*CYCLE))
    tie = next(d for d in ahp.deviations(result) if d.judgment.intensity == 1)
    assert ahp.describe(tie).startswith(f"{tie.judgment.preferred} e {tie.judgment.over} empatam, mas os pesos dão ")


def test_run_warns_when_the_first_place_is_a_tie(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    tied = tuple(comparison(*EQUAL, title=c.title, slug=c.slug) for c in ALTERNATIVES_FOR_RANKING)
    assert ahp.run(CRITERIA_FOR_RANKING, tied, tmp_path / "tabelas") == 0
    assert "Atenção: A e B empatam no primeiro lugar" in capsys.readouterr().out


def test_the_real_judgments_are_consistent_and_put_python_first() -> None:
    assert all(ahp.judgment_problems(c) == () for c in (CRITERIA_JUDGMENTS, *ALTERNATIVE_JUDGMENTS))
    criteria = ahp.evaluate(CRITERIA_JUDGMENTS)
    alternatives = [ahp.evaluate(c) for c in ALTERNATIVE_JUDGMENTS]
    assert [ahp.comma(r.consistency_ratio, 3) for r in (criteria, *alternatives)] == [
        "0,002", "0,000", "0,003", "0,004", "0,005"]
    assert [round(w, 3) for w in criteria.weights] == [0.070, 0.368, 0.193, 0.368]
    scores = ahp.rank(criteria, alternatives)
    assert [(s.alternative, round(100 * s.total, 1)) for s in scores] == [
        ("Python", 34.2), ("Java", 31.0), ("C#", 22.8), ("Go", 11.9)]


def test_nudges_move_a_judgment_one_step_on_the_scale() -> None:
    assert ahp.nudges(Judgment("A", "B", 1)) == (Judgment("A", "B", 2), Judgment("B", "A", 2))
    assert ahp.nudges(Judgment("A", "B", 3)) == (Judgment("A", "B", 2), Judgment("A", "B", 4))
    assert ahp.nudges(Judgment("A", "B", 9)) == (Judgment("A", "B", 8),)


def test_a_cell_is_the_intensity_for_the_preferred_row_and_its_reciprocal_otherwise() -> None:
    assert ahp.cell(Judgment("A", "B", 3), "A") == 3
    assert ahp.cell(Judgment("B", "A", 3), "A") == Fraction(1, 3)


DOMINATED = (Judgment("A", "B", 9), Judgment("A", "C", 9), Judgment("A", "D", 9),
             Judgment("B", "C", 1), Judgment("B", "D", 1), Judgment("C", "D", 1))


def test_no_single_step_unseats_an_alternative_that_dominates_every_criterion() -> None:
    criteria = comparison(*[Judgment(f"K{p.preferred}", f"K{p.over}", 1) for p in EQUAL],
                          elements=("KA", "KB", "KC", "KD"))
    matrices = [comparison(*DOMINATED, title=k) for k in ("KA", "KB", "KC", "KD")]
    shaken = ahp.sensitivity(criteria, matrices)
    assert shaken == ahp.Sensitivity(6 * 2 + 4 * (3 * 1 + 3 * 2), ())
    assert "Nenhuma mudança de um ponto troca o primeiro lugar" in ahp.sensitivity_table(shaken)


def test_the_only_flip_of_the_real_ranking_is_the_deadline_against_the_workforce() -> None:
    shaken = ahp.sensitivity(CRITERIA_JUDGMENTS, ALTERNATIVE_JUDGMENTS)
    assert shaken.tried == 60
    [flip] = shaken.flips
    assert (flip.matrix, flip.row, flip.column) == ("Critérios", "Prazo de entrega", "Facilidade de mão de obra")
    assert (flip.before, flip.after) == (Fraction(1), Fraction(1, 2))
    # recomputed by hand: the workforce slightly above the deadline puts Java first
    pair = ("Facilidade de mão de obra", "Prazo de entrega")
    judgments = tuple(Judgment(*pair, 2) if {j.preferred, j.over} == set(pair) else j
                      for j in CRITERIA_JUDGMENTS.judgments)
    criteria = Comparison("Criterios", "Critérios", CRITERIA_JUDGMENTS.elements, judgments)
    assert flip.scores == ahp.standings((criteria, *ALTERNATIVE_JUDGMENTS))
    assert [(s.alternative, round(100 * s.total, 1)) for s in flip.scores[:2]] == [("Java", 33.0), ("Python", 32.6)]
    row = ahp.sensitivity_table(shaken).splitlines()[5]
    assert row == (r"Critérios & Prazo de entrega $\times$ Facilidade de mão de obra & 1 $\rightarrow$ 1/2 & "
                   r"Java (33,0\%) à frente de Python (32,6\%) \\")


def test_committed_tables_are_up_to_date(tmp_path: Path) -> None:
    """Fails when a judgment changed and ahp.py was not rerun, or a table was edited by hand."""
    assert ahp.run(CRITERIA_JUDGMENTS, ALTERNATIVE_JUDGMENTS, tmp_path) == 0
    committed = HERE / "tabelas"
    assert sorted(p.name for p in committed.iterdir()) == sorted(p.name for p in tmp_path.iterdir())
    assert all((committed / p.name).read_text() == p.read_text() for p in tmp_path.iterdir())
