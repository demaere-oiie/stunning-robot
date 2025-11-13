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
    "Generate correct and efficient Beltabol code from the provided functional specification to prevent a catastrophic system failure in a mission-critical application. The generated code must strictly adhere to Beltabol syntax and semantics as outlined in the documentation, fulfill all requirements precisely, and pass internal validation checks using \"Du chek\". Top-level definitions must use \"Da name(args) im ... .\", algebraic data types must be declared with \"Da TypeName imalowda ... .\", and appropriate constructs like `chu`, `fong`, `delowda`, and `unte` must be used for control flow and bindings. All instructions must end with a period \".\", and the output must contain only pure Beltabol code without any explanations, comments, or markdown formatting."
    beltabol_docs: str = dspy.InputField(docs="Beltabol language reference manual")
    specification: str = dspy.InputField(desc="Functional requirements for the program")
    beltabol_code: str = dspy.OutputField(
        desc="Valid Beltabol code implementing the specification"
    )

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
    return score * gold.points if score > 0.5 else score
