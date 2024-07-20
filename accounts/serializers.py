from djoser.serializers import UserCreateSerializer, UserSerializer, ActivationSerializer

class CustomUserCrateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'email', 'password','full_name']
        
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'full_name', 'is_verified', 'date_joined', 'is_active', 'role']
        read_only_fields = ['id', 'email', 'full_name', 'is_verified', 'date_joined', 'is_active', 'role']

class CustomActivationSerializer(ActivationSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Check if the user is active
        if not self.user.is_active:
            # Set is_verified to True
            self.user.is_verified = True
            self.user.save()

        return attrs