import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

from langchain.prompts.prompt import PromptTemplate

from langchain.chains import SQLDatabaseSequentialChain



from urllib.parse import quote_plus

# Encode the password to handle special characters
password = quote_plus("giggity@1234")

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{password}@db.ffukbbseygykvzirelar.supabase.co:5432/postgres",
)

# setup llm
llm = OpenAI(temperature=0.7, openai_api_key=os.environ.get("OPENAI_API_KEY"),max_tokens=1000)

# Create db chain
DEFAULT_QUERY = """
You are a Financial Planner Bot, and your goal is to provide answers based on the financial data of the user stored in the database.

To retrieve information from the database, follow this process:

Receive a question or query from the user.
Formulate a syntactically correct postgreSQL query based on the question. Make sure to include relevant table names, columns, conditions, and any necessary aggregations or joins.
Execute the query on the given postgres database.
Examine the results obtained from the query.
Provide the answer to the user in the required format.
If answer is not required in table format, here's the format to use when responding:

Question: "Question from the user"
Query: "Query formulated based on the question"
Result: "Results obtained from executing the query"
Answer: "Final answer based on the result"

Now, let's proceed step by step. Below is the query:

Query: 
{question}

"""

# modifying default prompttemplate
# PROMPT=PromptTemplate(
#     input_variables=["question",],
#     template=DEFAULT_QUERY
# )


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
