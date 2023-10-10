from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.registration.views import (VerifyEmailView,
                                             ConfirmEmailView,
                                             ResendEmailVerificationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('auth/', include('dj_rest_auth.urls')),  # Registration, Login, logout

        # Registration endpoints
        path('auth/registration/account-confirm-email/<str:key>/',
             ConfirmEmailView.as_view()),
        path('auth/registration/', include('dj_rest_auth.registration.urls')),
        path('auth/registration/verify-email/', VerifyEmailView.as_view(),
             name='verify_email'),
        path('auth/registration/resend-email-verification/',
             ResendEmailVerificationView.as_view(),
             name='resend_email_verification'),
        path('auth/registration/account-confirm-email/', VerifyEmailView.as_view(),
             name='account_email_verification_sent'),
        re_path(r'^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
                VerifyEmailView.as_view(),
                name='account_confirm_email'),

        path('auth/password-reset/', PasswordResetView.as_view()),
        path('auth/password-reset-confirm/<uidb64>/<token>/',
             PasswordResetConfirmView.as_view(),
             name='password_reset_confirm'),

        # Login endpoints with Google OAuth2 and Apple
        path('auth/', include('allauth.urls')),

        # Accounts endpoints
        path('accounts/', include('accounts.urls')),
    ])),
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
