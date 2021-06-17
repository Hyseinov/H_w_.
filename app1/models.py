from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="title")
    text = models.CharField(max_length=100, verbose_name="text")
    created_date = models.DateField(auto_created=True, verbose_name="date")

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name="комент")
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
