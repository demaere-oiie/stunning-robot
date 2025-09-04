import dspy

from dspy.evaluate import Evaluate
from dsconfig import devset, lm, metric

dspy.configure(lm=lm())

evaluator = Evaluate(devset=devset(), num_threads=1, display_progress=True, display_table=5)

prog = dspy.load("./beltabolcoder/")

#evaluator(prog, metric=metric)

scores = []
for x in devset():
    pred = prog(**x.inputs())
    score = metric(x, pred)
    scores.append(score)

print(scores)
