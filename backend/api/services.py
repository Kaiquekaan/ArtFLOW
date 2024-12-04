from django.db.models import Count
from .models import Follower, Notification, UserData, FriendRequest, Comment, Interaction, Post, SharedPost  # Supondo que você tenha um model Follow
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.recommendation_service import *
import random
from django.utils import timezone
from datetime import timedelta

class FollowService:
    @staticmethod
    def follow_toggle(user_id, target_user_id):
        try:
            follow, created = Follower.objects.get_or_create(
                follower_id=user_id,
                user_id=target_user_id
            )
            if not created:
                follow.delete()
                return "Unfollowed"
            return "Followed"
        except Exception as e:
            return str(e)

    @staticmethod
    def is_following(user_id, target_user_id):
        return Follower.objects.filter(
            follower_id=user_id,
            user_id=target_user_id
        ).exists()

    @staticmethod
    def get_follow_counts(user_id):
        following_count = Follower.objects.filter(follower_id=user_id).count()
        followers_count = Follower.objects.filter(followed_id=user_id).count()
        return {
            "following_count": following_count,
            "followers_count": followers_count
        }



class FriendService:
    @staticmethod
    def toggle_friend(user_id, target_user_id):
        try:
            user_data = UserData.objects.get(user_id=user_id)
            target_user_data = UserData.objects.get(user_id=target_user_id)
            
            # Verificar se já são amigos
            if target_user_data in user_data.friends.all():
                user_data.friends.remove(target_user_data)
                target_user_data.friends.remove(user_data)
                return "Unfriended"
            else:
                user_data.friends.add(target_user_data)
                target_user_data.friends.add(user_data)
                return "Friended"
            
        


        except Exception as e:
            return str(e)

    @staticmethod
    def are_friends(user_id, target_user_id):
        user_data = UserData.objects.get(user_id=user_id)
        target_user_data = UserData.objects.get(user_id=target_user_id)
        return target_user_data in user_data.friends.all()
    
    @staticmethod
    def pending_request_friends(user_id, target_user_id):
        result = FriendRequest.objects.filter(from_user_id=user_id, to_user_id=target_user_id ).exists() or FriendRequest.objects.filter(from_user_id=target_user_id, to_user_id=user_id).exists()

        return result

    @staticmethod
    def get_friend_counts(user_id):
        user_data = UserData.objects.get(user_id=user_id)
        return {
            "friend_count": user_data.friends.count()
        }


    @staticmethod
    def reject_or_remove_friend(user_id, target_user_id):
        try:
            # Tenta remover a solicitação de amizade se ela existir
            friend_request = FriendRequest.objects.filter(from_user=user_id, to_user=target_user_id).first()
            print('dados da friend_request ', friend_request)
            if friend_request:
                friend_request.delete()
                # Aqui você também pode remover a notificação, se desejar
                Notification.objects.filter(sender_id=user_id , user_id=target_user_id, notification_type='friend_request').delete()
                return "Friend request rejected"
            
            # Caso contrário, tenta remover a amizade, se já for amigo
            user_data = UserData.objects.get(user_id=user_id)
            friend = user_data.friends.filter(id=target_user_id).first()
            if friend:
                user_data.friends.remove(friend)
                return "Friendship removed"
            
            return "No action taken"
        except Exception as e:
            return str(e)

    @staticmethod
    def get_online_friends(user_id):
        user_data = UserData.objects.get(user_id=user_id)
        friends_online = user_data.friends.filter(is_online=True)
        return [{'username': friend.user.username, 'user_tag': friend.user_tag, 'profile_picture_url': friend.profile_picture_url} for friend in friends_online]
    
    @staticmethod
    def get_friends(user_id):
        user_data = UserData.objects.get(user_id=user_id)
        friends = user_data.friends.all()
        return [{'username': friend.user.username, 'user_tag': friend.user_tag, 'profile_picture_url': friend.profile_picture_url, 'id': friend.id } for friend in friends]



