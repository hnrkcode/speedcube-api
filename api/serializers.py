from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = "__all__"


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeModel
        fields = "__all__"
