![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# markslack

A simple Slack message to Markdown converter. Handles all text emphasis, emoji, hyperlinks and more.

### Quickstart

```
$ pip install markslack
```

```python
from markslack import MarkSlack

marker = MarkSlack()

marker.mark('Hello world :thumbsup: :slightly_smiling_face:!')

# 'Hello world 👍 🙂!'

```
