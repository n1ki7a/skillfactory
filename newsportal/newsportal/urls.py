from django.urls import path

from . import views

# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsCreate, ArticlesList, ArticleDetail, ArticleCreate, ArticleUpdate, \
   NewsUpdate, NewsDelete, ArticleDelete, NewsSearch

urlpatterns = [
   path('', views.index),
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('news/search/', NewsSearch.as_view(), name='news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/edit/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/', ArticlesList.as_view(), name='articles_list'),
   path('articles/<int:pk>/', ArticleDetail.as_view(), name='articles_detail'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/edit/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
]