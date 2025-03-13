from django.urls import path
from api.views import ResetHackathonDatabase, AdminSignIn, DeleteTeam, AddQuestion, RemoveQuestion, UpdateQuestion, GetTeams, AdminDashboard, GetScoreSettings, UpdateScoreSettings, ExportLeaderboard, ResetCurrentHackathon

urlpatterns = [
    path('reset_database/', ResetHackathonDatabase.as_view()),
    path('admin_signin/', AdminSignIn.as_view()),
    path('delete_team/', DeleteTeam.as_view()),
    path('add_question/', AddQuestion.as_view()),
    path('remove_question/', RemoveQuestion.as_view()),
    path('update_question/', UpdateQuestion.as_view()),
    path('get_teams/', GetTeams.as_view()),
    path('dashboard/', AdminDashboard.as_view()),
    path('get_score_settings/', GetScoreSettings.as_view()),
    path('update_score_settings/', UpdateScoreSettings.as_view()),
    path('export_leaderboard/', ExportLeaderboard.as_view()),
    path('reset_hackathon/', ResetCurrentHackathon.as_view())
]