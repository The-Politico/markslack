![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# markslack

A simple Slack message to Markdown converter. Handles text emphasis, hyperlinks, emoji, custom markup and more.

At POLITICO, we use markslack to translate messages pulled from Slack's API into Markdown.

### Quickstart

```
$ pip install markslack
```

```python
from markslack import MarkSlack

marker = MarkSlack()

marker.mark('*Hello* world :thumbsup: :slightly_smiling_face:!')

# '**Hello** world 👍 🙂!'

```

### Emoji

Emoji support is provided by the [emoji](https://pypi.python.org/pypi/emoji/) package.

Not all Slack emoji are supported.

### Images

Images are replaced by matching against a link's file extension.

```python
image_extensions = ['.jpg', '.png']  # default extensions

marker = MarkSlack(
  image_extensions=image_extensions
)

marker.mark('<http://images.com/image.jpg>')

# ![](http://images.com/image.jpg)
```

### Named links

We provide a custom markup syntax for creating named links directly in Slack messages. Bracket a link name directly preceding a URL to create a named link in Markdown.

```python
# In Slack, format a named link in a message like this:
# [POLITICO home]https://www.politico.com

marker = MarkSlack()

marker.mark('[POLITICO home]<https://www.politico.com>')

# [POLITICO home](https://www.politico.com)


# Turn off this syntax
marker = MarkSlack(slackmark_links=False)
```


### Using templates

You can provide custom templates to replace images, user mentions and unnamed links with your own custom markup.

#### Image template

Provide a positional Python formatting string as a template.

```python
image_template = '<figure><img href="{}" class="myclass"/></figure>'

marker = MarkSlack(
  image_template=image_template
)

marker.mark('<http://images.com/image.jpg>')

# <figure><img href="http://images.com/image.jpg" class="myclass"/></figure>
```

#### User templates

Provide user templates as a dictionary keyed by a Slack user ID.

```python
user_templates = {
    'someuserid': '<a href="http://user.com">Some User</a>'
}

marker = MarkSlack(user_templates=user_templates)

marker.mark('<@someuserid>')

# <a href="http://user.com">Some User</a>

# Fallback for undefined
marker.mark('<@someotheruserid>')

# @someotheruserid
```

#### Link templates

Provide templates to render custom markup for unnamed links as a dictionary keyed by a string found in the link, for example, a domain name. As a value, provide a positional Python formatting string to use as a template.

```python
link_templates = {
    'twitter.com': '<blockquote class="twitter-tweet" data-lang="en"><a href="{}"></a></blockquote>',
}

marker = MarkSlack(link_templates=link_templates)

marker.mark('<https://twitter.com/jack/status/20>')

# <blockquote class="twitter-tweet" data-lang="en">
# <a href="https://twitter.com/jack/status/20"></a>
# </blockquote>
```

### Testing

Testing is done using [pytest](https://docs.pytest.org/en/latest/). To run tests, run pytest.

```
$ pytest
```
