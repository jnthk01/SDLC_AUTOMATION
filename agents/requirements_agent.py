import asyncio
import os
from typing import Any, Dict
from pathlib import Path
from fastmcp import FastMCP
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment
dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path)

# Get API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# MCP server
mcp = FastMCP("REQUIREMENTS AGENT")

# LLM model (async compatible)
requirements_model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    groq_api_key=groq_api_key,
    temperature=0.7,
)

# ✅ Async Tool Registration
@mcp.tool(
    name="generate_software_requirements",
    description="Generates functional and non-functional requirements from a software project description.",
)
async def generate_software_requirements(project_description: str) -> Dict[str, Any]:
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

    # ✅ Important: this MUST be async
    response = await requirements_model.ainvoke(prompt)
    content = response.content.strip()

    return {
        "project_description": project_description,
        "requirements": content,
        "status": "success"
    }

async def list_tools():
    tools = await mcp._list_tools()
    print("Available tools:", tools)

# MCP run
if __name__ == "__main__":
    asyncio.run(list_tools())
    mcp.run(transport="streamable-http")
