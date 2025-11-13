import dspy

from dsconfigtweak import Coder, submetric, devset, lm, metric

dspy.configure(lm=lm())

def score_program(prog: str) -> float:
    """Check prog as a valid Beltabol program.
       Return values:
       0.0 - not even valid
       0.5 - valid syntax
       1.0 - valid syntax, but semantic errors
    """
    return submetric(["../beltabol/bin/bb"], prog)

code = dspy.ReAct(Coder, tools=[score_program], max_iters=5)

scores = []
for x in devset("targ.bb"):
    pred = code(**x.inputs())
    pred.beltabol_code = pred.beltabol_in
    score = metric(x, pred)
    scores.append(score)
    print(pred.trajectory)

print(scores)
