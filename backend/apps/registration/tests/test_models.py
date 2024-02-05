from django.template.defaultfilters import slugify
from django.test import TestCase

from apps.registration.factories import UserProfileFactory
from apps.registration.models import Interest


class InterestTestCase(TestCase):
    def setUp(self):
        self.interest = Interest.objects.create(name="Interest")

    def test_interest_slug_filled(self):
        """Test slug field will be automatically be added"""
        self.assertEqual(self.interest.slug, slugify(self.interest.name))

    def test_interest_str(self):
        self.assertEqual(self.interest.__str__(), str(self.interest))


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.profile = UserProfileFactory()

    def test_user_profile_str(self):
        self.assertEqual(self.profile.__str__(), str(self.profile))
