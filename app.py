import psycopg2
from dotenv import load_dotenv
load_dotenv()
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

from langchain.prompts.prompt import PromptTemplate

from langchain.chains import SQLDatabaseSequentialChain



from urllib.parse import quote_plus

# Encode the password to handle special characters
password = quote_plus("giggity@1234")

# Establish a PostgreSQL connection using the URI connection string
# conn = psycopg2.connect(
#     f"postgresql://username:{password}@host:port/database"
# )




# Establish a connection to the PostgreSQL database
# conn = psycopg2.connect(
#     host="db.ffukbbseygykvzirelar.supabase.co",
#     port=5432,
#     user='postgres',
#     password="giggity@1234",
#     database="postgres",

# )

# cursor = conn.cursor()





# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{password}@db.ffukbbseygykvzirelar.supabase.co:5432/postgres",
)

# setup llm
llm = OpenAI(temperature=0, openai_api_key="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")

# Create db chain
DEFAULT_QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here



{question}


"""

# modifying default prompttemplate
PROMPT=PromptTemplate(
    input_variables=["question",],
    template=DEFAULT_QUERY
)


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