class NotificationService:
    @staticmethod
    def create_notification(user, notification_type, content, sender_id=None):
        Notification.objects.create(
            user=user,
            notification_type=notification_type,
            content=content,
            sender_id=sender_id 
        )
    
    @staticmethod
    def get_notifications(user):
        return Notification.objects.filter(user=user).order_by('-created_at')


    @staticmethod
    def get_sender_by_notification(notification_id):
        notification = Notification.objects.get(id=notification_id)
        sender_id = notification.sender_id  # ou como estiver estruturado
        return sender_id

    
    @staticmethod
    def mark_as_read(notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False
        

    @staticmethod
    def delete_notification(notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return True
        except Notification.DoesNotExist:
            return False


    @staticmethod
    def mark_all_as_read(user):
        # Marca todas as notificações de um usuário como lidas
        notifications = Notification.objects.filter(user=user, is_read=False)
        notifications.update(is_read=True)
        return True
    



class PostInteractionService:
    
    @staticmethod
    def like_post(user, post):
        result = post.toggle_like(user)
        PostInteractionService._save_interaction(user, post, 'like' if result == 'liked' else None)
        return result

    @staticmethod
    def comment_post(user, post, content):
        # Criação do comentário

        comment = Comment.objects.create(
            post=post,
            user=user,
            content=content,
        )

        # Atualiza o contador de comentários do post
       
        post.save()

        # Salva a interação no modelo Interaction
        PostInteractionService._save_interaction(user, post, 'comment')

        return comment

    @staticmethod
    def favorite_post(user, post):
        result = post.toggle_favorite(user)
        PostInteractionService._save_interaction(user, post, 'favorite' if result == 'favorited' else None)
        return result

    @staticmethod
    def share_post(user, post):
        # Lógica de compartilhamento (dependendo da implementação de compartilhamento)
        SharedPost.objects.create(user=user, post=post)
        PostInteractionService._save_interaction(user, post, 'share')
        return "shared"

    @staticmethod
    def _save_interaction(user, post, interaction_type):
        if interaction_type:
            Interaction.objects.create(user=user, post=post, interaction_type=interaction_type)




class PostService:
    
    @staticmethod
    def get_user_posts(request_user, target_user, page=1, page_size=10):
        """
        Retorna as postagens de um usuário específico, paginadas.
        """
        try:
            target_user_data = UserData.objects.get(user=target_user)
        except UserData.DoesNotExist:
            return PostService.paginate_posts([], page, page_size)  # Ou lançar uma exceção apropriada, dependendo da lógica da sua aplicação

        # Verificar se o perfil é privado
        if target_user_data.is_private:
            # Verificar se o usuário solicitante é o próprio usuário ou um amigo/seguidor
            if request_user != target_user and not (
                FriendService.are_friends(request_user.id, target_user.id) or 
                FollowService.is_following(request_user.id, target_user.id)
            ): 
             return PostService.paginate_posts([], page, page_size)

        # Se passar pelas verificações, retornar os posts
        posts = Post.objects.filter(user=target_user).order_by('-created_at')
        return PostService.paginate_posts(posts, page, page_size)
    
    @staticmethod
    def get_feed_posts(user, page=1, page_size=10):
        # Carregar o modelo SVD cacheado
        svd_model = get_cached_svd_model()

        # Obter a matriz de interações
        user_item_matrix = build_user_item_matrix()

        # Construir a matriz TF-IDF para recomendações baseadas em legendas
        df_posts, tfidf_matrix = build_tfidf_matrix()

        # Obter posts dos amigos
        friend_ids = user.userdata.friends.values_list('id', flat=True)
        recent_posts = Post.objects.filter(user__id__in=friend_ids, created_at__gte=timezone.now() - timedelta(days=1), is_private=False, is_sensitive=False).order_by('-created_at')
        older_posts = Post.objects.filter(user__id__in=friend_ids, created_at__lt=timezone.now() - timedelta(days=1), is_private=False, is_sensitive=False).order_by('-created_at')

        posts = recent_posts | older_posts 

        following_ids = Follower.objects.filter(follower=user.id).values_list('user_id', flat=True)

        if posts.exists():
            post_id = posts.first().id if posts.first() else None
            if post_id:
                hybrid_recommendations = hybrid_recommendation(
                    user.id, post_id, user_item_matrix, svd_model, df_posts, tfidf_matrix, excluded_user_ids=following_ids, n=50
                )
                recommended_posts = Post.objects.filter(id__in=hybrid_recommendations).order_by('-created_at')
                # Combine os posts de amigos e recomendados
                combined_posts = posts | recommended_posts
            else:
                combined_posts = posts
        else:
            # Se não houver posts de amigos, trazer apenas posts recomendados
            hybrid_recommendations = hybrid_recommendation(
                user.id, None, user_item_matrix, svd_model, df_posts, tfidf_matrix, excluded_user_ids=following_ids, n=50
            )
            recommended_posts = Post.objects.filter(id__in=hybrid_recommendations).order_by('-created_at')
            combined_posts = list(recommended_posts)

        

        # Certifique-se de que está retornando um queryset, não uma lista
        if not combined_posts:
            return Post.objects.none()  # Retorna um queryset vazio
        else:
            return Post.objects.filter(id__in=[post.id for post in combined_posts]).order_by('-created_at')
        

    @staticmethod
    def get_feed_following_posts(user, page=1, page_size=10):
        # Carregar o modelo SVD cacheado
        svd_model = get_cached_svd_model()

        # Obter a matriz de interações
        user_item_matrix = build_user_item_matrix()

        # Construir a matriz TF-IDF para recomendações baseadas em legendas
        df_posts, tfidf_matrix = build_tfidf_matrix()

        # Obter posts dos amigos
        following_ids = list(Follower.objects.filter(follower=user.id).values_list('user_id', flat=True))

        print('seguindo: ', following_ids)
        recent_posts = Post.objects.filter(
        user__id__in=following_ids,
        created_at__gte=timezone.now() - timedelta(days=1),
        is_private=False, is_sensitive=False
        ).order_by('-created_at')
    
        older_posts = Post.objects.filter(
        user__id__in=following_ids,
        created_at__lt=timezone.now() - timedelta(days=1),
        is_private=False, is_sensitive=False
        ).order_by('-created_at')


        posts = recent_posts | older_posts 

        friend_ids = user.userdata.friends.values_list('id', flat=True)

        if posts.exists():
            post_id = posts.first().id if posts.first() else None
            if post_id:
                hybrid_recommendations = hybrid_recommendation(
                    user.id, post_id, user_item_matrix, svd_model, df_posts, tfidf_matrix, excluded_user_ids=friend_ids, n=50
                )
                recommended_posts = Post.objects.filter(id__in=hybrid_recommendations).order_by('-created_at')
                # Combine os posts de amigos e recomendados
                combined_posts = posts | recommended_posts
            else:
                combined_posts = posts
        else:
            # Se não houver posts de amigos, trazer apenas posts recomendados
            hybrid_recommendations = hybrid_recommendation(
                user.id, None, user_item_matrix, svd_model, df_posts, tfidf_matrix, excluded_user_ids=friend_ids, n=50
            )
            recommended_posts = Post.objects.filter(id__in=hybrid_recommendations).order_by('-created_at')
            combined_posts = list(recommended_posts)

        

        # Certifique-se de que está retornando um queryset, não uma lista
        if not combined_posts:
            return Post.objects.none()  # Retorna um queryset vazio
        else:
            return Post.objects.filter(id__in=[post.id for post in combined_posts]).order_by('-created_at')

    
    @staticmethod
    def get_explore_posts(user, page=1, page_size=10):
        # Obter posts populares e filtrar por privado e sensível
        popular_posts = Post.objects.filter(is_private=False, is_sensitive=False).annotate(
            total_engagement=Count('likes') + Count('favorites')
        ).order_by('-total_engagement', '-created_at')[:50]

        hashtag_posts = hashtag_based_recommendation(user, limit=50).annotate(
            total_engagement=Count('likes') + Count('favorites')
        )

# Combine os querysets diretamente sem convertê-los em listas
        combined_posts = popular_posts.union(hashtag_posts)

        # Filtrar posts sensíveis e privados
        combined_posts = [post for post in combined_posts if not post.is_private and not post.is_sensitive]

        # Ordenar pela data de criação e engajamento (likes + favoritos)
        combined_posts.sort(key=lambda post: post.total_engagement, reverse=True)

        # Paginar os posts
        return combined_posts
    
    @staticmethod
    def get_posts_by_hashtag(hashtag):
        # Certifique-se de que o hashtag está devidamente formatado
        return Post.objects.filter(caption__icontains=f'#{hashtag}', is_private=False, is_sensitive=False)
    
    @staticmethod
    def paginate_posts(posts, page, page_size):
        """
        Pagina as postagens.
        """
        paginator = Paginator(posts, page_size)
        try:
            paginated_posts = paginator.page(page)
        except PageNotAnInteger:
            paginated_posts = paginator.page(1)  # Se a página não for um número, retorna a primeira página
        except EmptyPage:
            paginated_posts = paginator.page(paginator.num_pages) 
        except:
            raise NotFound("Página não encontrada.")
        return paginated_posts