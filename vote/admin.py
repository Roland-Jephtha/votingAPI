from django.contrib import admin
from .models import *
from django_q.tasks import schedule

# Register your models here.


admin.site.register(User_Data)
admin.site.register(Contestant)
admin.site.register(Position)
admin.site.register(UserVote)
admin.site.register(Election)