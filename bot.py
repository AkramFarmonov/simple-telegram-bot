import os
import random
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Savollar ro'yxati (variantlar va to'g'ri javob)
QUIZ_QUESTIONS = [
    {
        "savol": "1. O'zbekiston poytaxti qaysi shahar?",
        "variantlar": ["A) Samarqand", "B) Toshkent", "C) Buxoro", "D) Namangan"],
        "javob": "B"
    },
    {
        "savol": "2. 2 x 5 nechiga teng?",
        "variantlar": ["A) 7", "B) 10", "C) 12", "D) 15"],
        "javob": "B"
    },
    {
        "savol": "3. Dasturlashda 'print' nimani anglatadi?",
        "variantlar": ["A) O'chirish", "B) O'qish", "C) Chop etish (ekranga chiqarish)", "D) Qo'shish"],
        "javob": "C"
    },
    {
        "savol": "4. Quyidagi qaysi biri hayvon emas?",
        "variantlar": ["A) Qush", "B) Baliq", "C) Daraxt", "D) Ilon"],
        "javob": "C"
    },
]

# Har bir foydalanuvchi uchun sessionda so'ngi savol va javob saqlanadi
user_sessions = {}

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men ta'limiy botman. /quiz buyrug'ini yuboring va savollarga javob bering! Yordam uchun /help ni bosing."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Buyruqlar:
/start - Botni ishga tushirish
'ta'limiy bot haqida ma'lumot
/help - Yordam menyusi
/quiz - Random savol olish
Variant javobni harf bilan yuboring (masalan: B)
"""
    await update.message.reply_text(help_text)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Random savol tanlash
    question = random.choice(QUIZ_QUESTIONS)
    user_sessions[user_id] = question  # Sessionga saqlash
    # Variantlarni reply keyboard sifatida chiqarish
    variants = [[v] for v in question["variantlar"]]
    markup = ReplyKeyboardMarkup(variants, one_time_keyboard=True, resize_keyboard=True)
    savol_text = f"{question['savol']}\n" + "\n".join(question["variantlar"])
    await update.message.reply_text(savol_text, reply_markup=markup)

async def answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answer = update.message.text.strip().upper()
    if user_id not in user_sessions:
        await update.message.reply_text("Avval /quiz buyrug'ini yuboring!")
        return
    question = user_sessions[user_id]
    correct = question["javob"]
    if user_answer == correct:
        await update.message.reply_text("✅ To'g'ri javob!")
    else:
        await update.message.reply_text(f"❌ Noto'g'ri. To'g'ri javob: {correct}")
    del user_sessions[user_id]


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_handler))
    print("Ta'limiy bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
