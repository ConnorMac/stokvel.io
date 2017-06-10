from django.contrib import admin
from stokvel.models import User, Stokvel, Event, Vote

# Register your models here.
admin.site.register(User)
admin.site.register(Stokvel)
admin.site.register(Event)
admin.site.register(Vote)
