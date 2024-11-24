from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile
from .serializers import UserProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'password2', 'user_type',
                 'business_name', 'business_type', 'phone', 'address', 'tax_number',
                 'avatar', 'profile')
        extra_kwargs = {
            'email': {'required': True},
            'user_type': {'read_only': True},  # Can't be set via API
            'business_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Force user_type to BUSINESS_OWNER for API registrations
        validated_data['user_type'] = User.UserType.BUSINESS_OWNER
        profile_data = validated_data.pop('profile', None)
        password2 = validated_data.pop('password2', None)
        user = User.objects.create_user(**validated_data)
        
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
            
        return user