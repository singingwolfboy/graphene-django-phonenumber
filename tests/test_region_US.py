import json
import pytest
from django.contrib.auth.models import User
from phonenumber_field.phonenumber import PhoneNumber
from .models import UserProfile

pytestmark = [pytest.mark.national, pytest.mark.region_US]


@pytest.fixture(autouse=True)
def seed_data(transactional_db):
    u1 = User.objects.create(username="jenny", first_name="Jenny")
    u1.profile.phone_number = PhoneNumber.from_string("9998675309")
    u1.profile.save()
    u2 = User.objects.create(
        username="callmemaybe", first_name="Taylor", last_name="Swift"
    )
    u2.profile.phone_number = PhoneNumber.from_string("9921547733")
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
                "profile": {"phoneNumber": "(999) 867-5309"},
            },
            {
                "username": "callmemaybe",
                "firstName": "Taylor",
                "profile": {"phoneNumber": "(992) 154-7733"},
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
            "user": {"username": "alice", "profile": {"phoneNumber": "(212) 555-2368"}},
            "errors": [],
        }
    }
    assert User.objects.count() == 3
    user = User.objects.last()
    assert user.username == "alice"
    assert user.profile.phone_number == PhoneNumber.from_string("2125552368")


def test_introspection(client_query):
    response = client_query(
        """
        query {
            upType: __type(name: "UserProfileType") {
                fields {
                    name
                    type {
                        ofType {
                            name
                        }
                    }
                }
            }
            pnType: __type(name: "USPhoneNumber") {
                name
                kind
                description
            }
        }
        """,
    )

    content = json.loads(response.content)
    assert "errors" not in content
    assert content["data"] == {
        "upType": {
            "fields": [
                {"name": "id", "type": {"ofType": {"name": "ID"}}},
                {"name": "user", "type": {"ofType": {"name": "UserType"}}},
                {"name": "phoneNumber", "type": {"ofType": {"name": "USPhoneNumber"}}},
            ]
        },
        "pnType": {
            "name": "USPhoneNumber",
            "kind": "SCALAR",
            "description": "A national phone number, specific to the US region.",
        },
    }
