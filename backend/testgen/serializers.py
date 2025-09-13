from rest_framework import serializers
from .models import Requirement, TestCase

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = "__all__"

class RequirementSerializer(serializers.ModelSerializer):
    testcases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = Requirement
        fields = "__all__"
