from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = routers.SimpleRouter()
router.register("times", views.TimeViewSet, basename="times")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.register_view, name="register"),
    path("delete/account/", views.DeleteUserView.as_view(), name="delete"),
    path("change/password/", views.ChangePassword.as_view(), name="change-password"),
    path("profile/<int:id>/", views.ProfileView.as_view(), name="profile"),
    path("users/<int:id>/", views.UserView.as_view(), name="user"),
    # Check username or email adresses.
    path("check/<str:data>/", views.check_view),
    # Statistics about times.
    path("user/stats/", views.StatisticView.as_view()),
    path("user/stats/last/<int:amount>/", views.StatisticView.as_view()),
    # JWT Token.
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    # DRF web login.
    path("api-auth/", include("rest_framework.urls")),
]
