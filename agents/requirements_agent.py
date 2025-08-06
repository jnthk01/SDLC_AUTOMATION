# import os
# from pathlib import Path
# from fastmcp import FastMCP
# from typing import Any, Dict
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq

# dotenv_path = Path(__file__).parent.parent / '.env'
# load_dotenv(dotenv_path)

# groq_api_key = os.getenv("GROQ_API_KEY")
# if not groq_api_key:
#     raise ValueError("GROQ_API_KEY environment variable not set.")

# mcp = FastMCP("REQUIREMENTS AGENT")

# requirements_model = ChatGroq(
#     model_name="llama-3.1-8b-instant",
#     groq_api_key=groq_api_key,
#     temperature=0.7,
# )

# diagram_model = ChatGroq(
#     model_name="llama3-70b-8192",
#     groq_api_key=groq_api_key,
#     temperature=0.7,
# )

# @mcp.tool(
#     name="generate_software_requirements",
#     description="Generates functional and non-functional requirements from a software project description.",
# )
# async def generate_software_requirements(project_description: str) -> Dict[str, Any]:
#     prompt = f"""
#     You are a software requirements analyst.

#     From the project below, extract:
#     - functional_requirements
#     - non_functional_requirements

#     Respond in JSON with:
#     - "functional_requirements": [...]
#     - "non_functional_requirements": [...]

#     Project: {project_description}
#     """

#     response = await requirements_model.ainvoke(prompt)
#     content = response.content.strip()

#     return {
#         "project_description": project_description,
#         "requirements": content,
#         "status": "success"
#     }

#     print("Available tools:", tools)

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")


import base64
import io
import os
from pathlib import Path
import re
from dotenv import load_dotenv
import requests
from typing import Any, Dict
from PIL import Image as im
import matplotlib.pyplot as plt
from fastmcp import FastMCP
from langchain_groq import ChatGroq

dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path)

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Set up your Groq API model for diagram generation
diagram_model = ChatGroq(
    model_name="llama3-70b-8192",
    groq_api_key=groq_api_key,
    temperature=0.7,
)

# Set up your Groq API model for requirements (same or different from diagram_model)
requirements_model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    groq_api_key=groq_api_key,
    temperature=0.7,
)

mcp = FastMCP("REQUIREMENTS AGENT")

@mcp.tool(
    name="generate_software_requirements",
    description="Generates functional and non-functional requirements from a software project description and renders a Mermaid diagram.",
)
async def generate_software_requirements(project_description: str) -> Dict[str, Any]:
    # Step 1: Generate requirements
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
    response = await requirements_model.ainvoke(prompt)
    content = response.content.strip()

    # Step 2: Send to diagram model for mermaid generation
    
    mermaid_prompt = f"""
    You are a solution architect.

    Your task is to generate a **Mermaid flowchart** that visualizes the functional and non-functional requirements listed below.

    ---

    ### 📌 Use the following as a reference format (do not copy it directly):

    graph LR;
    User -->|Accesses| App;
    User -->|Create todo item| TodoItem;
    User -->|Retrieve todo items| TodoItemList;
    User -->|Update todo item| TodoItem;
    User -->|Delete todo item| DeletedTodoItem;
    User -->|Mark todo item as completed| TodoItem;
    User -->|Filter todo items| TodoItemList;
    User -->|Sort todo items| TodoItemList;

    %% Non-functional requirements
    JavaScript --> App;
    FrontendFramework --> App;
    CloudPlatform --> App;
    UserFriendlyInterface --> App;
    Security --> App;
    Scalability --> App;
    Database --> App;
    AutomatedTesting --> App;

    %% Styling
    classDef requirement fill:#f9f,stroke:#333,stroke-width:2px;
    classDef nonFunctionalRequirement fill:#ccc,stroke:#333,stroke-width:2px;

    class App,TodoItem,TodoItemList,DeletedTodoItem requirement;
    class JavaScript,FrontendFramework,CloudPlatform,UserFriendlyInterface,Security,Scalability,Database,AutomatedTesting nonFunctionalRequirement;
    class User actor;

    ---

    ### ✅ Requirements:
    {content}

    ---

    Respond **only** with a valid Mermaid diagram in the following format:

    ```mermaid
    graph LR;
    ...your diagram here...
    """

    diagram_response = await diagram_model.ainvoke(mermaid_prompt)
    mermaid_code = diagram_response.content.strip()


    # Step 3: Extract raw mermaid code
    if "```mermaid" in mermaid_code:
        mermaid_code = mermaid_code.split("```mermaid")[1].split("```")[0].strip()
    
    mermaid_code = re.sub(r'\|>', '|', mermaid_code)


    print("----------------------------------------------------")
    print(mermaid_code)
    print("----------------------------------------------------")

    # Step 4: Render and save mermaid diagram as image
    graphbytes = mermaid_code.encode("utf8")
    base64_bytes = base64.urlsafe_b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    img_url = 'https://mermaid.ink/img/' + base64_string

    response = requests.get(img_url)
    if response.status_code == 200:
        with open('requirements_phase.png', 'wb') as f:
            f.write(response.content)
    else:
        raise RuntimeError(f"Failed to download Mermaid image. Status code: {response.status_code}")




    return {
        "project_description": project_description,
        "requirements": content,
        "mermaid_code": mermaid_code,
        "status": "success"
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")