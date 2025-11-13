import dspy

from dsconfigshort import Coder, devset, lm, metric

dspy.configure(lm=lm())

prog = dspy.Predict(Coder)

scores = []
for x in devset("targ.bb-agent"):
    pred = prog(**x.inputs())
    score = metric(x, pred)
    scores.append(score)

print(scores)
