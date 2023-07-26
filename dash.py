import streamlit as st
from helper import get_semantic_answer
from helper import get_semantic_answer_native
from helper import get_semantic_answer_snowflake
from helper import get_semantic_answer_snowflake_test


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
    question = st.text_input("Question:")

    if question != '':
        answer, prompt = get_semantic_answer_snowflake(
            question)

        st.write(f"**Question:** {question}")
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
   st.header("How does this demo work?")
   st.markdown("""
               This demo leverages the following components to achieve a ChatGPT-like experience on unstructured documents:
               * **Azure OpenAI Service** to generate answers to questions
               * **Azure OpenAI Service Embeddings** to semantically extract the "meaning of a document"
               * **RediSearch** to store the embeddings and perform search queries
               * **Azure Form Recognizer** to extract the text from the documents
               """)
   #st.image("./architecture.png", caption="Solution Architecture")
   st.markdown("""
               So, what is happening here? Let's break it down:
               1. Firstly, we parse the documents in our knowledge base and extract the text using Azure Form Recognizer. We do this since data might be in PDF format, but it also allows to create smaller text chunks. We do not want to work on documents that are 100's of pages long.
               1. Next, we use Azure OpenAI Service Embeddings to semantically extract the "meaning of a document". This converts the sections of each document into a vector (basically a long series of numbers, 1536 to be more precise), which represents the semantics of each document section. We store this vector in RediSearch.
               1. As the user asks a question, we again use Azure OpenAI Service Embeddings to semantically extract the "meaning of the question". We then use RediSearch to find the most similar documents to the question. In our case, we use the top 3 documents. These documents are likely to contain the answer to our question.
               1. Now that we have the matching documents, we use Azure OpenAI Service to generate an answer to our question. To do this, we use the top 3 documents as the context to generate the answer, given the original question of the user. You can see this prompt when you click on the "Click here to see the prompt we've used to generate the answer" link.
               1. Finally, we return the answer to the user. Done!
               """)