from django.urls import path
from api.views import TeamSignIn

urlpatterns = [
    path('login/', TeamSignIn.as_view()),
]