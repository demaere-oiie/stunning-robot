import dspy
import subprocess

from dsconfigtweak import Coder, devset, lm, metric

dspy.configure(lm=lm())

def run_interpreter(prog: str) -> str:
    """Run the Beltabol interpreter.
       Returns:
           'VALID' if valid and all tests pass
           'ERROR' + output, if there was an error
    """
    cp = subprocess.run(["../beltabol/bin/bb","--test"],
             input=prog.encode("utf8"),
             capture_output=True)

    if cp.returncode==0 and len(cp.stderr)==0:
        return 'VALID'
    else:
        return 'ERROR '+(cp.stderr.decode("utf8") if len(cp.stderr)>0 else
                         cp.stdout.decode("utf8"))

code = dspy.ReAct(Coder, tools=[run_interpreter], max_iters=8)

scores = []
for x in devset("targ.bb")[4:5]:
    pred = code(**x.inputs())
    pred.beltabol_code = pred.beltabol_in
    score = metric(x, pred)
    scores.append(score)
    print(pred.trajectory)

print(scores)
