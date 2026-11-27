import os
import json

from src.test_design_validator import validate_designed_test_cases
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI()

model = os.getenv("OPENAI_MODEL")

# Find project directory
project_root = Path(__file__).resolve().parent.parent

# Load business rules from Agent 1
input_file = project_root / "test_data" / "business_rules.json"

with input_file.open("r", encoding="utf-8") as file:
    business_rules = json.load(file)

# Load Test Design prompt
prompt_file = project_root / "prompts" / "test_design_prompt.txt"

with prompt_file.open("r", encoding="utf-8") as file:
    prompt_template = file.read()

# Prepare prompt
prompt = f"""
{prompt_template}

Business rules:
{json.dumps(business_rules, indent=4)}
"""

# Call OpenAI API
response = client.responses.create(
    model=model,
    input=prompt,
    text={"format": {"type": "json_object"}}
)

# Parse AI response
test_design_output = json.loads(response.output_text)
# Validate AI-generated test cases
valid_requirement_ids = [
    rule["rule_id"] for rule in business_rules
]

validation_result = validate_designed_test_cases(
    test_design_output,
    valid_requirement_ids
)

print("\nTest Design Validation")
print("======================")
print(json.dumps(validation_result, indent=4))

if validation_result["status"] == "Rejected":
    raise ValueError("Test Design Agent output failed validation")

# Display generated test cases
print("\nAI Test Design Agent")
print("====================")

print(json.dumps(test_design_output, indent=4))

# Save generated test cases
output_file = project_root / "test_data" / "designed_test_cases.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(test_design_output, file, indent=4)

print("\nTest cases saved successfully.")
