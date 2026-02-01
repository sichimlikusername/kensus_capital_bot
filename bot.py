import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from playwright.async_api import async_playwright

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("BTCUSD", callback_data="BTCUSD")]
    ]
    await update.message.reply_text(
        "Salom 👋\nSizga qaysi para kerak?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "BTCUSD":
        keyboard = [
            [
                InlineKeyboardButton("M1", callback_data="BTCUSD_1"),
                InlineKeyboardButton("M5", callback_data="BTCUSD_5"),
                InlineKeyboardButton("M15", callback_data="BTCUSD_15"),
                InlineKeyboardButton("H1", callback_data="BTCUSD_60"),
            ]
        ]
        await query.edit_message_text(
            "Timeframe tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    tf = query.data.split("_")[1]
    await send_chart(query, tf)

async def send_chart(query, tf):
    url = f"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval={tf}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)
        await page.screenshot(path="chart.png")
        await browser.close()

    await query.message.reply_photo(
        photo=open("chart.png", "rb"),
        caption=f"📊 BTCUSD | TF: {tf}"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.run_polling()
