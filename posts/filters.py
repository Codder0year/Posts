import django_filters
from .models import Ad


# Фильтр для модели объявления
class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains',
                                      label='Название товара')  # Поиск по названию (без учёта регистра)

    class Meta:
        model = Ad
        fields = ['title']
