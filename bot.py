import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Salom! Men sizning test botingizman. Xabar yuboring!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Buyruqlar:
    /start - Botni ishga tushirish
    /help - Yordam menyusi
    """
    await update.message.reply_text(help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"Siz yozdingiz: {user_message}")

def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
