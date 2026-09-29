from pathlib import Path

import pytest

import aoa
from aoa import ACTIVITIES, POSITIONS, Activity, Arrow


@pytest.fixture(scope="module")
def plan() -> aoa.Schedule:
    return aoa.schedule(ACTIVITIES)


def test_network_encodes_exactly_the_precedence_table(plan: aoa.Schedule) -> None:
    assert aoa.implied_ancestors(plan.arrows) == aoa.ancestors(ACTIVITIES)


def test_arrows_go_forward_with_unique_pairs_and_one_start_and_end(plan: aoa.Schedule) -> None:
    assert all(a.tail < a.head for a in plan.arrows)
    pairs = [(a.tail, a.head) for a in plan.arrows]
    assert len(set(pairs)) == len(pairs)
    events = sorted(plan.earliest)
    assert [e for e in events if all(a.head != e for a in plan.arrows)] == [1]
    assert [e for e in events if all(a.tail != e for a in plan.arrows)] == [events[-1]]


def test_no_dummy_can_be_dropped_or_merged(plan: aoa.Schedule) -> None:
    assert aoa.simplify_once(plan.arrows, aoa.ancestors(ACTIVITIES)) is None


def test_network_size_duration_and_critical_path(plan: aoa.Schedule) -> None:
    assert len(plan.earliest) == 36
    assert sum(1 for a in plan.arrows if a.letter is None) == 8
    assert plan.total_weeks == 26
    assert plan.critical_letters() == {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "O", "V", "W", "X",
                                       "AB", "AC", "AD", "AE", "AF", "AG", "AI", "AJ", "AM", "AN"}


def test_parallel_activities_get_a_dummy() -> None:
    small = (Activity("A", "1", "a", 1, ()), Activity("B", "2", "b", 2, ("A",)),
             Activity("C", "3", "c", 3, ("A",)), Activity("D", "4", "d", 1, ("B", "C")))
    plan = aoa.schedule(small)
    assert sum(1 for a in plan.arrows if a.letter is None) == 1
    assert plan.total_weeks == 5
    assert plan.critical_letters() == frozenset({"A", "C", "D"})


def test_partial_dependency_gets_a_dummy() -> None:
    small = (Activity("A", "1", "a", 1, ()), Activity("B", "2", "b", 1, ()),
             Activity("C", "3", "c", 1, ("A", "B")), Activity("D", "4", "d", 1, ("A",)))
    plan = aoa.schedule(small)
    assert aoa.implied_ancestors(plan.arrows) == aoa.ancestors(small)
    assert sum(1 for a in plan.arrows if a.letter is None) == 1


def test_redundant_precedence_gets_no_dummy() -> None:
    """C waiting for A is already implied by C waiting for B, so the chain needs no dummy."""
    small = (Activity("A", "1", "a", 1, ()), Activity("B", "2", "b", 1, ("A",)), Activity("C", "3", "c", 1, ("A", "B")))
    plan = aoa.schedule(small)
    assert [(a.tail, a.head, a.letter) for a in plan.arrows] == [(1, 2, "A"), (2, 3, "B"), (3, 4, "C")]


def test_cycles_are_rejected() -> None:
    cyclic = (Activity("A", "1", "a", 1, ("B",)), Activity("B", "2", "b", 1, ("A",)))
    with pytest.raises(ValueError, match="cycle"):
        aoa.ancestors(cyclic)
    loop = [Arrow(1, 2, "A", 1), Arrow(2, 1, "B", 1)]
    assert aoa.topological_events(loop) is None
    assert aoa.implied_ancestors(loop) is None


def test_is_valid_rejects_self_loops_and_parallel_arrows() -> None:
    expected: dict[str, frozenset[str]] = {"A": frozenset(), "B": frozenset()}
    assert aoa.is_valid([Arrow(1, 2, "A", 1), Arrow(1, 3, "B", 1)], expected)
    assert not aoa.is_valid([Arrow(1, 2, "A", 1), Arrow(1, 2, "B", 1)], expected)
    assert not aoa.is_valid([Arrow(1, 2, "A", 1), Arrow(2, 2, None), Arrow(1, 3, "B", 1)], expected)


def test_tikz_styles_critical_arrows_and_events_dummies_and_routes(plan: aoa.Schedule) -> None:
    drawing = aoa.tikz(plan, POSITIONS)
    assert drawing.startswith(r"\begin{tikzpicture}[x=1.26cm, y=1.9cm,")
    assert drawing.count(r"\node[") == 36
    assert r"\node[evento, critica] (e1) at (0, 0) {1};" in drawing
    assert r"\node[evento] (e10) at (5, 0) {10};" in drawing
    assert r"""\path (e1) edge[ativ, critica, "A", "1"'] (e2);""" in drawing
    assert r"""\path (e7) edge[ativ, "M", "1"'] (e10);""" in drawing
    assert drawing.count("edge[fantasma") == 8
    assert r"\path (e14) edge[fantasma, critica] (e16);" in drawing
    assert r"\path (e30) edge[fantasma] (e32);" in drawing
    assert r"""\path (e12) edge[ativ, out=-90, in=-90, looseness=0.85, "AH", "1"'] (e31);""" in drawing


def test_tikz_needs_a_position_for_every_event(plan: aoa.Schedule) -> None:
    with pytest.raises(ValueError, match=r"\[36\]"):
        aoa.tikz(plan, {e: p for e, p in POSITIONS.items() if e != 36})


def test_table_rows() -> None:
    rows = aoa.table_rows(ACTIVITIES).splitlines()
    assert rows[0] == r"A & 1.1.1.1 & Coletar os requisitos de alto nível com a Diretoria & 1 & - \\"
    assert rows[1] == r"\hline"
    assert r"F & 1.1.3.2 & Aprovar o orçamento com a Diretoria & 1 & D, E \\" in rows
    assert len(rows) == 2 * len(ACTIVITIES)


def test_numbers_macros_list_the_critical_activities_in_table_order(plan: aoa.Schedule) -> None:
    assert aoa.numbers(plan, ACTIVITIES).splitlines() == [
        r"\newcommand{\duracaoTotal}{26}",
        r"\newcommand{\inicioDesenvolvimento}{10}",
        r"\newcommand{\fimTestes}{22}",
        (r"\newcommand{\caminhoCritico}{A, B, C, D, E, F, G, H, I, J, K, L, O, V, W, X, AB, AC, AD, AE, AF, AG, AI, "
         r"AJ, AM, AN}"),
    ]


def test_main_writes_the_three_fragments(tmp_path: Path, plan: aoa.Schedule) -> None:
    aoa.main(tmp_path)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["atividades.tex", "numeros.tex", "rede_aoa.tex"]
    assert (tmp_path / "rede_aoa.tex").read_text() == aoa.tikz(plan, POSITIONS)
    assert (tmp_path / "numeros.tex").read_text().startswith(r"\newcommand{\duracaoTotal}{26}")
