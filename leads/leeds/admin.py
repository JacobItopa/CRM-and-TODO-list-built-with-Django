from django.contrib import admin
from .models import lead, User, Agent, UserProfile, Category

# Register your models here.

admin.site.register(lead)
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(UserProfile)
admin.site.register(Category)

