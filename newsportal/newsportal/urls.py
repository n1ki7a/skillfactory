from django.urls import path

from .resources import news
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsCreate, ArticlesList, ArticleDetail, ArticleCreate

urlpatterns = [
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),

   path('articles/', ArticlesList.as_view(), name='articles_list'),
   path('articles/<int:pk>', ArticleDetail.as_view(), name='articles_detail'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
]