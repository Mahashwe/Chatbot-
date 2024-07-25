from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import openai

openai.api_key = "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"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the chatbot API"}

@app.post("/chatbot")
async def chatbot_post(message: str = Form(...)):
    return await get_chatbot_response(message)

@app.get("/chatbot")
async def chatbot_get(message: str):
    return await get_chatbot_response(message)

@app.put("/chatbot")
async def chatbot_put(message: str):
    return await get_chatbot_response(message)


async def get_chatbot_response(message: str):
    prompt = f"User: {message}\nChatbot: "
    chat_history = []

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a content generation assistant for small businesses who replies only to content generation queries,do not answer to any other queries."},
            {"role": "user", "content": "For example Can you help me write a content related stuff or contentfor my product or a product description"},
            {"role": "user", "content": message},
        ]
    )

    bot_response = response.choices[0].message["content"].strip()
    chat_history.append(f"User: {message}\nChatbot: {bot_response}")

    return {"user_input": message, "bot_response": bot_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)