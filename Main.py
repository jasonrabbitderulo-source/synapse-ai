import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# O Render usa variáveis de ambiente por segurança
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Synapse AI Ativada! Pronto para o mercado global.")

if __name__ == '__main__':
    if not TOKEN:
        print("Erro: Variável TELEGRAM_TOKEN não encontrada.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        print("Bot em execução...")
        app.run_polling()
