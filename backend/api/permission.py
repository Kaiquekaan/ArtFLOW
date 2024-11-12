from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permitir apenas a leitura se não for o dono do post
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permitir a edição e deleção apenas para o dono do post
        return obj.user == request.user