import uuid
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile_user")
    bio = models.TextField(
        blank=True, default="Hey there, I am using OnConnect !!!")
    profile_img = models.ImageField(
        upload_to="profile_images", default="blank-profile-picture.png")
    location = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_user")
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.user.username


class FollowersCnt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return self.user.username
