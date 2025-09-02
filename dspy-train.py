import dspy
import os

from dsconfig import *

dspy.configure(lm=dspy.LM("cerebras/qwen-3-coder-480b",
        api_key=os.environ['CEREBRAS_API_KEY']))

boot = dspy.BootstrapFewShot(metric=metric)
optimized_prog = boot.compile(dspy.Predict(Coder), trainset=trainingset())

optimized_prog.save("dspy-train.json")
