from dspy import datasets
from dspy.datasets import *

trainset = [x.with_inputs('question') for x in HotPotQA(train_seed=2024, train_size=5).train]

print(trainset)
