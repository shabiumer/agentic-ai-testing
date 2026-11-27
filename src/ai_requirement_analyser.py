import os
import json

from src.ai_output_validator import validate_ai_output
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from src.traceability import build_traceability_matrix
from src.test_case_quality import (
    assess_test_case_quality,
    find_duplicate_test_cases,
    validate_requirement_links
)

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


# Collect all AI-generated test cases
all_tests = (
    ai_output["positive_tests"]
    + ai_output["negative_tests"]
    + ai_output["boundary_tests"]
)

# Identify duplicate test cases
duplicates = find_duplicate_test_cases(all_tests)

# Get valid business rule IDs
valid_requirement_ids = [
    rule["rule_id"]
    for rule in ai_output["business_rules"]
]

print("\nAI Test Case Quality Report")
print("===========================")

passed_count = 0
rejected_count = 0

for test_case in all_tests:

    # Check general test case quality
    quality = assess_test_case_quality(test_case)

    # Check requirement links
    link_result = validate_requirement_links(
        test_case,
        valid_requirement_ids
    )

    issues = quality["issues"] + link_result["issues"]

    # Check duplicates
    if test_case["test_case_id"] in duplicates:
        issues.append("Duplicate test case detected")

    status = "Passed" if not issues else "Rejected"

    if status == "Passed":
        passed_count += 1
    else:
        rejected_count += 1

    print(f"\nTest ID: {test_case['test_case_id']}")
    print(f"Status: {status}")

    if issues:
        for issue in issues:
            print(f"Issue: {issue}")

print("\nQuality Assessment Summary")
print("==========================")
print(f"Total test cases: {len(all_tests)}")
print(f"Passed: {passed_count}")
print(f"Rejected: {rejected_count}")


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