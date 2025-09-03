import dsconfig
import dspy
import sys

if len(sys.argv) < 3:
    print("Usage: {} target task".format(sys.argv[0],))
    sys.exit()

target = open(sys.argv[1])
task   = open(sys.argv[2])

dspy.configure(lm=dsconfig.lm())

prog = dspy.Predict("target, task-> program")

print(prog(target=target.read(), task=task.read()))
