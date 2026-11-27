
import os
import json

from src.test_data_validator import validate_test_data
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

client = OpenAI()
model = os.getenv("OPENAI_MODEL")

project_root = Path(__file__).resolve().parent.parent


# Load designed test cases from Agent 2
input_file = project_root / "test_data" / "designed_test_cases.json"

with input_file.open("r", encoding="utf-8") as file:
    test_design_output = json.load(file)


# Load Test Data Agent prompt
prompt_file = project_root / "prompts" / "test_data_prompt.txt"

with prompt_file.open("r", encoding="utf-8") as file:
    prompt_template = file.read()


# Prepare input for AI
prompt = f"""
{prompt_template}

Designed test cases:
{json.dumps(test_design_output, indent=4)}
"""


# Execute Test Data Agent
response = client.responses.create(
    model=model,
    input=prompt,
    text={"format": {"type": "json_object"}}
)


# Read AI response
test_data_output = json.loads(response.output_text)
# Validate generated test data
valid_test_case_ids = [
    test_case["test_case_id"]
    for test_case in test_design_output["test_cases"]
]

validation_result = validate_test_data(
    test_data_output,
    valid_test_case_ids
)

print("\nTest Data Validation")
print("====================")
print(json.dumps(validation_result, indent=4))

if validation_result["status"] == "Rejected":
    raise ValueError("Test Data Agent output failed validation")

# Display results
print("\nAI Test Data Agent")
print("==================")

print(json.dumps(test_data_output, indent=4))


# Save generated test data
output_file = project_root / "test_data" / "generated_test_data.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(test_data_output, file, indent=4)


print("\nTest data generated and saved successfully.")
