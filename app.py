import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
import os
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

    # Start the processing and send replies accordingly
    handle_message(chat_id, text)

    return jsonify({'status': 'ok'})

async def handle_message(chat_id, text):
    # Responding with a 'composing' status is typically handled by your API
    send_presence_update(chat_id, 'composing')

    prompt = text  # You can customize the prompt or encode it if needed

    guru1 = os.getenv('CUSTOM_API_1')  # First custom API URL
    guru2 = os.getenv('CUSTOM_API_2')  # Second custom API URL

    try:
        # First API call
        async with httpx.AsyncClient() as client:
            response = await client.get(guru1, params={'prompt': prompt})
            data = response.json()
            result = data.get('response', {}).get('response')

            if not result:
                raise ValueError('No valid JSON response from the first API')

            await send_message(chat_id, result)

    except Exception as e:
        print('Error from the first API:', e)

        # Fallback to the second API call if the first one fails
        async with httpx.AsyncClient() as client:
            response = await client.get(guru2, params={'prompt': prompt})
            data = response.json()
            result = data.get('completion')

            await send_message(chat_id, result)

def send_presence_update(chat_id, status):
    # Implementation for sending the presence update
    # This will depend on the Telegram API library you are using
    pass

async def send_message(chat_id, text):
    # Implementation for sending the message back to Telegram
    # This will depend on the Telegram API library you are using
    
    # Replace `YOUR_TELEGRAM_TOKEN` with your actual bot token.
    url = f"https://api.telegram.org/bot{os.getenv('YOUR_TELEGRAM_TOKEN')}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 5000)))
 response back to the user
    await update.message.reply_text(bot_reply)

def main() -> None:
    """Start the Telegram bot."""
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Set up commands and message handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
