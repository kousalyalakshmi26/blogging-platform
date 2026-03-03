from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:pk>/comment/', add_comment),
    path('posts/<int:pk>/like/', like_post),
]