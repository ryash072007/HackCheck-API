from django.urls import path
from api.views import ChangeMaxParticipants, StartHackathon

urlpatterns = [
    path('change_max_participants/', ChangeMaxParticipants.as_view(), name='change_max_participants'),
    path('start_hackathon/', StartHackathon.as_view(), name='start_hackathon'),
]