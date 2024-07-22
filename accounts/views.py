from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from .models import UserLimit
from .serializers import UserLimitSerializer
from accounts.permissions import IsSuperAdmin, IsAdmin

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)

            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SetUserLimitView(generics.CreateAPIView):
    queryset = UserLimit.objects.all()
    serializer_class = UserLimitSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin | IsAdmin]

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        limit_name = request.data.get('limit_name')
        limit_value = request.data.get('limit_value')

        if not user_id or not limit_name or not limit_value:
            return Response({'error': 'user_id, limit_name, and limit_value are required'}, status=status.HTTP_400_BAD_REQUEST)

        limit, created = UserLimit.objects.update_or_create(
            user_id=user_id,
            limit_name=limit_name,
            defaults={'limit_value': limit_value}
        )

        if created:
            return Response({'status': 'Limit created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Limit updated successfully'}, status=status.HTTP_200_OK)