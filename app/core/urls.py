from dj_rest_auth.registration.views import (
    ConfirmEmailView,
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "schema/swagger-ui/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path("auth/login/", LoginView.as_view(), name="rest_login"),
                # URLs that require a user to be logged in with a valid session / token.
                path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
                # Registration endpoints
                path("auth/registration/", RegisterView.as_view(), name="rest_register"),
                path(
                    "auth/registration/account-confirm-email/<str:key>/",
                    ConfirmEmailView.as_view(),
                    name="account_confirm_email",
                ),
                path(
                    "auth/registration/resend-email-verification/",
                    ResendEmailVerificationView.as_view(),
                    name="resend_email_verification",
                ),
                path(
                    "auth/registration/verify-email/",
                    VerifyEmailView.as_view(),
                    name="verify_email",
                ),
                path(
                    "auth/password-reset/", PasswordResetView.as_view(), name="rest_password_reset"
                ),
                path(
                    "auth/password-reset-confirm/<str:uidb64>/<str:token>/",
                    PasswordResetConfirmView.as_view(),
                    name="password_reset_confirm",
                ),
                # HTML account flows have their own prefix to avoid the REST login route.
                path("auth/account/", include("allauth.urls")),
                # Preserve old callback paths while reversing new links to the account prefix.
                path("auth/", include(("allauth.urls", "allauth"), namespace="legacy_allauth")),
                # Accounts endpoints
                path("accounts/", include("accounts.urls")),
            ]
        ),
    ),
]

if settings.SERVE_MEDIA:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
