from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Ad, Review
from .serializers import AdSerializer, ReviewSerializer
from .filters import AdFilter
from .permissions import IsOwnerOrReadOnly, IsAdminOrOwner
from rest_framework.pagination import PageNumberPagination


# Пагинация
class AdPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4


# Список объявлений с пагинацией и фильтрацией
class AdListAPIView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filterset_class = AdFilter
    pagination_class = AdPagination
    permission_classes = [AllowAny]


# Создание объявления
class AdCreateAPIView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Сохраняем текущего пользователя как автора
        serializer.save(author=self.request.user)


# Просмотр одного объявления
class AdRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [AllowAny]


# Обновление объявления
class AdUpdateAPIView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrReadOnly]


# Удаление объявления
class AdDestroyAPIView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrReadOnly]


# Создание отзыва
class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Сохраняем текущего пользователя как автора
        serializer.save(author=self.request.user)


# Список отзывов
class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


# Обновление отзыва
class ReviewUpdateAPIView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwner]



# Удаление отзыва
class ReviewDestroyAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwner]
