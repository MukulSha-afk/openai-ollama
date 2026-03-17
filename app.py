import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Traking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "True"
os.environ["LANGCHAIN_PROJECT "] = "https://smith.langchain.com/api/v1"

    ##//Prompt ChatPromptTemplat
    
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant for answering questions about agents."),
        ("human", "{input}"),
    ]   
)
def generate_responce(input, api_key, llm, temperature, max_tokens):

    if not api_key:
        return "⚠️ Please enter your OpenAI API Key in the sidebar."

    llm = ChatOpenAI(
        model=llm,
        api_key=api_key,   
        temperature=temperature,
        max_tokens=max_tokens
    )

    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"input": input})

    return answer


st.title("Q&A Chatbot")

##Sidebar for setting
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

## Drop down to select to select various openai models
llm = st.sidebar.selectbox("Select OpenAI Model", ["gpt-3.5-turbo", "gpt-4"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 500, 150)

## Main interface for user input
st.write("Ask a question about agents:")
user_input = st.text_input("Your Question")
if user_input:
    responce = generate_responce(user_input, api_key, llm, temperature, max_tokens)
    st.write(responce)
else:
    st.write("Please enter a question to get an answer.")    
