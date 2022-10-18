from django.urls import path
from .views import Login, Logout, RegisterView, \
    ProfileView, ProfileUpdateView, \
    FriendsView, SendFriendRequest, accept_friend_request, decline_friend_request


urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:profile_id>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send_friend_request/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
]
