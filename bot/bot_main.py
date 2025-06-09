from telegram.ext import (
    Application,
    Filters,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler
)
from config import config
import handlers as hd
import database as db


async def main():
    pool = db.create_pool()
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.bot_data['pool'] = pool

    ingredients_search_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(hd.handle_ingredients_button, pattern='^search_by_ingredients$')],
        states={
            hd.SEARCH_BY_INGREDIENTS: [MessageHandler(hd.search_by_ingredients)]
        },
        fallbacks=[CommandHandler('cancel', hd.cancel)]
    )
    name_search_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(hd.handle_name_button, pattern='^search_by_name$')],
        states={
            hd.SEARCH_BY_INGREDIENTS: [MessageHandler(Filters.TEXT & ~Filters.COMMAND, hd.search_by_name)]
        },
        fallbacks=[CommandHandler('cancel', hd.cancel)]
    )

    app.add_handler(CommandHandler("start", hd.start))
    app.add_handler(CommandHandler("help", hd.start))
    app.add_handler(ingredients_search_conv)
    app.add_handler(name_search_conv)
    app.add_handler(CallbackQueryHandler(hd.handle_random_button, pattern='^random_cocktail$'))
    app.add_handler(CallbackQueryHandler(hd.show_cocktails, pattern='^all_cocktails$'))
    app.add_handler(CallbackQueryHandler(hd.show_cocktail_details, pattern='^cocktail_'))
    app.add_handler(CallbackQueryHandler(hd.prev_next_button_handler, pattern='^(prev_page|next_page)$'))

    await app.run_polling()


if __name__ == "__main__":
    main()