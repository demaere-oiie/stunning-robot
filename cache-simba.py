import dsconfig
import dspy

dspy.configure(lm=dsconfig.lm())

class GenerateBeltabolCode(dspy.Signature):
    """Generate Beltabol code from a program specification.

    You are given the Beltabol language documentation and a program specification.
    Produce only valid Beltabol code that statisfies the specification.

    Constraints:
    - Use "Du chek" to check your program.
    - Use Beltabol syntax only (per the provided docs).
    - End every top-level instruction with a period ".".
    - Prefer top-level definitions with: Da name(args) im ... .
    - For algebraic datatypes use: Da TypeName imalowda ... .
    - Use chu/fong/delowda/unte constructs as appropriate.
    - Do not include explanations, comments, or Markdown features
    """

    beltabol_docs: str = dspy.InputField(docs="Beltabol language reference manual")
    specification: str = dspy.InputField(desc="Functional requirements for the program")
    beltabol_code: str = dspy.OutputField(
        desc="Valid Beltabol code implementing the specification"
    )

class BeltabolCodeGenerator(dspy.Module):
    def __init__(self, beltabol_docs: str) -> None:
        super().__init__()
        self._docs = beltabol_docs
        self.predict = dspy.Predict(GenerateBeltabolCode)

    def forward(self, specification: str, **kwargs) -> dspy.Prediction:
        return self.predict(beltabol_docs=self._docs, specification=specification)

generator = BeltabolCodeGenerator(open("targ.bb").read())

simba = dspy.SIMBA(metric=dsconfig.metric)
trainset = dsconfig.devset()[:]*6
optimized_prog = simba.compile(generator, trainset=trainset)

optimized_prog.save("cache-simba.json")
