import dspy

from dsconfigtweak import Coder, submetric, devset, lm, metric

dspy.configure(lm=lm())

def check_syntax(prog: str) -> bool:
    """Check if prog is a valid Beltabol program"""
    return submetric(["../beltabol/bin/bb"], prog) > 0

code = dspy.ReAct(Coder, tools=[check_syntax], max_iters=5)

scores = []
for x in devset("targ.bb"):
    pred = code(**x.inputs())
    pred.beltabol_code = pred.beltabol_in
    score = metric(x, pred)
    scores.append(score)
    print(pred.trajectory)

print(scores)
