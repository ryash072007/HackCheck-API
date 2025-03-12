from django.urls import path
from api.views import ChangeMaxParticipants, StartHackathon, EndHackathon, PauseHackathon, ResumeHackathon

urlpatterns = [
    path('change_max_participants/', ChangeMaxParticipants.as_view(), name='change_max_participants'),
    path('start_hackathon/', StartHackathon.as_view(), name='start_hackathon'),
    path('end_hackathon/', EndHackathon.as_view(), name='end_hackathon'),
    path('pause_hackathon/', PauseHackathon.as_view(), name='pause_hackathon'),
    path('resume_hackathon/', ResumeHackathon.as_view(), name='resume_hackathon'),
]