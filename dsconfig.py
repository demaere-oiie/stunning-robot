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

def submetric(cmd, inp):
    score = 0.0

    cp = subprocess.run(cmd, input=inp.encode("utf8"), capture_output=True)
    print(cp.returncode)
    return 0.5 * (cp.returncode==0) + 0.5 * (len(cp.stderr)==0)

def metric(gold, pred, trace=None):
    score = 0.0

    print("----")
    print(pred.program)
    print("----")

    score += submetric(["../beltabol/bin/bb"], pred.program)/2.
    score += submetric(["../beltabol/bin/bb", "--test"], pred.program)/2.

    print("==== " + str(score))
    return score
