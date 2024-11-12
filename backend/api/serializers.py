from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import UserData, Post, PostMedia, Comment, Follower, Message
from django.conf import settings
from cloudinary.uploader import upload
from cloudinary.uploader import destroy
from cloudinary.exceptions import Error
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random
import re



class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['friends']




class FollowService:
    def __init__(self, user_id, target_user_id):
        self.user_id = user_id
        self.target_user_id = target_user_id

    def toggle_follow(self):
        try:
            # Tenta encontrar um registro de seguimento existente
            follow = Follower.objects.get(user_id=self.target_user_id, follower_id=self.user_id)
            # Se o registro existir, significa que o usuário já segue, então vamos desfazer o follow
            follow.delete()
            return {"status": "unfollowed"}
        except Follower.DoesNotExist:
            # Se não existir, vamos criar o registro e seguir o usuário
            Follower.objects.create(user_id=self.target_user_id, follower_id=self.user_id)
            return {"status": "followed"}
        
    def is_following(user_id, target_user_id):
        return Follower.objects.filter(
            follower_id=user_id,
            user_id=target_user_id
        ).exists()


class FollowersDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']    


class PostMediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    class Meta:
        model = PostMedia
        fields = ['file', 'file_url']

    def get_file_url(self, obj):
        return obj.file.url if obj.file else None


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_tag = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    edited_at = serializers.DateTimeField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'profile_picture_url', 'created_at','edited_at', 'likes_count', 'has_liked', 'replies','parent_comment', 'user_tag']

    def get_profile_picture_url(self, obj):
        return obj.user.userdata.profile_picture_url
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_user_tag(self, obj):
        return obj.user.userdata.user_tag

    def get_has_liked(self, obj):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        
        # Verifica se o usuário está autenticado e se ele curtiu o comentário
        return obj.likes.filter(id=user.id).exists() if user else False
    
    def get_replies(self, obj):
        replies = obj.replies.all()  # Usa a relação reversa para obter replies
        serialized_replies = CommentSerializer(replies, many=True, context=self.context).data
        
        # Adiciona o usuário do comentário pai para cada resposta
        for reply in serialized_replies:
            if reply['parent_comment']:  # Se é uma resposta a outro comentário
                parent_comment = Comment.objects.filter(id=reply['parent_comment']).first()
                if parent_comment:
                    reply['parent_user'] = parent_comment.user.userdata.user_tag  # Atribui o usuário do comentário pai
                else:
                    reply['parent_user'] = None  # Não encontrou o comentário pai
            else:
                reply['parent_user'] = None  # Não é uma resposta a um comentário

        return serialized_replies



class PostSerializer(serializers.ModelSerializer):
    media_files = PostMediaSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True) 
    user_displayname = serializers.CharField(source='user.userdata.displayname', read_only=True)   
    user_tag = serializers.CharField(source='user.userdata.user_tag', read_only=True)  
    profile_picture = serializers.CharField(source='user.userdata.profile_picture_url', read_only=True)  
    has_liked = serializers.SerializerMethodField()
    has_favorited = serializers.SerializerMethodField()
    last_edited_at = serializers.DateTimeField(read_only=True)
    hashtags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'created_at', 'is_sensitive', 'is_private', 
                  'likes_count','favorites_count', 'comments_count', 'media_files',
                  'user_username', 'user_displayname', 'user_tag', 'profile_picture', 'has_liked', 'has_favorited', 'last_edited_at', 'hashtags']  # Não esqueça de adicionar os novos campos aqui

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_favorites_count(self, obj):  # Adicione este método
        return obj.favorites.count()
    
    def get_has_liked(self, obj):
      request = self.context.get('request', None)
      if request and request.user.is_authenticated:
         return obj.likes.filter(id=request.user.id).exists()
      return False

    def get_has_favorited(self, obj):
      request = self.context.get('request', None)
      if request and request.user.is_authenticated:
        return obj.favorites.filter(id=request.user.id).exists()
      return False
    
    def get_comments(self, obj):
        # Filtra apenas os comentários que não têm parent_comment
        comments = obj.post_comments.filter(parent_comment=None)
        return CommentSerializer(comments, many=True, context=self.context).data
    
    def get_hashtags(self, obj):
        # Extrai hashtags do caption
        return re.findall(r'#([\wÀ-ÿ]+)', obj.caption)



