from django.urls import path
from api.views import GetTeamPoints, GetAllQuestions

urlpatterns = [
    path("get_points/", GetTeamPoints.as_view()),
    path("get_questions/", GetAllQuestions.as_view()),
]
