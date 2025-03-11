from .authentication import urlpatterns as authentication_urlpatterns
from .registration import urlpatterns as registration_urlpatterns

urlpatterns = [*authentication_urlpatterns, *registration_urlpatterns]
