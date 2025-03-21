from django.urls import re_path

from .authentication import urlpatterns as authentication_urlpatterns
from .registration import urlpatterns as registration_urlpatterns
from .test import urlpatterns as test_urlpatterns
from .participants import urlpatterns as participants_urlpatterns
from .admin import urlpatterns as admin_urlpatterns
from .team import urlpatterns as team_urlpatterns
from .hackathon import urlpatterns as hackathon_urlpatterns
from api.views.test import custom_404_view

urlpatterns = [
    *authentication_urlpatterns,
    *registration_urlpatterns,
    *test_urlpatterns,
    *participants_urlpatterns,
    *admin_urlpatterns,
    *team_urlpatterns,
    *hackathon_urlpatterns,
    re_path(r".*", custom_404_view),  # Catch-all for 404 errors
]
