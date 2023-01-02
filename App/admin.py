from django.contrib import admin
from .models import FollowersCnt, Profile, Post

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FollowersCnt)
