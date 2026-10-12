"""AHP for the semester project's tool choice: the judgments below are the single source for every matrix,
priority vector, CR and ranking the document shows. Run `python ahp.py` to check them and write tabelas/."""
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path

RANDOM_INDEX = 0.90  # Saaty's random index for n = 4 (Vargas 2010, Table 8)
CR_LIMIT = 0.10


@dataclass(frozen=True)
class Judgment:
    preferred: str
    over: str
    intensity: int
    reason: str = ""  # the fact behind the number; each matrix's paragraph in the document expands on it


@dataclass(frozen=True)
class Comparison:
    slug: str  # names the macros (\cr<Slug>, \peso<Slug>) and, lowercased, the file matriz_<slug>.tex
    title: str
    elements: tuple[str, ...]
    judgments: tuple[Judgment, ...]


@dataclass(frozen=True)
class Result:
    comparison: Comparison
    matrix: tuple[tuple[Fraction, ...], ...]
    weights: tuple[float, ...]
    lambda_max: float

    @property
    def consistency_ratio(self) -> float:
        n = len(self.weights)
        # lambda_max >= n for a reciprocal matrix; the clamp only drops floating-point noise
        return max(0.0, (self.lambda_max - n) / (n - 1)) / RANDOM_INDEX

    @property
    def consistent(self) -> bool:
        # judged on the 3 decimals the document prints, so "0,100" is never called consistent
        return round(self.consistency_ratio, 3) < CR_LIMIT


@dataclass(frozen=True)
class Deviation:
    judgment: Judgment
    implied: float  # preferred / over, as the weights put it
    ratio: float  # >= 1: how many times the judgment is off from what the weights imply


@dataclass(frozen=True)
class Score:
    alternative: str
    by_criterion: tuple[float, ...]
    total: float


@dataclass(frozen=True)
class Flip:
    matrix: str
    row: str
    column: str
    before: Fraction  # the entry at row x column, as the matrix tables print it
    after: Fraction
    scores: tuple[Score, ...]


@dataclass(frozen=True)
class Sensitivity:
    tried: int
    flips: tuple[Flip, ...]  # the one-step changes that put another alternative first


CRITERIA = ("Custo de desenvolvimento", "Prazo de entrega", "Facilidade de manutenção", "Facilidade de mão de obra")
ALTERNATIVES = ("Java", "C#", "Python", "Go")

# Judgment("X", "Y", 5, "motivo") reads "X is strongly preferred to Y" (Saaty scale, integer 1 to 9).
# To favour Y, swap the names; 1 means equal. Each matrix takes its 6 pairs.
CRITERIA_JUDGMENTS = Comparison("Criterios", "Critérios", CRITERIA, (
    Judgment("Prazo de entrega", "Custo de desenvolvimento", 5,
             "o time só existe nas 26 semanas de bolsa; as licenças são gratuitas nas quatro"),
    Judgment("Facilidade de manutenção", "Custo de desenvolvimento", 3,
             "o sistema vive anos depois da implantação; o custo quase não muda entre as linguagens"),
    Judgment("Facilidade de mão de obra", "Custo de desenvolvimento", 5,
             "sem bolsistas que saibam a linguagem não há time; o custo quase não muda"),
    Judgment("Prazo de entrega", "Facilidade de manutenção", 2,
             "as bolsas deixam só 9 semanas de reserva; a manutenção ficou fora do escopo"),
    Judgment("Prazo de entrega", "Facilidade de mão de obra", 1,
             "os dois limitam a entrega nos 6 meses de bolsa"),
    Judgment("Facilidade de mão de obra", "Facilidade de manutenção", 2,
             "o time precisa existir durante o projeto; a manutenção vem depois"),
))

