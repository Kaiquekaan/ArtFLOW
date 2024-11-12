from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, GetTokenSerializer, PostSerializer, PostMediaSerializer, CommentSerializer, UserDataSerializer, FollowService, MessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from cloudinary.uploader import upload
from rest_framework.pagination import PageNumberPagination
from .models import UserData, Post, PostMedia, Comment, FriendRequest, Notification, Room, Message
from .services import NotificationService, FriendService, PostInteractionService, PostService
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .permission import IsOwnerOrReadOnly
from backend.recommendation_service import *
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate
import random
from rest_framework.decorators import action
import json
import base64
import logging
logger = logging.getLogger(__name__)




class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]  

    @never_cache
    def put(self, request, *args, **kwargs):
        user = request.user
        userdata_data = request.data.get('userdata', {})

        # Processar a imagem de perfil base64 (se enviada)
        profile_picture_base64 = userdata_data.get('profile_picture_url')
        banner_picture_base64 = userdata_data.get('banner_picture_url')

        # Variáveis para armazenar a URL e o ID
        profile_picture_url = None
        profile_picture_id = None
        banner_picture_url = None
        banner_picture_id = None

        # Upload da imagem de perfil se for uma URL base64
        if profile_picture_base64 and 'data:image' in profile_picture_base64:
            try:
                header, encoded = profile_picture_base64.split(',', 1)
                upload_result = upload(base64.b64decode(encoded))
                profile_picture_url = upload_result['secure_url']
                profile_picture_id = upload_result['public_id']
                print('profile_id ', profile_picture_id)
            except Exception as e:
                return Response({'error': f'Erro ao fazer upload da imagem de perfil: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Upload da imagem de banner se for uma URL base64
        if banner_picture_base64 and 'data:image' in banner_picture_base64:
            try:
                header, encoded = banner_picture_base64.split(',', 1)
                upload_result = upload(base64.b64decode(encoded))
                banner_picture_url = upload_result['secure_url']
                banner_picture_id = upload_result['public_id']
                print('banner_id ', banner_picture_id)
                print('banner_url ', banner_picture_url)
            except Exception as e:
                return Response({'error': f'Erro ao fazer upload do banner: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Atualizar os dados no request antes de passar para o serializer
        if profile_picture_url:
            userdata_data['profile_picture_url'] = profile_picture_url
            userdata_data['profile_picture_id'] = profile_picture_id
        else:
            userdata_data.pop('profile_picture_url', None)  # Remove o campo se ele for None para evitar erros

        if banner_picture_url:
            userdata_data['banner_picture_url'] = banner_picture_url
            userdata_data['banner_picture_id'] = banner_picture_id
        else:
            userdata_data.pop('banner_picture_url', None)

        request.data['userdata'] = userdata_data

        # Enviar para o serializer
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Exibe os erros detalhados do serializer no log
            print("Erros do serializer:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        # Pega o usuário autenticado
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        userdata_data = request.data.get('userdata', {})

        # Atualizar imagens, similar ao que é feito em PostViewSet
        # Processamento de imagem de perfil
        profile_picture_base64 = userdata_data.get('profile_picture_url')
        if profile_picture_base64 and 'data:image' in profile_picture_base64:
            try:
                header, encoded = profile_picture_base64.split(',', 1)
                upload_result = upload(base64.b64decode(encoded))
                # Atualiza o campo do perfil do usuário
                user.userdata.profile_picture_url = upload_result.get('secure_url')
                user.userdata.profile_picture_id = upload_result.get('public_id')
            except Exception as e:
                return Response({"error": f"Erro no upload da imagem de perfil: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Processamento de imagem de banner
        banner_picture_base64 = userdata_data.get('banner_picture_url')
        if banner_picture_base64 and 'data:image' in banner_picture_base64:
            try:
                header, encoded = banner_picture_base64.split(',', 1)
                upload_result = upload(base64.b64decode(encoded))
                # Atualiza o campo do banner do usuário
                user.userdata.banner_picture_url = upload_result.get('secure_url')
                user.userdata.banner_picture_id = upload_result.get('public_id')
            except Exception as e:
                return Response({"error": f"Erro no upload da imagem de banner: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Atualizar outros dados do usuário diretamente
        user.userdata.displayname = userdata_data.get('displayname', user.userdata.displayname)
        user.userdata.user_tag = userdata_data.get('user_tag', user.userdata.user_tag)
        user.userdata.bio = userdata_data.get('bio', user.userdata.bio)
        user.userdata.is_private = userdata_data.get('is_private', user.userdata.is_private)
        user.userdata.save()  # Salva as alterações no UserData

        # Salva alterações no usuário principal, se necessário
        user.save()

        # Retornar os dados atualizados
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['patch'], url_path='update-email')
    def update_email(self, request):
        user = self.request.user
        current_password = request.data.get('current_password')
        new_email = request.data.get('email')

        # Autentica o usuário usando a senha atual
        if not authenticate(username=user.username, password=current_password):
            return Response({"error": "Senha incorreta."}, status=status.HTTP_403_FORBIDDEN)

        # Atualiza o e-mail principal
        if new_email:
            user.email = new_email
            user.save()
            return Response({"success": "E-mail atualizado com sucesso."}, status=status.HTTP_200_OK)

        return Response({"error": "E-mail não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=False, methods=['patch'], url_path='update-recovery-email')
    def update_recovery_email(self, request):
        user = self.request.user
        new_recovery_email = request.data.get('recovery_email')

        # Atualiza o e-mail de recuperação no UserData
        if new_recovery_email:
            user.userdata.recovery_email = new_recovery_email
            user.userdata.save()
            return Response({"success": "E-mail de recuperação atualizado com sucesso."}, status=status.HTTP_200_OK)

        return Response({"error": "E-mail de recuperação não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=['patch'], url_path='update-password')
    def update_password(self, request):
        user = self.request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Verifica a senha atual
        if not authenticate(username=user.username, password=current_password):
            return Response({"error": "Senha incorreta."}, status=status.HTTP_403_FORBIDDEN)

        # Verifica se a nova senha e a confirmação coincidem
        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return Response({"success": "Senha atualizada com sucesso."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "As senhas não coincidem."}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'], url_path='toggle-2fa')
    def toggle_2fa(self, request):
        user = self.request.user
        enable_2fa = request.data.get('two_factor_enabled', False)

        user.userdata.two_factor_enabled = enable_2fa
        user.userdata.save()
        return Response({"success": f"2FA {'ativado' if enable_2fa else 'desativado'} com sucesso."}, status=status.HTTP_200_OK)

 


class GetToken(TokenObtainPairView):
    serializer_class = GetTokenSerializer



class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, exclude_user_fields=True)
        user_data = serializer.data

        # Remover o campo de senha dos dados serializados
        if 'password' in user_data:
            user_data.pop('password')
            
        return Response(user_data)

class CheckUserTagView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        usertag = request.GET.get('usertag')
        exists = UserData.objects.filter(user_tag=usertag).exists()
        return Response({'exists': exists}, status=status.HTTP_200_OK)
    

class CheckEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.GET.get('email')
        exists = User.objects.filter(email=email).exists()
        return Response({'exists': exists}, status=status.HTTP_200_OK)


class RequestResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        use_recovery_email = request.data.get('use_recovery_email', False)

        try:
            if use_recovery_email:
                user_data = UserData.objects.get(recovery_email=email)
            else:
                user = User.objects.get(email=email)
                user_data = user.userdata

            if user_data:
                user = user_data.user

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            frontend_url = f"http://localhost:5173/reset-password/{uid}/{token}"

            # Renderiza o template HTML
            context = {
                'user': user,
                'reset_url': frontend_url
            }
            email_html_message = render_to_string('password_reset_email.html', context)

            # Configura e envia o e-mail
            subject = 'Redefinição de Senha - ArtFlow'
            from_email = 'noreply.artflow@gmail.com'
            to_email = [email] if not use_recovery_email else [user_data.recovery_email]
            email_message = EmailMultiAlternatives(subject, email_html_message, from_email, to_email)
            email_message.attach_alternative(email_html_message, "text/html")
            email_message.send(fail_silently=False)

            return Response({'success': 'Email enviado com sucesso.'}, status=200)

        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=404)
        

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')
                user.set_password(new_password)
                user.save()
                return Response({'success': 'Senha redefinida com sucesso.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        

class SendTwoFactorCodeView(APIView):
    def post(self, request):
        user = request.user
        if not user.userdata.two_factor_enabled:
            return Response({"error": "2FA não está ativada."}, status=400)
        
        # Gera um código de 6 dígitos e o salva no perfil do usuário
        code = "{:06d}".format(random.randint(0, 999999))
        user.userdata.two_factor_code = code
        user.userdata.save()

        # Envia o código por e-mail
        send_mail(
            'Seu código de verificação',
            f'Seu código de verificação é {code}',
            'noreply@seusite.com',
            [user.email],
            fail_silently=False,
        )

        return Response({"success": "Código de verificação enviado."})
    

class VerifyTwoFactorCodeView(APIView):
    def post(self, request):
        code = request.data.get("code")
        user = request.user

        if user.userdata.two_factor_code == code:
            # Código correto, 2FA concluída
            user.userdata.two_factor_code = None  # Reseta o código
            user.userdata.save()
            return Response({"success": "Verificação concluída com sucesso."})
        else:
            return Response({"error": "Código incorreto."}, status=400)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data) 

        caption = request.data.get('caption', '')
        is_sensitive = request.data.get('is_sensitive', False)
        is_private = request.data.get('is_private', False)
        files = request.FILES.getlist('files')

        if isinstance(is_sensitive, str):
            is_sensitive = is_sensitive.lower() == 'true'

        if isinstance(is_private, str):
            is_private = is_private.lower() == 'true'


        # Criar o post
        post = Post.objects.create(
            user=request.user,
            caption=caption,
            is_sensitive=is_sensitive,
            is_private=is_private
        )

        # Upload dos arquivos para o Cloudinary e criação dos objetos PostMedia
        for file in files:
            file_extension = file.name.split('.').pop().lower()
            try:
                if file_extension in ['mp4', 'webm', 'ogg']:  # Verifica se é vídeo
                    upload_result = upload(file, resource_type="video")
                else:  # Caso contrário, trata como imagem
                    upload_result = upload(file)

                print("Upload Result:", upload_result)
                PostMedia.objects.create(post=post, file=upload_result['secure_url'])
            except Exception as e:
                print("Error uploading file:", e)
                return Response({"error": "Error uploading file"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)


class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_data = request.user.userdata
        friend_user_data = UserData.objects.get(user_id=user_id)

        if user_data != friend_user_data:
            if friend_user_data in user_data.friends.all():
                user_data.friends.remove(friend_user_data)
                return Response({"status": "Amizade removida"}, status=status.HTTP_200_OK)
            else:
                user_data.friends.add(friend_user_data)
                return Response({"status": "Amizade adicionada"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Você não pode se adicionar como amigo"}, status=status.HTTP_400_BAD_REQUEST)


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, target_user_id):
        service = FollowService(user_id=request.user.id, target_user_id=target_user_id)
        result = service.toggle_follow()
        return Response({"status": result})
    


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        from_user_data = request.user.userdata  # Usuário logado
        to_user_data = UserData.objects.get(user_id=user_id)  # Usuário alvo

        if from_user_data != to_user_data:
            # 1. Verificar se já são amigos
            print('Não sao o mesmo usuario')
            if FriendService.are_friends(from_user_data.user_id, to_user_data.user_id):
                # Se já forem amigos, desfaz a amizade
                FriendService.toggle_friend(from_user_data.user_id, to_user_data.user_id)
                return Response({"status": "Friendship removed"}, status=status.HTTP_200_OK)

            # 2. Verificar se o usuário alvo já enviou uma solicitação de amizade para o usuário logado
            incoming_request = FriendRequest.objects.filter(from_user=to_user_data, to_user=from_user_data).first()
            if incoming_request:
                # Aceitar a solicitação de amizade
                FriendService.toggle_friend(from_user_data.user_id, to_user_data.user_id)  # Adicionar ambos como amigos
                incoming_request.delete()  # Remover a solicitação
                Notification.objects.filter(sender_id=to_user_data.user_id, user_id=from_user_data.user_id, notification_type='friend_request').delete()  # Remover a notificação
                return Response({"status": "Friend request accepted, now friends"}, status=status.HTTP_200_OK)

            # 3. Verificar se já existe uma solicitação de amizade pendente do usuário logado para o usuário alvo
            outgoing_request = FriendRequest.objects.filter(from_user=from_user_data.user_id, to_user=to_user_data.user_id).first()
            print('dados da outgoing', outgoing_request)
            if outgoing_request:
                print('Solicitaçao ja enviada')
                print(from_user_data.user_id)
                print(to_user_data.user_id)
                print(user_id)
                # Se houver uma solicitação de amizade pendente, cancelar a solicitação e remover a notificação
                FriendService.reject_or_remove_friend(from_user_data.user_id, to_user_data.user_id)
                return Response({"status": "Friend request cancelled"}, status=status.HTTP_200_OK)

            # 4. Caso contrário, criar uma nova solicitação de amizade
            FriendRequest.objects.create(from_user=from_user_data, to_user=to_user_data)

            # Criar uma notificação para o destinatário da solicitação
            NotificationService.create_notification(
                to_user_data.user,  # Usuário que receberá a notificação
                'friend_request',  # Tipo de notificação
                f"{from_user_data.user.username} enviou uma solicitação de amizade.",  # Conteúdo da notificação
                from_user_data.user_id  # ID do remetente
            )
            return Response({"status": "Friend request sent"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Você não pode se adicionar como amigo"}, status=status.HTTP_400_BAD_REQUEST)

    

class RejectOrRemoveFriendView(APIView):
    def post(self, request, target_user_id):
        user_id = request.user.id  # Usuário logado
        result = FriendService.reject_or_remove_friend(user_id, target_user_id)
        
        if "rejected" in result or "removed" in result:
            return Response({"message": result}, status=status.HTTP_200_OK)
        return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)

    

class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)  # Buscar usuário pelo username
            user_data = UserData.objects.get(user=user)  # Buscar UserData associado

            pending_request_friend= FriendService.pending_request_friends(
                request.user.id,
                user.id
            ) if request.user.is_authenticated else False

            if user_data.is_private and user != request.user:
                if not (FriendService.are_friends(request.user.id, user.id) or 
                        FollowService.is_following(request.user.id, user.id)):
                      public_data = {
                     "user_id": user.id,
                     "username": user.username,
                     "displayname": user_data.displayname,
                     "user_tag": user_data.user_tag,
                     "bio": user_data.bio,
                     "profile_picture_url": user_data.profile_picture_url,
                     "banner_picture_url": user_data.banner_picture_url,
                     "posts_count": user_data.count_posts(),
                     "friends_count": user_data.count_friends(),
                     "followers_count": user_data.count_followers(),
                     "following_count": user_data.count_following(),
                     "pending_request_friend": pending_request_friend,
                     "is_locked": True,
                    }
                      return Response(public_data, status=status.HTTP_200_OK)

            is_following = FollowService.is_following(
                request.user.id,
                user.id
            ) if request.user.is_authenticated else False

            are_friends = FriendService.are_friends(
                request.user.id,
                user.id
            ) if request.user.is_authenticated else False


            serializer = UserDataSerializer(user_data, exclude_posts_friends=True)

            response_data = {
                **serializer.data,
                "is_following": is_following,
                "are_friends": are_friends,
                "pending_request_friend": pending_request_friend,
                
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except UserData.DoesNotExist:
            return Response({"error": "Dados do usuário não encontrados"}, status=status.HTTP_404_NOT_FOUND)


        
    

class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            # Recupera a notificação pelo ID
            notification = Notification.objects.get(id=notification_id, user=request.user)
            print(f"Notification ID: {notification_id}")
            

            # Verifica se a notificação é do tipo "solicitação de amizade"
            if notification.notification_type != 'friend_request':
                return Response({"error": "Tipo de notificação inválido."}, status=status.HTTP_400_BAD_REQUEST)

            # Recupera o sender_id da notificação para obter o usuário que enviou a solicitação
            from_user = User.objects.get(id=notification.sender_id)  # sender_id representa o usuário que enviou a solicitação
            print(f"Retorno do from_user: {from_user}")
            from_user_data = from_user.userdata  # Recupera o UserData do remetente
            print(f"Retorno do from_user_data: {from_user_data}")

            # Verifica se o usuário logado já é amigo do remetente
            user_data = request.user.userdata
            

            if from_user_data in user_data.friends.all():
                return Response({"error": "Vocês já são amigos."}, status=status.HTTP_400_BAD_REQUEST)

            FriendService.toggle_friend(
                user_data.user_id,
                from_user_data.user_id
            )

            # Marca a notificação como lida
            NotificationService.delete_notification(notification_id)

            # Cria uma nova notificação de "amizade aceita" para o remetente
            NotificationService.create_notification(
                from_user,
                'friend_accepted',
                f"{request.user.username} aceitou sua solicitação de amizade.",
                
            )

            return Response({"status": "Solicitação de amizade aceita"}, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response({"error": "Notificação não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        friends = FriendService.get_friends(user_id)
        return Response(friends)

    


class UserSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '').strip()  # Obtém o parâmetro de consulta
        if query:
            usersearch = User.objects.filter(
                Q(username__icontains=query) | Q(userdata__user_tag__icontains=query)
            ).distinct()
        else:
            usersearch = User.objects.none()  # Não retorna nada se não houver query

        results = [
            {
                'username': user_data.username,  # Pega o username do user associado
                'user_tag': user_data.userdata.user_tag,
                'profile_picture_url': user_data.userdata.profile_picture_url,
                'bio': user_data.userdata.bio,
            }
            for user_data in usersearch
        ]

        return Response(results)




class CreateNotificationView(APIView):
    def post(self, request):
        user = request.user
        notification_type = request.data.get('notification_type')
        content = request.data.get('content')
        
        if not user or not notification_type or not content:
            return Response({"error": "Dados insuficientes"}, status=status.HTTP_400_BAD_REQUEST)
        
        NotificationService.create_notification(user, notification_type, content)
        return Response({"status": "Notificação criada"}, status=status.HTTP_201_CREATED)

class GetNotificationsView(APIView):
    def get(self, request):
        user = request.user
        notifications = NotificationService.get_notifications(user)
        data = [{"id": n.id, "type": n.notification_type, "content": n.content, "created_at": n.created_at, "is_read": n.is_read} for n in notifications]
        return Response(data, status=status.HTTP_200_OK)

class MarkNotificationAsReadView(APIView):
    def post(self, request, notification_id):
        success = NotificationService.mark_as_read(notification_id)
        if success:
            return Response({"status": "Notificação marcada como lida"}, status=status.HTTP_200_OK)
        return Response({"error": "Notificação não encontrada"}, status=status.HTTP_404_NOT_FOUND)
    

class MarkAllAsReadNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        NotificationService.mark_all_as_read(user)
        return Response({"message": "Todas as notificações foram marcadas como lidas."})


class DeleteNotificationView(APIView):
    def post(self, request, notification_id):
        success = NotificationService.delete_notification(notification_id)
        if success:
            return Response({"status": "Notificação marcada como lida"}, status=status.HTTP_200_OK)
        return Response({"error": "Notificação não encontrada"}, status=status.HTTP_404_NOT_FOUND)



class LikePostView(APIView):

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        result = PostInteractionService.like_post(request.user, post)
        return Response({"status": result})

class FavoritePostView(APIView):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            result = PostInteractionService.favorite_post(request.user, post)
            return Response({"status": result}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


class CommentPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)  # Obtenha o post
        text = request.data.get('content')  # Obtenha o conteúdo do comentário

        # Cria o comentário usando o PostInteractionService
        comment = PostInteractionService.comment_post(request.user, post, text)

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
    

class PostListView2(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')  # Ordenar por data de criação
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Número de postagens por página

        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        page = int(request.query_params.get('page', 1))
        page_size = 10

        # Obtenha os posts
        posts = PostService.get_feed_posts(user, page=page, page_size=page_size)

        paginator = PageNumberPagination()
        paginator.page_size = page_size

        # Paginação para a página atual
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})

        # Calcule a contagem de posts na próxima página manualmente
        next_page_start = page * page_size
        next_count = posts[next_page_start:next_page_start + page_size].count()

        # Obtenha a resposta paginada e adicione `next_count`
        paginated_response = paginator.get_paginated_response(serializer.data)
        paginated_response.data['next_count'] = next_count

        return paginated_response
    
class PostListFollowingView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        page = int(request.query_params.get('page', 1))
        page_size = 10

        # Obtenha os posts
        posts = PostService.get_feed_following_posts(user, page=page, page_size=page_size)

        paginator = PageNumberPagination()
        paginator.page_size = page_size

        # Paginação para a página atual
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})

        # Calcule a contagem de posts na próxima página manualmente
        next_page_start = page * page_size
        next_count = posts[next_page_start:next_page_start + page_size].count()

        # Obtenha a resposta paginada e adicione `next_count`
        paginated_response = paginator.get_paginated_response(serializer.data)
        paginated_response.data['next_count'] = next_count

        return paginated_response
    
class ExplorePostsView(APIView):
    """
    View para retornar os posts da aba Explorar.
    """
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if query:
            return SearchPostsView.as_view()(request._request)
        
        user = request.user
        # Definir o número da página e o tamanho da página
        page = int(request.query_params.get('page', 1))
        page_size = 10

        # Obter posts da aba Explorar
        posts = PostService.get_explore_posts(user, page=page, page_size=page_size)

        # Paginação
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        # Aplicar paginação nos posts da página atual
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})

        # Calcule o número de posts na próxima página manualmente
        next_page_start = page * page_size
        next_count = len(posts[next_page_start:next_page_start + page_size])

        # Obtenha a resposta paginada e adicione `next_count`
        paginated_response = paginator.get_paginated_response(serializer.data)
        paginated_response.data['next_count'] = next_count

        return paginated_response
    
class CommunityFeedView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if query:
            return SearchPostsView.as_view()(request._request)
        user = request.user
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        posts = PostService.get_feed_posts(user, page=page, page_size=page_size)
        posts_com_midia = posts.filter(media_files__isnull=False).distinct()

        paginator = PageNumberPagination()
        paginator.page_size = page_size

        # Paginação dos posts com mídia
        result_page = paginator.paginate_queryset(posts_com_midia, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})

        # Calcular o número de mídias na próxima página
        next_page_start = page * page_size
        proxima_pagina_posts = posts_com_midia[next_page_start:next_page_start + page_size]
        next_count = sum(post.media_files.count() for post in proxima_pagina_posts)

        # Obter a resposta paginada e adicionar `next_count`
        paginated_response = paginator.get_paginated_response(serializer.data)
        paginated_response.data['next_count'] = next_count

        return paginated_response

class TrendingHashtagsView(APIView):
    def get(self, request, *args, **kwargs):
          trending_hashtags = get_trending_hashtags()
          response_data = {
                "recommended_topics": [hashtag for hashtag, count in trending_hashtags]
            }
          return Response(response_data)

    

class SearchPostsView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '').strip()

        print('Query: ', query)

        if not query:
            return Response({"error": "Query parameter is required."}, status=400)
        

        # Filtra postagens com base no tema pesquisado (palavra-chave)
        posts = search_posts(query)

       
        
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Define o tamanho da página

        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        
        return paginator.get_paginated_response(serializer.data)



class RecommendedTopicsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Obtenha as hashtags das interações do usuário
        recommended_posts = hashtag_based_recommendation(user, limit=50)
        recommended_hashtags = set()

        for post in recommended_posts:
            recommended_hashtags.update(extract_hashtags(post.caption))
        
        limited_hashtags = list(recommended_hashtags)[:9]
        
        # Retorna apenas as hashtags exclusivas limitadas para exibição
        return Response({"recommended_topics": limited_hashtags})



class PostCommentsView(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = post.post_comments.filter(parent_comment=None)  # Assumindo que o related_name seja `post_comments`
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Verifique se o usuário já curtiu o comentário
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            message = "Like removed."
        else:
            comment.likes.add(request.user)
            message = "Like added."

        return Response({"message": message}, status=status.HTTP_200_OK)
    
class ReplyToCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        try:
            parent_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        text = request.data.get('content')
        if not text:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Cria uma resposta ao comentário usando o campo correto parent_comment
        reply = Comment.objects.create(
            user=request.user,
            content=text,
            parent_comment=parent_comment,  # Usando o campo correto para o comentário pai
            post=parent_comment.post  # O post é o mesmo do comentário original
        )

        # Passar o contexto da requisição ao serializer
        serializer = CommentSerializer(reply, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class UserPostListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        # Obtém o usuário pelo username
        user = get_object_or_404(User, username=username)
        
        # Pega os posts paginados desse usuário
        page = request.query_params.get('page', 1)
        paginated_posts = PostService.get_user_posts(request.user, user, page)
        
        # Serializa os posts
        serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
        
        return Response({
            'results': serializer.data,
            'page': paginated_posts.number,
            'total_pages': paginated_posts.paginator.num_pages
        })
    

class UserFavoritePostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username=None):
        # Se nenhum username for fornecido, usa o usuário autenticado
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user

        # Busca os posts onde o usuário está nos favoritos
        favorited_posts = Post.objects.filter(favorites=user)

        # Obtendo o número da página e o tamanho da página da query string, ou usando valores padrão
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)  # tamanho padrão de 10

        # Paginação usando o método correto
        paginated_posts = PostService.paginate_posts(favorited_posts, page, page_size)

        # Serializa os posts
        serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
        return Response({
            'results': serializer.data,
            'page': paginated_posts.number,
            'total_pages': paginated_posts.paginator.num_pages,
        })
    


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        # Deletar todas as mídias associadas antes de deletar o post
        for media in post.media_files.all():
            media.delete()
        # Deletar o post
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        post = self.get_object()

        # Log dos dados recebidos na requisição
        logger.info(f"Dados recebidos no update: {request.data}")

        caption = request.data.get('caption', post.caption)
        is_sensitive = request.data.get('is_sensitive', post.is_sensitive)
        is_private = request.data.get('is_private', post.is_private)
    
        logger.info(f"Legenda: {caption}, Sensível: {is_sensitive}, Privado: {is_private}")

        # Verificação e conversão dos campos de is_sensitive e is_private
        if isinstance(is_sensitive, str):
            is_sensitive = is_sensitive.lower() == 'true'
        if isinstance(is_private, str):
            is_private = is_private.lower() == 'true'

        # Atualizando o post
        post.caption = caption
        post.is_sensitive = is_sensitive
        post.is_private = is_private
        post.save()

        # Log das listas de arquivos recebidos
        existing_files = request.data.getlist('existing_files', [])
        remove_files = request.data.getlist('remove_files', [])
        print(f"Arquivos existentes: {existing_files}")
        print(f"Arquivos para remover: {remove_files}")


        # Processar arquivos para remover
        if remove_files:
            for media in post.media_files.all():
                if media.file in remove_files:
                    media.delete()

        # Verificar se existem arquivos para manter
        if existing_files:
          for media in post.media_files.all():
            # Extrair a URL completa do arquivo de mídia
            media_url = media.file.url  # Usar .url para garantir que estamos pegando a URL corretamente
          if media_url not in existing_files:
            print(f"Deletando arquivo não encontrado na lista de existentes: {media_url}")
            media.delete()

        # Verificar upload de novos arquivos
        files = request.FILES.getlist('files')
        

        if files:
            for file in files:
                try:
                    file_extension = file.name.split('.').pop().lower()    
                
                    # Fazer o upload do arquivo
                    if file_extension in ['mp4', 'webm', 'ogg']:
                        upload_result = upload(file, resource_type="video")
                    else:
                        upload_result = upload(file)

                    # Criar nova instância de PostMedia
                    PostMedia.objects.create(post=post, file=upload_result['secure_url'])
                    
                
                except Exception as e:
                    return Response({"error": f"Error uploading file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]  

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        
        # Atualiza o conteúdo e o timestamp de edição
        comment.content = request.data.get('content', comment.content)
        comment.edited_at = timezone.now()
        comment.save()
        
        return Response(self.get_serializer(comment).data)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProfileHighlightPostsView2(APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            target_user = User.objects.get(username=username)
            # Filtrar posts mais populares do usuário
            highlighted_posts = Post.objects.filter(
                user=target_user,
                is_private=False,
                is_sensitive=False
            ).annotate(
                engagement=Count('likes') + Count('comments_count') + Count('favorites')
            ).order_by('-engagement')[:5]  # Limite de 5 posts

            serializer = PostSerializer(highlighted_posts, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        

class ProfileHighlightedMediaView(APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            target_user = UserData.objects.get(user__username=username)

            if target_user.is_private:
            # Verificar se o usuário solicitante é o próprio usuário ou um amigo/seguidor
                if request.user != target_user.user and not (
                FriendService.are_friends(request.user.id, target_user.id) or 
                FollowService.is_following(request.user.id, target_user.id)
            ): return Response([], status=200)
                
            # Obter posts de destaque com base no engajamento
            highlighted_posts = Post.objects.filter(
                user=target_user.user,
                is_private=False,
                is_sensitive=False
            ).annotate(
                engagement=Count('likes') + Count('post_comments') + Count('favorites')
            ).order_by('-engagement')[:5]  # Limite de 5 posts

            # Serializar apenas as mídias dos posts
            media = []
            for post in highlighted_posts:
                media.extend(PostMediaSerializer(post.media_files.all()[:6], many=True).data)
            
            return Response(media, status=200)
        
        except UserData.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        

class RecommendedProfilesView(APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            target_user = User.objects.get(username=username)
            
            # Exclui o próprio usuário alvo e o usuário autenticado das recomendações
            recommended_users = User.objects.exclude(
                id__in=[target_user.id, request.user.id]
            ).annotate(
                similar_interactions=Count('interaction', filter=Q(interaction__post__user=target_user))
            ).order_by('-similar_interactions')[:4]

            # Serializa os usuários recomendados
            serializer = UserSerializer(recommended_users, many=True, context={'request': request}, exclude_sensitive_fields=True)
            recommended_data = serializer.data

            if request.user.is_authenticated:
                for idx, user_data in enumerate(recommended_data):
                    user = recommended_users[idx]  # Usuário recomendado

                    # Verifica se o usuário autenticado segue o usuário recomendado
                    is_following = FollowService.is_following(
                        request.user.id,
                        user.id
                    )

                    # Atualiza os dados serializados com as informações de seguimento
                    user_data["is_following"] = is_following
            else:
                for user_data in recommended_data:
                    user_data["is_following"] = False

            return Response(recommended_data, status=200)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            # Busca o post pelo ID fornecido
            print('post_id: ', post_id)
            post = Post.objects.get(id=post_id)
            print('post enviado: ', post)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        

class PostRecommendationView(APIView):
    def get(self, request, post_id):

        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            # Obtenha IDs de posts similares
            
            similar_post_ids = get_similar_posts(post_id, df_posts, tfidf_matrix, n=10)
            
            # Obtenha os objetos de post usando os IDs
            recommended_posts = Post.objects.filter(id__in=similar_post_ids)  
            posts_com_midia = recommended_posts.filter(media_files__isnull=False).distinct()          

            paginator = PageNumberPagination()
            paginator.page_size = page_size

            # Paginação dos posts com mídia
            result_page = paginator.paginate_queryset(posts_com_midia, request)
            serializer = PostSerializer(result_page, many=True, context={'request': request})
            
            next_page_start = page * page_size
            proxima_pagina_posts = posts_com_midia[next_page_start:next_page_start + page_size]
            next_count = sum(post.media_files.count() for post in proxima_pagina_posts)

            # Obter a resposta paginada e adicionar `next_count`
            paginated_response = paginator.get_paginated_response(serializer.data)
            paginated_response.data['next_count'] = next_count

            return paginated_response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class MessageHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        try:
            room = Room.objects.get(name=room_name)
            messages = Message.objects.filter(room=room).order_by('timestamp')  # Ordena por data
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=404)