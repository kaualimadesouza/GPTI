"""Exercise 2 schedule: the activity table is the single source for the table, the AOA network and the
numbers the text quotes. Run `python aoa.py` after editing ACTIVITIES to regenerate the LaTeX fragments."""
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import chain
from pathlib import Path


@dataclass(frozen=True)
class Activity:
    letter: str
    code: str
    name: str
    weeks: int
    predecessors: tuple[str, ...]


@dataclass(frozen=True)
class Arrow:
    tail: int
    head: int
    letter: str | None  # None marks a dummy (atividade fantasma)
    weeks: int = 0


@dataclass(frozen=True)
class Schedule:
    arrows: tuple[Arrow, ...]
    earliest: Mapping[int, int]
    latest: Mapping[int, int]

    @property
    def total_weeks(self) -> int:
        return self.earliest[max(self.earliest)]

    def is_critical_event(self, event: int) -> bool:
        return self.earliest[event] == self.latest[event]

    def is_critical(self, arrow: Arrow) -> bool:
        return (self.is_critical_event(arrow.tail) and self.is_critical_event(arrow.head)
                and self.earliest[arrow.tail] + arrow.weeks == self.earliest[arrow.head])

    def critical_letters(self) -> frozenset[str]:
        return frozenset(a.letter for a in self.arrows if a.letter and self.is_critical(a))


ACTIVITIES = (
    Activity("A", "1.1.1.1", "Coletar os requisitos de alto nível com a Diretoria", 1, ()),
    Activity("B", "1.1.1.2", "Elaborar a declaração do escopo, a EAP e o dicionário", 1, ("A",)),
    Activity("C", "1.1.2.1", "Definir e sequenciar as atividades", 1, ("B",)),
    Activity("D", "1.1.2.2", "Estimar as durações e aprovar o cronograma", 1, ("C",)),
    Activity("E", "1.1.3.1", "Estimar os custos", 1, ("C",)),
    Activity("F", "1.1.3.2", "Aprovar o orçamento com a Diretoria", 1, ("D", "E")),
    Activity("G", "1.1.4.1", "Selecionar os bolsistas ou a start-up", 3, ("F",)),
    Activity("H", "1.1.4.2", "Formalizar os estágios ou o contrato", 1, ("G",)),
    Activity("I", "1.2.1.1", "Levantar as regras de negócio", 1, ("B",)),
    Activity("J", "1.2.1.2", "Escrever os casos de uso", 2, ("I",)),
    Activity("K", "1.2.2.1", "Definir a stack tecnológica", 1, ("J",)),
    Activity("L", "1.2.2.2", "Projetar a integração com os equipamentos e a base da USP", 2, ("K",)),
    Activity("M", "1.2.3.1", "Prototipar as telas", 1, ("J",)),
    Activity("N", "1.2.3.2", "Validar os protótipos com a portaria", 1, ("M",)),
    Activity("O", "1.3.1.1", "Especificar os equipamentos", 1, ("L",)),
    Activity("P", "1.3.1.2", "Cotar os equipamentos", 2, ("O",)),
    Activity("Q", "1.3.1.3", "Comprar e receber os equipamentos", 4, ("P", "F")),
    Activity("R", "1.3.2.1", "Preparar os pontos de entrada", 1, ("O",)),
    Activity("S", "1.3.2.2", "Fixar os equipamentos", 2, ("Q", "R")),
    Activity("T", "1.3.3.1", "Passar o cabeamento", 1, ("R",)),
    Activity("U", "1.3.3.2", "Configurar a rede", 1, ("S", "T")),
    Activity("V", "1.4.1.1", "Desenvolver a API de comunicação com os equipamentos", 3, ("H", "N", "O")),
    Activity("W", "1.4.1.2", "Implementar a rotina de liberação", 2, ("V", "X")),
    Activity("X", "1.4.2.1", "Implementar o cadastro e os níveis de acesso", 3, ("H", "N", "O")),
    Activity("Y", "1.4.2.2", "Implementar o cadastro de visitantes", 2, ("X",)),
    Activity("Z", "1.4.3.1", "Implementar a importação em lote", 2, ("X",)),
    Activity("AA", "1.4.3.2", "Emitir as credenciais de evento", 1, ("Z",)),
    Activity("AB", "1.4.4.1", "Escrever as consultas de frequência", 1, ("W",)),
    Activity("AC", "1.4.4.2", "Construir o painel gerencial", 2, ("AB",)),
    Activity("AD", "1.5.1.1", "Escrever e rodar os testes unitários", 2, ("Y", "AA", "AC")),
    Activity("AE", "1.5.1.2", "Corrigir os defeitos", 1, ("AD",)),
    Activity("AF", "1.5.2.1", "Simular passagens nos equipamentos", 1, ("AE", "U")),
    Activity("AG", "1.5.2.2", "Testar a resiliência a falhas de rede", 1, ("AF",)),
    Activity("AH", "1.6.1.1", "Extrair os dados da base da USP", 1, ("L",)),
    Activity("AI", "1.6.1.2", "Importar e conferir a carga inicial", 1, ("AH", "AG")),
    Activity("AJ", "1.5.3.1", "Homologar com a Diretoria e assinar o termo de aceite", 1, ("AI",)),
    Activity("AK", "1.6.2.1", "Escrever os manuais", 1, ("AE",)),
    Activity("AL", "1.6.2.2", "Dar as aulas práticas", 1, ("AK", "AG")),
    Activity("AM", "1.6.3.1", "Ativar o sistema em todas as portarias", 1, ("AJ", "AL")),
    Activity("AN", "1.1.6.1", "Registrar as lições aprendidas e encerrar o projeto", 1, ("AM",)),
)

