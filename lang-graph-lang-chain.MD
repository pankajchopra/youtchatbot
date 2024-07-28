# prompt: lang-graph create agent and a function @tool

!pip install langchain
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
os.environ["OPENAI_API_KEY"] = "" # replace with your OpenAI API key
agent = create_csv_agent(OpenAI(temperature=0), 'path/to/your/file.csv', verbose=True)
agent.run("Your question here")

@tool("search_wikipedia")
def search_wikipedia(query: str) -> str:
    """Searches Wikipedia for the given query."""
    # Code to search Wikipedia and return the result
    return result


# prompt: with lang-graph create three agents and three functions making call to Gemini Pro using ReAct  One function finding weather, one stock price/analysis, one Wikipedia. One Agent will Analysis the tasks and distribute the tasks to agents they will use appropriate @tool function calls

from langchain.agents import create_react_agent
from langchain.agents.agent_toolkits import create_python_agent
from langchain.llms import OpenAI
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
  AIMessage,
  HumanMessage,
  SystemMessage
)

llm = ChatOpenAI(temperature=0)

tools = [
  PythonREPLTool()
]

# Weather agent
weather_agent = create_python_agent(
  llm,
  tools,
  verbose=True
)

# Stock analysis agent
stock_agent = create_python_agent(
  llm,
  tools,
  verbose=True
)

# Wikipedia agent
wiki_agent = create_python_agent(
  llm,
  tools,
  verbose=True
)

# Analysis agent
analysis_agent = create_react_agent(
  llm,
  tools,
  verbose=True
)

# Define functions for each task

def get_weather(location):
  # Use weather API or library to get weather data
  return weather_data

def get_stock_info(symbol):
  # Use stock API or library to get stock data
  return stock_data

def get_wiki_summary(topic):
  # Use Wikipedia API or library to get summary
  return wiki_summary

# Example usage
task = "What's the weather in London? Get me the stock price for AAPL. Summarize the Wikipedia article on Artificial Intelligence."

# Analysis agent distributes tasks
analysis_result = analysis_agent.run(task)

# Extract individual tasks from analysis result
weather_task = # Extract weather task
stock_task = # Extract stock task
wiki_task = # Extract wiki task

# Execute tasks using appropriate agents
weather_result = weather_agent.run(weather_task)
stock_result = stock_agent.run(stock_task)
wiki_result = wiki_agent.run(wiki_task)

# Print results
print("Weather:", weather_result)
print("Stock:", stock_result)
print("Wikipedia:", wiki_result)







# prompt:  use LangGraph  using DAG each node as an Agent conditional edges create three agents and three functions making call to Gemini Pro using ReAct  One function finding weather, one stock price/analysis, one Wikipedia. One Agent will Analysis the tasks and distribute the tasks to agents they will use appropriate @tool function calls

!pip install langchain langflow

from langflow import load_flow_from_json
from langchain.chat_models import ChatOpenAI
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage

# Replace with your actual OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY" 

# Define the tools (functions)
def get_weather(location: str) -> str:
    """Gets the current weather in a given location."""
    llm = ChatOpenAI(temperature=0)
    prompt = f"What is the current weather in {location}?"
    result = llm([HumanMessage(content=prompt)])
    return result.content

def get_stock_info(symbol: str) -> str:
    """Gets stock price and analysis for a given symbol."""
    llm = ChatOpenAI(temperature=0)
    prompt = f"Give me the current price and a brief analysis of {symbol} stock."
    result = llm([HumanMessage(content=prompt)])
    return result.content

def get_wiki_summary(topic: str) -> str:
    """Gets a summary from Wikipedia for a given topic."""
    llm = ChatOpenAI(temperature=0)
    prompt = f"Summarize the Wikipedia article for {topic}."
    result = llm([HumanMessage(content=prompt)])
    return result.content

# Create LangChain Tools from the functions
tools = [
    Tool(
        name="Get Weather",
        func=get_weather,
        description="Useful for getting the current weather in a location."
    ),
    Tool(
        name="Get Stock Info",
        func=get_stock_info,
        description="Useful for getting stock price and analysis."
    ),
    Tool(
        name="Get Wiki Summary",
        func=get_wiki_summary,
        description="Useful for getting a summary of a Wikipedia article."
    )
]

# Initialize the main LLM (Gemini Pro in this case)
llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0) 

# Initialize the agent (using ReAct agent type)
agent_executor = initialize_agent(
    tools, llm, agent=AgentType.REACT_DOCSTORE, verbose=True
)

# Example usage
task = "What's the weather like in London? Also, tell me about Tesla stock and give me a summary of World War II."
agent_executor.run(task) 



from langgraph.graph import Graph
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.prebuilt.condition_node import ConditionNode
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Set up Gemini Pro
os.environ["GOOGLE_API_KEY"] = "your_api_key_here"
gemini = ChatGoogleGenerativeAI(model="gemini-pro")

# Define tool functions
def get_weather(location):
    # Implement weather API call using Gemini Pro
    prompt = f"What's the current weather in {location}?"
    response = gemini.invoke(prompt)
    return response.content

def get_stock_info(symbol):
    # Implement stock API call using Gemini Pro
    prompt = f"Provide current price and brief analysis for stock {symbol}"
    response = gemini.invoke(prompt)
    return response.content

def get_wikipedia_info(topic):
    # Implement Wikipedia search using Gemini Pro
    prompt = f"Provide a brief summary of {topic} from Wikipedia"
    response = gemini.invoke(prompt)
    return response.content

# Define agents
class TaskAnalysisAgent(ToolNode):
    def run(self, task):
        prompt = f"Analyze this task and determine which function to use: {task}"
        response = gemini.invoke(prompt)
        return response.content

class WeatherAgent(ToolNode):
    def run(self, location):
        return get_weather(location)

class StockAgent(ToolNode):
    def run(self, symbol):
        return get_stock_info(symbol)

class WikipediaAgent(ToolNode):
    def run(self, topic):
        return get_wikipedia_info(topic)

# Create the graph
workflow = Graph()

# Add nodes
workflow.add_node("task_analysis", TaskAnalysisAgent())
workflow.add_node("weather", WeatherAgent())
workflow.add_node("stock", StockAgent())
workflow.add_node("wikipedia", WikipediaAgent())

# Add edges with conditions
def route_task(result):
    if "weather" in result.lower():
        return "weather"
    elif "stock" in result.lower():
        return "stock"
    elif "wikipedia" in result.lower():
        return "wikipedia"
    else:
        return "end"

workflow.add_edge("task_analysis", route_task)
workflow.add_edge("weather", "end")
workflow.add_edge("stock", "end")
workflow.add_edge("wikipedia", "end")

# Set the entry point
workflow.set_entry_point("task_analysis")

# Compile the graph
app = workflow.compile()

# Example usage
result = app.invoke("What's the weather like in New York?")
print(result)
