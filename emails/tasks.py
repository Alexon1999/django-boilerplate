import logging
from typing import Any, Dict, List, Optional

from celery import shared_task

from .templating import TemplateEmail, TemplateEmailEnum
from .utils import call_function

logger = logging.getLogger(__name__)


@shared_task
def send_mail(
    to: List[str],
    subject: str,
    template: TemplateEmailEnum,
    context: Optional[Dict[str, Any]] = None,
    post_function_path: Optional[str] = None,
    post_function_args: Optional[List[Any]] = None,
    post_function_kwargs: Optional[Dict[str, Any]] = None,
):
    email = TemplateEmail(to=to, subject=subject, template=template, context=context)
    email.send()

    if post_function_path:
        if post_function_args is None:
            post_function_args = []
        if post_function_kwargs is None:
            post_function_kwargs = {}
        call_function(post_function_path, *post_function_args, **post_function_kwargs)