DEFAULT_PROFILE_PICTURES = [
    "https://res.cloudinary.com/dynymtlrt/image/upload/v1724900246/default-img-perfil/uitqsvayiua7nbh8dcru.jpg",
    "https://res.cloudinary.com/dynymtlrt/image/upload/v1724900246/default-img-perfil/vnah1vjvm0iooft4afn4.jpg",
    "https://res.cloudinary.com/dynymtlrt/image/upload/v1724900246/default-img-perfil/a3kyhkx4nupdh8wbragg.jpg",
    "https://res.cloudinary.com/dynymtlrt/image/upload/v1724900246/default-img-perfil/fsnckgqd0qels3scumcq.jpg",
    "https://res.cloudinary.com/dynymtlrt/image/upload/v1724900246/default-img-perfil/aolk1oltith7evzhry4j.jpg"
    # Adicione aqui todas as URLs das imagens de perfil padrão no Cloudinary
]

class UserDataSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    recovery_email = serializers.EmailField(allow_blank=True, required=False)
    two_factor_enabled = serializers.BooleanField(required=False)
    displayname = serializers.CharField(allow_blank=True, required=False)
    profile_picture_url = serializers.URLField(allow_blank=True, required=False)
    banner_picture_url = serializers.URLField(allow_blank=True, required=False)
    profile_picture_id = serializers.CharField(allow_blank=True, required=False)  # Inclua o ID do Cloudinary
    banner_picture_id = serializers.CharField(allow_blank=True, required=False)
    posts = PostSerializer(many=True, read_only=True)
    friends_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_private = serializers.BooleanField(required=False)
    

    class Meta:
        model = UserData
        fields = ['user_id','user_tag', 'profile_picture_url','banner_picture_url','profile_picture_id', 'banner_picture_id', 'bio', 'birth_date', 
                  'posts', 'friends','friends_count','posts_count', 'followers_count', 'following_count', 'username', 'displayname', 'is_private',
                  'recovery_email', 'two_factor_enabled', 'two_factor_code']
        
    
    def __init__(self, *args, **kwargs):
        exclude_posts_friends = kwargs.pop('exclude_posts_friends', False)
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(UserDataSerializer, self).__init__(*args, **kwargs)

        if exclude_posts_friends:
            self.fields.pop('posts', None)
            self.fields.pop('friends', None)
        
        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field, None)

    def create(self, validated_data):
        friends_data = validated_data.pop('friends', [])  # Retirar, se houver
        followers_data = validated_data.pop('followers_ids', [])  # Retirar, se houver

        # Cria o UserData sem friends ou followers inicialmente
        user_data = UserData.objects.create(**validated_data)

        # Adicionar amigos e seguidores apenas se necessário
        user_data.friends.set(friends_data)
        user_data.followers.set(followers_data)
        user_data.save()

        return user_data
    
    def update(self, instance, validated_data):

        new_profile_picture_url = validated_data.get('profile_picture_url')
        new_banner_picture_url = validated_data.get('banner_picture_url')

        # Excluir a antiga imagem de perfil se ela não for uma imagem padrão e se uma nova for enviada
        if new_profile_picture_url and instance.profile_picture_url not in DEFAULT_PROFILE_PICTURES:
            if instance.profile_picture_id:  # Certifique-se de que há um ID de imagem para excluir
                destroy(instance.profile_picture_id)  # Excluir a imagem antiga do Cloudinary

        # Excluir a antiga imagem de banner se uma nova for enviada
        if new_banner_picture_url and instance.banner_picture_url not in DEFAULT_PROFILE_PICTURES:
            if instance.banner_picture_id:  # Certifique-se de que há um ID de imagem para excluir
                destroy(instance.banner_picture_id)  # Excluir a imagem antiga do Cloudinary

        # Atualiza cada campo com o valor de `validated_data`, se fornecido
        instance.profile_picture_url = new_profile_picture_url or instance.profile_picture_url
        instance.profile_picture_id = validated_data.get('profile_picture_id', instance.profile_picture_id)
        instance.banner_picture_url = new_banner_picture_url or instance.banner_picture_url
        instance.banner_picture_id = validated_data.get('banner_picture_id', instance.banner_picture_id)

        instance.displayname = validated_data.get('displayname', instance.displayname)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.user_tag = validated_data.get('user_tag', instance.user_tag)
        instance.is_private = validated_data.get('is_private', instance.is_private)
        
        # Salva as mudanças no perfil
        instance.save()
        return instance

    
    def get_followers_count(self, obj):
        return obj.count_followers()

    def get_following_count(self, obj):
        return obj.count_following()
    
    def get_friends_count(self, obj):
        return obj.count_friends()

    def get_posts_count(self, obj):
        return obj.count_posts()
    




