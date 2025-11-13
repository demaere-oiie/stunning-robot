import dspy

from dsconfig3 import Coder, devset, lm, metric

dspy.configure(lm=lm())

base = "Generate program source"

for s in [base]:

    Coder.__doc__ = s
    prog = dspy.Predict(Coder)

    scores = []
    for x in devset():
        pred = prog(**x.inputs())
        score = metric(x, pred)
        scores.append(score)

    print("####   " + str(scores))
