from dotenv import dotenv_values
import psycopg2
from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI


#db connect
from urllib.parse import quote_plus



# Load environment variables from .env file
config = dotenv_values('.env')

# Encode the password to handle special characters
password = quote_plus("giggity@1234")

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{password}@db.ffukbbseygykvzirelar.supabase.co:5432/postgres",
)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=config['OPENAI_API_KEY'])
search = SerpAPIWrapper(serpapi_api_key="d83ef4d47ce9c820b3e1e84ac54310ea9af63ce4a7d536f34a394ad85dd1e0f0")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)


db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    ),
    Tool(
        name="PostgreSQL-DB",
        func=db_chain.run,
        description="useful for when you need to answer questions about PostgresQL-DB. Input should be in the form of a question containing full context"
    )
]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

# agent.run("My name is Robyn Vecard. Can you summarize my overall income for the  year 2023")

def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = prompt
                print(agent.run(question))
            except Exception as e:
                print(e)

get_prompt()