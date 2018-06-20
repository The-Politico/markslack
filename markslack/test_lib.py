from markslack import MarkSlack

marker = MarkSlack()


def test_unformatted_string():
    assert marker.mark('test') == 'test'


def test_emoji():
    assert marker.mark(
        '... :thumbsup: test :slightly_smiling_face: ...'
    ) == '... 👍 test 🙂 ...'

    assert marker.mark(
        '... :thumbsup: test :fake_emoji: ...'
    ) == '... 👍 test :fake_emoji: ...'


def test_channel():
    assert marker.mark('test <#channelid|channel-name> test') == \
        'test #channel-name test'


def test_announcement():
    assert marker.mark('... <!here> ...') == (
        '... <span class="slack-announcement">@here</span> ...')
    assert marker.mark('<!channel> ...') == (
        '<span class="slack-announcement">@channel</span> ...')


def test_named_hyperlink():
    assert marker.mark(
        '... <http://site.com|site> ...'
    ) == '... [site](http://site.com) ...'


def test_bracket_named_hyperlink():
    assert marker.mark(
        '... [a named link]<http://site.com> ...'
    ) == '... [a named link](http://site.com) ...'
    assert marker.mark(
        '... [a named link in\'t]<http://site.com> ...'
    ) == '... [a named link in\'t](http://site.com) ...'


def test_unnamed_hyperlink():
    assert marker.mark(
        '... <http://site.com> ...'
    ) == '... [http://site.com](http://site.com) ...'


def test_unnamed_hyperlink_with_template():
    tweet_template = (
        '<blockquote class="twitter-tweet" data-lang="en">'
        '<a href="{}"></a></blockquote>'
    )

    link_templates = {
        'twitter.com': tweet_template,
    }
    marker = MarkSlack(link_templates=link_templates)
    assert marker.mark(
        '... <https://twitter.com/jack/status/20> ...'
    ) == (
        '... <blockquote class="twitter-tweet" data-lang="en">'
        '<a href="https://twitter.com/jack/status/20"></a>'
        '</blockquote> ...'
    )


def test_emphasis():
    assert marker.mark(
        'a *test* \*of\* *bolding a string* and *extra'
    ) == 'a **test** \*of\* **bolding a string** and \*extra'

    assert marker.mark(
        'does* not* *bold'
    ) == 'does\* not\* \*bold'

    assert marker.mark(
        'another* test* *of* *bold'
    ) == 'another\* test\* **of** \*bold'

    assert marker.mark(
        'another* test* *of* *bold\n*and newline*'
    ) == 'another\* test\* **of** \*bold\n**and newline**'

    assert marker.mark(
        '* spaced* asterisk* \n*newline'
    ) == '** spaced** asterisk\* \n\*newline'

    assert marker.mark(
        'a _test_ of _italicizing a string_ and _extra'
    ) == 'a *test* of *italicizing a string* and \_extra'

    assert marker.mark(
        'does_ not_ _italicize'
    ) == 'does\_ not\_ \_italicize'

    assert marker.mark(
        '*a *bold* and_ an _italic_'
    ) == '**a \*bold** and\_ an *italic*'

    assert marker.mark(
        '*a *bold* and _an _italic_'
    ) == '**a \*bold** and *an \_italic*'


def test_strikethrough():
    assert marker.mark(
        'a ~test~ of ~striking a string~ and ~extra'
    ) == 'a ~~test~~ of ~~striking a string~~ and ~extra'

    assert marker.mark(
        'does~ not~ ~strikethrough'
    ) == 'does~ not~ ~strikethrough'


def test_bullet():
    assert marker.mark(
        '... • test • ...'
    ) == '... + test + ...'


def test_user_with_template():
    user_templates = {
        'someusercode': '<a href="http://user.com">Some User</a>'
    }
    marker = MarkSlack(user_templates=user_templates)
    assert marker.mark(
        '... <@someusercode> ...'
    ) == '... <a href="http://user.com">Some User</a> ...'


