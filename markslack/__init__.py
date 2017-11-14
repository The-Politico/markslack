import re
import os
import emoji

url_pattern = (
    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
    '|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)


class MarkSlack(object):
    def __init__(
        self,
        slackmark_links=True,
        link_templates=None,
        user_templates=None,
        image_template=None,
        image_extensions=['.jpg', '.png'],
    ):
        self.user_templates = user_templates
        self.slackmark_links = slackmark_links
        self.image_extensions = image_extensions
        self.image_template = image_template
        self.link_templates = link_templates

    def mark_emoji(self):
        self.marked = emoji.emojize(self.marked, use_aliases=True)

    def mark_image(self):
        def sub_image(match):
            url = match.group(1)
            extension = os.path.splitext(url)[1]
            if extension.lower() in self.image_extensions:
                if self.image_template:
                    return self.image_template.format(url)
                return '![]({})'.format(url)
            return '<{}>'.format(url)

        self.marked = re.sub(
            '<({})>'.format(url_pattern), sub_image, self.marked)

    def mark_channel(self):
        self.marked = re.sub(
            r'<#[a-zA-Z0-9-]+\|(.+?)>', r'#\1', self.marked)

    def mark_named_hyperlink(self):
        self.marked = re.sub(
            '<({})\|(.+?)>'.format(url_pattern), r'[\2](\1)', self.marked)
        # Slackmark links use a markdown-like syntax
        # to allow users to create named hyperlinks.
        # e.g., [my name]<http://...>
        if self.slackmark_links:
            self.marked = re.sub(
                '\[([\w ]+?)\]<({})>'.format(url_pattern),
                r'[\1](\2)', self.marked)

    def mark_unnamed_hyperlink(self):
        if not self.link_templates:
            self.marked = re.sub(
                '<({})>'.format(url_pattern), r'[\1](\1)', self.marked)
            return

        def sub_link(match):
            link_keys = list(self.link_templates.keys())
            url = match.group(1)
            for key in link_keys:
                if key in url:
                    return self.link_templates[key].format(url)
            return '[{}]({})'.format(url)

        self.marked = re.sub(
            '<({})>'.format(url_pattern), sub_link, self.marked)

    def mark_emphasis(self):
        """
        Mark bold and italic text.

        In order to ensure emphasis marks render the same in Slack and
        Markdown, we need to escape all underscores and asterisks that
        don't belong to a matched pair. To do that, we first mark the
        matched pairs with a placeholder pattern ('|*'), then escape the
        remaining underscores and asterisks. Finally, we replace the
        placeholders with asterisks.
        """
        # Pattern catches matched pairs
        regex = r'(?<![\\|a-zA-Z0-9])\{0}(.+?)(?<!\\)\{0}(?![a-zA-Z0-9])'
        # Replace bold paired asterisks with placeholder
        self.marked = re.sub(regex.format('*'), r'|*|*\1|*|*', self.marked)
        # Replace italic paired underscores with placeholder
        self.marked = re.sub(regex.format('_'), r'|*\1|*', self.marked)

        # Escape unmatched, unescaped asterisks
        self.marked = re.sub(r'(?<![\|\\])\*', '\*', self.marked)
        # Escape unmatched, unescaped underscores
        self.marked = re.sub(r'\_', '\_', self.marked)
        # Replace matched pair placeholders
        self.marked = re.sub(r'\|\*', '*', self.marked)

    def mark_strikethrough(self):
        regex = r'(?<![\\|a-zA-Z0-9])\~(.+?)(?<!\\)\~(?![a-zA-Z0-9])'
        self.marked = re.sub(regex, r'~~\1~~', self.marked)

    def mark_bullet(self):
        # Add whitespace if none
        self.marked = re.sub(r'•([a-zA-Z0-9])', r'+ \1', self.marked)
        # Preserve whitespace
        self.marked = re.sub(r'•(\s)', r'+\1', self.marked)

    def mark_user(self):
        def sub_user(match):
            return self.user_templates.get(
                match.group(1),
                '@{}'.format(match.group(1))
            )

        if self.user_templates:
            self.marked = re.sub(r'<@(.+?)>', sub_user, self.marked)
        else:
            self.marked = re.sub(r'<(@.+?)>', r'\1', self.marked)

    def mark(self, slack):
        self.slack = slack
        self.marked = slack
        self.mark_emoji()
        self.mark_image()
        self.mark_channel()
        self.mark_named_hyperlink()
        self.mark_unnamed_hyperlink()
        self.mark_user()
        self.mark_emphasis()
        self.mark_strikethrough()
        self.mark_bullet()
        return self.marked
