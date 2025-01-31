from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# from .models import User
from .models import Trope, Media

admin.site.register(Trope)
admin.site.register(Media)

# admin.site.register(User, UserAdmin)
