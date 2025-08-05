from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

async def main():
    client = MultiServerMCPClient(
        {
            "requirements phase":{
                "url":"http://localhost:8000/mcp",
                "transport":"streamable_http"
            }
        }
    )

    tools = await client.get_tools()

    model = ChatGroq(
        model_name="llama3-70b-8192",
        groq_api_key=groq_api_key,
        temperature=0.7,
    )

    agent = create_react_agent(model,tools)

    req_res = agent.invoke(
        {"messages":[{"role":"user","content":"Please generate requirements for a todo app in javascript"}]}
    )

    print("Req_res: ",req_res)

asyncio.run(main())