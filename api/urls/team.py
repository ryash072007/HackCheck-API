from django.urls import path
from api.views import GetTeamPoints

urlpatterns = [
    path('get_points/', GetTeamPoints.as_view()),
]