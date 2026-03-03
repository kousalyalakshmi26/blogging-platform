from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Post, Comment
from .serializers import *
from .permissions import IsAuthorOrReadOnly

# Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Retrieve, Update, Delete Post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


# Add Comment
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_comment(request, pk):
    post = Post.objects.get(pk=pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data)
    return Response(serializer.errors)


# Like/Unlike Post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return Response({'message': 'Unliked'})
    else:
        post.likes.add(request.user)
        return Response({'message': 'Liked'})