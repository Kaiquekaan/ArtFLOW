from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from cloudinary.uploader import destroy
from django.utils import timezone

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recovery_email = models.EmailField(blank=True, null=True)  # E-mail de recuperação
    two_factor_enabled = models.BooleanField(default=False)    # Indica se a 2FA está ativa
    two_factor_code = models.CharField(max_length=6, blank=True, null=True)
    displayname = models.CharField(max_length=100, blank=True)
    user_tag = models.CharField(max_length=30, unique=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    banner_picture_url = models.URLField(blank=True, null=True) 
    profile_picture_id = models.CharField(max_length=255, null=True, blank=True)  # ID da imagem no Cloudinary
    banner_picture_id = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField()
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    is_online = models.BooleanField(default=False) 
    is_private = models.BooleanField(default=False)

    
    
    def __str__(self):
        return f"{self.user.username} - {self.user_tag}"
    
    def posts(self):
        return self.user.posts.all()
    
    def count_posts(self):
        return self.user.posts.count()
    
    def count_friends(self):
        return self.friends.count()
    
    def count_followers(self):
        return Follower.objects.filter(user=self).count()

    def count_following(self):
        return Follower.objects.filter(follower=self).count()
    

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'Message'),
        ('friend_request', 'Friend Request'),
        ('friend_accepted', 'Friend Accepted'),
        ('tag', 'Tag'),

        # Adicione outros tipos de notificação conforme necessário
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.TextField()  # Conteúdo da notificação
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)   
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserData, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserData, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Request from {self.from_user} to {self.to_user}"



class Follower(models.Model):
    user = models.ForeignKey(UserData, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(UserData, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'follower')



    
class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to="achievement_icons/")
    users= models.ManyToManyField(User, related_name='achievement')

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sensitive = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    favorites = models.ManyToManyField(User, related_name='favorited_posts', blank=True)
    last_edited_at = models.DateTimeField(null=True, blank=True)
    comments_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if self.pk:  # Verifica se o post já existe (para distinguir entre criar e editar)
            self.last_edited_at = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def toggle_like(self, user):
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
            return 'unliked'
        else:
            self.likes.add(user)
            return 'liked'
    
    def toggle_favorite(self, user):
        if self.favorites.filter(id=user.id).exists():
            self.favorites.remove(user)
            return 'unfavorited'
        else:
            self.favorites.add(user)
            return 'favorited'


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_files')
    file = CloudinaryField('media')

    def __str__(self):
        return f"Media for post {self.post.id}"
    
    def delete(self, *args, **kwargs):
        # Extraindo o public_id da URL do arquivo no Cloudinary
        if self.file:
            # A URL completa é algo como 'https://res.cloudinary.com/.../upload/v123456/tjyecamcn4ysxllobvy3.jpg'
            # Precisamos extrair apenas o 'tjyecamcn4ysxllobvy3'
            public_id = self.extract_public_id(self.file.url)
            if public_id:
                destroy(public_id)  # Deletar a mídia no Cloudinary
        # Deletar a mídia no banco de dados
        super().delete(*args, **kwargs)

    def extract_public_id(self, url):
        # Extrair o public_id da URL
        parts = url.split('/')
        public_id_with_extension = parts[-1]  # Obtém 'tjyecamcn4ysxllobvy3.jpg'
        public_id = public_id_with_extension.split('.')[0]  # Remove a extensão, ficando apenas 'tjyecamcn4ysxllobvy3'
        return public_id
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')  # Defina um related_name único
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.post.comments_count += 1
        super().save(*args, **kwargs)
        self.post.save()

    def delete(self, *args, **kwargs):
        self.post.comments_count -= 1
        self.post.save()
        super().delete(*args, **kwargs)

    def likes_count(self):
        return self.likes.count()
    

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('favorite', 'Favorite')  # Novo tipo de interação
    ]
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.interaction_type} {self.post}"
    


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name='rooms')

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)