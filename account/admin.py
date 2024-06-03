from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister models
admin.site.unregister(Group)
