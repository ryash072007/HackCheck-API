from django.urls import path
from api.views import ResetHackathon, AdminSignIn, DeleteTeam, AddQueston

urlpatterns = [
    path('reset/', ResetHackathon.as_view()),
    path('admin_signin/', AdminSignIn.as_view()),
    path('delete_team/', DeleteTeam.as_view()),
    path('add_question/', AddQueston.as_view())
]