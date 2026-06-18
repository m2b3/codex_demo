---
name: my-skill
description: Echo short text in uppercase. Use when the user explicitly asks for my-skill, shout-back, uppercase echo, or a simple skill test.
---

Use this skill as a small, deterministic echoing of user input

When invoked:

1. Identify the text the user wants converted to uppercase.
2. If the user says exactly `stop` or `quit`, respond with `Stopped.` and do not run the script.
3. Otherwise, run `/usr/bin/python3 scripts/shout.py` with the user's text as arguments from this skill directory.
4. Return the script output exactly.

Example:

```text
Use $my-skill on: hello user
```

Expected output:

```text
HELLO USER
```
