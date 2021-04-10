import json
import pytest
from django.contrib.auth.models import User
from .models import UserProfile


@pytest.fixture(autouse=True)
def seed_data(transactional_db):
    u1 = User.objects.create(username="jenny")
    p1 = UserProfile.objects.create(
        user=u1, name="Jenny", phone_number="+1 999 8675309"
    )
    u2 = User.objects.create(username="callmemaybe")
    p2 = UserProfile.objects.create(
        user=u2, name="Taylor", phone_number="+31 9921547733"
    )


def test_basic_phone(client_query):
    response = client_query(
        """
        query {
            users {
                username
                profile {
                    name
                    phoneNumber
                }
            }
        }
        """,
    )

    content = json.loads(response.content)
    assert "errors" not in content
    assert content["data"] == {
        "users": [
            {
                "username": "jenny",
                "profile": {"name": "Jenny", "phoneNumber": "+19998675309"},
            },
            {
                "username": "callmemaybe",
                "profile": {"name": "Taylor", "phoneNumber": "+319921547733"},
            },
        ]
    }
