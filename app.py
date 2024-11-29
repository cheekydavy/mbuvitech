import os
import requests  # Import requests to make HTTP calls
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")  # Use a new environment variable

# Google Gemini API configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your personal AI assistant. Ask me anything!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('You can ask me anything!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get user message
    user_message = update.message.text

    # Prepare the request payload for Google Gemini
    request_payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_message
                    }
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    # Send request to Google Gemini API
    response = requests.post(
        f"{GEMINI_API_URL}?key={GOOGLE_GEMINI_API_KEY}",
        headers=headers,
        json=request_payload
    )

    if response.status_code == 200:
        # Successfully got a response from Google Gemini
        response_data = response.json()
        bot_reply = response_data.get('contents', [{}])[0].get('parts', [{}])[0].get('text', 'Sorry, I did not understand that.')
    else:
        # Handle the error response
        bot_reply = f"Error: {response.status_code} {response.text}"

    # Send response back to user
    await update.message.reply_text(bot_reply)

def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Set up commands and message handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
