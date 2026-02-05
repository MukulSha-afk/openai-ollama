import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

st.title("LangChain Demo with Google Gemma 1B")

input_text = st.text_input("What question do you have?")
ask = st.button("Ask")

prompt = PromptTemplate(
    input_variables=["input"],
    template="{input}"
)

llm = Ollama(model="gemma3:1b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if ask and input_text:
    response = chain.invoke({"input": input_text})
    st.write(response)
