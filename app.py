import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure DeepAI
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your personal AI assistant. Ask me anything!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('You can ask me anything!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get user message
    user_message = update.message.text
    
    # Fetch response from DeepAI
    response = openai.ChatCompletion.create(
    model="gpt-3.5",  # Change this to gpt-3.5-turbo
    messages=[{"role": "user", "content": user_message}]
    )
    
    bot_reply = response.choices[0].message.content
    
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
