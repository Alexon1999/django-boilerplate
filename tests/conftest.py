from datetime import datetime

import pytest
from django.utils import timezone


@pytest.fixture(autouse=True)
def mock_timezone_now(monkeypatch):
    class MockedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return timezone.make_aware(datetime(2023, 7, 7, 9, 0, 0, tzinfo=tz))

    monkeypatch.setattr('django.utils.timezone.now',
                        MockedDatetime.now)
