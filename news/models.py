from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    title = models.CharField(verbose_name="Название категории", max_length=100)

    def get_absolute_url(self):
        return reverse("category_articles", kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(verbose_name="Название статьи", max_length=100, unique=True)
    description = models.TextField(verbose_name="Описание статьи")
    image = models.ImageField(verbose_name="Фото статьи", upload_to="photos/", blank=True, null=True)
    views = models.IntegerField(verbose_name="Кол-во просмотров", default=0)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время обновления", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Активна?", default=True)
    category = models.ForeignKey(to=Category, verbose_name="Категория", on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, verbose_name="Автор", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"article_id": self.pk})

    def __str__(self):
        return self.title

# user.comments.all


class Comment(models.Model):  # author, article, created_at, content
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.author}: {self.article}"


class ArticleCountViews(models.Model):
    session_id = models.CharField(max_length=150, db_index=True)
    article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.session_id
