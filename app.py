import os
import httpx  # Use httpx for async HTTP calls
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")  # Ensure this is set correctly

# Google Gemini API configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your personal AI assistant. Ask me anything!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help instructions when the command /help is issued."""
    await update.message.reply_text('You can ask me anything!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and respond using the Google Gemini API."""
    # Get user message
import os
import httpx  # Use httpx for async HTTP calls
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from openai import DeepAI  # Import DeepAI

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure this is set correctly

# Initialize DeepAI client
client = DeepAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your personal AI assistant. Ask me anything!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help instructions when the command /help is issued."""
    await update.message.reply_text('You can ask me anything!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and respond using the DeepAI API."""
    # Get user message
    user_message = update.message.text

    # Prepare the request payload for DeepAI
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # Use your desired model here
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Get the response from the API
        bot_reply = completion.choices[0].message['content']
    except Exception as e:
        # Handle any exceptions or errors
        bot_reply = f"Error: {str(e)}"

    # Send response back to user
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
    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
