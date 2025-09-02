import dspy
import os

from dsconfig import *

dspy.configure(lm=dspy.LM("cerebras/qwen-3-coder-480b",
        api_key=os.environ['CEREBRAS_API_KEY']))

mipro = dspy.MIPROv2(metric=metric)
optimized_prog = mipro.compile(dspy.Predict(Coder),
                               trainset=trainingset(),
                               fewshot_aware_proposer=False)

optimized_prog.save("dspy-mipro.json")