ALTERNATIVE_JUDGMENTS = (
    Comparison("Custo", "Custo de desenvolvimento", ALTERNATIVES, (
        Judgment("Java", "C#", 1, "a extensão C# do VS Code é gratuita sem limite de porte; só o Dev Kit é restrito"),
        Judgment("Python", "C#", 1, "a extensão C# do VS Code é gratuita sem limite de porte; só o Dev Kit é restrito"),
        Judgment("Go", "C#", 1, "a extensão C# do VS Code é gratuita sem limite de porte; só o Dev Kit é restrito"),
        Judgment("Java", "Python", 1, "licenças e ferramentas gratuitas nas duas"),
        Judgment("Java", "Go", 1, "licenças e ferramentas gratuitas nas duas"),
        Judgment("Python", "Go", 1, "licenças e ferramentas gratuitas nas duas"),
    )),
    Comparison("Prazo", "Prazo de entrega", ALTERNATIVES, (
        Judgment("Python", "Java", 3, "Django traz o admin pronto para os cadastros, além de login e permissões"),
        Judgment("Python", "C#", 3, "Django traz o admin pronto para os cadastros, além de login e papéis"),
        Judgment("Python", "Go", 7, "Django traz admin e usuários com permissões; o Gin não traz nenhum dos dois"),
        Judgment("Java", "C#", 1, "Spring Security e Data JPA equivalem a Identity e EF Core; nenhum traz admin"),
        Judgment("Java", "Go", 3, "Spring Security dá usuários e papéis; o Gin só tem BasicAuth e usa o GORM à parte"),
        Judgment("C#", "Go", 3, "Identity dá usuários e papéis; o Gin só tem BasicAuth e usa o GORM à parte"),
    )),
    Comparison("Manutencao", "Facilidade de manutenção", ALTERNATIVES, (
        Judgment("C#", "Java", 2, "os dois têm tipagem estática; LTS de 3 anos no ASP.NET, 13 meses no Spring Boot"),
        Judgment("Java", "Python", 2, "a tipagem estática pesa mais que o suporte mais longo de Django e Python"),
        Judgment("Java", "Go", 1, "tipagem estática nos dois; Spring Boot e Go pedem atualizar a cada ano"),
        Judgment("C#", "Python", 3, "o compilador pega erros de tipo; suporte de 3 anos nos dois frameworks"),
        Judgment("C#", "Go", 2, "os dois têm tipagem estática; LTS de 3 anos no .NET, cerca de 1 ano no Go"),
        Judgment("Go", "Python", 2, "a tipagem estática pesa mais que o suporte mais longo de Django e Python"),
    )),
    Comparison("MaoDeObra", "Facilidade de mão de obra", ALTERNATIVES, (
        Judgment("Java", "C#", 3, "ACH2003, obrigatória em SI, tem bibliografia de Java; C# não aparece na grade"),
        Judgment("Java", "Python", 2, "ACH2003 é obrigatória em SI; Python é a mais usada das quatro na pesquisa"),
        Judgment("Java", "Go", 5, "ACH2003 é obrigatória em SI; Go não aparece na grade e tem 17,4% na pesquisa"),
        Judgment("Python", "C#", 2, "Python tem 54,8% na pesquisa, contra 29,9% do C#"),
        Judgment("Python", "Go", 3, "Python tem 54,8% na pesquisa, contra 17,4% do Go"),
        Judgment("C#", "Go", 2, "C# tem 29,9% na pesquisa, contra 17,4% do Go"),
    )),
)


