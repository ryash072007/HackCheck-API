from django.urls import path
from api.views import ResetHackathon, AdminSignIn, DeleteTeam, AddQuestion, RemoveQuestion, UpdateQuestion

urlpatterns = [
    path('reset/', ResetHackathon.as_view()),
    path('admin_signin/', AdminSignIn.as_view()),
    path('delete_team/', DeleteTeam.as_view()),
    path('add_question/', AddQuestion.as_view()),
    path('remove_question/', RemoveQuestion.as_view()),
    path('update_question/', UpdateQuestion.as_view())
]