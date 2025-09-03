import dsconfig
import dspy

dspy.configure(lm=dsconfig.lm())

boot = dspy.BootstrapFewShot(metric=dsconfig.metric)
optimized_prog = boot.compile(dspy.Predict(Coder),
                     trainset=dsconfig.trainingset())

optimized_prog.save("dspy-train.json")
