import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import Field
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import litellm
from crewai_tools import BraveSearchTool
from tools import WriteToTerminalTool
from crewai_tools import ScrapeElementFromWebsiteTool
scraping_tool = ScrapeElementFromWebsiteTool()
searchtool = BraveSearchTool()

llm = LLM(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key="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",
)


# Instantiate the custom tool
write_tool = WriteToTerminalTool()

# Researcher Agent
researcher = Agent(
    role="thinker",
    goal="think of an interesting fact about something and write it to the terminal, you can also ask to researcher to search for them on the internet, you should only search once.",
    backstory="An expert in telling interesting facts.",
    tools=[write_tool],  # Use the instantiated custom tool
    verbose=True,
    allow_delegation= True,
    llm=llm
)

internetresearcher = Agent(
    role="researcher",
    goal="search for information that you are asked for",
    backstory="An expert in researching",
    tools=[searchtool, scraping_tool],  # Use the instantiated custom tool
    verbose=True,
    llm=llm,
    allow_delegation=True

# Research Task
research_task = Task(
    description="Just use your tool to research and write an interesting fact about something to the terminal.",
    expected_output="Using the Write to Terminal tool, write an interesting fact about something to the terminal.",
    agent=researcher
)

#gamarjoba
# Creating the Crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential  # Ensures research happens before storage
)

# Running the Crew with a Topic
result = crew.kickoff(inputs={"topic": "AI in Healthcare"})
print(result)