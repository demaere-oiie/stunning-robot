import asyncio
import dsconfig
import dspy
import sys

if len(sys.argv) < 3:
    print("Usage: {} target task".format(sys.argv[0],))
    sys.exit()

target = open(sys.argv[1])
task   = open(sys.argv[2])

dspy.configure(lm=dsconfig.lm())

prog = dspy.Predict("target, task-> program")

sprog = dspy.streamify(prog, stream_listeners=[
    dspy.streaming.StreamListener(signature_field_name="program")])

async def readstream():
    output = sprog(target=target.read(), task=task.read())

    rv = None
    async for chunk in output:
        if isinstance(chunk, dspy.Prediction):
            rv = chunk
        else:
            print(chunk)
    return rv

print(asyncio.run(readstream()))
