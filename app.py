import os
import httpx
import asyncio
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()  # Load environment variables from .env file

# Define the custom API URL
API_URL = "https://api.gurusensei.workers.dev/llama?prompt={prompt}"

async def handle_webhook(request):
    data = await request.json()
    # Extract necessary information from the incoming request
    message = data.get('message')
    chat_id = message['chat']['id']
    text = message.get('text') or (message.get('reply_to_message') and message['reply_to_message']['text'])

    if not text:
        return web.json_response({'error': 'Please provide some text or quote a message to get a response.'})
    
    # Start the processing and send replies accordingly
    await handle_message(chat_id, text)

    return web.json_response({'status': 'ok'})

async def handle_message(chat_id, text):
    # Responding with a 'composing' status
    await send_presence_update(chat_id, 'composing')

    prompt = text  # You can customize the prompt or encode it if needed

    try:
        # API call to custom endpoint
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL.format(prompt=prompt))
            data = response.json()
            result = data.get('completion')  # Assuming you get 'completion' in the response

            if not result:
                raise ValueError('No valid JSON response from the API')

            await send_message(chat_id, result)

    except Exception as e:
        print('Error from the API:', e)

async def send_presence_update(chat_id, status):
    # Placeholder for sending the presence update
    # This will depend on the Telegram API library you are using
    pass

async def send_message(chat_id, text):
    # Send the message back to Telegram
    url = f"https://api.telegram.org/bot{os.getenv('YOUR_TELEGRAM_TOKEN')}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.post('/webhook', handle_webhook)])  # Route to handle webhooks
    web.run_app(app, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))import os
import httpx
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import asyncio

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # Extract necessary information from the incoming request
    message = data.get('message')
    chat_id = message['chat']['id']
    text = message.get('text') or (message.get('reply_to_message') and message['reply_to_message']['text'])

    if not text:
        return jsonify({'error': 'Please provide some text or quote a message to get a response.'})

 with httpx.AsyncClient() as client:
                response = await client.get(guru2, params={'prompt': prompt})
                data = response.json()
                result = data.get('completion')

                await send_message(chat_id, result)

def send_presence_update(chat_id, status):
    # Placeholder for sending the presence update
    # This will depend on the Telegram API library you are using
    pass

async def send_message(chat_id, text):
    # Send the message back to Telegram
    url = f"https://api.telegram.org/bot{os.getenv('YOUR_TELEGRAM_TOKEN')}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