def test_user_without_map():
    assert marker.mark(
        '... <@someusercode> ...'
    ) == '... @someusercode ...'


def test_image():
    assert marker.mark(
        '... <http://images.com/image.jpg> ...'
    ) == '... ![](http://images.com/image.jpg) ...'


def test_image_with_template():
    marker = MarkSlack(
        image_template='<figure><img href="{}" class="myclass"/></figure>'
    )
    assert marker.mark(
        '... <http://images.com/image.jpg> ...'
    ) == (
        '... <figure><img href="http://images.com/image.jpg"'
        ' class="myclass"/></figure> ...'
    )


def test_underscore_in_url():
    assert marker.mark(
        '... <http://images.com/my_image.jpg> ...'
    ) == (
        '... ![](http://images.com/my_image.jpg) ...'
    )
    assert marker.mark(
        '... <http://site.com/my_thing/> ...'
    ) == (
        '... [http://site.com/my_thing/](http://site.com/my_thing/) ...'
    )


def test_complex():
    user_templates = {
        'someuser': '<a href="http://someone.com">Some One</a>'
    }
    link_templates = {
        'twitter.com': (
            '<blockquote class="twitter-tweet" data-lang="en">'
            '<a href="{}"></a></blockquote>'
        ),
    }
    image_template = '<figure><img href="{}"/></figure>'

    marker = MarkSlack(
        user_templates=user_templates,
        link_templates=link_templates,
        image_template=image_template
    )

    assert marker.mark(
        (
            'this is a test of *bold* and _italic_ *text\n'
            'and a _named link to <https://www.politico.com|POLITICO> '
            'and a (:crying_cat_face:) in parens and a :japanese_ogre:\n'
            'and a tweet <https://www.twitter.com/tweet/123> '
            'and a [named link]<https://www.politico.com>.\n'
            'Strike ~this~ through ~and another *bold* for measure '
            'and an image <https://images.com/pic.jpg>. '
            'And a channel <#channelid|channel-name>. '
            '\n• Test\n+ A list item\n•And spaced.'
            '\n--<@someuser>'
        )
    ) == (
        'this is a test of **bold** and *italic* \*text\n'
        'and a \_named link to [POLITICO](https://www.politico.com) '
        'and a (😿) in parens and a 👹\n'
        'and a tweet <blockquote class="twitter-tweet" data-lang="en">'
        '<a href="https://www.twitter.com/tweet/123"></a></blockquote> '
        'and a [named link](https://www.politico.com).\n'
        'Strike ~~this~~ through ~and another **bold** for measure '
        'and an image '
        '<figure><img href="https://images.com/pic.jpg"/></figure>. '
        'And a channel #channel-name. '
        '\n+ Test\n+ A list item\n+ And spaced.'
        '\n--<a href="http://someone.com">Some One</a>'
    )


def test_no_replace_emoji():
    marker = MarkSlack(replace_emoji=False)
    
    assert marker.mark(
        'this is a test of emoji being left alone :cry:.'
    ) == 'this is a test of emoji being left alone :cry:.'


def test_remove_no_replace_emoji():
    marker = MarkSlack(replace_emoji=False, remove_bad_emoji=True)

    assert marker.mark(
        'this is a test of :fake_emoji: and real emoji being removed :cry:.'
    ) == 'this is a test of and real emoji being removed.'

    assert marker.mark(
        ':fake_emoji: should be gone.'
    ) == 'should be gone.'
    assert marker.mark(
        'white :fake_emoji: space should be preserved :fake_emoji:.'
    ) == 'white space should be preserved.'


def test_remove_and_replace_emoji():
    marker = MarkSlack(remove_bad_emoji=True)

    assert marker.mark(
        'this is a test of only :fake_emoji: being removed :thumbsup:'
    ) == 'this is a test of only being removed 👍'
