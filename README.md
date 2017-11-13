![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# markslack

A simple Slack message to Markdown converter. Handles text emphasis, hyperlinks, emoji and more.

At POLITICO, we use markslack to translate messages gathered from Slack's API to Markdown.

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
