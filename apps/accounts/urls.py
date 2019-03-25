from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('<str:username>/', views.post_list, name='post_list'),
    path('<str:username>/follow/', views.follow, name='follow'),
    # path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    # path('profile/', views.ProfileDetail.as_view(), name='profile_detail'),
    # path('profile/edit/', views.ProfileUpdate.as_view(), name='profile_update'),
]
