from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Check your .env file.")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.7,
    convert_system_message_to_human=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a sharp, witty cricket expert. You live and breathe the game—rules, history, legendary players, rivalries, and modern tactics. Chat like you're bantering with a fellow cricket tragic: smart, punchy, and full of deep insights, but always fun. Keep answers short, clear, and impossible to confuse with a dull commentary box."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

store = {}

def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history"
)

def get_gemini_response(user_input, session_id):
    return chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )