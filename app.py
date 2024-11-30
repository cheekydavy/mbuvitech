import os
import httpx
from flask import Flask, request, jsonify
from dotenv import load_dotenv

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

    # Start the processing and send replies accordingly
    handle_message(chat_id, text)

    return jsonify({'status': 'ok'})

async def handle_message(chat_id, text):
    # Responding with a 'composing' status
    send_presence_update(chat_id, 'composing')

    prompt = text  # You can customize the prompt or encode it if needed

    guru1 = os.getenv('CUSTOM_API_1')  # First custom API URL
    api_key = os.getenv('API_KEY')      # API key
    guru2 = os.getenv('CUSTOM_API_2')   # Second custom API URL

    try:
        # First API call
        async with httpx.AsyncClient() as client:
            response = await client.get(guru1, params={'apikey': api_key, 'q': prompt})
            data = response.json()
            result = data.get('response', {}).get('response')

            if not result:
                raise ValueError('No valid JSON response from the first API')

            await send_message(chat_id, result)

    except Exception as e:
        print('Error from the first API:', e)

        # Fallback to the second API call if the first one fails
        if guru2:  # Check if CUSTOM_API_2 is defined
            async with httpx.AsyncClient() as client:
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
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))import os
import httpx
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # Extract necessary information from incoming request
    message = data.get('message')
    chat_id = message['chat']['id']
    text = message.get('text') or (message.get('reply_to_message') and message['reply_to_message']['text'])

    if not text:
        return jsonify({'error': 'Please provide some text or quote a message to get a response.'})

            async with httpx.AsyncClient() as client:
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
    app.run(port=int(os.getenv("PORT", 5000)))
