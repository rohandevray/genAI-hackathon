from django.db import models

# Create your models here.
class Requirement(models.Model):
    req_id = models.CharField(max_length=100, unique=True)
    source = models.CharField(max_length=255)
    text = models.TextField()
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.req_id

class TestCase(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name="testcases")
    test_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    steps = models.JSONField()
    expected_result = models.TextField()
    compliance_refs = models.JSONField(default=list)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.test_id

class TraceabilityLink(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    jira_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
