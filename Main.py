import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# 1. Cérebro da IA
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# 2. Servidor Web Simples para o Render não dar erro
class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Synapse AI esta viva!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), WebHandler)
    server.serve_forever()

# 3. Funções do Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá Gelson! Sou a Synapse AI. O que vamos criar hoje?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except:
        await update.message.reply_text("Tive um erro ao pensar. Tenta de novo!")

if __name__ == '__main__':
    # Inicia o servidor web numa thread separada
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Inicia o Bot
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    
    print("Bot e Servidor Web iniciados!")
    app.run_polling()
