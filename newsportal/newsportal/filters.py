import django_filters
from django.forms import DateInput
from django_filters import FilterSet

from .models import Post


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    create_time = django_filters.DateFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # поиск по имени автора
            'author__user__username': ['icontains'],
            # 'price': [
            #     'lt',  # цена должна быть меньше или равна указанной
            #     'gt',  # цена должна быть больше или равна указанной
            # ],
        }
