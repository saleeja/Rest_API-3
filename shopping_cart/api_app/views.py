from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView,CreateAPIView,RetrieveAPIView
from .serializers import ProfileUpdateSerializer
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer
from rest_framework.generics import DestroyAPIView

class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveAPIView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            profile = Profile.objects.select_related('user', 'role').get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class ProfileUpdateAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            return response

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            return response


class ProfileDeleteAPIView(DestroyAPIView):
    queryset = Profile.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ProfileBulkDeleteAPIView(APIView):
    def post(self, request):
        profile_ids = request.data.get('profile_ids', [])
        profiles = Profile.objects.filter(id__in=profile_ids)

        if not profiles:
            return Response({"detail": "No profiles found for deletion."}, status=status.HTTP_404_NOT_FOUND)

        deleted_count = profiles.delete()[0]

        return Response({"message": f"{deleted_count} profiles deleted successfully."}, status=status.HTTP_200_OK)
