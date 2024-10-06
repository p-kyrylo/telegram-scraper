# Telegram Scraping Tool

This tool allows users to scrape messages from a specified Telegram channel. The scraped data can be saved as JSON or CSV format and can also include media downloads.

## Features

- Scrape messages from public Telegram channels.
- Save data in JSON or CSV formats.
- Option to download media from messages.
- Simple web interface for entering the channel name and message limit.

## Requirements

Before running the tool, ensure you have the following installed:

- Python 3.8 or later
- FastAPI
- Telethon
- Python-dotenv
- Uvicorn

### Install the dependencies:

```bash
pip install -r backend/requirements.txt
```

### Enviroment setup 

Create a **.env** file in the backend folder and add your Telegram credentials:

```bash
API_ID=your_api_id
API_HASH=your_api_hash
```

### Usage 

#### Run the application:

```bash
python main.py 
```
This will start the FastAPI server and open the web interface in your default browser. You can then access the interface at:

```bash
http://localhost:8000/static/index.html
```
all the scraped messages will be saved inside the `backend` folder, and media will be saved inside the `backend/media`folder.  