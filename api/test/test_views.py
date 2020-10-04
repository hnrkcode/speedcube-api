from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import UserModel


class TestRegisterView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        UserModel.objects.create(
            username="user1", email="test@mail.com", password="testpassword"
        )

    def test_create_account_successfully(self):
        """Ensure we can create a new account object."""

        url = reverse("register")
        data = {"username": "user2", "password": "12345678", "confirmation": "12345678"}
        response = self.client.post(url, data, format="json")
        expected_response = {"success": True, "message": "User created."}

        self.assertDictEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_username_already_taken(self):
        """Ensure new user can't register if the choosen username is already taken."""

        url = reverse("register")
        data = {"username": "user1", "password": "12345678", "confirmation": "12345678"}
        response = self.client.post(url, data, format="json")
        expected_response = {"success": False, "message": "Username already taken."}

        self.assertDictEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_too_short_password(self):
        """Ensure the password is long enough."""

        url = reverse("register")
        data = {"username": "user2", "password": "123", "confirmation": "123"}
        response = self.client.post(url, data, format="json")
        expected_response = {
            "success": False,
            "message": "The password must be at least 8 characters long.",
        }

        self.assertDictEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_username_entered(self):
        """Ensure the user has entered a username."""

        url = reverse("register")
        data = {"username": "", "password": "12345678", "confirmation": "12345678"}
        response = self.client.post(url, data, format="json")
        expected_response = {
            "success": False,
            "message": "Please enter a username.",
        }

        self.assertDictEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_missing_user_attribute(self):
        """Check that all necessary attributes are sent to the server."""

        url = reverse("register")
        missing_username_response = self.client.post(
            url, {"password": "12345678", "confirmation": "12345678"}, format="json"
        )
        missing_password_response = self.client.post(
            url, {"username": "test", "confirmation": "12345678"}, format="json"
        )
        missing_confirmation_response = self.client.post(
            url, {"username": "test", "password": "12345678"}, format="json"
        )
        expected_response = {
            "success": False,
            "message": "Missing user attribute.",
        }

        self.assertDictEqual(missing_username_response.data, expected_response)
        self.assertEqual(missing_username_response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(missing_password_response.data, expected_response)
        self.assertEqual(missing_password_response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(missing_confirmation_response.data, expected_response)
        self.assertEqual(missing_confirmation_response.status_code, status.HTTP_200_OK)

    def test_requests(self):
        url = reverse("register")

        get_response = self.client.get(url)
        post_response = self.client.post(url)
        put_response = self.client.put(url)
        patch_response = self.client.patch(url)
        delete_response = self.client.delete(url)
        head_response = self.client.head(url)
        options_response = self.client.options(url)

        self.assertEqual(post_response.status_code, status.HTTP_200_OK)
        self.assertEqual(options_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(head_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
