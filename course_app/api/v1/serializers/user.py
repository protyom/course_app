from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords are different")
        return data

    def create(self, validated_data):
        validated_data['password'] = validated_data['password1']
        user = get_user_model().objects.create_user(**validated_data)
        return user
