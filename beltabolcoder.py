import argparse
import dspy
from pathlib import Path
import os
import sys

import dspy.teleprompt


BELTABOL_DOCS_PATH = Path(__file__).parent / "targ.bb"


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        raise RuntimeError(f"Failed to read file: {path}: {e}")


def load_beltabol_docs() -> str:
    if not BELTABOL_DOCS_PATH.exists():
        raise FileNotFoundError(f"Beltabol docs not found at {BELTABOL_DOCS_PATH}")
    return read_text_file(BELTABOL_DOCS_PATH)


class GenerateBeltabolCode(dspy.Signature):
    """Generate Beltabol code from a program specification.

    You are given the Beltabol language documentation and a program specification.
    Produce only valid Beltabol code that statisfies the specification.

    Constraints:
    - Use "Du chek" to check your program.
    - Use Beltabol syntax only (per the provided docs).
    - End every top-level instruction with a period ".".
    - Prefer top-level definitions with: Da name(args) im ... .
    - For algebraic datatypes use: Da TypeName imalowda ... .
    - Use chu/fong/delowda/unte constructs as appropriate.
    - Do not include explanations, comments, or Markdown features
    """

    beltabol_docs: str = dspy.InputField(docs="Beltabol language reference manual")
    specification: str = dspy.InputField(desc="Functional requirements for the program")
    beltabol_code: str = dspy.OutputField(
        desc="Valid Beltabol code implementing the specification"
    )


class BeltabolCodeGenerator(dspy.Module):
    def __init__(self, beltabol_docs: str) -> None:
        super().__init__()
        self._docs = beltabol_docs
        self.predict = dspy.Predict(GenerateBeltabolCode)

    def forward(self, specification: str, **kwargs) -> dspy.Prediction:
        return self.predict(beltabol_docs=self._docs, specification=specification)


def build_trainset(beltabol_docs: str) -> list[dspy.Example]:
    """Create a small bootstrap trainset from examples in targ.bb"""
    examples: list[dspy.Example] = []

    # 1) Factorial
    examples.append(
        dspy.Example(
            beltabol_docs=beltabol_docs,
            specification=(
                "Define a recursive factorial function `fak(n)` over non-negative integers. "
                "Use 1 as the base case for n==0; otherwise compute n*fak(n-1)."
            ),
            beltabol_code=(
                "Da fak(n) im chu\n"
                "    n*fak(n-1) detim 1<=n;\n"
                "    1          detim owta."
            ),
        ).with_inputs("beltabol_docs", "specification")
    )

    # 2) Integer division returning quotient and remainder
    examples.append(
        dspy.Example(
            beltabol_docs=beltabol_docs,
            specification=(
                "Define a function `div(n,m)` that returns [q, r] such that n = q*m + r and 0 <= r < m."
            ),
            beltabol_code=(
                "Da h#p im p++h.\n"
                "Da div(n,m) im chu\n"
                "    (fong (chu [q#1, r-m] detim m<=r;\n"
                "               [q#0, r  ] detim owta)\n"
                "        wit [q,r] deting div(n,m#0)) detim m<=n;\n"
                "               [  0, n  ]            detim owta."
            ),
        ).with_inputs("beltabol_docs", "specification")
    )

    # 3) Flatten a list of lists
    examples.append(
        dspy.Example(
            beltabol_docs=beltabol_docs,
            specification=(
                "Define `flatten(xss)` that concatenates all inner lists in order into a single list."
            ),
            beltabol_code=(
                "Da flatten(xss) im fong x\n"
                "    wit x  delowda xs;\n"
                "    wit xs delowda xss."
            ),
        ).with_inputs("beltabol_docs", "specification")
    )

    # 4) Remove duplicates while preserving first occurrences
    examples.append(
        dspy.Example(
            beltabol_docs=beltabol_docs,
            specification=(
                "Define `nub(xs)` that removes duplicate elements from a list while preserving first occurrences."
            ),
            beltabol_code=(
                "Da nub(xs) im fong (chu\n"
                "    h<:nub(nawit(h,t)) detim xs?=h<:t;\n"
                "    []                 detim owta)\n"
                "    wit nawit(y,xs) deting (chu\n"
                "        (chu  nawit(y,t) detim h==y;\n"
                "           h<:nawit(y,t) detim owta) detim xs?=h<:t;\n"
                "         []                          detim owta)."
            ),
        ).with_inputs("beltabol_docs", "specification")
    )

    # 5) Example algebraic datatype
    examples.append(
        dspy.Example(
            beltabol_docs=beltabol_docs,
            specification=(
                "Create an algebraic datatype `peano` with constructors Zero and Succ(n) for natural numbers."
            ),
            beltabol_code=("Da peano imalowda Zero | Succ(n)."),
        ).with_inputs("beltabol_docs", "specification")
    )

    return examples


def validate_beltabol_code(
    example: dspy.Example, pred: dspy.Prediction, trace=None
) -> bool:
    """A light validation that the output looks like Beltabol code.

    This is a heuristic: checks structural cues and avoids explanatory text.
    """
    code = (pred.beltabol_code or "").strip()
    if not code:
        return False

    if code.startswith("`") or "```" in code:
        return False

    last_line = code.splitlines()[-1].strip()
    if not last_line.endswith("."):
        return False

    has_keyword = any(k in code for k in ["Da ", " im ", " chu", " fong ", "imalowda"])
    return has_keyword


def configure_lm(model: str, api_base: str | None) -> dspy.LM:
    if api_base:
        return dspy.LM(model=model, api_base=api_base)
    return dspy.LM(model=model)


def build_and_compile(beltabol_docs: str, *, shots: int = 4) -> dspy.Module:
    generator = BeltabolCodeGenerator(beltabol_docs)
    trainset = build_trainset(beltabol_docs)

    optimizer = dspy.teleprompt.BootstrapFewShot(
        metric=validate_beltabol_code,
        max_bootstrapped_demos=shots,
        max_labeled_demos=shots,
    )
    compiled = optimizer.compile(generator, trainset=trainset)
    return compiled


def read_specification_arg(raw: str) -> str:
    candidate = Path(raw)
    if raw == "-":
        return sys.stdin.read()
    if candidate.exists() and candidate.is_file():
        return read_text_file(candidate)
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Beltabol code")
    parser.add_argument(
        "spec",
    )
    parser.add_argument(
        "--model", default=os.getenv("OLLAMA_MODEL", "ollama_chat/deepseek-coder:33b")
    )
    parser.add_argument(
        "--api-base", default=os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=4,
    )
    args = parser.parse_args()

    lm = configure_lm(args.model, args.api_base)
    dspy.settings.configure(lm=lm)

    beltabol_docs = load_beltabol_docs()
    compiled = build_and_compile(beltabol_docs, shots=args.shots)

    specification = read_specification_arg(args.spec)
    result = compiled(specification=specification)

    print((result.beltabol_code or "").strip())


if __name__ == "__main__":
    main()
