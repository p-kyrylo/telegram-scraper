from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
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
import webbrowser


load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('my_session', api_id, api_hash)

class FileFormat(Enum):
    JSON = 'json'
    CSV = 'csv'

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.start()
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get('/scrape_channel/{channel_name}')
async def scrape_channel(channel_name: str, format, limit: int = None, download_media: bool = False):
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
        
        file_name = f"{channel_name}_messages.{FileFormat(format).value}"
        savefile(file_name, messages, format)

        return FileResponse(file_name, media_type='application/octet-stream', filename=file_name)
        
    except ChannelInvalidError:
        raise HTTPException(status_code=400, detail="Invalid channel name.")
    
    except ChannelPrivateError:
        raise HTTPException(status_code=403, detail="The channel is private and cannot be scraped.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
def savefile(filename: str, content: list, format: str):
    match format:
        case FileFormat.JSON.value:
            with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(content, file, ensure_ascii=False, indent=4)
        case FileFormat.CSV.value:
            with open(filename, 'w', newline= '', encoding= 'utf-8') as file:
                if content:
                    writer = DictWriter(file, fieldnames=content[0].keys())
                    writer.writeheader()
                    writer.writerows(content)

     
if __name__=='__main__':
    webbrowser.open("http://localhost:8000/static/index.html") 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level='debug')