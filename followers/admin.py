from django.contrib import admin

from .models import Follower


class FollowersAdmin(admin.ModelAdmin):
    pass


admin.site.register(Follower, FollowersAdmin)
