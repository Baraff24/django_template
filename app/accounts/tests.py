from allauth.account.models import EmailAddress
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .constants import COMPLETE, PENDING_COMPLETE_DATA
from .models import User


class UserFixtureMixin:
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.user.status = COMPLETE
        self.user.save()
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True, primary=True
        )
        self.client = APIClient()


class UserTests(UserFixtureMixin, TestCase):
    def test_users_list_api(self):
        # Ensure that the UsersListAPI view returns
        # a 200 status code when accessed by a superuser
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_api(self):
        # Ensure that the UserDetailAPI view returns
        # a 200 status code when accessed by a superuser
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_profile_api(self):
        # Ensure that the CompleteProfileAPI view updates the user's profile correctly
        self.user.status = PENDING_COMPLETE_DATA
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse("complete-profile")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "telephone": "1234567890",
            "gender": "NONE",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.telephone, "1234567890")
        self.assertEqual(self.user.status, COMPLETE)

    def test_complete_profile_api_already_completed(self):
        # Ensure that the CompleteProfileAPI view returns
        # a 400 status code if the profile is already completed
        self.user.status = COMPLETE
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse("complete-profile")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "telephone": "1234567890",
            "gender": "NONE",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user(self):
        # Ensure that an inactive user cannot access protected views
        self.user.is_active = False
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserModelTests(TestCase):
    def test_user_model_str(self):
        # Ensure that the User model's __str__ method returns the expected string
        user = User(username="testuser", email="test@example.com")
        self.assertEqual(str(user), "testuser - test@example.com")


class AccountPermissionTests(UserFixtureMixin, TestCase):
    def test_anonymous_user_cannot_read_users(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_list_users(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_read_another_profile(self):
        other = User.objects.create_user(username="other", email="other@example.com")
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("user-detail", args=[other.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unverified_user_cannot_complete_profile(self):
        EmailAddress.objects.filter(user=self.user).update(verified=False)
        self.user.status = PENDING_COMPLETE_DATA
        self.user.save()
        self.client.force_authenticate(self.user)
        response = self.client.put(
            reverse("complete-profile"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "telephone": "123",
                "gender": "NONE",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pending_profile_cannot_read_protected_details(self):
        self.user.status = PENDING_COMPLETE_DATA
        self.user.save()
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("user-detail", args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_response_excludes_credentials_and_privileges(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("user-detail", args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ("password", "is_superuser", "is_staff", "groups", "user_permissions"):
            self.assertNotIn(field, response.data)

    def test_profile_update_cannot_change_privileges_or_verified_email(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            reverse("user-detail", args=[self.user.pk]),
            {
                "is_superuser": True,
                "is_staff": True,
                "email": "attacker@example.com",
                "status": PENDING_COMPLETE_DATA,
                "first_name": "Jane",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.status, COMPLETE)
        self.assertEqual(self.user.first_name, "Jane")

    def test_profile_completion_rejects_missing_fields(self):
        self.user.status = PENDING_COMPLETE_DATA
        self.user.save()
        self.client.force_authenticate(self.user)
        for method in (self.client.put, self.client.patch):
            response = method(reverse("complete-profile"), {"first_name": "Jane"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.user.refresh_from_db()
            self.assertEqual(self.user.status, PENDING_COMPLETE_DATA)
            self.assertEqual(self.user.first_name, "")

    def test_profile_completion_accepts_complete_patch(self):
        self.user.status = PENDING_COMPLETE_DATA
        self.user.save()
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            reverse("complete-profile"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "telephone": "123",
                "gender": "NONE",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"user_status": COMPLETE})
        self.user.refresh_from_db()
        self.assertEqual(self.user.status, COMPLETE)

    def test_delete_deactivates_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(reverse("user-detail", args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "UniquePass!2026-for-tests"
        self.user = User.objects.create_user(
            username="authuser",
            email="auth@example.com",
            password=self.password,
            status=COMPLETE,
        )
        self.email = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            verified=True,
            primary=True,
        )

    def test_login_by_username_and_email(self):
        from rest_framework.authtoken.models import Token

        for credentials in ({"username": self.user.username}, {"email": self.user.email}):
            client = APIClient()
            response = client.post(
                reverse("rest_login"),
                {
                    **credentials,
                    "password": self.password,
                },
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
            self.assertTrue(Token.objects.filter(user=self.user, key=response.data["key"]).exists())

    def test_unverified_login_is_rejected(self):
        self.email.verified = False
        self.email.save()
        response = self.client.post(
            reverse("rest_login"),
            {
                "email": self.user.email,
                "password": self.password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_access_and_logout(self):
        from rest_framework.authtoken.models import Token

        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        url = reverse("user-detail", args=[self.user.pk])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
        response = self.client.post(reverse("rest_logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(pk=token.pk).exists())
        self.assertEqual(self.client.get(url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_email_verification_and_login(self):
        from allauth.account.models import EmailConfirmationHMAC
        from django.core import mail

        response = self.client.post(
            reverse("rest_register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": self.password,
                "password2": self.password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        email = EmailAddress.objects.get(email="new@example.com")
        self.assertFalse(email.verified)
        self.assertEqual(len(mail.outbox), 1)
        key = EmailConfirmationHMAC(email).key
        confirmation_url = reverse("account_confirm_email", args=[key])
        self.assertIn(confirmation_url, mail.outbox[0].body)
        self.assertTrue(mail.outbox[0].alternatives)
        self.assertIn(confirmation_url, mail.outbox[0].alternatives[0].content)
        response = self.client.post(reverse("verify_email"), {"key": key}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        email.refresh_from_db()
        self.assertTrue(email.verified)
        response = self.client.post(
            reverse("rest_login"),
            {
                "email": email.email,
                "password": self.password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_password_reset_email_and_confirmation(self):
        from allauth.account.forms import default_token_generator
        from allauth.account.utils import user_pk_to_url_str
        from django.core import mail

        response = self.client.post(
            reverse("rest_password_reset"),
            {
                "email": self.user.email,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(mail.outbox), 1)
        uid = user_pk_to_url_str(self.user)
        token = default_token_generator.make_token(self.user)
        url = reverse("password_reset_confirm", args=[uid, token])
        self.assertIn(url, mail.outbox[0].body)
        browser_url = reverse(
            "account_reset_password_from_key", kwargs={"uidb36": uid, "key": token}
        )
        self.assertIn(browser_url, mail.outbox[0].alternatives[0].content)
        self.assertEqual(self.client.get(browser_url, follow=True).status_code, status.HTTP_200_OK)
        new_password = "AnotherUniquePass!2026"
        response = self.client.post(
            url,
            {
                "uid": uid,
                "token": token,
                "new_password1": new_password,
                "new_password2": new_password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_unknown_password_reset_email_does_not_expose_accounts(self):
        from django.core import mail

        response = self.client.post(
            reverse("rest_password_reset"),
            {
                "email": "unknown@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

    def test_email_confirmation_link_opens_working_login_page(self):
        from allauth.account.models import EmailConfirmationHMAC

        self.email.verified = False
        self.email.save()
        key = EmailConfirmationHMAC(self.email).key
        response = self.client.get(reverse("account_confirm_email", args=[key]), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.email.refresh_from_db()
        self.assertTrue(self.email.verified)
        self.assertIn("/api/v1/auth/account/login/", reverse("account_login"))
