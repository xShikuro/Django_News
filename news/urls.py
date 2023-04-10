from django.urls import path

from . import views

# http://127.0.0.1:8000/auth/login/
# http://127.0.0.1:8000/auth/registration/


urlpatterns = [
    # path("", views.home_page, name="home"),  # http://127.0.0.1:8000/
    path("", views.HomeView.as_view(), name="home"),  # http://127.0.0.1:8000/
    path("categories/<int:category_id>/", views.category_articles, name="category_articles"),
    path("articles/<int:article_id>/", views.article_detail, name="article_detail"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/registration/", views.registration_view, name="registration"),
    path("auth/logout/", views.user_logout, name="logout"),

    path("create/", views.add_article, name="create"),
    path("delete/<int:pk>/", views.ArticleDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", views.ArticleUpdateView.as_view(), name="update"),

    path("auth/users/<str:username>/", views.user_articles, name="user_articles"),

    path("search/", views.SearchResults.as_view(), name="search"),
    path("comments/<int:comment_id>/delete/", views.del_comment, name="del_comment"),
    path("comments/<int:pk>/edit/", views.UpdateComment.as_view(), name="edit_comment"),
]
