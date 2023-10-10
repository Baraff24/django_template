from django.urls import path

from .views import UsersListAPI, UserDetailAPI, CompleteProfileAPI

urlpatterns = [
    path("users/", UsersListAPI.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailAPI.as_view(), name="user-detail"),
    path("users/complete-profile/", CompleteProfileAPI.as_view(),
         name="complete-profile"),
]
