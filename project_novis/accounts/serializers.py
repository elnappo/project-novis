from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    validated = serializers.BooleanField(read_only=True)
    country = serializers.StringRelatedField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'country', 'validated', 'created', 'modified')
        read_only = ('email', 'validated', 'created', 'modified')
        extra_kwargs = {'email': {'read_only': True}}
