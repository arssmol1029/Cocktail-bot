from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
import re
import database as db

PAGE_LIMIT = 5
SEARCH_BY_INGREDIENTS = 0
SEARCH_BY_NAME  = 0

async def process_start_command(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Поиск по ингредиенту", callback_data='search_by_ingredients'),
            InlineKeyboardButton("Поиск по названию", callback_data='search_by_name')
        ],
        [InlineKeyboardButton("Случайный коктейль", callback_data='random_cocktail')],
        [InlineKeyboardButton("Список всех коктейлей", callback_data='all_cocktails')]
    ]
    await update.message.answer(
        "Добро пожаловать, я бот-бармен! Могу подобрать для тебя коктейль и подсказать, как его приготовить",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def ingredients_button_handler(update, _):
    await update.message.answer(
        text="""
            Введите названия ингредиентов:\n
            Ввод через запятую, например, по запросу _*ром, лайм*_ я найду все коктейли, в составе который есть и ром, и лайм
        """, 
        parse_mode="MarkdownV2"
    )
    return SEARCH_BY_INGREDIENTS

async def search_by_ingredients(update, context):
    try:
        ingredients = [x.strip() for x in update.message.text.split(',')]
        ingredients = [x for x in ingredients if x]
        
        if not ingredients:
            await update.message.answer("Укажите ингредиенты через запятую")
            return SEARCH_BY_INGREDIENTS
        
        context.user_data['cocktail_name'] = ''
        context.user_data['cocktail_ingredients'] = ingredients
        context.user_data['page'] = 0

        return await show_cocktails(update, context)
        
    except Exception as e:
        await update.message.answer("Укажите ингредиенты через запятую")
        return SEARCH_BY_INGREDIENTS



async def name_button_handler(update, _):
    await update.message.answer(text="Введите название коктейля:", parse_mode="MarkdownV2")
    return SEARCH_BY_NAME

async def search_by_name(update, context):
    try:
        name = update.messageюtext
        
        if not name:
            await update.message.answer("Укажите название коктейля")
            return SEARCH_BY_NAME
        
        context.user_data['cocktail_name'] = name
        context.user_data['cocktail_ingredients'] = []
        context.user_data['page'] = 0
        
        return await show_cocktails(update, context)
        
    except Exception as e:
        await update.message.answer("Укажите название коктейля")
        return SEARCH_BY_NAME



async def random_button_handler(update, context):
    pool = context.bot_data['pool']

    async with pool.acquire() as conn:
        cocktail = await conn.fetchrow(db.GET_RANDOM_COCKTAIL)

    if not cocktail:
        await update.message.answer("Коктейли не найдены")
        return

    keyboard = []
    keyboard.append([InlineKeyboardButton("Показать полностью", callback_data='cocktail_' + str(cocktail['id']))])

    response = ""

    await update.message.answer(response, parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def show_cocktails(update, context):
    pool = context.bot_data['pool']
    page = context.user_data.get('page', 0)
    name = context.user_data.get('cocktail_name', '')
    ingredients = context.user_data.get('cocktail_ingredients', [])
        
    async with pool.acquire() as conn:
        if name:
            cocktails = await conn.fetch(db.GET_COCKTAILS_BY_NAME, name, PAGE_LIMIT + 1, page * PAGE_LIMIT)
        elif ingredients:
            cocktails = await conn.fetch(db.GET_COCKTAILS_BY_INGREDIENTS, ingredients, PAGE_LIMIT + 1, page * PAGE_LIMIT)
        else:
            cocktails = await conn.fetch(db.GET_ALL_COCKTAILS, PAGE_LIMIT + 1, page * PAGE_LIMIT)

    if not cocktails:
        await update.message.answer("Коктейли не найдены")
        return ConversationHandler.END

    keyboard = []
    
    navigation_buttons = []
    if len(cocktails) > PAGE_LIMIT:
        navigation_buttons.append(InlineKeyboardButton("➡️", callback_data='next_page'))
        
        context.user_data['page'] = page + 1
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("⬅️", callback_data='prev_page'))
    if navigation_buttons:
        keyboard.append(navigation_buttons)

    num_buttons = []
    response = ""
    for i in range(len(cocktails) - 1):
        response += ""
        num_buttons.append(InlineKeyboardButton(f"{i}", callback_data='cocktail_' + str(cocktails[i]['id'])))
    if num_buttons:
        keyboard.append(num_buttons)
    response += "\n\n_Если поиск отработал некорректно, попробуйте повторить запрос через команду */start*_"

    if update.callback_query:
        if keyboard:
            await update.callback_query.edit_message_text(response, parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup([keyboard])
            )
        else:
            await update.callback_query.edit_message_text(response, parse_mode="MarkdownV2")
    else:
        if keyboard:
            await update.message.answer(response, parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup([keyboard])
            )
        else:
            await update.message.answer(response, parse_mode="MarkdownV2")

    return ConversationHandler.END



async def prev_next_button_handler(update, context):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    current_page = context.user_data.get('page', 0)
    
    if data.startswith('next_'):
        new_page = current_page + 1
    elif data.startswith('prev_'):
        new_page = max(0, current_page - 1)
    context.user_data['page'] = new_page

    await show_cocktails(update, context)



async def cancel(update, context):
    if "cocktail_name" in context.user_data:
        del context.user_data["cocktail_name"]
    if "cocktail_ingredients" in context.user_data:
        del context.user_data["cocktail_ingredients"]

    update.message.answer("Как пожелаете, если понадоблюсь - обращайтесь", parse_mode="MarkdownV2")

    return ConversationHandler.END



async def show_cocktail_details(update, context):
    pool = context.bot_data['pool']
    cocktail_id = int(update.callback_query.data.split('_')[1])

    async with pool.acquire() as conn:
        cocktail = await conn.fetchrow(db.GET_COCKTAIL_BY_ID, cocktail_id)
        ingredients = await conn.fetch(db.GET_INGREDIENTS_FOR_COCKTAIL, cocktail_id)

    if not cocktail:
        await update.callback_query.answer("Коктейль не найден")
        return

    response = ""

    await update.message.answer(response, parse_mode="MarkdownV2")