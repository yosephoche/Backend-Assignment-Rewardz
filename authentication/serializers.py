from rest_framework import serializers

from authentication.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserMinimalSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]
