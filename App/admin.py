from django.contrib import admin
from .models import FollowersCnt, PostLike, Profile, Post

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(FollowersCnt)
