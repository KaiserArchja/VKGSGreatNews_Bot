import os
import telebot
import requests
from rss_parser import RSSParser

def Send_Message(message, rss_url):
    msg = message.text.split()
    try:
        if(len(msg) == 2 and int(msg[1]) <= 50 and rss_url != "https://www.irna.ir/rss"):
            item_num = int(msg[1])
        elif(len(msg) == 2 and int(msg[1]) <= 28):
            item_num = int(msg[1])
        else:
            item_num = 3
    except:
        bot.send_message(message.chat.id, "You entered unsupported number!")
        return
    print(msg)
    Answer = ""
    rss = requests.get(rss_url)
    parsed = RSSParser.parse(rss.content.decode("utf-8"))
    showing_num_5 = item_num//7
    for shownum in range(showing_num_5):
        Answer = ""
        for item in range(shownum*7, (shownum+1)*7):
            title = str(parsed.channel.items[item].title.content).split("\u200c")
            for i in title:
                Answer += i + " "
            Answer+= "\n"
            desc = str(parsed.channel.items[item].description.content).split("\u200c")
            for i in desc:
                Answer += i + " "
            Answer += "\n [Click Here]" + "(" +str(parsed.channel.items[item].content.link.content)+") "
            Answer+= "\n ------------\n"
        if Answer == "":
            pass
        else:
            bot.send_message(message.chat.id, Answer , parse_mode="Markdown")
    Answer = ""
    for shownum in range(showing_num_5*7, item_num):
        title = str(parsed.channel.items[shownum].title.content).split("\u200c")
        for i in title:
            Answer += i + " "
        Answer+= "\n"
        desc = str(parsed.channel.items[shownum].description.content).split("\u200c")
        for i in desc:
            Answer += i + " "
        Answer += "\n [Click Here]" + "(" +str(parsed.channel.items[shownum].content.link.content)+") "
        Answer+= "\n ------------\n"
    if Answer == "":
        pass
    else:
        bot.send_message(message.chat.id, Answer, parse_mode="Markdown")

API = os.getenv("API")

bot = telebot.TeleBot(API)
global Agency
global again


bot.set_my_commands([telebot.types.BotCommand(command="start", description="Start Of Bot"), 
                     telebot.types.BotCommand(command="persian_euronews", description="Persion Language of EuroNews"),
                     telebot.types.BotCommand(command="euronews", description="English Version of EuroNews"),
                     telebot.types.BotCommand(command="persian_irna", description="Perisan Version of IRNA")])

Greeting_Message = """Dear Subscriber. This Bot can help you to get latest News Around the world. You can choose your News Agency and get the latest News! \n \n
News Agencies: \n
/EuroNews ["Number of News(default:3)"]\n
/Persian_EuroNews ["Number of News(default:3)"] \n
/Persian_IRNA ["Number of News(default:3)"]
"""

@bot.message_handler(commands=["start", "help", "Start", "Help"])
def Help(message):
    bot.send_message(message.chat.id, Greeting_Message)

@bot.message_handler(commands=["Persian_EuroNews", "persian_euronews"])
def parsi_euronews_latest(message):
    global Agency
    Send_Message(message=message, rss_url="https://parsi.euronews.com/rss?format=mrss&level=theme&name=news")


@bot.message_handler(commands=["EuroNews", "euronews"])
def euronews_latest(message):
    global Agency
    Send_Message(message=message, rss_url="https://euronews.com/rss?format=mrss&level=theme&name=news")
@bot.message_handler(commands=["Persian_IRNA", "persian_irna"])
def irna_latest(message):
    Send_Message(message=message, rss_url="https://www.irna.ir/rss")
bot.polling(timeout=10)