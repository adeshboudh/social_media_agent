import os
import requests
from crewai import LLM
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Union
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

os.environ["GEMINI_API_KEY"]=os.getenv('GEMINI_API_KEY')
os.environ["SERPER_API_KEY"]=os.getenv('SERPER_API_KEY')
# os.environ["FIRECRAWL_API_KEY"]=os.getenv('FIRECRAWL_API_KEY')
os.environ['OPENROUTER_API_KEY']=os.getenv('OPENROUTER_API_KEY')

class GetContentInput(BaseModel):
    """Input schema for GetContentTool."""
    urls: List[str] = Field(..., description="List of URLs to fetch content from.")

class GetContentTool(BaseTool):
    name: str = "get_content"
    description: str = "Fetches and returns the content from the provided list of URLs."
    args_schema: Type[BaseModel] = GetContentInput

    def _run(self, urls: List[str]) -> List[str]:
        """Fetch content from the provided URLs."""
        loader = WebBaseLoader(urls)
        docs = loader.load()
        return [doc.page_content for doc in docs]

class ImageSearchInput(BaseModel):
    """Input schema for ImageSearchTool."""
    query: str = Field(..., description="Search term for the image search.")

class ImageSearchTool(BaseTool):
    name: str = "image_search"
    description: str = "Performs an image search using the specified query."
    args_schema: Type[BaseModel] = ImageSearchInput

    def _run(self, query: str) -> str:
        """Execute the image search and return the results."""
        api_key = os.getenv('SERPER_API_KEY')
        if not api_key:
            raise ValueError("API key not found. Please set the SERPER_API_KEY environment variable.")
        url = f"https://google.serper.dev/images?q={query}&apiKey={api_key}"
        response = requests.get(url)
        return response.text

class EvaluationCategory(BaseModel):
    score: float = Field(..., ge=0.0, le=10.0, description="Score between 0.0 and 10.0")
    explanation: str = Field(..., description="Explanation for the score")

class EvaluationOutput(BaseModel):
    clarity: EvaluationCategory
    tone: EvaluationCategory
    engagement: EvaluationCategory
    platform_alignment: EvaluationCategory
    hashtags: EvaluationCategory
    overall_effectiveness: EvaluationCategory

    def get_overall_effectiveness_score(self) -> float:
        """Returns the overall effectiveness score."""
        return self.overall_effectiveness.score

# Initialize a search tool (to fetch real-time travel info)
serper_tool = SerperDevTool()

scrape_tool = GetContentTool()

image_search_tool = ImageSearchTool()

# llm_creator = LLM(model="openrouter/google/gemini-2.0-flash-thinking-exp:free",
#                   verbose=True, 
#                   temperature=0.5,
#                   api_key=os.getenv("OPENROUTER_API_KEY"),
#                   base_url="https://openrouter.ai/api/v1"
# )

llm_creator = LLM(model="gemini/gemini-2.0-flash",
                  verbose=True, 
                  temperature=0.5,
                  api_key=os.getenv("GEMINI_API_KEY")
                  )