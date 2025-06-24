import os
from fastapi import FastAPI, Request
import openai
import requests

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUR_ID = os.getenv("OWNER_ID")  # Giới hạn 1 user

openai.api_key = OPENAI_API_KEY
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.post("/")
async def webhook(req: Request):
    data = await req.json()
    chat_id = data["message"]["chat"]["id"]
    user_id = data["message"]["from"]["id"]
    message = data["message"].get("text")

    if str(user_id) != str(YOUR_ID):
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id, "text": "Unauthorized."
        })
        return {"ok": True}

    if message:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}],
        )
        reply = response.choices[0].message.content
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id, "text": reply
        })

    return {"ok": True}
