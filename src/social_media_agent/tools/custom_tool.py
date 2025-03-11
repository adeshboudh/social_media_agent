import os
from dotenv import load_dotenv
from crewai import LLM
from crewai_tools import SerperDevTool

load_dotenv()

os.environ["GEMINI_API_KEY"]=os.getenv('GEMINI_API_KEY')
os.environ["SERPER_API_KEY"]=os.getenv('SERPER_API_KEY')

# Initialize a search tool (to fetch real-time travel info)
search_tool = SerperDevTool()

# Research LLM (Factual & Deterministic)
llm_research = LLM(
    model="gemini/gemini-1.5-flash",
    verbose=True,
    temperature=0.3,
    api_key=os.environ["GEMINI_API_KEY"]
)

# Content Creation LLM (More Creative)
llm_content = LLM(
    model="gemini/gemini-1.5-flash",
    verbose=True,
    temperature=0.6,
    api_key=os.environ["GEMINI_API_KEY"]
)
