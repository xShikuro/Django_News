from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from .models import Category, Article, ArticleCountViews, Comment
from .forms import LoginForm, RegistrationForm, ArticleForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DeleteView, ListView

from django.utils.datetime_safe import datetime
from django.db.models import Q


# Create your views here.
# kachishop


class HomeView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "pages/index.html"


class SearchResults(HomeView):
    def get_queryset(self):
        query = self.request.GET.get("q")
        articles = Article.objects.filter(
            # title__icontains=query,
            Q(title__iregex=query) | Q(description__iregex=query)
        )
        return articles


def home_page(request):
    articles = Article.objects.all()

    context = {
        "articles": articles,
    }

    return render(request, "pages/index.html", context)


def category_articles(request, category_id):
    category = Category.objects.get(pk=category_id)

    articles = Article.objects.filter(category=category)
    context = {
        "articles": articles,
    }

    return render(request, "pages/index.html", context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    comments = article.comments.filter(article=article)

    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key
    is_views = ArticleCountViews.objects.filter(article=article,
                                                session_id=session_key)

    if is_views.count() == 0 and str(session_key) != "None":
        views = ArticleCountViews()
        views.article = article
        views.session_id = session_key
        views.save()

        article.views += 1
        article.save()

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = article
            form.save()
            return redirect("article_detail", article.pk)
    else:
        form = CommentForm()

    context = {
        "article": article,
        "form": form,
        "comments": comments
    }
    return render(request, "pages/article_detail.html", context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Вы успешно вошли в аккаунт")
                return redirect("home")
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "pages/login.html", context)


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь добавлен")
            return redirect("login")
    else:
        form = RegistrationForm()

    context = {
        "form": form
    }
    return render(request, "pages/registration.html", context)


def user_logout(request):
    logout(request)
    messages.error(request, "Вы успешно вышли из аккаунта", extra_tags="danger")
    return redirect("home")


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, "Статья успешно создана")
            return redirect("article_detail", form.pk)
    else:
        form = ArticleForm()

    context = {
        "form": form
    }

    return render(request, "pages/article_form.html", context)


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = "/"
    template_name = "pages/article_confirm_delete.html"


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "pages/article_form.html"


def user_articles(request, username):
    user = User.objects.filter(username=username).first()
    articles = Article.objects.filter(author=user)
    total_views = sum([item.views for item in articles])
    total_comments = sum([item.comments.all().count() for item in articles])

    context = {
        "username": username,
        "articles": articles,
        "total_views": total_views,
        "total_comments": total_comments,
        "total_posts": articles.count(),
        "user": user,
        "registered_time": (datetime.now().date() - user.date_joined.date()).days
    }

    return render(request, "pages/user_articles.html", context)


def del_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    article_id = comment.article.pk
    comment.delete()
    return redirect("article_detail", article_id)


class UpdateComment(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "pages/article_detail.html"

    def form_valid(self, form):
        obj = self.get_object()
        article = Article.objects.get(pk=obj.article.pk)
        form.save()
        return redirect("article_detail", article.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        article = Article.objects.get(pk=obj.article.pk)
        comments = Comment.objects.filter(article=article)
        context["comments"] = comments
        context["article"] = article

        return context


# TODO ГОТОВО
# КОЛ-ВО ПРОСМОТРОВ
# СТРАНИЦА ПРОФИЛЯ
# ПОИСК
# ИЗМЕНЕНИЕ КОММЕНТАРИЯ
# УДАЛЕНИЕ КОММЕНТАРИЯ

# TODO ОСТАЛОСЬ СДЕЛАТЬ


# ЛАЙК ДИЗЛАЙК ДЛЯ КОММЕНТАРИЯ


# ПОПУЛЯРНЫЕ СТАТЬИ
