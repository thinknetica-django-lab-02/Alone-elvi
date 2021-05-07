import logging
import re

from user_agents import parse

from django.http import HttpRequest

logger = logging.getLogger(__name__)


class MobileAgentCheckingMiddleware:
    """
    Класс призванный определить используется ли мобильный агент.
    """

    def __init__(self, get_response: HttpRequest):
        self._get_response = get_response

    def __call__(self, request: HttpRequest):
        user_agent = parse(request.META['HTTP_USER_AGENT'])
        request.mobile_version = user_agent.is_mobile
        response = self._get_response(request)
        return response
