from djoser.serializers import UserCreateSerializer, UserSerializer, ActivationSerializer
from rest_framework import serializers
from .models import UserLimit

class UserLimitRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLimit
        fields = ['limit_name', 'limit_value', 'unit']
        
class UserLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLimit
        fields = '__all__'
        
class CustomUserCrateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['id','full_name', 'email', 'password']
        
class CustomUserSerializer(UserSerializer):
    limits = serializers.SerializerMethodField()
    
    def get_limits(self, obj):
        limits = UserLimit.objects.filter(user=obj)
        if limits.exists():
            return UserLimitRetrieveSerializer(limits, many=True).data
        return None
    
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'full_name', 'is_verified', 'date_joined', 'is_active', 'role', 'limits']
        read_only_fields = ['id', 'email', 'full_name', 'is_verified', 'date_joined', 'is_active', 'role', 'limits']

class CustomActivationSerializer(ActivationSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Check if the user is active
        if not self.user.is_active:
            # Set is_verified to True
            self.user.is_verified = True
            self.user.save()

        return attrs
    

