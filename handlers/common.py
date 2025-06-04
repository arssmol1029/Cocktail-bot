from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ContextTypes
import re
import handlers as hd
import database as db

PAGE_LIMIT = 5
SEARCH_BY_NAME, SEARCH_BY_INGREDIENTS  = range (2)

async def process_start_command(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Поиск по ингредиенту", callback_data='search_by_ingredients'),
            InlineKeyboardButton("Поиск по названию", callback_data='search_by_name')
        ],
        [InlineKeyboardButton("Случайный коктейль", callback_data='random')],
        [InlineKeyboardButton("Список всех коктейлей", callback_data='all_cocktails')],
        [InlineKeyboardButton("Помощь по командам", callback_data='help')]
    ]
    await update.message.answer(
        "Добро пожаловать, я бот-бармен! Могу подобрать для тебя коктейль и подсказать, как его приготовить",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def search_by_ingredients(update, context):
    await update.message.answer(
        text="""
            Введите названия ингредиентов: \n
            Ввод через запятую, например, по запросу _ром, лайм_ я найду все коктейли, в составе который есть и ром, и лайм
        """, 
        parse_mode="MarkdownV2"
    )
    return SEARCH_BY_INGREDIENTS

async def handle_ingredients_input(update, context):
    try:
        ingredients = [x.strip() for x in update.message.text.split(',')]
        ingredients = [x for x in ingredients if x]
        
        if not ingredients:
            await update.message.answer("Укажите ингредиенты через запятую")
            return
        
        pool = context.bot_data['pool']
        async with pool.acquire() as conn:
            cocktails = await conn.fetch(db.GET_COCKTAILS_BY_INGREDIENTS, ingredients, PAGE_LIMIT + 1, 0)

        if not cocktails:
            await update.message.answer("Коктейли не найдены")
            return

        response = ""
        for i, cocktail in enumerate(cocktails):
            response += ""
        await update.message.answer(response)

    except Exception as e:
        await update.message.answer("Укажите ингредиенты через запятую")


async def search_by_name(update, context):
    await update.message.answer(text="Введите название коктейля:", parse_mode="MarkdownV2")
    return SEARCH_BY_NAME

