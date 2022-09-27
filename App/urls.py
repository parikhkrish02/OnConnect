from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('likePost', views.likePost, name='likePost'),
    path('signUp', views.signUp, name='signUp'),
    path('signIn', views.signIn, name='signIn'),
    path('logout/', views.logout, name='logout'),
]
