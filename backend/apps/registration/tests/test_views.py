from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.registration.factories import (
    InterestFactory,
    UserProfileFactory,
)
from apps.registration.models import (
    Interest,
    UserProfile,
)


class TestInterestsViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="user", password="pass")
        self.interest = InterestFactory()
        self.url = reverse("interests-list")

    def test_list_interest(self):
        """
        Test listing all interests
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Interest.objects.count(), 1)
        data = response.json()
        self.assertEqual(data[0]["id"], self.interest.id)
        self.assertEqual(data[0]["name"], self.interest.name)

    def test_list_interest_not_loggedin(self):
        """
        Test requesting list interests without logged in user
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUserViewSet(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username="user1", password="pass")
        self.user = User.objects.create_user(username="user2", password="pass")

    def test_user_login(self):
        """
        Test for user login
        """
        url = reverse("users-login")
        response = self.client.post(url, {"username": "user2", "password": "pass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], self.user.id)
        self.assertEqual(data["first_name"], self.user.first_name)
        self.assertEqual(data["last_name"], self.user.last_name)
        self.assertEqual(data["birth_date"], None)
        self.assertEqual(data["gender"], None)
        self.assertFalse(data["completed_welcome"])

    def test_user_login_not_found(self):
        """
        Test login for user not found
        """
        url = reverse("users-login")
        response = self.client.post(url, {"username": "notfound", "password": "pass"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_register(self):
        """
        Test register new user
        """
        url = reverse("users-list")
        response = self.client.post(url, {"username": "newuser", "password": "pass", "password2": "pass"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["username"], "newuser")

    def test_user_register_mismatch_password(self):
        """
        Test register new user with mismatched password
        """
        url = reverse("users-list")
        response = self.client.post(url, {"username": "newuser", "password": "pass", "password2": "mismatch"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(data, ["Passwords do not match"])

    def test_user_register_existing_username(self):
        """
        Test register new user with existing username
        """
        url = reverse("users-list")
        response = self.client.post(url, {"username": "user2", "password": "pass", "password2": "pass"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(data["username"], ["A user with that username already exists."])

    def test_session_unauthenticated(self):
        """
        Test get session with unauthenticated user
        """
        url = reverse("users-session")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertFalse(data["is_authenticated"])

    def test_session_authenticated(self):
        """
        Test get session with unauthenticated user
        """
        self.client.force_login(self.user)
        url = reverse("users-session")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data["is_authenticated"])
        self.assertEqual(data["user_id"], self.user.id)

    def test_logout_unauthenticated(self):
        """
        Test logout with unauthenticated user
        """
        url = reverse("users-logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logout_authenticated(self):
        """
        Test logout with authenticated user
        """
        self.client.force_login(self.user)
        url = reverse("users-logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_user(self):
        """
        Test update user details
        """
        self.client.force_login(self.user)
        url = reverse("users-detail", kwargs={"pk": self.user.id})
        birth_date = timezone.now().date()
        response = self.client.put(
            url, {"first_name": "John", "last_name": "Doe", "birth_date": birth_date, "gender": UserProfile.MALE}
        )
        data = response.json()
        self.user.refresh_from_db()
        profile = self.user.profile
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["first_name"], self.user.first_name)
        self.assertEqual(data["last_name"], self.user.last_name)
        self.assertEqual(data["birth_date"], profile.birth_date.strftime("%Y-%m-%d"))
        self.assertEqual(data["gender"], profile.gender)
        self.assertEqual(data["completed_welcome"], profile.completed_welcome)

    def test_put_user_existing_profile(self):
        """
        Test update user details with existing user profile
        """
        profile = UserProfileFactory(user=self.user)
        self.client.force_login(self.user)
        url = reverse("users-detail", kwargs={"pk": self.user.id})
        birth_date = timezone.now().date()
        response = self.client.put(
            url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": birth_date,
                "gender": UserProfile.FEMALE,
            },
        )
        data = response.json()
        self.user.refresh_from_db()
        profile = self.user.profile
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["birth_date"], profile.birth_date.strftime("%Y-%m-%d"))
        self.assertEqual(data["gender"], UserProfile.FEMALE)
        self.assertFalse(data["completed_welcome"])

    def test_put_user_not_self(self):
        """
        Test update user details with different user
        """
        self.client.force_login(self.user)
        url = reverse("users-detail", kwargs={"pk": self.superuser.id})
        birth_date = timezone.now().date()
        response = self.client.put(
            url, {"first_name": "John", "last_name": "Doe", "birth_date": birth_date, "gender": UserProfile.MALE}
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data["detail"], "Not allowed to access other users")

    def test_get_user_detail(self):
        """
        Test get user details
        """
        self.client.force_login(self.user)
        url = reverse("users-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["first_name"], self.user.first_name)
        self.assertEqual(data["last_name"], self.user.last_name)
        self.assertIsNone(data["birth_date"])
        self.assertIsNone(data["gender"])
        self.assertIsNone(data["completed_welcome"])

    def test_get_user_detail_not_self(self):
        """
        Test get user details for different user
        """
        self.client.force_login(self.user)
        url = reverse("users-detail", kwargs={"pk": self.superuser.id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data["detail"], "Not allowed to access other users")

    def test_list_not_allowed(self):
        """
        Test list users not allowed
        """
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.json()
        self.assertEqual(data["detail"], 'Method "GET" not allowed without lookup')


class TestUserProfileViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.profile = UserProfileFactory(user=self.user)

    def test_list_not_allowed(self):
        """
        Test list profile not allowed
        """
        self.client.force_login(self.user)
        url = reverse("userprofiles-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.json()
        self.assertEqual(data["detail"], 'Method "GET" not allowed without lookup')

    def test_unauthenticated_user(self):
        """
        Test list profile not allowed for unauthenticated user
        """
        url = reverse("userprofiles-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        data = response.json()
        self.assertEqual(data["detail"], "Authentication credentials were not provided.")

    def test_get_userprofile(self):
        """
        Test get userprofile detail
        """
        self.client.force_login(self.user)
        url = reverse("userprofiles-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["experience_level"], self.profile.experience_level)
        self.assertEqual(data["expected_salary"], str(self.profile.expected_salary))

    def test_get_userprofile_not_self(self):
        """
        Test get user profile detail not own user
        """
        self.client.force_login(self.user)
        url = reverse("userprofiles-detail", kwargs={"pk": self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUserInterestsViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.profile = UserProfileFactory(user=self.user)
        self.interest1 = InterestFactory()
        self.interest2 = InterestFactory()

    def test_list_not_allowed(self):
        """
        Test list users interests not allowed
        """
        self.client.force_login(self.user)
        url = reverse("user-interests-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.json()
        self.assertEqual(data["detail"], 'Method "GET" not allowed without lookup')

    def test_unauthenticated_user(self):
        """
        Test list users interests not allowed for unauthenticated user
        """
        url = reverse("user-interests-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        data = response.json()
        self.assertEqual(data["detail"], "Authentication credentials were not provided.")

    def test_get_userinterests_not_self(self):
        """
        Test get user interests detail not own user
        """
        self.client.force_login(self.user)
        url = reverse("user-interests-detail", kwargs={"pk": self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_userinterests(self):
        """
        Test get user interests detail
        """
        self.client.force_login(self.user)
        self.user.interests.add(self.interest1)
        url = reverse("user-interests-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["interests"], [{"id": self.interest1.id, "name": self.interest1.name}])

    def test_put_userinterests(self):
        """
        Test put user interests
        """
        self.client.force_login(self.user)
        url = reverse("user-interests-detail", kwargs={"pk": self.user.id})
        response = self.client.put(url, {"interests": [self.interest2.id]})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["interests"], [2])
