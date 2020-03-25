from django.contrib import admin
from .models import Post

admin.site.site_header = "Moderator panel"
admin.site.register(Post)

