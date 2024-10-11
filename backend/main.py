from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import ChannelInvalidError, ChannelPrivateError
from enum import Enum
from csv import DictWriter
import os
import json
import uvicorn
from io import StringIO

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = None

class FileFormat(Enum):
    JSON = 'json'
    CSV = 'csv'

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = TelegramClient('my_session', api_id, api_hash)
    await client.start()
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get('/')
async def root():
    return RedirectResponse("/static/index.html")

@app.get('/scrape_channel/{channel_name}', response_class=PlainTextResponse)
async def scrape_channel(channel_name: str, format, limit: int | None = None, download_media: bool = False):
    try:
        print(f"Received channel name: {channel_name}")
        entity = await client.get_entity(channel_name)
        
        messages = []
        async for message in client.iter_messages(entity, limit=limit):
            messages.append({
                "message": message.text,
                "id": message.id,
                "date": message.date.isoformat()
            })

            if download_media and message.media:
                await message.download_media(file=f'media/{message.id}')
        
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found.")
        
        content = format_content(messages, format)

        return PlainTextResponse(content=content, media_type=f'application/{FileFormat(format).value}')

    except ChannelInvalidError:
        raise HTTPException(status_code=400, detail="Invalid channel name.")
    
    except ChannelPrivateError:
        raise HTTPException(status_code=403, detail="The channel is private and cannot be scraped.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
def format_content(content: list, format: str):
    match format:
        case FileFormat.JSON.value:
            return json.dumps(content, ensure_ascii=False, indent=4)
        case FileFormat.CSV.value:
            if content:
                string_stream = StringIO()
                writer = DictWriter(string_stream, fieldnames=content[0].keys())
                writer.writeheader()
                writer.writerows(content)
                return string_stream.getvalue()

if __name__=='__main__':
    uvicorn.run("main:app", host="192.168.100.134", port=8000, reload=True)