from markslack import MarkSlack

marker = MarkSlack()


def test_unformatted_string():
    assert marker.mark('test') == 'test'


def test_emoji():
    assert marker.mark(
        '... :thumbsup: test :slightly_smiling_face: ...'
    ) == '... 👍 test 🙂 ...'


def test_channel():
    assert marker.mark('test <#channelid|channel-name> test') == \
        'test #channel-name test'


def test_named_hyperlink():
    assert marker.mark(
        '... <http://site.com|site> ...'
    ) == '... [site](http://site.com) ...'


def test_bracket_named_hyperlink():
    assert marker.mark(
        '... [a named link]<http://site.com> ...'
    ) == '... [a named link](http://site.com) ...'


def test_unnamed_hyperlink():
    assert marker.mark(
        '... <http://site.com> ...'
    ) == '... [http://site.com](http://site.com) ...'


def test_bold():
    assert marker.mark(
        'a *test* of *bolding a string* and *extra'
    ) == 'a **test** of **bolding a string** and *extra'


def test_italic():
    assert marker.mark(
        'a _test_ of _italicizing a string_ and _extra'
    ) == 'a *test* of *italicizing a string* and _extra'


def test_strikethrough():
    assert marker.mark(
        'a ~test~ of ~striking a string~ and ~extra'
    ) == 'a ~~test~~ of ~~striking a string~~ and ~extra'


def test_bullet():
    assert marker.mark(
        '... • test • ...'
    ) == '... + test + ...'


def test_user_with_map():
    user_map = {
        'someusercode': '<a href="http://user.com">Some User</a>'
    }
    marker = MarkSlack(user_map)
    assert marker.mark(
        '... <@someusercode> ...'
    ) == '... <a href="http://user.com">Some User</a> ...'


def test_user_without_map():
    assert marker.mark(
        '... <@someusercode> ...'
    ) == '... @someusercode ...'
