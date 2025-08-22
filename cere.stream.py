import os
import sys
import time
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY")
)

if len(sys.argv) < 3:
    print("Usage: {} target task".format(sys.argv[0],))
    sys.exit()

target = open(sys.argv[1])
task   = open(sys.argv[2])

tare = time.time()

stream = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": target.read()
        },
        {
            "role": "user",
            "content": task.read()
        }
    ],
    model="qwen-3-coder-480b",
    stream=True,
    max_completion_tokens=40000,
    temperature=0.7,
    top_p=0.8
)

for chunk in stream:
  print(time.time()-tare)
  print(chunk.choices[0].delta.content or "", end="")
