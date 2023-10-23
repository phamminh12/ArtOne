from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
# m > a > f > v > u

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)

    avatar = models.ImageField(null=True, default="avatar.jpg")

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['username']


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Picture(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_images/', null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    # participant
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} likes {self.picture.name}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body