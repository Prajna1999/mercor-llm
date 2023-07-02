import os


from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

from urllib.parse import quote_plus

from dotenv import dotenv_values
import psycopg2

# Load environment variables from .env file
config = dotenv_values('.env')

# Encode the password to handle special characters
password = quote_plus("giggity@1234")

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{password}@db.ffukbbseygykvzirelar.supabase.co:5432/postgres",
)

llm = OpenAI(temperature=0.7, openai_api_key=config['OPENAI_API_KEY'],max_tokens=1000)

# Create db chain
DEFAULT_QUERY = """
You are a Financial Planner Bot, and your goal is to provide answers based on the financial data of the user stored in the database.

To retrieve information from the database, follow this process:

Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here


{question}

"""



# Setup the database chain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = DEFAULT_QUERY.format(question=prompt)
                print(db_chain.run(question))
            except Exception as e:
                print(e)

get_prompt()