import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

def llama3_70b(query: str) -> str:
    """
    Calls Groq's LLaMA3-70B model and returns the text output.
    """
    model = ChatGroq(
        model_name="llama3-70b-8192",
        groq_api_key=groq_api_key,
        temperature=0.7,
    )
    response = model.invoke([HumanMessage(content=query)])
    return response.content
