from django.contrib import admin
from .models import Thread

admin.site.site_header = "Moderator panel"
admin.site.register(Thread)