# (column, lane) of each event: management above the start, requirements below it and infrastructure
# at the bottom; development, tests and deployment follow the critical path on lane 0
POSITIONS = {
    1: (0, 0), 2: (1, 0), 3: (2, 0),
    4: (3, 1), 6: (4, 1.8), 8: (4, 1), 11: (5, 1), 13: (6, 1),
    5: (3, -1), 7: (4, -1), 9: (5, -1), 10: (5, 0), 12: (6, -1), 14: (7, -1),
    16: (7, 0), 18: (8, 1), 20: (8, 0), 21: (9, 1.8), 23: (9, 0), 24: (10, 0), 25: (11, 0), 26: (12, 0),
    27: (13, 1), 28: (13, 0), 29: (14, 0), 30: (15, 0), 31: (15, -1), 32: (15, 1), 33: (16, 0),
    34: (17, 0), 35: (18, 0), 36: (19, 0),
    15: (8, -1), 19: (9, -1), 17: (8, -2), 22: (10, -2),
}
COLUMN_CM, LANE_CM = 1.26, 1.9
# Extra TikZ options for arrows that would otherwise cross a node or another label
ROUTES = {"AH": "out=-90, in=-90, looseness=0.85"}


def ancestors(activities: Sequence[Activity]) -> dict[str, frozenset[str]]:
    """Every activity that must finish before each activity starts, directly or not."""
    direct = {a.letter: a.predecessors for a in activities}
    found: dict[str, frozenset[str]] = {}
    visiting: set[str] = set()
    def visit(letter: str) -> frozenset[str]:
        if letter in visiting:
            raise ValueError(f"the precedence table has a cycle through {letter}")
        if letter not in found:
            visiting.add(letter)
            found[letter] = frozenset(direct[letter]).union(*(visit(p) for p in direct[letter]))
            visiting.discard(letter)
        return found[letter]
    return {letter: visit(letter) for letter in direct}


