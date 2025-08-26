import os
import sys
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY")
)

if len(sys.argv) < 2:
    print("Usage: {} task".format(sys.argv[0],))
    sys.exit()

target = open("targ.rapira")
task   = open(sys.argv[1])

messages=[
        {
            "role": "system",
            "content": target.read()
        },
        {
            "role": "system",
            "content": """
Use lowercase for keywords.
For comments use an initial backslash instead of `(*` and `*)`.
If you get an error for for loops,
instead of `::` and `всё` use `цикл` and `кц`.
Do not use the `?` shortcut.
            """
        },
        {
            "role": "user",
            "content": task.read()
        }
]

def prompt(msgs):
    stream = client.chat.completions.create(
        messages=msgs,
        model="qwen-3-coder-480b",
        stream=False,
        max_completion_tokens=40000,
        temperature=0.7,
        top_p=0.8
    )
    return stream.choices[0].message.content

for n in range(10):
    print("Shot: "+str(n))
    ans = prompt(messages)
    print(ans)

    f=open("y.rap","w")
    f.write(ans)
    f.close()

    r = os.system("./rap y.rap")
    print(r)
    if r==0:
        sys.exit(0)

    f=open("a.err")
    err=f.read()
    f.close()

    messages[2]["content"] = """
Given the program
```
""" + ans + """
```

and the error

```
""" + err + """
```

can you please write a revised program?
"""

messages[2]["content"] = open(sys.argv[1]).read()
messages[2]["content"] += """
Try to write the program in a functional style.
"""

for n in range(10,20):
    print("Shot: "+str(n))
    ans = prompt(messages)
    print(ans)

    f=open("y.rap","w")
    f.write(ans)
    f.close()

    r = os.system("./rap y.rap")
    print(r)
    if r==0:
        sys.exit(0)

    f=open("a.err")
    err=f.read()
    f.close()

    messages[2]["content"] = """
Given the program
```
""" + ans + """
```

and the error

```
""" + err + """
```

can you please write a revised program?
"""

