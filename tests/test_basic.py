import json
import pytest
from django.contrib.auth.models import User
from phonenumber_field.phonenumber import PhoneNumber
from .models import UserProfile


@pytest.fixture(autouse=True)
def seed_data(transactional_db):
    u1 = User.objects.create(username="jenny", first_name="Jenny")
    u1.profile.phone_number = PhoneNumber.from_string("+1 999 8675309")
    u1.profile.save()
    u2 = User.objects.create(
        username="callmemaybe", first_name="Taylor", last_name="Swift"
    )
    u2.profile.phone_number = PhoneNumber.from_string("+31 9921547733")
    u2.profile.save()


def test_basic_read(client_query):
    response = client_query(
        """
        query {
            users {
                username
                firstName
                profile {
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
                "firstName": "Jenny",
                "profile": {"phoneNumber": "+19998675309"},
            },
            {
                "username": "callmemaybe",
                "firstName": "Taylor",
                "profile": {"phoneNumber": "+319921547733"},
            },
        ]
    }


def test_basic_write(client_query):
    response = client_query(
        """
        mutation CreateUser {
            createUser(input: { username: "alice", password: "alicepw", phoneNumber: "+1 2125552368"}) {
                user {
                    username
                    profile {
                        phoneNumber
                    }
                }
                errors {
                    field
                    messages
                }
            }
        }
        """,
    )

    content = json.loads(response.content)
    assert "errors" not in content
    assert content["data"] == {
        "createUser": {
            "user": {
                "username": "alice",
                "profile": {"phoneNumber": "+12125552368"},
            },
            "errors": [],
        }
    }
    assert User.objects.count() == 3
    user = User.objects.last()
    assert user.username == "alice"
    assert user.profile.phone_number == PhoneNumber.from_string("+12125552368")


def test_no_country_code(client_query):
    response = client_query(
        """
        mutation CreateUser {
            createUser(input: { username: "alice", password: "alicepw", phoneNumber: "2125552368"}) {
                user {
                    username
                    profile {
                        phoneNumber
                    }
                }
                errors {
                    field
                    messages
                }
            }
        }
        """,
    )

    content = json.loads(response.content)
    assert "errors" not in content
    assert content["data"] == {
        "createUser": {
            "errors": [
                {
                    "field": "phoneNumber",
                    "messages": ["Enter a valid phone number (e.g. +12125552368)."],
                }
            ],
            "user": None,
        }
    }
    assert User.objects.count() == 2
