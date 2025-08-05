import os
import json
from typing import Any, Dict
from pathlib import Path
from fastmcp import FastMCP
from langchain_groq import ChatGroq
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path)

mcp = FastMCP("DESIGN AGENT")

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

design_model = ChatGroq(
    model_name="gemma2-9b-it",
    groq_api_key=groq_api_key,
    temperature=0.7,
)

@mcp.tool()
def generate_software_design(project_description: str) -> Dict[str, Any]:
    """
    Generates a high-level software system design based on the given project description.

    Input:
    - project_description: A brief explanation of the software project.

    Output:
    - A dictionary containing:
        - "project_description": the original input
        - "design": the generated design details (e.g., architecture, components, data flow)
        - "status": processing status
    """

    prompt = f"""
        You are a software architect.

        Design a system for the project below. Respond in JSON format with these keys:
        - "architecture": e.g. client-server, microservices, etc.
        - "components": main modules or services with brief purpose.
        - "data_flow": how data moves across components.

        Project: {project_description}
        """

    response = design_model.invoke(prompt)
    content = response.content.strip()

    return {
        "project_description": project_description,
        "design": content,
        "status": "success"
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")