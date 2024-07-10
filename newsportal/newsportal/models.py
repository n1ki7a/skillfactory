import django.contrib.auth
from django.db import models
from django.db.models import Sum
from django.urls import reverse

from newsportal.resources import POSTTYPES, article


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(django.contrib.auth.get_user_model(), on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = (self.posts.aggregate(Sum("rating", default=0))['rating__sum'] * 3
                       + self.user.comments.aggregate(Sum("rating", default=0))['rating__sum']
                       + Comment.objects.filter(post__author=self).aggregate(Sum("rating", default=0))['rating__sum'])
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(django.contrib.auth.get_user_model(), through='CategorySubscribers')

    def __str__(self):
        return f'{self.name}'


class CategorySubscribers(models.Model):
    user = models.ForeignKey(django.contrib.auth.get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=7,
                            choices=POSTTYPES,
                            default=article)
    create_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        return self.content[0:124] + "..." * (len(self.content) > 124)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        viewname = 'articles_detail' if self.type == article else 'news_detail'
        return reverse(viewname, args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(django.contrib.auth.get_user_model(), on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
