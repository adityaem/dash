import openai
import os
from dotenv import load_dotenv
from langchain.document_loaders import SnowflakeLoader
from langchain.prompts.prompt import PromptTemplate
import settings as s

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base =  os.getenv("OPENAI_API_BASE")
openai.api_type = 'azure'
openai.api_version = '2022-12-01'
completion_model = os.getenv("OPENAI_ENGINES")
embedding_model = os.getenv("OPENAI_EMBEDDINGS_ENGINE_DOC")
question_prompt = os.getenv("QUESTION_PROMPT").replace(r'\n', '\n')

def get_semantic_answer(question):
    prompt = question_prompt.replace("_QUESTION_", question)
    # Note: The openai-python library support for Azure OpenAI is in preview.
    import os
    import openai
    openai.api_type = "azure"
    openai.api_base = "https://spebi.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=[{"role": "system", "content": "You are an AI assistant that helps people find information."},
                  {"role": "user", "content": prompt},
                  {"role": "assistant", "content": "The founders of Microsoft are Bill Gates and Paul Allen."}],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    print(prompt)
    print(response['choices'][0]['message']['content'])
    answer=response['choices'][0]['message']['content']
    return question, answer
def get_semantic_answer_native(question):
    import os
    import openai
    openai.api_type = "azure"
    openai.api_base = "https://spebi.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt =  question
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assistant that helps people find information at Sony Pictures"},{"role": "user", "content": prompt}],
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    print(prompt)
    print(response['choices'][0]['message']['content'])
    answer=response['choices'][0]['message']['content']
    return question, answer


def get_semantic_answer_snowflake(question):
    import os
    import openai
    from langchain.memory import ConversationBufferWindowMemory
    import openai
    import pandas as pd
    from langchain.agents import create_csv_agent
    from langchain.llms import AzureOpenAI
    from langchain.agents import create_sql_agent
    from langchain.agents.agent_toolkits import SQLDatabaseToolkit
    from langchain import SQLDatabase
    from sqlalchemy import create_engine
    openai.api_type = "azure"
    openai.api_base = "https://spebi.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = question

   #######
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_type = 'azure'
    openai.api_version = "2023-05-15"
    model_name = "gpt-4"
    engine = "gpt-4"
    deployment_id = "gpt-4"
    user = os.getenv("user"),
    password = os.getenv("password"),
    account = os.getenv("account"),
    warehouse = os.getenv("warehouse"),
    role = os.getenv("role"),
    database = os.getenv("database"),
    schema = os.getenv("schema"),
    db = SQLDatabase.from_uri(
        'snowflake://{user}:{password}@{account_identifier}/{database}/{schema_name}?warehouse={warehouse}&role={role}'.format(
            user=s.USER_NAME, password=s.PASSWORD, account_identifier=s.ACCOUNT, database=s.DATABASE,
            schema_name=s.SCHEMA, warehouse=s.WAREHOUSE, role=s.ROLE))

    llm = AzureOpenAI(openai_api_key=api_key, engine=engine, model_name=model_name, temperature=0.0,
                      deployment_id=deployment_id)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        #memory=ConversationBufferWindowMemory(k=2),
    )

    ###############

    _DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    {table_info}
    Always use INTBM2023C table for all queries
    Always use double quotes around column names both in select and where clauses
    When someones asks for Spend or Impressions then use the Metric Name Column to look for the value and retrieve the Metric Value 
    Always use Impressions when asked for impressions or any derivation of impressions
 
    {question}
    Question: {input}"""

    #prompt = PromptTemplate(
     #   input_variables=["input", "table_info","question", "dialect"], template=_DEFAULT_TEMPLATE
    #)
    prompt = question
##########################################
    print(prompt)
    #print(response['choices'][0]['message']['content'])
    answer=agent_executor.run(prompt)
    return question, answer

def get_semantic_answer_snowflake_test(question):
    QUERY = "show tables"
    snowflake_loader = SnowflakeLoader(
        query=QUERY,
        user='admin',
        password='Sony@2018',
        account='sony',
        warehouse='SPHEIT',
        role='CSG',
        database='FIVETRAN_DATABASE',
        schema='DASH',
    )
    snowflake_documents = snowflake_loader.load()
    answer=snowflake_documents
    return question, answer