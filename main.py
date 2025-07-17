from fastapi import FastAPI, Query
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

app = FastAPI()

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_string = os.environ["SESSION_STRING"]

@app.get("/search")
def search_telegram(number: str = Query(...)):
    result = asyncio.run(handle_query(number))
    return {"response": result}

async def handle_query(number):
    output = None
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        try:
            await client.send_message('@IntelXOSINTBot', '/start')
            await asyncio.sleep(2)

            async for msg in client.iter_messages('@IntelXOSINTBot', limit=1):
                buttons = msg.buttons
                if not buttons:
                    return "No buttons found"
                await buttons[1][0].click()  # Tap button 3
                break

            await asyncio.sleep(2)
            await client.send_message('@IntelXOSINTBot', number)
            await asyncio.sleep(3)

            async for msg in client.iter_messages('@IntelXOSINTBot', limit=1):
                output = msg.text
                break

        except Exception as e:
            return f"ERROR: {str(e)}"

    return output or "No response"