def topological_events(arrows: Iterable[Arrow]) -> list[int] | None:
    """Events in an order where every arrow goes forward, or None when the arrows form a cycle."""
    arrows = list(arrows)
    events = {a.tail for a in arrows} | {a.head for a in arrows}
    incoming = {e: sum(1 for a in arrows if a.head == e) for e in events}
    ready = sorted(e for e in events if incoming[e] == 0)
    order: list[int] = []
    while ready:
        event = ready.pop(0)
        order.append(event)
        for arrow in sorted((a for a in arrows if a.tail == event), key=lambda a: a.head):
            incoming[arrow.head] -= 1
            if incoming[arrow.head] == 0:
                ready.append(arrow.head)
    return order if len(order) == len(events) else None


def implied_ancestors(arrows: Sequence[Arrow]) -> dict[str, frozenset[str]] | None:
    """The precedences a network encodes: A precedes B when A's head reaches B's tail."""
    order = topological_events(arrows)
    if order is None:
        return None
    reach = {e: {e} for e in order}
    for event in reversed(order):
        for arrow in arrows:
            if arrow.tail == event:
                reach[event] |= reach[arrow.head]
    heads = {a.letter: a.head for a in arrows if a.letter is not None}
    tails = {a.letter: a.tail for a in arrows if a.letter is not None}
    return {b: frozenset(a for a, head in heads.items() if tails[b] in reach[head]) for b in tails}


def is_valid(arrows: Sequence[Arrow], expected: Mapping[str, frozenset[str]]) -> bool:
    pairs = [(a.tail, a.head) for a in arrows]
    no_loops = all(a.tail != a.head for a in arrows)
    return no_loops and len(set(pairs)) == len(pairs) and implied_ancestors(arrows) == expected


def merge_events(arrows: Sequence[Arrow], removed: Arrow, source: int, target: int) -> list[Arrow]:
    """Drops a dummy and fuses one of its events into the other."""
    def move(event: int) -> int:
        return target if event == source else event
    return [Arrow(move(a.tail), move(a.head), a.letter, a.weeks) for a in arrows if a is not removed]


def simplify_once(arrows: Sequence[Arrow], expected: Mapping[str, frozenset[str]]) -> list[Arrow] | None:
    """The network with one dummy fewer (dropped if implied, else merged into a neighbour), or None."""
    dummies = [a for a in arrows if a.letter is None]
    dropped = ([a for a in arrows if a is not d] for d in dummies)
    merged = (merge_events(arrows, d, source, target) for d in dummies
              for source, target in ((d.tail, d.head), (d.head, d.tail)))
    return next((c for c in chain(dropped, merged) if is_valid(c, expected)), None)


def build_arrows(activities: Sequence[Activity]) -> list[Arrow]:
    """Starts with one dummy per dependency and simplifies until every remaining dummy is needed."""
    predecessor_sets = sorted({frozenset(a.predecessors) for a in activities}, key=sorted)
    start_event = {s: i for i, s in enumerate(predecessor_sets, start=1)}
    end_event = len(start_event) + len(activities) + 1
    arrows: list[Arrow] = []
    for i, activity in enumerate(activities, start=len(start_event) + 1):
        feeds = [s for s in predecessor_sets if activity.letter in s]
        head = i if feeds else end_event
        arrows.append(Arrow(start_event[frozenset(activity.predecessors)], head, activity.letter, activity.weeks))
        arrows += [Arrow(i, start_event[s], None) for s in feeds]
    expected = ancestors(activities)
    while (simpler := simplify_once(arrows, expected)) is not None:
        arrows = simpler
    return arrows


