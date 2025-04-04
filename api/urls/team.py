from django.urls import path
from api.views import (
    GetTeamPoints,
    GetAllQuestions,
    GetSingleQuestion,
    GetTeamParticipantsNames,
    SaveSharedCode,
    GetSharedCode,
    ClearAllSharedCode,
    ServeSharedCode,
)

urlpatterns = [
    path("get_points/", GetTeamPoints.as_view()),
    path("get_questions/", GetAllQuestions.as_view()),
    path("get_question/", GetSingleQuestion.as_view()),
    path("get_team_participants_names/", GetTeamParticipantsNames.as_view()),
    path("save_shared_code/", SaveSharedCode.as_view()),
    path("get_shared_code/", GetSharedCode.as_view()),
    path("clear_all_shared_code/", ClearAllSharedCode.as_view()),
    path("saved_codes/<str:UUID>/", ServeSharedCode.as_view()),
]
