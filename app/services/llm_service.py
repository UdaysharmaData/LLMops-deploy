from langchain_groq import ChatGroq
from langgraph.graph import StateGraph , START,END
from dotenv import load_dotenv
from app.schemas.chat_schema import LLMstate

load_dotenv()

# class 
llm = ChatGroq(model="openai/gpt-oss-20b")

def chat_node(state:LLMstate):
    message = state['message']
    response = llm.invoke(message)
    return {'message':[response]}


graph = StateGraph(LLMstate)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

#***************Sqlite connection ******************
# conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)
# checkpointer = SqliteSaver(conn=conn)

chatbot = graph.compile()