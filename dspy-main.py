import dspy
import os
import sys

if len(sys.argv) < 3:
    print("Usage: {} target task".format(sys.argv[0],))
    sys.exit()

target = open(sys.argv[1])
task   = open(sys.argv[2])

lm = dspy.LM("cerebras/qwen-3-coder-480b",
        api_key=os.environ['CEREBRAS_API_KEY'])
dspy.configure(lm=lm)

prog = dspy.Predict("target, task-> program")

print(prog(target=target.read(), task=task.read()))
