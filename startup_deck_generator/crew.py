import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

# Load environment variables (e.g., GROQ_API_KEY from .env)
load_dotenv()

# Define a lightweight Groq LLM with capped token usage to stay within rate limits
llm = ChatGroq(
    model_name="groq/llama-3.1-8b-instant",
    temperature=0.7,
    max_tokens=1000  # Helps prevent exceeding Groq's tokens-per-minute cap
)

# Utility function to load YAML files (for agents and task definitions)
def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# Builds the CrewAI agent system based on YAML config and a user-defined startup idea
def build_crew(startup_idea: str):
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, "config")

    # Load agent and task configuration
    agents_config = load_yaml(os.path.join(config_path, "agents.yaml"))["agents"]
    tasks_config = load_yaml(os.path.join(config_path, "tasks.yaml"))

    # Initialize agents using the shared LLM instance
    agent_map = {}
    for agent_data in agents_config:
        agent = Agent(
            role=agent_data["role"],
            goal=agent_data["goal"],
            backstory=agent_data["backstory"],
            llm=llm
        )
        agent_map[agent_data["role"]] = agent

    # Replace placeholder {{ idea }} in task description
    task_text = tasks_config["task"].replace("{{ idea }}", startup_idea)

    # Create tasks based on predefined agent order
    tasks = []
    for role in tasks_config["agent_order"]:
        tasks.append(
            Task(
                description=task_text,
                expected_output=f"{role} output for deck generation",
                agent=agent_map[role]
            )
        )

    # Return a sequential crew execution (agents work one after another)
    return Crew(
        agents=list(agent_map.values()),
        tasks=tasks,
        verbose=True,
        sequential=True
    )
