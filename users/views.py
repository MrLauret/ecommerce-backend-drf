from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from .serializers import UserSerializer

User = get_user_model() #gets the defined user model in settings

class RegisterView(generics.CreateAPIView):
    queryset = User
    serializer_class = UserSerializer


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    try:
        findUser =  User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"Error": "Email not found"}, status=404)
    username = findUser.username
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"Error": "Invalid credentials"}, status=400)
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    avatar = findUser.avatar.url
    return Response({
        "access_token": str(access_token),
        "refresh_token": str(refresh_token),
        "avatar": avatar,
        "username": username,
        "user_id": findUser.id,
        "user_email": findUser.email
    }, status=status.HTTP_200_OK)
    
class profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'avatar': user.avatar.url,
            'username': user.username,
            'user_id': user.id,
            'email': user.email
        })

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

 
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    user_auth = request.user
    if user_id != user_auth.id:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"errors": "User not found"}, status=404)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK) #I dont speak viet :3
    if request.method == "PATCH" and not user.is_staff: #để admin cũng có quyền sửa
        user_data = request.data
        user_data = {key: value for key, value in user_data.items() if value not in ("", None, "undefined", "null")} #Để tránh update "" và None vào db
        print(user_data)
        serializer = UserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)