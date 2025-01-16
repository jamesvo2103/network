from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=140)
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    comments = models.ManyToManyField(User, through='Comment', related_name='commented_posts')

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
class Follow(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_is_following")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_is_being_followed") 

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"