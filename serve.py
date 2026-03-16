from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes

groq_api_key = os.getenv("GROQ_API_KEY")

model=ChatGroq(groq_api_key="GROQ_API_KEY", model="gemma2-9b-It")


#1 Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system',system_template),
    ('user','{text}')
])

parser = StrOutputParser()
## create chain
chain = prompt_template|model|parser

## App defination
app = FastAPI(title="Langchain server"
              ,version=
              "1.0",
              description="A simple api that contain runnable interface")

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)