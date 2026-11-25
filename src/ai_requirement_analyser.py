import os

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

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
print(response.output_text)