import streamlit as st
from helper import get_semantic_answer
from helper import get_semantic_answer_native
from helper import get_semantic_answer_snowflake
from helper import get_semantic_answer_snowflake_test
import snowflake.connector
import settings

# Snowflake connection parameters
SNOWFLAKE_ACCOUNT = settings.ACCOUNT
SNOWFLAKE_USER = settings.USER_NAME
SNOWFLAKE_PASSWORD = settings.PASSWORD
SNOWFLAKE_WAREHOUSE = settings.WAREHOUSE
SNOWFLAKE_DATABASE = settings.DATABASE
SNOWFLAKE_SCHEMA = settings.SCHEMA

# Establish the connection
ctx = snowflake.connector.connect(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

# Write your SQL query
query = 'SELECT DISTINCT("Title") as Title_Name,MIN("Start Date") as Impressions FROM INTBM2023C GROUP BY "Title"'

# Execute the query
cursor = ctx.cursor()
cursor.execute(query)

# Fetch the data
data = cursor.fetchall()

# st.set_page_config(layout="wide")
hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

#st.image('./microsoft.png', width=200)
st.title('DASH-Chat ')
st.caption('Fireside Data Chat')
st.write('Welcome I am Marvin Dash Jr your Media Performance Campaign Tracker Assistant, looking forward to answering your questions and hopefully correctly')

tab1, tab2, tab3 = st.tabs(["DASH", "Sample questions", "How does this DASH work?"])

with tab1:
    st.write('Try asking a question like:\n\nWhat is the best performing campaign and for which Title?')
    # Extract the required data for the dropdown
    dropdown_data = [row[0] for row in data]

    # Create the multi-select dropdown
    selected_items = st.multiselect("Select a Title:", options=dropdown_data)

    # Display the selected items
    st.write("You selected:", selected_items)

    cursor.close()
    ctx.close()

    # Create a text input field for the question
    question = st.text_input("Enter your question:")

    # Check if any items are selected
    if selected_items:
        # Convert the selected items into a string
        selected_items_str = ",".join(selected_items)

        #Where Condtion
        where = "for the title(s)"

        # Concatenate the question field with the selected items string
        combined_text = f"{question} {where} ({selected_items_str})"
    else:
        combined_text = question

        # Display the concatenated text
    st.write("Combined text:", combined_text)

    if question != '':
        answer, prompt = get_semantic_answer_snowflake(
            combined_text)

        st.write(f"**Question:** {combined_text}")
        st.write(f"**Answer:** {answer}")
        with st.expander("Click here to see the prompt we've used to generate the answer", expanded=False):
            #prompt = prompt.replace('$',answer,'\$')
            st.markdown(f":star: **Short explanation**\n1. The first part of the prompt is the retrieved documents that were likely to contain the answer\n1. The second part is the actual prompt to answer our question\n\n:star: **Prompt:**\n{prompt}")
with tab2:
    st.write('Try asking questions like:')
    st.markdown("""**:blue[Overall Performance]**  :sunglasses:""")
    st.markdown("""*How many total impressions have we delivered between Date X and Date Y""")
    st.markdown("""*Has the overall performance been trending up/down/flat? :3:""")
    st.markdown("""*What is the performance trend week over week (general campaign and by individual spot)?:2: """)
    st.markdown("""*Pacing: How much $$ has the campaign delivered to date?  How many impressions? :4: """)
    st.markdown("""*Creative-Trailer How many impressions have delivered across all platforms? Views?  """)
    st.markdown("""*Creative-Trailer What platforms media is performing the best? """)
    st.markdown("""*Creative-Trailer How is it doing compared to benchmark? """)
    st.markdown("""*Creative General What are the top 3 performing spots in terms of engagement rate on Meta, TikTok, Snap? :12:""")
    st.markdown("""*Audience Reporting  What’s the top performing audience/demo on each platform?""")
    st.markdown("""*Audience Reporting What demos are being favored the most, with impression delivery?""")

    st.write("If you want a shorter answer, you can say \"Write a short answer\" or do the opposite and say \"Give me a long answer\".")
    st.write("You can also ask questions in other languages, e.g., try to ask a question in German or Spanish.")

with tab3:
   st.header("How does this DASH Chat work?")
   st.markdown("""
               * **DASH Chat Connects to the Snowflake Database using the SQL Alchemy connector for snowflake
               * **The SQL Alchemy Connector is invoked via a Langchain SQL Agent
               * **Using Streamlit we construct the prompt and enforce certain conditions
               * **We then use Langchain to perform the completion against the LLM in this use case we are using Azure Open AI GPT-4
               * **We are also setting the role and guidelines using Prompt templates
               * **No offline embeddings are being used 

               """)
