import dspy

from dsconfigtweak import Coder, Tweaker, devset, lm, metric

dspy.configure(lm=lm())

code = dspy.Predict(Coder)
tweak= dspy.Predict(Tweaker)

scores = []
for x in devset("targ.bb"):
    c = code(**x.inputs())
    c.beltabol_docs = x.beltabol_docs
    print(":-:-:")
    print(c.beltabol_in)
    print(":-:-:")
    pred = tweak(**c)
    score = metric(x, pred)
    scores.append(score)

print(scores)
