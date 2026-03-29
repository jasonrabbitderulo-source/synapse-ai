import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Configuração de Logs para ver erros no Render
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configurar o Cérebro (Gemini)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou a Synapse AI. Agora sou inteligente! O que queres perguntar?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # O bot envia a tua mensagem para a IA e recebe a resposta
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Erro: {e}")
        await update.message.reply_text("Tive um pequeno erro ao pensar. Tenta perguntar outra vez!")

if __name__ == '__main__':
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("Erro: Variável TELEGRAM_TOKEN não encontrada.")
    else:
        app = ApplicationBuilder().token(token).build()
        
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
        
        print("Bot em execução com IA...")
        app.run_polling()
