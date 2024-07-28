from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import openai

openai.api_key = "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"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origins you want to allow
    allow_credentials=True, #cookies
    allow_methods=["*"], #get post put
    allow_headers=["*"], 
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the chatbot API"} #welcome msg display

@app.post("/chatbot")
async def chatbot_post(message: str = Form(...)):
    return await get_chatbot_response(message) #user input posted

@app.get("/chatbot")
async def chatbot_get(message: str):
    return await get_chatbot_response(message) #queryparamater - to send msg to server in url

@app.put("/chatbot")
async def chatbot_put(message: str):
    return await get_chatbot_response(message) #recives msg from client via url and returns response from chatbot


async def get_chatbot_response(message: str):
    prompt = f"User: {message}\nChatbot: " #fstring used , responses stored in array to update memory
    chat_history = []

    response = openai.ChatCompletion.create(  #This sends a request to the OpenAI API to get a response from the chatbot.
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a content generation assistant for small businesses who replies only to content generation queries,do not answer to any other queries."},
            {"role": "user", "content": "For example Can you help me write a content related stuff or contentfor my product or a product description"},
            {"role": "user", "content": message},  
        ]
    )


    bot_response = response.choices[0].message["content"].strip() #remove spaces
    chat_history.append(f"User: {message}\nChatbot: {bot_response}") # add to memory

    return {"user_input": message, "bot_response": bot_response} #returns message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
