from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.memory import  LongTermMemory
from tools import WriteToTerminalTool
from crewai_tools import BraveSearchTool
from tools import WriteToTerminalTool
from crewai_tools import ScrapeElementFromWebsiteTool,FileWriterTool,FileReadTool
import logging

llm = LLM(
    model="llama-3.3-70b-versatile",
    api_base="https://api.groq.com/openai/v1",
    api_key="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",
    temperature=0
)

path = "C:\\Users\\giorg\\OneDrive\\Desktop\\enviroment\\chaster\\case.txt"


write_tool = WriteToTerminalTool()
scraping_tool = ScrapeElementFromWebsiteTool()
searchtool = BraveSearchTool()
createfile = FileWriterTool()
#memories = LongTermMemory()
FileRead=FileReadTool()




from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    file_path: str = Field(..., description="The file path to append to")
    text: str = Field(..., description="The text to append")
class myappend(BaseTool):
    name: str = "myappend"
    description: str = "This tool appends text to a specified file"
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, file_path: str, text: str) -> str:
            with open(file_path, "a") as f:
                f.append(text)
            return "Appended text sucessfully"

appendFile = myappend()

reciever = Agent(
    role="reciever",
    goal="You are a reciever of information",
    backstory=r"Use your file read tool by provoding path 'C:\Users\giorg\OneDrive\Desktop\enviroment\chaster\case.txt' and read from it after that send it to problem analyzer",
    tools=[write_tool,FileRead],
    verbose=True,
    llm=llm,
    allow_delegation=True
)   

mathematician = Agent(
    role="mathematician",
    goal="You are a mathematician",
    backstory="You are an expert in mathematics reciever and ticket manager",
    tools=[write_tool],
    verbose=True,
    llm=llm,
    allow_delegation=True
)


webCrawler = Agent(
    role="webcrawler",
    goal="You are a webcrawler",
    backstory="Your goal is to crawl the web and find information send it to reciever and ticket manager",
    tools=[write_tool, scraping_tool, searchtool],
    verbose=True,
    llm=llm,
    allow_delegation=True
)

problem_analyzer = Agent(
    role="problem analyzer",
    goal="You are a problem analyzer",
    backstory="You have to analyze the recieved problems from reciever ,solve it and send the information to agent that solves the problem",
    tools=[write_tool],
    verbose=True,
    llm=llm,
    allow_delegation=True
)

ticket_manager = Agent(
    role="ticket manager",
    goal=r"You are a ticket manager and you have to manage this C:\Users\giorg\OneDrive\Desktop\enviroment\ticket_folder\ticket.json after recieving the information from the agent you have to add ticket using json or append text with appropriate title and description alongside with possible solution inside ticket folder with myappend tool",
    backstory="You are the best troubleshootingticket manager in the entire world",
    tools=[createfile, appendFile],
    verbose=True,
    #memory = memories,
    llm=llm,
    allow_delegation=True
)


myAgent = Agent(
    role="About tickets",
    goal="You know everything about the tickets.",
    backstory="""You are a master at tickets and you know everything about them.You can read tickets, and search for tickets. then you can send the information to me if i tell you to do so.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[FileRead],
)

task =Task(
    description="Your goal is to analyze the information and send it to other agents according to recieved information",
    expected_output=r"Solve the problem given by 'C:\Users\giorg\OneDrive\Desktop\enviroment\chaster\case.txt' which should be read using fileread tool and send the information to ticket manager",
    agent=reciever,
    llm=llm
)


 
crew = Crew(
    agents=[ticket_manager,reciever,mathematician,webCrawler,problem_analyzer,myAgent],
    tasks=[task],
    verbose=True  # Enable knowledge by adding the sources here. You can also add more sources to the sources list.
)


result = crew.kickoff()
loggs=logging.debug("Result: %s", result)
print(result,loggs)

