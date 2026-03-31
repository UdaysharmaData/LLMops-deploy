from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from app.services.llm_service import chatbot
import os
from sqlalchemy import create_engine
from app.services.chat_history import DBSaver
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


saver  = DBSaver()



def bot_response(question: str, thread_id="1"):

    # Load previous state
    prev_state = saver.load(thread_id)

    if prev_state:
        state = prev_state
        state["message"].append(HumanMessage(content=question))
    else:
        state = {"message": [HumanMessage(content=question)]}

    # Run graph
    response = chatbot.invoke(state)

    # Save new state
    saver.save(thread_id, response)

    return response['message'][-1].content



@app.post("/chat/{question}")
def response(question:str):
    # return StreamingResponse(content=stream_response(question=question),media_type="text/event-stream") 
    return bot_response (question=question)