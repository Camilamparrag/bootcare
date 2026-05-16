from django.db import models
from django.conf import settings


class AnonymousConfession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="confessions",
    )
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_confessions",
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]


class AnonymousComment(models.Model):
    confession = models.ForeignKey(
        AnonymousConfession,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
