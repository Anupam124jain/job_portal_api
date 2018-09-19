"""Serilizers of job listing"""

from rest_framework import serializers
from common.messages import REQUIRED
from test_app.models import JobSeeker


class JobsListSerializer(serializers.Serializer):

    """Create a joblist Serilizers"""

    title = serializers.CharField(error_messages={'blank': REQUIRED}, max_length=100)
    location = serializers.CharField(error_messages={'blank': REQUIRED}, max_length=100)
    title_id = serializers.CharField(read_only=True)
    normalized_title = serializers.CharField(read_only=True)


    def create(self, validated_data):
        """Create and return a new `Jobs` instance, given the validated data."""
        return JobSeeker.objects.create(**validated_data)


class JobsDetailsSerializer(serializers.Serializer):

    """ Create a job details Serilizers """

    title = serializers.CharField(error_messages={'blank': REQUIRED}, max_length=100)
    location = serializers.CharField(error_messages={'blank': REQUIRED}, max_length=100)
    title_id = serializers.CharField(read_only=True)
    normalized_title = serializers.CharField(read_only=True)
    skills = serializers.CharField(read_only=True)
