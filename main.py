import telebot
from google.oauth2.service_account import Credentials
import gspread
import schedule
import random
import time
from datetime import datetime

BOT_TOKEN = "8527756554:AAFlIMd5biQ_gKJAAZuTrHnzGA_Yo-nISN8"
CHAT_ID = "-1003193612748"

bot = telebot.TeleBot(BOT_TOKEN)

# -------------------------------------
#  GOOGLE SHEETS CONNECT
# -------------------------------------

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)
client = gspread.authorize(creds)

sheet = client.open("QuizQuestionBank").sheet1

# -------------------------------------
#  FETCH QUESTIONS
# -------------------------------------

def get_questions(category, limit=10):
    all_rows = sheet.get_all_records()
    filtered = [q for q in all_rows if q['category'] == category]

    return random.sample(filtered, min(limit, len(filtered)))

# -------------------------------------
#  SEND QUIZ
# -------------------------------------

def send_quiz_set():
    categories = ["class8", "class9", "class10", "class11", "class12", "jee", "neet", "ias"]
    
    for cat in categories:
        questions = get_questions(cat, limit=1)  # 1 question per category

        for q in questions:
            bot.send_poll(
                CHAT_ID,
                question=f"{cat.upper()} | {q['question']}",
                options=[q['option1'], q['option2'], q['option3'], q['option4']],
                type="quiz",
                correct_option_id=int(q["correct"]) - 1,
                is_anonymous=False
            )

# -------------------------------------
#  WEEKLY TEST
# -------------------------------------

def send_weekly_test():
    questions = get_questions("jee", limit=20)
    bot.send_message(CHAT_ID, "📘 WEEKLY JEE TEST STARTING...")
    for q in questions:
        bot.send_poll(
            CHAT_ID,
            question=q['question'],
            options=[q['option1'], q['option2'], q['option3'], q['option4']],
            type="quiz",
            correct_option_id=int(q["correct"]) - 1,
            is_anonymous=False
        )

# -------------------------------------
#  MONTHLY TEST
# -------------------------------------

def send_monthly_test():
    questions = get_questions("ias", limit=50)
    bot.send_message(CHAT_ID, "📙 MONTHLY IAS MOCK TEST STARTING...")
    for q in questions:
        bot.send_poll(
            CHAT_ID,
            question=q['question'],
            options=[q['option1'], q['option2'], q['option3'], q['option4']],
            type="quiz",
            correct_option_id=int(q["correct"]) - 1,
            is_anonymous=False
        )

# -------------------------------------
#  SCHEDULE
# -------------------------------------

schedule.every().day.at("07:00").do(send_quiz_set)           # Daily quiz  
schedule.every().sunday.at("09:00").do(send_weekly_test)     # Weekly  
schedule.every().month.at("1 07:00").do(send_monthly_test)   # Monthly


print("Pro Quiz Bot Running...")

while True:
    schedule.run_pending()
    time.sleep(1)
