from django.urls import path
from api.views import GetTeamPoints, GetAllQuestions, GetSingleQuestion, GetTeamParticipantsNames

urlpatterns = [
    path("get_points/", GetTeamPoints.as_view()),
    path("get_questions/", GetAllQuestions.as_view()),
    path("get_question/", GetSingleQuestion.as_view()),
    path("get_team_participants_names/", GetTeamParticipantsNames.as_view()),
]
