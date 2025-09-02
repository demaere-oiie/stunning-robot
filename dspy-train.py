import dspy
import os
import sys

target = open("targ.bb")
task   = open("task.fac")

lm = dspy.LM("cerebras/qwen-3-coder-480b",
        api_key=os.environ['CEREBRAS_API_KEY'])
dspy.configure(lm=lm)

prog = dspy.Predict("target, task-> program")

trainset = [
    dspy.Example({
        'target': target.read(),
        'task': task.read() + "Please use `Du chek` to check your program",
	'program': 'Da fak(n) im chu\n    n*fak(n-1) detim 1<=n;\n    1          detim owta.'}).with_inputs('target','task')
]

def submetric(cmd):
    score = 0.0

    r = os.system(cmd + " 2> a.err")
    print(r)
    if r==0:
        score += 0.5

    f=open("a.err")
    err=f.read()
    f.close()
    if len(err)==0:
        score += 0.5

    return score

def metric(gold, pred, trace=None):
    score = 0.0

    print("----")
    print(pred.program)
    print("----")

    f=open("a.bb","w")
    f.write(pred.program)
    f.close()

    score += submetric("./bb < a.bb")/2.
    score += submetric("./bb --test < a.bb")/2.

    print("==== " + str(score))
    return score


boot = dspy.BootstrapFewShot(metric=metric)
optimized_prog = boot.compile(prog, trainset=trainset)
