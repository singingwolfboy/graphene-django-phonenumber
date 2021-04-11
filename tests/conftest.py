import os
import sys

import pytest
import django
from django.core import management
from phonenumber_field.phonenumber import validate_region


def pytest_addoption(parser):
    parser.addoption("--phone-number-region", help="Test with regional phone numbers")


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
            "secondary": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
        },
        SITE_ID=1,
        SECRET_KEY="not very secret in tests",
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL="/static/",
        ROOT_URLCONF="tests.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "debug": True,  # We want template errors to raise
                },
            },
        ],
        MIDDLEWARE=(
            "django.middleware.common.CommonMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "phonenumber_field",
            "graphene_django",
            "graphene_django_phonenumber",
            "tests",
        ),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        GRAPHENE={"SCHEMA": "tests.schema.schema"},
    )

    region = config.getoption("--phone-number-region")
    if region:
        validate_region(region)
        settings.PHONENUMBER_DB_FORMAT = "NATIONAL"
        settings.PHONENUMBER_DEFAULT_REGION = region

    django.setup()


def pytest_collection_modifyitems(config, items):
    region = config.getoption("--phone-number-region")
    if region:
        reason = "wrong phone number region"
        item_filter = (
            lambda item: "international" in item.keywords
            or f"region_{region}" not in item.keywords
        )
    else:
        reason = "no phone number region provided: skip national tests"
        item_filter = lambda item: "national" in item.keywords

    skip_conflicting = pytest.mark.skip(reason=reason)
    for item in items:
        if item_filter(item):
            item.add_marker(skip_conflicting)


# This uses the `client` fixture from `pytest-django`
@pytest.fixture
def client_query(client):
    # Can't import until we've called `django.setup()` in `pytest_configure`
    from graphene_django.utils.testing import graphql_query

    def graphql_query_with_client(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return graphql_query_with_client