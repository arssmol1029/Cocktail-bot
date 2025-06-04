from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ContextTypes
from config import config
import handlers as hd
import database as db


async def main():
    pool = db.create_pool()
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.bot_data['pool'] = pool

    app.add_handler(CommandHandler("start", hd.start))

    await app.run_polling()


if __name__ == "__main__":
    main()