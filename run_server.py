from waitress import serve
from HackCheckAPI.wsgi import application as wsgiapp

serve(wsgiapp, host= "0.0.0.0", port=8000, _quiet=False, threads=8)