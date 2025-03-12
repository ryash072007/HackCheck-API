from .authentication import urlpatterns as authentication_urlpatterns
from .registration import urlpatterns as registration_urlpatterns
from .test import urlpatterns as test_urlpatterns
from .participants import urlpatterns as participants_urlpatterns
from .admin import urlpatterns as admin_urlpatterns
from .team import urlpatterns as team_urlpatterns

urlpatterns = [
    *authentication_urlpatterns,
    *registration_urlpatterns,
    *test_urlpatterns,
    *participants_urlpatterns,
    *admin_urlpatterns,
    *team_urlpatterns
]
