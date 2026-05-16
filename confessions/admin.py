from django.contrib import admin
from .models import AnonymousConfession, AnonymousComment

admin.site.register(AnonymousConfession)
admin.site.register(AnonymousComment)
