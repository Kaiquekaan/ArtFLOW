from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verifica se o objeto tem um atributo `user`
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Se não tiver, verifica se tem o atributo `sender`
        elif hasattr(obj, 'sender'):
            return obj.sender == request.user
        # Caso contrário, nega a permissão
        return False
    
