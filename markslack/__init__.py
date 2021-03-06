import re
import os
import emoji


url_pattern = (
    r"(?i)\b(?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.]"
    r"[a-z]{2,4}/)(?:[^\s()<>\|]+|\([^\s()<>\|]+|\([^\s()<>\|]+\)*\))+(?:\([^"
    r"""\s()<>\|]+|\([^\s()<>\|]+\)*\)|[^\s`!()\[\]{};:'".,<>\|?«»“”‘’])"""
)


emoji_pattern = u":[a-zA-Z0-9\+\-_&.ô’Åéãíç()!#*]+:"


class MarkSlack(object):
    def __init__(
        self,
        markslack_links=True,
        replace_emoji=True,
        remove_bad_emoji=False,
        link_templates=None,
        user_templates=None,
        image_template=None,
        image_extensions=[".jpg", ".png"],
    ):
        self.user_templates = user_templates
        self.markslack_links = markslack_links
        self.replace_emoji = replace_emoji
        self.remove_bad_emoji = remove_bad_emoji
        self.image_extensions = image_extensions
        self.image_template = image_template
        self.link_templates = link_templates

    def mark_emoji(self):
        if self.replace_emoji:
            self.marked = emoji.emojize(self.marked, use_aliases=True)

        if self.remove_bad_emoji:
            # Emojis at the end of text
            p1 = re.compile(u"(\s*)((?:{0})+)(\s*|\.*)$".format(emoji_pattern))
            self.marked = p1.sub(r"\3", self.marked)

            # Emojis throughout text
            p2 = re.compile(u"(\s*)((?:{0})+)(\s*)".format(emoji_pattern))
            self.marked = p2.sub(r"\1", self.marked)

    def mark_image(self):
        def sub_image(match):
            url = match.group(1)
            extension = os.path.splitext(url)[1]
            if extension.lower() in self.image_extensions:
                if self.image_template:
                    return self.image_template.format(url)
                return "![]({0})".format(url)
            return "<{0}>".format(url)

        regex_ext = "|".join([s[1:] for s in self.image_extensions])
        self.marked = re.sub(
            "<(.*\.(?:{0}))>".format(regex_ext), sub_image, self.marked
        )

    def mark_channel(self):
        self.marked = re.sub(r"<#[a-zA-Z0-9-]+\|(.+?)>", r"#\1", self.marked)

    def mark_announcements(self):
        self.marked = re.sub(
            r"<\!(.+?)>",
            r'<span class="slack-announcement">@\1</span>',
            self.marked,
        )

    def mark_named_hyperlink(self):
        # Wrap All URLs in ~
        self.marked = re.sub(
            "<({0})".format(url_pattern), r"<~\1~", self.marked
        )

        # If a URL name follows a ~-wrapped URL, replace the URL and name
        # with markdown
        self.marked = re.sub("<~([^~]+)~\|(.+)>", r"[\2](\1)", self.marked)

        # If a URL has no name, remove the ~ wraps
        self.marked = re.sub("<~([^~]+)~>", r"<\1>", self.marked)

        # Markslack links use a markdown-like syntax
        # to allow users to create named hyperlinks.
        # e.g., [my name]<http://...>
        if self.markslack_links:
            self.marked = re.sub(
                "\[([\w ']+?)\]<({0})>".format(url_pattern),
                r"[\1](\2)",
                self.marked,
            )

        # Handle Link Templates
        if self.link_templates:

            def sub_link(match):
                link_keys = list(self.link_templates.keys())
                name = match.group(1)
                url = match.group(2)
                for key in link_keys:
                    if key in url:
                        return self.link_templates[key].format(url)
                return "[{0}]({1})".format(name, url)

            self.marked = re.sub(
                "\[(.+)\]\((.+)\)".format(url_pattern), sub_link, self.marked
            )

    def mark_unnamed_hyperlink(self):
        if not self.link_templates:
            self.marked = re.sub(
                "<({0})>".format(url_pattern), r"[\1](\1)", self.marked
            )
            return

        def sub_link(match):
            link_keys = list(self.link_templates.keys())
            url = match.group(1)
            for key in link_keys:
                if key in url:
                    return self.link_templates[key].format(url)
            return "[{0}]({0})".format(url)

        self.marked = re.sub(
            "<({0})>".format(url_pattern), sub_link, self.marked
        )

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
        regex = r"(?<![\\|a-zA-Z0-9])\{0}(.+?)(?<!\\)\{0}(?![a-zA-Z0-9])"
        # Replace bold paired asterisks with placeholder
        self.marked = re.sub(regex.format("*"), r"|*|*\1|*|*", self.marked)
        # Replace italic paired underscores with placeholder
        self.marked = re.sub(regex.format("_"), r"|*\1|*", self.marked)

        # Escape unmatched, unescaped asterisks
        self.marked = re.sub(r"(?<![\|\\])\*", "\*", self.marked)

        self.marked = "".join(
            [
                re.sub(r"\_", "\_", line)
                if not re.search(url_pattern, line)
                and not re.search(emoji_pattern, line)
                else line
                for line in re.split("({0})".format(url_pattern), self.marked)
            ]
        )
        # Replace matched pair placeholders
        self.marked = re.sub(r"\|\*", "*", self.marked)

    def mark_strikethrough(self):
        regex = r"(?<![\\|a-zA-Z0-9])\~(.+?)(?<!\\)\~(?![a-zA-Z0-9])"
        self.marked = re.sub(regex, r"~~\1~~", self.marked)

    def mark_bullet(self):
        # Add whitespace if none
        self.marked = re.sub(r"•([a-zA-Z0-9])", r"+ \1", self.marked)
        # Preserve whitespace
        self.marked = re.sub(r"•(\s)", r"+\1", self.marked)

    def mark_user(self):
        def sub_user(match):
            return self.user_templates.get(
                match.group(1), "@{0}".format(match.group(1))
            )

        if self.user_templates:
            self.marked = re.sub(r"<@(.+?)>", sub_user, self.marked)
        else:
            self.marked = re.sub(r"<(@.+?)>", r"\1", self.marked)

    def mark(self, slack):
        self.slack = slack
        self.marked = slack
        self.mark_emoji()
        self.mark_image()
        self.mark_channel()
        self.mark_announcements()
        self.mark_named_hyperlink()
        self.mark_unnamed_hyperlink()
        self.mark_user()
        self.mark_emphasis()
        self.mark_strikethrough()
        self.mark_bullet()
        return self.marked