def judgment_problems(comparison: Comparison) -> tuple[str, ...]:
    title, elements = comparison.title, comparison.elements
    if len(set(elements)) != 4 or len(elements) != 4:
        return (f"{title}: a matriz precisa de 4 elementos distintos (RI = 0,90 vale para n = 4)",)
    problems, seen = [], set()
    for j in comparison.judgments:
        unknown = [name for name in (j.preferred, j.over) if name not in elements]
        if unknown:
            problems += [f"{title}: {name} não é um elemento desta matriz" for name in unknown]
        elif j.preferred == j.over:
            problems.append(f"{title}: {j.preferred} aparece nos dois lados do julgamento")
        elif frozenset((j.preferred, j.over)) in seen:
            first, second = sorted((j.preferred, j.over), key=elements.index)
            problems.append(f"{title}: o par {first} e {second} aparece mais de uma vez")
        if type(j.intensity) is not int or not 1 <= j.intensity <= 9:
            problems.append(f"{title}: {j.preferred} e {j.over}: a intensidade {j.intensity}"
                            " não é um inteiro de 1 a 9")
        seen.add(frozenset((j.preferred, j.over)))
    problems += [f"{title}: falta comparar {a} com {b}" for a, b in combinations(elements, 2)
                 if frozenset((a, b)) not in seen]
    return tuple(problems)


def hierarchy_problems(criteria: Comparison, alternatives: Sequence[Comparison]) -> tuple[str, ...]:
    if not alternatives or tuple(c.title for c in alternatives) != criteria.elements:
        return ("as matrizes de alternativas precisam seguir os critérios, na ordem: " + ", ".join(criteria.elements),)
    first = alternatives[0]
    return tuple(f"{c.title}: as alternativas precisam ser as mesmas de {first.title}"
                 for c in alternatives[1:] if c.elements != first.elements)


def reciprocal_matrix(comparison: Comparison) -> tuple[tuple[Fraction, ...], ...]:
    index = {name: i for i, name in enumerate(comparison.elements)}
    n = len(comparison.elements)
    rows = [[Fraction(1)] * n for _ in range(n)]
    for j in comparison.judgments:
        rows[index[j.preferred]][index[j.over]] = Fraction(j.intensity)
        rows[index[j.over]][index[j.preferred]] = Fraction(1, j.intensity)
    return tuple(tuple(row) for row in rows)


