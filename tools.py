
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import litellm
from crewai_tools import BraveSearchTool
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import Field
from typing import Type





class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    text: str = Field(..., description="gives a string to print")




class WriteToTerminalTool(BaseTool):
    name: str = "write to terminal"
    description: str = "this tool prints text to terminal"
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, text: str) -> str:
        print(text)
        return "Tool's result"
