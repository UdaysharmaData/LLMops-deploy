from fastapi import FastAPI
from fastapi.responses import StreamingResponse
# from schemas.chat_schema import Response
from services.llm_service import chatbot


app = FastAPI()




def bot_response(question:str):
    # config = {"configurable":{"thread_id":"1"}}
    # response = chatbot.invoke({"message":question},config=config)
    response = chatbot.invoke({"message":question})

    return response['message'][-1].content


@app.post("/chat/{question}")
def response(question:str):
    # return StreamingResponse(content=stream_response(question=question),media_type="text/event-stream") 
    return bot_response (question=question)