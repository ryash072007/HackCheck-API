from django.urls import path
from api.views import ResetHackathon, AdminSignIn

urlpatterns = [
    path('reset/', ResetHackathon.as_view()),
    path('admin_signin/', AdminSignIn.as_view())
]