def evaluate(comparison: Comparison) -> Result:
    """Principal eigenvector as the normalized row sums of A^(2^30): for a positive matrix the powers
    converge to it, and 30 squarings leave any gap to the second eigenvalue far below float precision."""
    matrix = reciprocal_matrix(comparison)
    n = len(matrix)
    power = [[float(a) for a in row] for row in matrix]
    for _ in range(30):
        power = [[sum(power[i][k] * power[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        top = max(max(row) for row in power)
        power = [[x / top for x in row] for row in power]
    row_sums = [sum(row) for row in power]
    weights = [s / sum(row_sums) for s in row_sums]
    # with the weights summing to 1, the sum of A.w is lambda_max (Vargas: weights times column totals)
    lambda_max = sum(sum(float(a) * w for a, w in zip(row, weights)) for row in matrix)
    return Result(comparison, matrix, tuple(weights), lambda_max)


def deviations(result: Result) -> tuple[Deviation, ...]:
    index = {name: i for i, name in enumerate(result.comparison.elements)}
    found = []
    for j in result.comparison.judgments:
        implied = result.weights[index[j.preferred]] / result.weights[index[j.over]]
        off = j.intensity / implied
        found.append(Deviation(j, implied, max(off, 1 / off)))
    return tuple(sorted(found, key=lambda d: d.ratio, reverse=True))


def describe(d: Deviation) -> str:
    j = d.judgment
    said = (f"{j.preferred} e {j.over} empatam" if j.intensity == 1
            else f"{j.preferred} é preferível a {j.over} com intensidade {j.intensity}")
    return f"{said}, mas os pesos dão {j.preferred}/{j.over} = {comma(d.implied, 2)}"


def rank(criteria: Result, alternatives: Sequence[Result]) -> tuple[Score, ...]:
    names = alternatives[0].comparison.elements
    scores = []
    for i, name in enumerate(names):
        local = tuple(r.weights[i] for r in alternatives)
        scores.append(Score(name, local, sum(w * x for w, x in zip(criteria.weights, local))))
    return tuple(sorted(scores, key=lambda s: s.total, reverse=True))


def standings(matrices: Sequence[Comparison]) -> tuple[Score, ...]:
    results = [evaluate(c) for c in matrices]
    return rank(results[0], results[1:])


def nudges(j: Judgment) -> tuple[Judgment, ...]:
    """The judgments one step away on Saaty's scale: 1 becomes 2 for either side, k becomes k-1 or k+1."""
    if j.intensity == 1:
        return Judgment(j.preferred, j.over, 2), Judgment(j.over, j.preferred, 2)
    return tuple(Judgment(j.preferred, j.over, k) for k in (j.intensity - 1, j.intensity + 1) if k <= 9)


def cell(j: Judgment, row: str) -> Fraction:
    return Fraction(j.intensity) if j.preferred == row else Fraction(1, j.intensity)


def sensitivity(criteria: Comparison, alternatives: Sequence[Comparison]) -> Sensitivity:
    matrices = (criteria, *alternatives)
    leader = standings(matrices)[0].alternative
    tried, flips = 0, []
    for i, m in enumerate(matrices):
        for j in m.judgments:
            for n in nudges(j):
                tried += 1
                changed = Comparison(m.slug, m.title, m.elements, tuple(n if x == j else x for x in m.judgments))
                scores = standings((*matrices[:i], changed, *matrices[i + 1:]))
                if scores[0].alternative != leader:
                    row, column = sorted((j.preferred, j.over), key=m.elements.index)
                    flips.append(Flip(m.title, row, column, cell(j, row), cell(n, row), scores))
    return Sensitivity(tried, tuple(flips))


def comma(value: float, digits: int) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def percent(value: float) -> str:
    return comma(100 * value, 1) + r"\%"


def fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def escape(name: str) -> str:
    for special in "#&%_$":
        name = name.replace(special, "\\" + special)
    return name


def matrix_table(result: Result) -> str:
    names = [escape(e) for e in result.comparison.elements]
    # \nohyphens is defined by the document; 2.7cm fits "desenvolvimento" in bold without breaking it
    lines = [(r"\begin{tabular}{|>{\raggedright\arraybackslash\nohyphens}p{2.7cm}|"
              r"*{4}{>{\centering\arraybackslash\nohyphens}p{2.7cm}|}>{\centering\arraybackslash}p{1.8cm}|}"),
             r"\hline", r"\rowcolor{eapC}",
             " & " + " & ".join(rf"\textbf{{{n}}}" for n in names) + r" & \textbf{Prioridade} \\", r"\hline"]
    for name, row, weight in zip(names, result.matrix, result.weights):
        lines += [rf"\textbf{{{name}}} & " + " & ".join(fraction(a) for a in row) + f" & {percent(weight)} \\\\",
                  r"\hline"]
    return "\n".join(lines + [r"\end{tabular}"]) + "\n"


def ranking_table(criteria: Result, scores: Sequence[Score]) -> str:
    headers = [rf"\textbf{{{escape(c)}}} ({percent(w)})"
               for c, w in zip(criteria.comparison.elements, criteria.weights)]
    lines = [r"\begin{tabular}{|c|l|*{4}{>{\centering\arraybackslash\nohyphens}p{2.7cm}|}c|}",
             r"\hline", r"\rowcolor{eapC}",
             r"\textbf{Posição} & \textbf{Alternativa} & " + " & ".join(headers) + r" & \textbf{Total} \\", r"\hline"]
    for place, s in enumerate(scores, start=1):
        cells = [f"{place}º", escape(s.alternative), *(percent(x) for x in s.by_criterion), percent(s.total)]
        lines += [" & ".join(cells) + r" \\", r"\hline"]
    return "\n".join(lines + [r"\end{tabular}"]) + "\n"


def sensitivity_table(s: Sensitivity) -> str:
    lines = [(r"\begin{tabular}{|>{\raggedright\arraybackslash}p{2.6cm}|>{\raggedright\arraybackslash}p{5.4cm}|c|"
              r">{\raggedright\arraybackslash}p{4.6cm}|}"),
             r"\hline", r"\rowcolor{eapC}",
             r"\textbf{Matriz} & \textbf{Linha $\times$ coluna} & \textbf{Valor} & \textbf{Novo ranking} \\", r"\hline"]
    for f in s.flips:
        first, second = f.scores[0], f.scores[1]
        cells = [escape(f.matrix), rf"{escape(f.row)} $\times$ {escape(f.column)}",
                 rf"{fraction(f.before)} $\rightarrow$ {fraction(f.after)}",
                 (f"{escape(first.alternative)} ({percent(first.total)}) à frente de "
                  f"{escape(second.alternative)} ({percent(second.total)})")]
        lines += [" & ".join(cells) + r" \\", r"\hline"]
    if not s.flips:
        lines += [r"\multicolumn{4}{|c|}{Nenhuma mudança de um ponto troca o primeiro lugar} \\", r"\hline"]
    return "\n".join(lines + [r"\end{tabular}"]) + "\n"


def numbers(criteria: Result, alternatives: Sequence[Result], scores: Sequence[Score], s: Sensitivity) -> str:
    """Macros for every figure the text quotes, so the prose cannot drift from the matrices."""
    macros = [(f"cr{r.comparison.slug}", comma(r.consistency_ratio, 3)) for r in (criteria, *alternatives)]
    macros += [(f"peso{r.comparison.slug}", percent(w)) for r, w in zip(alternatives, criteria.weights)]
    macros += [("primeiroLugar", escape(scores[0].alternative)), ("pontuacaoPrimeiro", percent(scores[0].total)),
               ("segundoLugar", escape(scores[1].alternative)), ("pontuacaoSegundo", percent(scores[1].total)),
               ("mudancasTestadas", str(s.tried)), ("mudancasQueTrocam", str(len(s.flips)))]
    return "".join(f"\\newcommand{{\\{name}}}{{{value}}}\n" for name, value in macros)


def run(criteria: Comparison, alternatives: Sequence[Comparison], out_dir: Path) -> int:
    problems = hierarchy_problems(criteria, alternatives)
    problems += tuple(p for c in (criteria, *alternatives) for p in judgment_problems(c))
    if problems:
        print("Julgamentos incompletos ou inválidos:", *problems, sep="\n  ")
        return 1
    results = [evaluate(c) for c in (criteria, *alternatives)]
    for r in results:
        verdict = "consistente" if r.consistent else f"não é menor que {comma(CR_LIMIT, 2)}, revise"
        print(f"{r.comparison.title}: CR = {comma(r.consistency_ratio, 3)} ({verdict})")
        if not r.consistent:
            print(*(f"  {describe(d)}" for d in deviations(r)[:3]), sep="\n")
    if not all(r.consistent for r in results):
        return 1
    scores = rank(results[0], results[1:])
    shaken = sensitivity(criteria, alternatives)
    out_dir.mkdir(exist_ok=True)
    for r in results:
        (out_dir / f"matriz_{r.comparison.slug.lower()}.tex").write_text(matrix_table(r))
    (out_dir / "ranking.tex").write_text(ranking_table(results[0], scores))
    (out_dir / "sensibilidade.tex").write_text(sensitivity_table(shaken))
    (out_dir / "numeros.tex").write_text(numbers(results[0], results[1:], scores, shaken))
    print(*(f"{place}º {s.alternative}: {comma(100 * s.total, 1)}%" for place, s in enumerate(scores, start=1)),
          sep="\n")
    print(f"Mudanças de um ponto que trocam o primeiro lugar: {len(shaken.flips)} de {shaken.tried}")
    if comma(100 * scores[0].total, 1) == comma(100 * scores[1].total, 1):
        print(f"Atenção: {scores[0].alternative} e {scores[1].alternative} empatam no primeiro lugar")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(run(CRITERIA_JUDGMENTS, ALTERNATIVE_JUDGMENTS, Path(__file__).parent / "tabelas"))
