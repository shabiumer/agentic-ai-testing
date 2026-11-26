import os
import json

from src.ai_output_validator import validate_ai_output
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from src.traceability import build_traceability_matrix


load_dotenv()

client = OpenAI()

model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

requirement = """
The energy billing system must calculate a customer's bill
using the difference between the previous and current meter
readings multiplied by the unit rate.

The system must reject negative readings and must not accept
a current reading lower than the previous reading.
"""
project_root = Path(__file__).resolve().parent.parent

prompt_file = project_root / "prompts" / "requirement_prompt.txt"

with prompt_file.open("r", encoding="utf-8") as file:
    prompt_template = file.read()

prompt = prompt_template + f"""

Requirement:
{requirement}
"""


response = client.responses.create(
    model=model,
    input=prompt,
    text={
        "format": {
            "type": "json_object"
        }
    }
)

print("\nAI Requirement Analysis")
print("======================")

ai_output = json.loads(response.output_text)
print(json.dumps(ai_output, indent=4))

validate_ai_output(ai_output)

matrix = build_traceability_matrix(ai_output)

print("\nRequirement Traceability Matrix")
print("================================")

for rule_id, details in matrix.items():
    print(f"\n{rule_id}: {details['description']}")
    print(f"Test cases: {details['test_cases']}")
    print(f"Coverage: {details['coverage']}")

print("AI output validation: PASSED")
print(f"Business rules: {len(ai_output['business_rules'])}")
print(f"Positive tests: {len(ai_output['positive_tests'])}")
print(f"Negative tests: {len(ai_output['negative_tests'])}")
print(f"Boundary tests: {len(ai_output['boundary_tests'])}")
print("All test cases have valid structure and unique IDs.")