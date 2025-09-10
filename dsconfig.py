import dspy
import logging
import os
import subprocess

def lm():
    if 'CEREBRAS_API_KEY' in os.environ:
        return dspy.LM("cerebras/qwen-3-coder-480b",
            api_key=os.environ['CEREBRAS_API_KEY'])
    else:
        logging.getLogger("dspy").setLevel(logging.DEBUG)
        return dspy.LM("ollama_chat/deepseek-coder:33b",
            cache=False,
            api_base='http://localhost:11434')

class Coder(dspy.Signature):
    """Generate program source."""
    target: str = dspy.InputField(desc="Documentation for the target language")
    task: str = dspy.InputField(desc="The algorithm we want code for")
    program: str = dspy.OutputField(desc="The generated program")

def trainingset():
    target = open("targ.bb").read()
    return [
      dspy.Example({
        'target': target,
        'task': task + "Please use `Du chek` to check your program",
	'program': ''}).with_inputs('target','task')
      for t in "fac gcd is ms kos tarj".split()
      for task in [open("task."+t).read()]
    ]

def devset():
    target = open("targ.bb").read()
    return [
      dspy.Example({
        'beltabol_docs': target,
        'specification': task + "Please use `Du chek` to check your program",
        'points': p,
	}).with_inputs('beltabol_docs','specification')
      for t,p in [("fac",1),("gcd",1),("is",2),("ms",2),("kos",3),("tarj",4)]
      for task in [open("task."+t).read()]
    ]


def submetric(cmd, inp):
    score = 0.0

    cp = subprocess.run(cmd, input=inp.encode("utf8"), capture_output=True)
    return 0.5 * (cp.returncode==0) + 0.5 * (len(cp.stderr)==0)

def metric(gold, pred, trace=None):
    score = 0.0

    if hasattr(pred,'program'):
        prog = pred.program
    else:
        prog = pred.beltabol_code

    print("---- " + str(gold.points))
    print(prog)
    print("----")

    score += submetric(["../beltabol/bin/bb"], prog)/2.
    if "Du chek" in prog:
        score += submetric(["../beltabol/bin/bb", "--test"], prog)/2.

    print("==== " + str(score))
    return score * gold.points