class UserSerializer(serializers.ModelSerializer):
    userdata = UserDataSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'userdata']

    def __init__(self, *args, **kwargs):
        # Verifica se é necessário excluir os campos `password` e `email`
        exclude_sensitive_fields = kwargs.pop('exclude_sensitive_fields', False)
        exclude_user_fields = kwargs.pop('exclude_user_fields', False)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if exclude_user_fields:
            self.fields.pop('password', None)

        if exclude_user_fields:
            self.fields['userdata'] = UserDataSerializer(exclude_fields=[ 'friends',  'banner_picture_id','posts', 
            'profile_picture_id', 'posts', 'two_factor_code'])
        
        # Remove `password` e `email` caso `exclude_sensitive_fields` seja `True`
        if exclude_sensitive_fields:
            self.fields.pop('email', None)
            self.fields.pop('password', None)

        if exclude_sensitive_fields:
            self.fields['userdata'] = UserDataSerializer(exclude_fields=['birth_date', 'friends', 'is_private', 'banner_picture_id','posts', 'username', 
            'profile_picture_id','recovery_email', 'two_factor_enabled', 'two_factor_code'])

    def create(self, validated_data):
        userdata_data = validated_data.pop('userdata', {})

        # Criar o usuário com email, username e senha
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Selecionar uma imagem de perfil aleatória
        profile_picture_url = random.choice(DEFAULT_PROFILE_PICTURES)

        # Criar o UserData associado, sem amigos e seguidores
        user_data = UserData.objects.create(
            user=user,
            user_tag=userdata_data['user_tag'],
            birth_date=userdata_data['birth_date'],
            profile_picture_url=profile_picture_url,
            bio=userdata_data.get('bio', '')
        )

        # Se houver friends e followers, adicione-os usando o método set
        friends_data = userdata_data.get('friends', [])
        followers_data = userdata_data.get('followers', [])

        if friends_data:
            user_data.friends.set(friends_data)

        if followers_data:
            user_data.followers.set(followers_data)

        return user


    def update(self, instance, validated_data):
        userdata_data = validated_data.pop('userdata', {})
        profile = instance.userdata

        UserDataSerializer().update(profile, userdata_data)

        # Atualização do usuário principal
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance
    
class GetTokenSerializer(TokenObtainPairSerializer):
    code = serializers.CharField(required=False, allow_blank=True) 
    
    def validate(self, attrs):
        print("Atributos recebidos no validate:", attrs) 
        data_input = attrs.get("username", "")
        password = attrs.get("password", "")
        code = attrs.get("code", None)  # Verifica se o código foi enviado

        print('code vindo: ', code)
        print('senha vindo: ', password)
        print('data vindo: ', data_input)

        try:
            user = User.objects.get(email=data_input)
            attrs['username'] = user.username
        except User.DoesNotExist:
            attrs['username'] = data_input

        # Autenticar o usuário
        user = authenticate(username=attrs['username'], password=password)
        if user is None:
            raise serializers.ValidationError("Credenciais inválidas.")

        # Verificar se o 2FA está ativado
        if user.userdata.two_factor_enabled:
            # Caso o código de 2FA não tenha sido enviado, envie-o por e-mail e peça o código
            if not code:
                generated_code = "{:06d}".format(random.randint(0, 999999))
                user.userdata.two_factor_code = generated_code
                user.userdata.save()

                send_mail(
                    "Seu código de verificação - ArtFlow",
                    f"Seu código de verificação é {generated_code}",
                    "noreply@seusite.com",
                    [user.email],
                    fail_silently=False,
                )

                return {"detail": "2FA necessário. Verifique o código enviado para seu e-mail."}

            # Verifique o código 2FA enviado
            if str(user.userdata.two_factor_code) != str(code):
                print('code recebido: ', code)
                print('code real: ', user.userdata.two_factor_code)
                raise serializers.ValidationError("Código de 2FA incorreto.")

            # Limpe o código após verificação
            user.userdata.two_factor_code = None
            user.userdata.save()

        # Se 2FA estiver desativado ou validado com sucesso, gere os tokens
        return super().validate(attrs)

    

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)  # Inclui o nome de usuário
    sender_displayname = serializers.CharField(source='sender.userdata.displayname', read_only=True)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['sender_username', 'sender_displayname','profile_picture_url', 'content', 'timestamp'] 

    def get_profile_picture_url(self, obj):
        return obj.sender.userdata.profile_picture_url
