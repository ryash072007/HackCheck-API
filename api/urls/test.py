from django.urls import path
from api.views import TestAuthenticationView

urlpatterns = [
    path('test_auth/', TestAuthenticationView.as_view()),
]