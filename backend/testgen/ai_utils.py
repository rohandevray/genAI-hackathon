import vertexai
from vertexai.preview.generative_models import GenerativeModel
from django.conf import settings

# Initialize Google Vertex AI client
vertexai.init(project=settings.GCP_PROJECT_ID, location="us-central1")
model = GenerativeModel("gemini-pro")

def generate_test_cases(requirement_text, req_id):
    prompt = f"""
    Convert the following healthcare software requirement into structured test cases:

    Requirement: {requirement_text}

    Output format (JSON array):
    [
      {{
        "test_id": "TC-{req_id}-1",
        "title": "...",
        "steps": ["step 1", "step 2"],
        "expected_result": "...",
        "compliance_refs": ["ISO13485", "IEC62304"]
      }}
    ]
    """

    response = model.generate_content(prompt)
    try:
        import json
        test_cases = json.loads(response.text)
    except Exception:
        test_cases = []
    return test_cases
