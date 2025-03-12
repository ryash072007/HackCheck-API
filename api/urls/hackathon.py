from django.urls import path
from api.views import ChangeMaxParticipants

urlpatterns = [
    path('change_max_participants/', ChangeMaxParticipants.as_view(), name='change_max_participants'),
]