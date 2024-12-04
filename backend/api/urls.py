from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import  TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='register'),
    path('user/token/', GetToken.as_view(), name='get_token'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('user/data/', UserDataView.as_view(), name='user_data'),
    path('user/update/', UserViewSet.as_view({'patch': 'partial_update'}), name='user-update'),
    path('check-usertag/', CheckUserTagView.as_view(), name='check_usertag'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('request-reset-password/', RequestResetPasswordView.as_view(), name='request_reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('send-friend-request/<int:user_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('remove-or-reject-friend/<int:target_user_id>/', RejectOrRemoveFriendView.as_view(), name='send_friend_request'),
    path('accept-friend-request/<int:notification_id>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('messages/history/<str:room_name>/', MessageHistoryView.as_view(), name='message-history'),
    path('delete-notification/<int:notification_id>/', DeleteNotificationView.as_view(), name='delete_notification'),
    path('notifications/mark-all-as-read/', MarkAllAsReadNotificationAsReadView.as_view(), name='mark_all_notifications_as_read'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/<str:username>/highlighted-media/', ProfileHighlightedMediaView.as_view(), name='user_profile_highlighted'),
    path('profile/<str:username>/recommended-profiles/', RecommendedProfilesView.as_view(), name='user_profile_recommended'),
    path('add-friend/<int:user_id>/', AddFriendView.as_view(), name='add-friend'),
    path('notifications/create/', CreateNotificationView.as_view(), name='create_notification'),
    path('notifications/', GetNotificationsView.as_view(), name='get_notifications'),
    path('notifications/<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/recommendations/', PostRecommendationView.as_view(), name='post-recommendations'),
    path('posts/following/', PostListFollowingView.as_view(), name='following-post-list'),
    path('posts/cflow/', CommunityFeedView.as_view(), name='post-list'),
    path('trending-hashtags/', TrendingHashtagsView.as_view(), name='post-list'),
    path('posts/recommended-topics/', RecommendedTopicsView.as_view(), name='post-list'),
    path('posts/explore/', ExplorePostsView.as_view(), name='post-list'),
    path('posts/search/', SearchPostsView.as_view(), name='-search-post-list'),
    path('posts/user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('posts/<str:username>/favorites/', UserFavoritePostsView.as_view(), name='user-favorites'),
    path('follow-toggle/<int:target_user_id>/', FollowToggleView.as_view(), name='follow_toggle'),
    path('search-users/', UserSearchView.as_view(), name='search_users'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('posts/<int:post_id>/comment/', CommentPostView.as_view(), name='comment_post'),
    path('posts/<int:post_id>/comments/', PostCommentsView.as_view(), name='comment_post'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('posts/<int:post_id>/share/', SharePostView.as_view(), name='share_post'),
    path('comments/<int:comment_id>/like/', LikeCommentView.as_view(), name='like_comment'),
    path('comments/<int:comment_id>/reply/', ReplyToCommentView.as_view(), name='reply_comment'),
    path('posts/<int:post_id>/favorite/', FavoritePostView.as_view(), name='favorite_post'),
    path('', include(router.urls)),
    path('api-auth/', include("rest_framework.urls"))
]


