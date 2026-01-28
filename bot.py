import os
import google.generativeai as genai
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 1. Gemini AI Setup
# Yahan apni NAYI API Key dhyan se check karke daalo
GEMINI_KEY = "AIzaSyC9btAe3O6RjUkMbffSra1MJ1-eE8OEC9c"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Flask setup
app = Flask('')
@app.route('/')
def home(): return "AI Bot is Live!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 3. AI Chat Logic
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        response = model.generate_content(user_msg)
        if response.text:
            await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)[:50]}")

if __name__ == '__main__':
    Thread(target=run_flask).start()
    TOKEN = "8517096826:AAFqDuzx2AwCZvMZ2on6stRDAdcot2UYBTM" 
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ai_chat))
    app_bot.run_polling()
