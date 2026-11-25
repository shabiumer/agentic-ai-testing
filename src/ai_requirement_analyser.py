import os

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

prompt = f"""
You are a software testing analyst.

Analyse the following energy billing requirement.

Identify:
1. The main business rules.
2. Positive test scenarios.
3. Negative test scenarios.
4. Boundary test scenarios.

Requirement:
{requirement}

Explain your findings clearly using numbered lists.
"""

response = client.responses.create(
    model=model,
    input=prompt
)

print("\nAI Requirement Analysis")
print("======================")
print(response.output_text)