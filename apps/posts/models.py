from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def post_image_path(instance, filename):
    return 'posts/{}/{}'.format(instance.user.username, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    image = ProcessedImageField(
        upload_to=post_image_path,
        processors=[ResizeToFill(600, 600)],
        format='PNG',
        blank=False,
    )
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_posts') # Flag for users who have like posts
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
