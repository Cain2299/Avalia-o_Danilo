from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

response = model.invoke([HumanMessage(content="Qual é a capital do Brasil?")])
print(response.content)