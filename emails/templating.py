from enum import Enum

from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags


class TemplateEmailEnum(Enum):
    """Description and Email Template Name."""

    NEW_POST = "new_post"


class TemplateEmail:
    def __init__(
        self,
        to,
        subject,
        template,
        context=None,
        from_email=None,
        reply_to=None,
        **email_kwargs,
    ):
        self.to = to
        self.subject = subject
        self.template = template
        self.context = context or {}
        self.from_email = from_email
        self.reply_to = reply_to
        self.email_kwargs = email_kwargs

    def render_template(self):
        return get_template(self.get_html_template_name()).render(self.context)

    def get_html_template_name(self):
        return f"email/{self.template}.html"

    def send(self):
        html_message = self.render_template()
        plain_message = strip_tags(html_message)
        send_mail(
            self.subject,
            plain_message,
            self.from_email,
            self.to,
            html_message=html_message,
            fail_silently=False,
            **self.email_kwargs,
        )
