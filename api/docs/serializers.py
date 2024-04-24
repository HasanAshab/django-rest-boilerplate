from rest_framework import serializers

class SuccessfulResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
