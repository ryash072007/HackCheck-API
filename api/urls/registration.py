from django.urls import path
from api.views import TeamRegistration

urlpatterns = [
    path("register/", TeamRegistration.as_view()),
]
