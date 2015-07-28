from django.contrib import admin

from .models import Golfer, Scorecard, Hole, Comment

admin.site.register(Golfer)
admin.site.register(Scorecard)
admin.site.register(Hole)
admin.site.register(Comment)

