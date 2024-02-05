import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

from apps.registration.models import (
    Interest,
    UserProfile,
)


class InterestFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Interest-{n}")

    class Meta:
        model = Interest
        django_get_or_create = ["name"]


class UserFactory(DjangoModelFactory):

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User
        django_get_or_create = ["username"]


class UserProfileFactory(DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    gender = factory.Faker("random_element", elements=(UserProfile.MALE, UserProfile.FEMALE, UserProfile.OTHER))
    experience_level = factory.Faker(
        "random_element", elements=(UserProfile.ENTRY_LEVEL, UserProfile.MANAGER, UserProfile.OTHER)
    )
    expected_salary = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
    completed_welcome = False

    class Meta:
        model = UserProfile
