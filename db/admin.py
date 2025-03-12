from django.contrib import admin
from db.models import *

# Register your models here.
admin.site.register(Account)
admin.site.register(TeamProfile)
admin.site.register(TeamMember)
admin.site.register(Question)
admin.site.register(Answer)
