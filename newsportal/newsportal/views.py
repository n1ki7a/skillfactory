from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm
from .models import Post
from .resources import news, article


def index(request):
    return render(request, "land.html")


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-create_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_list'
    # Показывать только новости отбираем по типу
    queryset = Post.objects.filter(type=news)
    paginate_by = 10


class NewsSearch(NewsList):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'news_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news_detail'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = news
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticlesList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'articles_list.html'
    context_object_name = 'articles_list'
    queryset = Post.objects.filter(type=article)


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'article_detail'


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    success_url = reverse_lazy('articles_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = article
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles_list')
