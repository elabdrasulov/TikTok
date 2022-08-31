from django.db import models
from django.contrib.auth import get_user_model

from .check_size import file_size

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=70)
    # posts = models.ManyToManyField() 

    def __str__(self):
        return self.title

class Post(models.Model):
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    video = models.FileField(upload_to='videos', validators=[file_size], blank=True, null=True)
    video_tags = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True, default=0)
    # similars = models.ManyToManyField(Category, related_name='similars')

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='sub_comments', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user} -> {self.post}'

class LikePost(models.Model):
    user = models.ForeignKey(User, related_name='post_likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} -> {self.post}'


class LikeComment(models.Model):
    user = models.ForeignKey(User, related_name='comment_likes', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} -> {self.comment}'


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='favorites', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} -> {self.post}'