def schedule(activities: Sequence[Activity]) -> Schedule:
    """Numbers the events so arrows only go forward, then runs the forward and backward passes."""
    arrows = build_arrows(activities)
    order = topological_events(arrows)
    assert order is not None, "build_arrows only returns acyclic networks"
    number = {event: i for i, event in enumerate(order, start=1)}
    arrows = [Arrow(number[a.tail], number[a.head], a.letter, a.weeks) for a in arrows]
    events = sorted(number.values())
    earliest = {e: 0 for e in events}
    for event in events:
        for arrow in arrows:
            if arrow.head == event:
                earliest[event] = max(earliest[event], earliest[arrow.tail] + arrow.weeks)
    latest = {e: earliest[events[-1]] for e in events}
    for event in reversed(events):
        for arrow in arrows:
            if arrow.tail == event:
                latest[event] = min(latest[event], latest[arrow.head] - arrow.weeks)
    return Schedule(tuple(sorted(arrows, key=lambda a: (a.tail, a.head))), earliest, latest)


def tikz(plan: Schedule, positions: Mapping[int, tuple[float, float]]) -> str:
    missing = set(plan.earliest) - set(positions)
    if missing:
        raise ValueError(f"events without a position: {sorted(missing)}")
    lines = [f"\\begin{{tikzpicture}}[x={COLUMN_CM}cm, y={LANE_CM}cm, >=Stealth,",
             r"        evento/.style={circle, draw=eapA, fill=white, minimum size=6mm, inner sep=0pt, font=\sffamily\scriptsize},",
             r"        ativ/.style={->, draw=eapA, semithick}, fantasma/.style={->, draw=eapA, dashed},",
             r"        critica/.style={draw=red!75!black, very thick},",
             r"        every edge quotes/.style={font=\sffamily\scriptsize, inner sep=1.5pt, auto, sloped, pos=0.45}]"]
    for event in sorted(plan.earliest):
        column, lane = positions[event]
        style = "evento, critica" if plan.is_critical_event(event) else "evento"
        lines.append(f"    \\node[{style}] (e{event}) at ({column:g}, {lane:g}) {{{event}}};")
    for arrow in plan.arrows:
        options = ["ativ" if arrow.letter else "fantasma"] + (["critica"] if plan.is_critical(arrow) else [])
        if arrow.letter in ROUTES:
            options.append(ROUTES[arrow.letter])
        if arrow.letter:
            options += [f'"{arrow.letter}"', f'"{arrow.weeks}"\'']
        lines.append(f"    \\path (e{arrow.tail}) edge[{', '.join(options)}] (e{arrow.head});")
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def table_rows(activities: Sequence[Activity]) -> str:
    return "".join(f"{a.letter} & {a.code} & {a.name} & {a.weeks} & {', '.join(a.predecessors) or '-'} \\\\\n\\hline\n"
                   for a in activities)


def numbers(plan: Schedule, activities: Sequence[Activity]) -> str:
    """Macros for every figure the text quotes, so the prose cannot drift from the network."""
    development = [a.letter for a in activities if a.code.startswith(("1.4.", "1.5.1.", "1.5.2."))]
    tail_of = {a.letter: a.tail for a in plan.arrows if a.letter}
    head_of = {a.letter: a.head for a in plan.arrows if a.letter}
    macros = {
        "duracaoTotal": plan.total_weeks,
        # an activity that starts after week 9 runs in week 10
        "inicioDesenvolvimento": min(plan.earliest[tail_of[x]] for x in development) + 1,
        "fimTestes": max(plan.earliest[head_of[x]] for x in development),
        "caminhoCritico": ", ".join(a.letter for a in activities if a.letter in plan.critical_letters()),
    }
    return "".join(f"\\newcommand{{\\{name}}}{{{value}}}\n" for name, value in macros.items())


def main(out_dir: Path) -> None:
    plan = schedule(ACTIVITIES)
    (out_dir / "rede_aoa.tex").write_text(tikz(plan, POSITIONS))
    (out_dir / "atividades.tex").write_text(table_rows(ACTIVITIES))
    (out_dir / "numeros.tex").write_text(numbers(plan, ACTIVITIES))


if __name__ == "__main__":  # pragma: no cover
    main(Path(__file__).parent)
