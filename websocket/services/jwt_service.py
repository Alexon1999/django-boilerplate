import logging

import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger("django")


class JWTService:
    @staticmethod
    @database_sync_to_async
    def get_user_from_token(token):
        """
        Decode JWT and return user instance.

        Args:
            token (str): The JWT token.

        Returns:
            user (User instance): The user associated with the token.
        """
        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Return the user using the user_id from the payload
            return get_user_model().objects.get(id=payload["user_id"])

        except Exception as e:
            logger.error("Token is invalid: %s", str(e))
            return None
