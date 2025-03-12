from django.urls import path
from api.views import SubmitAnswer

urlpatterns = [
    path('submit/', SubmitAnswer.as_view()),
]