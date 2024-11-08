from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение для того, чтобы только владельцы объектов могли редактировать или удалять их.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить просмотр для всех пользователей
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить редактирование/удаление только владельцу объекта
        return obj.author == request.user


class IsAdminOrOwner(permissions.BasePermission):
    """
    Разрешение для администратора или владельца объекта (для редактирования/удаления)
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить администраторам редактировать/удалять любой объект
        if request.user and request.user.is_staff:
            return True

        # Разрешить владельцу объекта редактировать/удалять его
        return obj.author == request.user
