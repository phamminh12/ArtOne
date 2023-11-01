from django.urls import path
from . import views

# m > f > v > u

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('discover', views.discover, name="discover"),
    path('news', views.news, name="news"),
    path('picture/<str:pk>/', views.picture, name="picture"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    
    path('create-picture/', views.createPicture, name="create-picture"),
    path('update-picture/<str:pk>/', views.updatePicture, name="update-picture"),
    path('delete-picture/<str:pk>/', views.deletePicture, name="delete-picture"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),

    path('update-user/', views.updateUser, name="update-user"),

    path('like-home/<str:pk>/', views.like_picture_home, name="like-picture-home"),
    path('like-detail/<str:pk>/', views.like_picture_detail, name="like-picture-detail")
]