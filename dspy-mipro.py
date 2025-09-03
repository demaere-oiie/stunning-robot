import dsconfig
import dspy
from .dsconfig import Coder

dspy.configure(lm=dsconfig.lm())

mipro = dspy.MIPROv2(metric=dsconfig.metric)
optimized_prog = mipro.compile(dspy.Predict(Coder),
                               trainset=dsconfig.trainingset(),
                               fewshot_aware_proposer=False)

optimized_prog.save("dspy-mipro.json")
