from django.contrib import admin
from .models import Studio, Platform, Game, Person, Award


admin.site.register(Studio)
admin.site.register(Platform)
admin.site.register(Game)
admin.site.register(Person)
admin.site.register(Award)
