from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .models import TrashLocation, Reward
from .serializers import TrashLocationSerializer, RewardSerializer, UserSerializer
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # Allow anyone to create a new user
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Extract and remove the password from the data dictionary
        password = data.pop('password', None)

        # Ensure the password is provided
        if not password:
            return Response({"detail": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user using the `create_user` method
        user = User.objects.create_user(
            email=data.get('email'),
            full_name=data.get('full_name'),
            password=password,
        )

        # Generate a token for the new user
        token, created = Token.objects.get_or_create(user=user)

        # Serialize the user and return the response
        serializer = self.get_serializer(user)
        return Response({
            "user": serializer.data,
            "token": token.key,
        }, status=status.HTTP_201_CREATED)

class TrashLocationViewSet(viewsets.ModelViewSet):
    queryset = TrashLocation.objects.all()
    serializer_class = TrashLocationSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all actions

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        location = self.get_object()
        user = request.user

        if user in location.users_joined.all():
            return Response({"detail": "User already joined this location."}, status=status.HTTP_400_BAD_REQUEST)

        location.users_joined.add(user)
        location.save()

        return Response({"detail": "User successfully joined the location."}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()

        if 'users_joined' in data:
            users = data.pop('users_joined')
            instance.users_joined.set(users)  # Update joined users

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)  # Authenticate using email

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "reward_points": user.reward_points,
                "token": token.key,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)