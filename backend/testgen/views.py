from django.shortcuts import render

# Create your views here.
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Requirement, TestCase
from .serializers import RequirementSerializer, TestCaseSerializer
from .ai_utils import generate_test_cases

@api_view(["POST"])
def upload_requirement(request):
    """Upload a requirement document and extract dummy requirements"""
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    # Simulated parsing: in real scenario use PyPDF2, docx, or XML parser
    dummy_reqs = [
        {"req_id": str(uuid.uuid4())[:8], "text": "System shall encrypt patient data using AES-256"},
        {"req_id": str(uuid.uuid4())[:8], "text": "System shall lock user account after 5 failed login attempts"},
    ]

    saved_reqs = []
    for req in dummy_reqs:
        saved = Requirement.objects.create(
            req_id=req["req_id"],
            source=file.name,
            text=req["text"],
        )
        saved_reqs.append(saved)

    serializer = RequirementSerializer(saved_reqs, many=True)
    return Response({"requirements": serializer.data}, status=201)

@api_view(["POST"])
def generate_testcases(request, req_id):
    """Generate test cases for a given requirement"""
    try:
        requirement = Requirement.objects.get(req_id=req_id)
    except Requirement.DoesNotExist:
        return Response({"error": "Requirement not found"}, status=404)

    test_cases = generate_test_cases(requirement.text, req_id)

    created = []
    for tc in test_cases:
        created.append(
            TestCase.objects.create(
                requirement=requirement,
                test_id=tc["test_id"],
                title=tc["title"],
                steps=tc["steps"],
                expected_result=tc["expected_result"],
                compliance_refs=tc["compliance_refs"],
            )
        )

    serializer = TestCaseSerializer(created, many=True)
    return Response({"testCases": serializer.data}, status=201)

@api_view(["PUT"])
def approve_testcase(request, test_id):
    """Approve a test case"""
    try:
        testcase = TestCase.objects.get(test_id=test_id)
        testcase.approved = True
        testcase.save()
        return Response({"message": "Test case approved"})
    except TestCase.DoesNotExist:
        return Response({"error": "Test case not found"}, status=404)
