import dspy

from dsconfigplan import Planner, Implementer, devset, lm, metric

dspy.configure(lm=lm())

plan = dspy.Predict(Planner)
impl = dspy.Predict(Implementer)

scores = []
for x in devset("targ.bb"):
    p = plan(**x.inputs())
    p.beltabol_docs = x.beltabol_docs
    print(":-:-:")
    print(p.plan)
    print(":-:-:")
    pred = impl(**p)
    score = metric(x, pred)
    scores.append(score)

print(scores)
