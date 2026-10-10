import os
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from database import get_engine
from dotenv import load_dotenv

load_dotenv()

def get_sql_agent():
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    engine = get_engine()
    # SQLDatabase wrapper to interact with the database
    db = SQLDatabase(engine)

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="qwen/qwen3.8-27b", 
        temperature=0
    )

    # Creating the SQL agent
    # We use agent_type="tool-calling" for modern LLMs that support function calling
    # The prefix instructs the agent to perform both DML (Data Manipulation) and DDL (Data Definition) operations.
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=True,
        handle_parsing_errors=True,
        prefix="You are an agent designed to interact with a SQL database. You can perform SELECT queries, create tables (DDL), insert data, update data, and delete data (DML) based on the user's requests. If the user asks to create a table or modify data, generate and execute the appropriate SQL. Always double check your SQL before executing it."
    )
    return agent_executor

def process_prompt(prompt: str):
    try:
        agent = get_sql_agent()
        response = agent.invoke({"input": prompt})
        return response.get("output")
    except Exception as e:
        return f"An error occurred: {str(e)}"
