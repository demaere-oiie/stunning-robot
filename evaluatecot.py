import dspy

from dsconfigshort import Coder, devset, lm, metric

dspy.configure(lm=lm())

prog = dspy.ChainOfThought(Coder)

scores = []
for x in devset("targ.bb"):
    pred = prog(**x.inputs())
    score = metric(x, pred)
    scores.append(score)

print(scores)
