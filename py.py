from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup  
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters  
import random  
from uuid import uuid4  

TOKEN = "7643441213:AAEZMMUOh1JwNgN3xaawPh2t6AtbFPyKXII"  
users_cart = {}  # {user_id: {"items": [], "address": ""}}  
CRYPTO_WALLETS = ["BTC", "ETH", "XMR"]  

PRODUCTS = {  
    # 15 товаров  
    "🔥 Мефедрон (1г)": {"desc": "Стимулятор. Эффект: 2ч эйфории. Цена: $50", "price": 50},  
    "🌿 Spice (10г)": {"desc": "Синтетический каннабис. Цена: $20", "price": 20},  
    "💎 Кокаин (0.5г)": {"desc": "Элитный стимулятор. Цена: $80", "price": 80},  
    "🌈 LSD (200мкг)": {"desc": "12-часовой трип. Цена: $15", "price": 15},  
    "💉 Героин (доза)": {"desc": "Опиатный релакс. Цена: $100", "price": 100},  
    "🌀 Кетамин (1г)": {"desc": "Диссоциатив. Цена: $40", "price": 40},  
    "🎭 2C-B (таблетка)": {"desc": "Психоделик-эмпатоген. Цена: $25", "price": 25},  
    "☠️ Фентанил (доза)": {"desc": "Смертельный опиоид. Цена: $2", "price": 2},  
    "🌌 ДМТ (кристалл)": {"desc": "Прорыв в иные миры. Цена: $120", "price": 120},  
    "💊 МДМА (таблетка)": {"desc": "Эмпатия+эйфория. Цена: $30", "price": 30},  
    "⚡ Метамфетамин (1г)": {"desc": "Энергия на 12ч. Цена: $60", "price": 60},  
    "🌙 GHB (флакон)": {"desc": "Релакс+афродизиак. Цена: $45", "price": 45},  
    "🍄 Псилоцибин (3г)": {"desc": "Натуральные галлюцинации. Цена: $35", "price": 35},  
    "❄️ Мефедрон+Кокаин (микс)": {"desc": "Взрывная энергия. Цена: $130", "price": 130},  
    "💀 Карфентанил (доза)": {"desc": "Экстремальный опиоид. Цена: $5", "price": 5},  
}  

def start(update: Update, context):  
    user_id = update.effective_user.id  
    users_cart[user_id] = {"items": [], "address": ""}  
    update.message.reply_text(  
        text="💊 Добро пожаловать в NeuralDrugsBot!\n"  
             "👉 /products - Товары\n"  
             "👉 /cart - Корзина\n"  
             "👉 /consult - Консультация нейросети",  
        parse_mode="Markdown"  
    )  

def products_menu(update: Update, context):  
    buttons = [  
        [InlineKeyboardButton(name, callback_data=f"add_{name}")] for name in PRODUCTS  
    ]  
    update.message.reply_text("📦 Выберите товар:", reply_markup=InlineKeyboardMarkup(buttons))  

def add_to_cart(update: Update, context):  
    query = update.callback_query  
    product = query.data.split("_", 1)[1]  
    user_id = query.from_user.id  
    users_cart[user_id]["items"].append(product)  
    query.answer(f"✅ {product} добавлен в корзину!")  

def show_cart(update: Update, context):  
    user_id = update.effective_user.id  
    cart = users_cart.get(user_id, {"items": []})  
    total = sum(PRODUCTS[item]["price"] for item in cart["items"])  
    buttons = [  
        [InlineKeyboardButton("💳 Оплатить", callback_data="pay")],  
        [InlineKeyboardButton("❌ Очистить корзину", callback_data="clear_cart")]  
    ]  
    update.message.reply_text(  
        text=f"🛒 Корзина:\n" + "\n".join(cart["items"]) + f"\n\n💵 Итого: ${total}",  
        reply_markup=InlineKeyboardMarkup(buttons)  
    )  

def generate_crypto_invoice():  
    return f"{random.choice(CRYPTO_WALLETS)}:{str(uuid4()).replace('-', '')}"  

def payment(update: Update, context):  
    query = update.callback_query  
    user_id = query.from_user.id  
    total = sum(PRODUCTS[item]["price"] for item in users_cart[user_id]["items"])  
    address = generate_crypto_invoice()  
    query.message.reply_text(  
        f"⚠️ Оплатите ${total} на адрес:\n`{address}`\n"  
        "После оплаты отправьте TXID боту.",  
        parse_mode="Markdown"  
    )  

def neural_consult(update: Update, context):  
    user_text = update.message.text.lower()  
    responses = [  
        f"🤖 NeuralGPT: Рекомендую {random.choice(list(PRODUCTS))} для {'энергии' if 'устал' in user_text else 'релакса'}.",  
        f"🤖 NeuralGPT: {random.choice(list(PRODUCTS))} вызывает {random.choice(['выброс серотонина', 'паранойю', 'видения'])}.","🤖 NeuralGPT: Дозировка: начните с 1/4 дозы. Не умрите."  
    ]  
    update.message.reply_text(random.choice(responses))  

updater = Updater(TOKEN)  
updater.dispatcher.add_handler(CommandHandler("start", start))  
updater.dispatcher.add_handler(CommandHandler("products", products_menu))  
updater.dispatcher.add_handler(CommandHandler("cart", show_cart))  
updater.dispatcher.add_handler(CommandHandler("consult", neural_consult))  
updater.dispatcher.add_handler(CallbackQueryHandler(add_to_cart, pattern="^add_"))  
updater.dispatcher.add_handler(CallbackQueryHandler(payment, pattern="^pay$"))  
updater.dispatcher.add_handler(MessageHandler(Filters.text, neural_consult))