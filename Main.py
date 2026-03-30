import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# 1. Configurar IA (Usando o modelo Flash que é melhor para o plano grátis)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Servidor Web para o Render não dar Timed Out
class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Online")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', port), WebHandler).serve_forever()

# 3. Lógica do Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Synapse AI pronta! O que queres saber?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Gera a resposta com a IA
        response = model.generate_content(update.message.text)
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("A IA não conseguiu gerar texto desta vez.")
    except Exception as e:
        print(f"Erro na IA: {e}")
        await update.message.reply_text("Tive um erro ao pensar. Verifica se a API KEY está correta no Render!")

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    token = os.environ.get("TELEGRAM_TOKEN")
    # O drop_pending_updates=True limpa conflitos antigos ao ligar
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    
    print("Bot Iniciado!")
    app.run_polling(drop_pending_updates=True)
