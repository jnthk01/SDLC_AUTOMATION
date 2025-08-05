import os
from typing import Any, Dict
from pathlib import Path
from fastmcp import FastMCP
from langchain_groq import ChatGroq
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent.parent / '.env' 
load_dotenv(dotenv_path)

mcp = FastMCP("REQUIREMENTS AGENT")

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

requirements_model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    groq_api_key=groq_api_key,
    temperature=0.7,
)


@mcp.tool()
def generate_software_requirements(project_description: str) -> Dict[str, Any]:
    """
    Given a software project description, generates:
      - functional_requirements
      - non_functional_requirements
      - user_stories
    """
    
    prompt = f"""
    You are a software requirements analyst.

    From the project below, extract:
    - functional_requirements
    - non_functional_requirements

    Respond in JSON with:
    - "functional_requirements": [...]
    - "non_functional_requirements": [...]

    Project: {project_description}
    """

    
    response = requirements_model.invoke(prompt)
    content = response.content.strip()
    
    return {
        "project_description": project_description,
        "requirements": content,
        "status": "success"
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")  # Running on http://127.0.0.1:8000