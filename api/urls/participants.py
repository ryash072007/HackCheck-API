from django.urls import path
from api.views import SubmitAnswer, CheckHackathonStatus, LogActivity

urlpatterns = [
    path("submit/", SubmitAnswer.as_view()),
    path("check_hackathon_status/", CheckHackathonStatus.as_view()),
    path("log_activity/", LogActivity.as_view()),
]
