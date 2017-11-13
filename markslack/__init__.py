import re
import emoji

url_pattern = (
    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
    '|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)


class MarkSlack(object):
    def __init__(self, user_map=None, bracket_link_names=True):
        self.user_map = user_map
        self.bracket_link_names = bracket_link_names

    def mark_emoji(self):
        self.marked = emoji.emojize(self.marked, use_aliases=True)

    def mark_channel(self):
        self.marked = re.sub(
            r'<#[^\|]*\|(.*)>', r'#\1', self.marked)

    def mark_hyperlink(self):
        # slack named hyperlinks
        self.marked = re.sub(
            '<({})\|([^\|]*)>'.format(url_pattern), r'[\2](\1)', self.marked)
        # A markdown-like syntax for named hyperlinks
        # [my name]<http://...>
        if self.bracket_link_names:
            self.marked = re.sub(
                '\[([a-zA-Z ]+)\]<({})>'.format(url_pattern),
                r'[\1](\2)', self.marked)
        # unnamed hyperlinks
        self.marked = re.sub(
            '<({})>'.format(url_pattern), r'[\1](\1)', self.marked)

    def mark_bold(self):
        self.marked = re.sub(
            r'\*(.+?)\*', r'**\1**', self.marked)

    def mark_italic(self):
        self.marked = re.sub(
            r'_(.+?)_', r'*\1*', self.marked)

    def mark_strikethrough(self):
        self.marked = re.sub(
            r'~(.+?)~', r'~~\1~~', self.marked)

    def mark_bullet(self):
        self.marked = re.sub(r'•', '+', self.marked)

    def mark_user(self):
        def sub_user(match):
            return self.user_map[match.group(1)]

        if self.user_map:
            self.marked = re.sub(
                r'<@(.+?)>', sub_user, self.marked)
        else:
            self.marked = re.sub(
                r'<(@.+?)>', r'\1', self.marked)

    def mark(self, slack):
        self.slack = slack
        self.marked = slack
        self.mark_emoji()
        self.mark_channel()
        self.mark_hyperlink()
        self.mark_bold()
        self.mark_italic()
        self.mark_strikethrough()
        self.mark_bullet()
        self.mark_user()
        return self.marked
