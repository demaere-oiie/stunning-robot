import dspy

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
