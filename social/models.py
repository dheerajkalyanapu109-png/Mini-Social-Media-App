from django.conf import settings
from django.db import models
U = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=160, blank=True)
    def __str__(self): return self.user.username

class Post(models.Model):
    author = models.ForeignKey(U, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(U, related_name="liked_posts", blank=True)
    class Meta: ordering = ["-created"]
    def __str__(self): return f"{self.author}: {self.text[:30]}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(U, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["created"]

class Follow(models.Model):
    follower = models.ForeignKey(U, on_delete=models.CASCADE, related_name="following_set")
    following = models.ForeignKey(U, on_delete=models.CASCADE, related_name="follower_set")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ("follower", "following")
    def __str__(self): return f"{self.follower} follows {self.following}"
