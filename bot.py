import os
import logging
import google.generativeai as genai
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 1. Gemini AI Setup
# Yahan apni bilkul nayi API Key check kar lein
GEMINI_KEY = "AIzaSyAQccwr30Hpjn6PEyJlo6kcHHyoTbKKlnY"
genai.configure(api_key=GEMINI_KEY)

# Safety settings taaki bot error kam de
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    safety_settings=safety_settings
)

# 2. Flask setup (Render ko zinda rakhne ke liye)
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
        else:
            await update.message.reply_text("AI ne koi jawab nahi diya, kuch aur pucho.")
    except Exception as e:
        # Error aane par exact message dikhayega
        await update.message.reply_text(f"Opps! Error: {str(e)[:100]}")

if __name__ == '__main__':
    Thread(target=run_flask).start()
    
    # --- APNA TELEGRAM BOT TOKEN ---
    TOKEN = "8517096826:AAGfHRlT0vB2Y1_T9X40y_AY8wwQPGZ1HJ8" 
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ai_chat))
    
    print("Bot is starting...")
    app_bot.run_polling()
