import dspy

from dsconfig3 import Coder, devset, lm, metric

dspy.configure(lm=lm())

base = """Generate Beltabol code from a program specification.

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

newp = "Given a target object and task description, generate a Beltabol program that accomplishes the specified task. Beltabol uses unique syntax including `chu` for conditionals, `fong` for let expressions with bottom-to-top evaluation, `imalowda` for user-defined algebraic datatypes, and `?=` for pattern matching.  Consider the standard prelude utilities and list comprehension binding order when constructing your solution. The program should be written in proper Beltabol syntax and be functionally complete for the given task."

crit = "Generate correct and efficient Beltabol code from the provided functional specification to prevent a catastrophic system failure in a mission-critical application. The generated code must strictly adhere to Beltabol syntax and semantics as outlined in the documentation, fulfill all requirements precisely, and pass internal validation checks using \"Du chek\". Top-level definitions must use \"Da name(args) im ... .\", algebraic data types must be declared with \"Da TypeName imalowda ... .\", and appropriate constructs like `chu`, `fong`, `delowda`, and `unte` must be used for control flow and bindings. All instructions must end with a period \".\", and the output must contain only pure Beltabol code without any explanations, comments, or markdown formatting."

for s in [base, newp, crit]:

    Coder.__doc__ = s
    prog = dspy.Predict(Coder)

    scores = []
    for x in devset():
        pred = prog(**x.inputs())
        score = metric(x, pred)
        scores.append(score)

    print("####   " + str(scores))
