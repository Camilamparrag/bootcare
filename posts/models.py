from django.db import models
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    image = models.ImageField(upload_to="posts/")
    caption = models.TextField(max_length=1000, blank=True)
    hashtags = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
