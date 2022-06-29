import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
import random
from main import checker, dispatcher , game
import json
import os
from telegram.ext.dispatcher import run_async
import time
from main import database as DB
import requests

DB_PATH=os.environ['DATABASE_URL']
DB.init(DB_PATH)
DB.setup()

#state
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)
#callback data
S_START , S_INCREASE ,S_POP , SS_POP, FIRST , SECOND ,THIRD,CHECK, SHOW, *_ = range(1000)
owners = [163494588,652962567,1027794428,801509492,935241907]

ancts = [{''
}]

my_hero = [
{'heroname': '綠谷出久',
'heroeng': 'Midoriya Izuku',
'heropic': 'https://telegra.ph/file/941400195a0a69e52e50a.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'heroname': '爆豪勝己',
'heroeng': 'Bakugo Katsuki',
'heropic': 'https://telegra.ph/file/06acfd23cd90d1046c192.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'heroname': '轟焦凍',
'heroeng': 'Todoroki Shoto',
'heropic': 'https://telegra.ph/file/cb7a798294d81ff21076e.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'heroname': '蛙吹梅雨',
'heroeng': 'Asui Tsuyu',
'heropic': 'https://telegra.ph/file/3a020708800371fdbc23f.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'heroname': '切島銳兒郎',
'heroeng': ' Kirishima Eijirou',
'heropic': 'https://telegra.ph/file/03fe8e76ea1b870aa2245.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'heroname': '麗日御茶子',
'heroeng': 'Uraraka Ochako',
'heropic': 'https://telegra.ph/file/1290e2b4b540ffd956ab6.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'heroname': '飯田天哉',
'heroeng': 'Lida Tenya',
'heropic': 'https://telegra.ph/file/32098a70501394c69a56a.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'heroname': '心操人使',
'heroeng': 'Shinso Hitoshi',
'heropic': 'https://telegra.ph/file/60dd02600c66f9c67fdde.jpg',
'herostar': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'}
]

def draw(update ,context):
    msg = update.message.text.split()[-1]
    user = update.effective_user.name
    user_id = update.effective_user.id
    #random.choice(list, weights=(20, 50, 30, 10), k=1)
    #aa = random.choice(ancts)
    aa = random.choices(ancts, (0.0125,0.0125,0.0125,0.008,0.008,0.008,0.008,0.008,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,), k=1)
    '''bb = aa['name']
    pic = aa['link']
    star = aa['star']
    eng = aa['eng']'''
    bb = aa[0]['name']
    pic = aa[0]['link']
    star = aa[0]['star']
    eng = aa[0]['eng']

    hero = random.choices(my_hero,(0.025,0.10,0.10,0.155,0.155,0.155,0.155,0.155,),k=1) 
    heropic = hero[0]['heropic']
    herostar = hero[0]['herostar']
    heroname = hero[0]['heroname']
    heroeng = hero[0]['heroeng']
    

    user_exp = DB.get_user_value(user_id, "exp")
    user_level = DB.get_user_value(user_id, "level")
    user_diamonds = DB.get_user_value(user_id, "diamonds")
    user_bagslot = DB.get_user_value(user_id, "bagslot")
    user_maxbagslot = DB.get_user_value(user_id, "maxbagslot")
    if user_diamonds ==None:
        update.message.reply_text('先启动\n /starts')
        return -1
    if user_diamonds < 5:
        update.message.reply_text('不够魔法石💎\nNot Enough Diamonds💎')
        return -1
    if user_bagslot>=user_maxbagslot:
        update.message.reply_text('背包已满\nBag full')
        return -1


    if msg == '古币' or msg == 'gubi' or msg == '古幣':
     DB.add_diamonds(user_id, -5)
     DB.add_slot(user_id)
     a = update.message.reply_text(f'3')
     a.edit_text('2')
     a.edit_text('1')
     context.bot.delete_message(chat_id =update.effective_chat.id , message_id = a.message_id)
     context.bot.send_photo(chat_id=update.message.chat.id,
            photo=f'{pic}',
            caption=f'{user} 你拿到/You Got : \n\n<b>{bb}</b>'
                    f'\n{eng}\n\n稀有度/Rarity : \n{star}\n\n'
                    f'◈剩余魔法石/Diamond left : <b>{user_diamonds-5}</b> 💎\n'
                    f'◈背包空间/bag slots : <b>{user_bagslot+1}/{user_maxbagslot}</b>📦\n\n\n'
                    f'<i><b>**卡片以加入背包/Card added to bag**</b></i>', parse_mode=ParseMode.HTML
        )
     DB.add_user_card(user_id,bb,eng)
     DB.add_exp(user_id, 500)
     if user_exp >= user_level*500:
         DB.add_exp(user_id,-user_exp)
         DB.add_level(user_id)
         DB.add_diamonds(user_id , 5)
         context.bot.send_message(chat_id=update.effective_chat.id, text=f'{user} 升级到了 level : {user_level + 1}\n 魔法石 +5 \nDiamonds +5\n\n再按一次 /inventory 刷新\ntype /inventory again to refresh'
                                                                         f'\n再按一次 /inventory') 
 
    elif msg == '我英' or msg == 'myhero':
     DB.add_diamonds(user_id, -5)
     DB.add_slot(user_id)
     a = update.message.reply_text(f'3')
     a.edit_text('2')
     a.edit_text('1')
     context.bot.delete_message(chat_id =update.effective_chat.id , message_id = a.message_id)
     context.bot.send_photo(chat_id=update.message.chat.id,
            photo=f'{heropic}',
            caption=f'{user} 你拿到/You Got : \n\n<b>{heroname}</b>'
                    f'\n{heroeng}\n\n稀有度/Rarity : \n{herostar}\n\n'
                    f'◈剩余魔法石/Diamond left : <b>{user_diamonds-5}</b> 💎\n'
                    f'◈背包空间/bag slots : <b>{user_bagslot+1}/{user_maxbagslot}</b>📦\n\n\n'
                    f'<i><b>**卡片以加入背包/Card added to bag**</b></i>', parse_mode=ParseMode.HTML
        )
     DB.add_user_card(user_id,heroname,heroeng)
     DB.add_exp(user_id, 500)
     if user_exp >= user_level*500:
         DB.add_exp(user_id,-user_exp)
         DB.add_level(user_id)
         DB.add_diamonds(user_id , 5)
         context.bot.send_message(chat_id=update.effective_chat.id, text=f'{user} 升级到了 level : {user_level + 1}\n 魔法石 +5 \nDiamonds +5\n\n再按一次 /inventory 刷新\ntype /inventory again to refresh') 
                            
     
    else:
        update.message.reply_text('没这个卡池/或者还没加入\n\n'
                                  '目前卡池 : \n'
                                  '◆ /Draw 古币\n'
                                  '◆　。。。。。。', parse_mode=ParseMode.HTML)


def starts(update , context):
    user_name = update.effective_user.first_name
    user = update.effective_user
    username = update.effective_user.name
    user_id = update.effective_user.id
    DB.add_user(user_id)
    update.message.reply_text(f'♢ 欢迎 ♢ \n*{user_name}*\n*ID :* {user_id}'
                              f'\n*USERNAME : {username}*\n'
                              f'*您的资料已开始记录在数据库*\n\n[点击这里/Click here](https://t.me/Game_Gamez)', parse_mode =ParseMode.MARKDOWN_V2)
    logger.info("User %s started the conversation.", user.first_name)


def shop(update , context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    cd = context.chat_data
    cd["id"] = id
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
        update.message.reply_text("use in pm \n请私聊机器人")
        return -1'''
    keyboard = [
        [InlineKeyboardButton("买称号", callback_data="name")],
        [InlineKeyboardButton("精魄", callback_data="e")],
        [InlineKeyboardButton("音符兑换", callback_data="f")],
        [InlineKeyboardButton("素材", callback_data="g")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("<u>欢迎来到商店🏪</u>\n<b>请点击想要进去的区域</b>\n\n(目前只有买称号可以罢了，其他按钮还没弄好)",
                              parse_mode = ParseMode.HTML, reply_markup=reply_markup)
    return FOUR

def name1(update , context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    cd = context.chat_data
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("1", callback_data="1"),InlineKeyboardButton("2", callback_data="2")],
        [InlineKeyboardButton("3", callback_data="3"),InlineKeyboardButton("4", callback_data="4")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("以下是可以被购买的称号:\n\n"
                            "1. <b>赌神之塔</b>\n<b>价格 :</b> 💎5000\n\n"
                            "2. <b>最接近神的男人</b>\n<b>价格 :</b> 💎1000\n\n"
                            "3. <b>玛雅万岁</b>\n<b>价格 :</b> 💎500\n\n"
                            "4. <b>Hoo 之守护者</b>\n<b>价格 :</b> 💎70\n\n", parse_mode = ParseMode.HTML, reply_markup=reply_markup)
    return FOUR

def finname(update , context):
    name = update.effective_user.first_name
    cd = context.chat_data
    user_id = cd["id"]
    c = DB.get_name(user_id, name)
    
    user_diamonds = DB.get_user_value(user_id, "diamonds")
    query = update.callback_query
    if query.data == "1":
     if ('赌神之塔',) not in c:
      if user_diamonds>=5000:
       query.edit_message_text(f"你现在拥有称呼: \n\n <b>赌神之塔</b>\n\n{c}", parse_mode = ParseMode.HTML)
       DB.add_diamonds(user_id, -5000)
       DB.add_name(user_id, "赌神之塔")
      else:
         query.edit_message_text("不够宝石")
     else:
         query.edit_message_text("已经有此称号了")
    if query.data == "2":
     if ('最接近神的男人',) not in c:
      if user_diamonds >= 1000:
       query.edit_message_text("你现在拥有称呼: \n\n <b>最接近神的男人</b>",parse_mode = ParseMode.HTML)
       DB.add_diamonds(user_id, -1000)
       DB.add_name(user_id, "最接近神的男人")
      else:
         query.edit_message_text("不够宝石")
     else:
      query.edit_message_text("已经有此称号了")
    if query.data == "3":
     if ('玛雅万岁',) not in c:
      if user_diamonds >= 500:
       query.edit_message_text("你现在拥有称呼: \n\n <b>玛雅万岁</b>",parse_mode = ParseMode.HTML)
       DB.add_diamonds(user_id, -500)
       DB.add_name(user_id, "玛雅万岁")
      else:
         query.edit_message_text("不够宝石")
     else:
      query.edit_message_text("已经有此称号了")
    if query.data == "4":
     if ('Hoo 之守护者',) not in c:
      if user_diamonds >= 70:
       query.edit_message_text("你现在拥有称呼: \n\n <b>Hoo 之守护者</b>",parse_mode = ParseMode.HTML)
       DB.add_diamonds(user_id, -70)
       DB.add_name(user_id , "Hoo 之守护者")
      else:
         query.edit_message_text("不够宝石")
     else:
      query.edit_message_text("已经有此称号了")
    return FOUR
    
    
def inventory(update , context):
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    user_diamonds = DB.get_user_value(user_id, "diamonds")
    user_bagslot = DB.get_user_value(user_id, "bagslot")
    user_maxbagslot = DB.get_user_value(user_id, "maxbagslot")
    user_gold = DB.get_user_value(user_id, "gold")
    user_exp = DB.get_user_value(user_id, "exp")
    user_level = DB.get_user_value(user_id, "level")
    chenghu = DB.get_name(user_id, "name")
    #context.bot.send_message(chat_id = update.effective_chat.id , text = f'{chenghu}')
    b = 1 
    finS = ''
    for i in chenghu:
     finS+= str(b) + '. ' + str("".join(i))+ "\n"
     b+=1
    if user_exp >= user_level * 500:
        DB.add_exp(user_id, -user_exp)
        DB.add_level(user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{user_name} 升级到了 level : {user_level + 1}\n type /inventory again to refresh'
                                                                         f'\n再按一次 /inventory 刷新')

    if user_diamonds ==None:
        update.message.reply_text('先启动 /start')
        return -1
    keyboard = [
        [InlineKeyboardButton('龙刻', callback_data='dragon'),InlineKeyboardButton('素材', callback_data='material')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'<b>{user_name}\'s Inventory</b>\n'
                              f'ID : <code>{user_id}</code>\n\n'
                              f'<b>🧬 等级/Level : {user_level} </b>\n'
                              f'<code>exp : {user_exp}/{user_level*500}</code>\n\n'
                              f'<b>🟡 金币/Gold  : {user_gold}</b>\n'
                              f'<b>💎 魔法石/Diamonds  : {user_diamonds}</b>\n'
                              f'<b>📦 背包空间/Bagpack : {user_bagslot}/{user_maxbagslot}</b>\n\n\n'
                              f'<u><b>🎖称号🎖</b></u>\n'
                              f'{finS}\n\n'
                              #f'<b>⚡ 体力/energy</b> : <b>30/30</b>\n\n\n'
                              f'<i>button is not done yet\n按钮没功能。摆美罢了</i>'
                              , parse_mode =ParseMode.HTML, reply_markup=reply_markup)

def add(update , context):
    if not update.message.reply_to_message:
             update.message.reply_text('reply to someone')
             return
    msg = update.message.text.split()[1]
    user_name = update.message.from_user.first_name
    to = update.message.reply_to_message.from_user.first_name
    to_id = update.message.reply_to_message.from_user.id
    user_id = update.message.from_user.id

    a = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id).status

    
    msg = int(msg)

    if user_id in owners:
         DB.add_diamonds(to_id, msg)
         update.message.reply_text(f'{user_name} 奖励 {msg}魔法石💎给 {to}\n'
                               f'{user_name} gift {msg} diamonds to {to}')

    else:
         update.message.reply_text('not authorized')
         return -1


def give(update , context):
    if not update.message.reply_to_message:
             update.message.reply_text('reply to someone')
             return
    user = update.message.from_user.first_name
    to = update.message.reply_to_message.from_user.first_name
    to_id = update.message.reply_to_message.from_user.id
    from_id = update.message.from_user.id
    from_gold = DB.get_user_value(from_id, "gold")
    try:
     msg = update.message.text.split(None,1)[1]
     msg = int(msg)
     if from_gold<=0:
        update.message.reply_text('金币数量错误/Invalid Amount')
        return -1
     if from_gold< int(msg):
        update.message.reply_text('您不够金币来支付这笔款/Not Enough Gold for Payment')
        return -1
     if msg <=0:
        update.message.reply_text('错误/ Error')
        return -1
    except TypeError:
        update.message.reply_text('这是数字吗？/ is this number?')
        return -1
    except IndexError:
        update.message.reply_text('这是数字吗？/ is this number?')
        return -1
    except ValueError:
        update.message.reply_text('这是数字吗？/ is this number?')
        return -1
    except AttributeError:
        update.message.reply_text('回复人/ reply to someone')
        return -1

    DB.add_gold(to_id, msg)
    DB.minus_gold(from_id, msg)
    update.message.reply_text(f'{user}支付{msg} 金币🟡给 {to}\n'
                              f'{user} sent {msg} gold🟡 to {to}')

def gift(update , context):
    if not update.message.reply_to_message:
             update.message.reply_text('reply to someone')
             return
    user = update.message.from_user.first_name
    to = update.message.reply_to_message.from_user.first_name
    to_id = update.message.reply_to_message.from_user.id
    from_id = update.message.from_user.id
    from_gold = DB.get_user_value(from_id, "diamonds")
    try:
     msg = update.message.text.split(None,1)[1]
     msg = int(msg)
     if from_gold<=0:
        update.message.reply_text('魔法石数量错误/Invalid Amount')
        return -1
     if from_gold< int(msg):
        update.message.reply_text('您不够魔法石来支付这笔款/Not Enough diamonds for Payment')
        return -1
     if msg <=0:
        update.message.reply_text('错误/ Error')
        return -1
    except TypeError:
        update.message.reply_text('这是数字吗？/ is this number?')
        return -1
    except IndexError:
        update.message.reply_text('这是数字吗？/ is this number?')
        return -1
    except ValueError:
        update.message.reply_text('这是数字吗？/ is this number?')
        return -1
    except AttributeError:
        update.message.reply_text('回复人/ reply to someone')
        return -1

    DB.add_diamonds(to_id, msg)
    DB.minus_diamonds(from_id, msg)
    update.message.reply_text(f'{user}支付{msg} 魔法石💎给 {to}\n'
                              f'{user} sent {msg} Diamonds 💎 to {to}')


def button(update, context):  # query = None means?
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    query = update.callback_query
    hyperlink = f'[{user}](tg://user?id={id})'
    keyboard = [
        [InlineKeyboardButton('1', callback_data='one'), InlineKeyboardButton('2', callback_data='two'),
         InlineKeyboardButton('3', callback_data='three'), InlineKeyboardButton('4', callback_data='four'),
         InlineKeyboardButton('5', callback_data='five'), InlineKeyboardButton('6', callback_data='six')],

        [InlineKeyboardButton('下一页', callback_data=f's{update.effective_user.id}')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query == None:
        update.message.reply_text(f"[{user}](tg://user?id={id})\n"
                                  f"1\n2\n3\n4\n5\n6\n\n"
                                  f'*以下按钮没功能，请按下一页*',
                                  reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN_V2)
    else:
        query.answer()
        if int(query.data[1:]) != update.effective_user.id:
            return
        query.message.edit_text(f"[{user}](tg://user?id={id})\n"
                                f'1\n2\n3\n4\n5\n6\n\n'
                                  f'*以下按钮没功能，请按下一页*',
                                reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN_V2)
    return S_START


def switch(update, context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    query = update.callback_query
    query.answer()
    if int(query.data[1:]) != update.effective_user.id:
        return
    keyboard = [
        [InlineKeyboardButton('7', callback_data='one'), InlineKeyboardButton('8', callback_data='two'),
         InlineKeyboardButton('9', callback_data='three'), InlineKeyboardButton('10', callback_data='four'),
         InlineKeyboardButton('11', callback_data='five'), InlineKeyboardButton('12', callback_data='six')],

        [InlineKeyboardButton('前一页', callback_data=f'b{update.effective_user.id}')]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'[{user}](tg://user?id={id})\n'
                            f'7\n8\n9\n10\n11\n12\n\n'

                            f'*以下按钮没功能，请回前一页*',
                            reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN_V2)

    return S_START


def slot(update , context):
    msg = update.message.text
    msg = msg.split()[-1]
    if msg =='古币':
        update.message.reply_text('这咯\n写\n卡池\n跟%')
    else:
        update.message.reply_text('写 /slot <卡池名字>')

def credit(update , context):
    update.message.reply_text(f'*信誉/credit to :*'
                              f'\n*Dev* : Billy\n[ID: 163494588](tg://user?id=163494588)\n'
                              f'\n*Coder* : Hoo Ming Yang\n[ID: 652962567](tg://user?id=652962567)\n'
                              f'\n*Assistant* : BearBear\n[ID: 1027794428](tg://user?id=1027794428)\n'
                              f'\n\n_〔机器人是由以上工作人员的贡献\n任何问题和bug请通知谢谢〕_', parse_mode = ParseMode.MARKDOWN_V2)


def increase(update , context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    cd = context.chat_data
    keyboard = [
        [InlineKeyboardButton('Confirm', callback_data='confirm'), InlineKeyboardButton('Back', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    cd['a'] = update.message.reply_text(f'*{user}* are you sure you want to spend *5* diamond to expand *5* bagpack space?', reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN_V2)
    return S_INCREASE

def end_increase(update , context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    max = DB.get_user_value(user_id, "maxbagslot")
    diamonds = DB.get_user_value(user_id, "diamonds")
    cd = context.chat_data
    query = update.callback_query
    if update.callback_query.from_user.id != user_id:
        query.answer('不能使用')
        return None
    if query.data == 'confirm':
         if diamonds <5:
            query.message.edit_text(f'{user} You dont have enough diamonds')
            return -1
         else:
          DB.buy_slot(user_id)
          DB.add_diamonds(user_id, -5)
          query.message.edit_text(f'successfully increase from* {max}* to *{max+5}*\n  '
                                  f'成功把背包空间提升从 *{max}* 到 *{max+5}*', parse_mode = ParseMode.MARKDOWN_V2)
          return ConversationHandler.END
    if query.data == 'back':
        context.bot.delete_message(chat_id = update.effective_chat.id , message_id = cd['a'].message_id)

def pop(update , context):
    user = update.effective_user.first_name
    msg = update.message
    user_id = update.effective_user.id
    query = update.callback_query
    cd = context.chat_data
    random.seed(time.time())
    b = cd['a'] = random.randint(1,5)
    #query.answer()
    owner = 163494588

    keyboard = [
        [InlineKeyboardButton('领取\nclaim', callback_data='claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    a = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id).status
    
    if user_id in owners:
     update.message.reply_text(f'*领取* {b} 魔法石 💎\n'
                              f'*Claim* {b} diamond',
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
     context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
  
    else:
      update.message.reply_text('not authorized')
    return S_POP

def end_pop(update , context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    query = update.callback_query
    user_exp = DB.get_user_value(user_id, "exp")
    user_level = DB.get_user_value(user_id, "level")
    query.answer()
    cd = context.chat_data
    name = update.callback_query.from_user.first_name
    user_id = update.callback_query.from_user.id
    b = cd['a']

    
    query.message.edit_text(f'*{name}*成功领取*{b}*粒魔法石\n'
                                f'*{name}* claimed *{b}* diamonds\n'
                                f'EXP : 250\n\n', parse_mode = ParseMode.MARKDOWN_V2)
    if user_exp >= user_level * 500:
            DB.add_exp(user_id, -user_exp)
            DB.add_level(user_id)
            context.bot.send_message(chat_id = update.effective_chat.id  , text = f'{name} 升级到了 level : {user_level+1}\n type /inventory again to refresh'
                                                                         f'\n再按一次 /inventory 刷新')
    DB.add_diamonds(user_id, b)
    DB.add_exp(user_id , 250)

    return ConversationHandler.END
  
  
def bigpop(update , context):
    user = update.effective_user.first_name
    msg = update.message
    user_id = update.effective_user.id
    query = update.callback_query
    cd = context.chat_data
    random.seed(time.time())
    b = cd['a'] = random.randint(5,15)
    #query.answer()
    owner = 163494588

    keyboard = [
        [InlineKeyboardButton('领取\nclaim', callback_data='claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    a = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id).status
    
    if user_id in owners:
     update.message.reply_text(f'*领取* {b} 魔法石 💎\n'
                              f'*Claim* {b} diamond',
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
     context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
  
    else:
      update.message.reply_text('not authorized')
    return SS_POP

def end_bigpop(update , context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    query = update.callback_query
    user_exp = DB.get_user_value(user_id, "exp")
    user_level = DB.get_user_value(user_id, "level")
    query.answer()
    cd = context.chat_data
    name = update.callback_query.from_user.first_name
    user_id = update.callback_query.from_user.id
    b = cd['a']

    
    query.message.edit_text(f'*{name}*成功领取*{b}*粒魔法石\n'
                                f'*{name}* claimed *{b}* diamonds\n'
                                f'EXP : 250\n\n', parse_mode = ParseMode.MARKDOWN_V2)
    if user_exp >= user_level * 500:
            DB.add_exp(user_id, -user_exp)
            DB.add_level(user_id)
            context.bot.send_message(chat_id = update.effective_chat.id  , text = f'{name} 升级到了 level : {user_level+1}\n type /inventory again to refresh'
                                                                         f'\n再按一次 /inventory 刷新')
    DB.add_diamonds(user_id, b)
    DB.add_exp(user_id , 250)

    return ConversationHandler.END
      
def help(update , context):
    cd = context.chat_data
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton('Give \n给金币', callback_data='give'),InlineKeyboardButton('Draw \n抽卡', callback_data='draw')],
        [InlineKeyboardButton('Increase \n扩充背包', callback_data='increase'), InlineKeyboardButton('Inventory \n个人资产', callback_data='inventory')],
        [InlineKeyboardButton('Mycards \n拥有的卡', callback_data='mycards'), InlineKeyboardButton('Game \n小游戏', callback_data='game')],
        [InlineKeyboardButton('Support \n支援', callback_data='support'), InlineKeyboardButton('Group \n群组', callback_data='group')],
        [InlineKeyboardButton('Channel \n频道', callback_data='channel'), InlineKeyboardButton('Check \n查找', callback_data = 'check')],
        [InlineKeyboardButton('Close \n关闭', callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    cd['message'] = update.message.reply_text('以下是可以帮到你的信息，请在使用前阅读，谢谢合作\n\n'
                              'Below are explantion of the bot , please take a momment to read , thank you.',reply_markup=reply_markup)
    return THIRD
  
def cls(update , context):
    query = update.callback_query
    query.answer() 
    cd = context.chat_data
    context.bot.delete_message(chat_id = update.effective_chat.id, message_id = cd['message'].message_id)
    return THIRD
    
def bk(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Give \n给金币', callback_data='give'),InlineKeyboardButton('Draw \n抽卡', callback_data='draw')],
        [InlineKeyboardButton('Increase \n扩充背包', callback_data='increase'), InlineKeyboardButton('Inventory \n个人资产', callback_data='inventory')],
        [InlineKeyboardButton('Mycards \n拥有的卡', callback_data='mycards'), InlineKeyboardButton('Game \n小游戏', callback_data='game')],
        [InlineKeyboardButton('Support \n支援', callback_data='support'), InlineKeyboardButton('Group \n群组', callback_data='group')],
        [InlineKeyboardButton('Channel \n频道', callback_data='channel'), InlineKeyboardButton('Check \n查找', callback_data = 'check')],
        [InlineKeyboardButton('Close \n关闭', callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    cd['message'] = query.edit_message_text('以下是可以帮到你的信息，请在使用前阅读，谢谢合作\n\n'
                              'Below are explantion of the bot , please take a moment to read , thank you.',reply_markup=reply_markup)
    return THIRD
def st(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('先启动机器人 /starts 后你的数据才会被记录\n'
                    'start the bot first with /starts so that your data will be recorded', reply_markup=reply_markup)
    return THIRD
def inc(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('花费5个魔法石增加5个背包空间\n'
                    'spend 5 diamonds to increase 5 bag space', reply_markup=reply_markup)
    return THIRD

def gi(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('把你的金币给其他人\n'
                    '- 不能给机器人或者自己，没效的\n'
                    '- 不能写负数\n'
                    '- 不能写除了数字以外的东西\n\n'
                    'give your gold to other people for some reason\n'
                    '- cant give to bot or yourself\n'
                    '- cant write negative number\n'
                    '- cant write non interger ', reply_markup=reply_markup)
    return THIRD
def inv(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('查看你的个人信息\n\n'
                    'check your personal statistics', reply_markup=reply_markup)
    return THIRD
def grp(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('欢迎来这个群玩\n\n'
                    'come and join here to play\n\n'
                    '@Game_Gamez', reply_markup=reply_markup)
    return THIRD
def spt(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('想要通报任何bug和问题，或者想来看机器人测试的话可以来这里\n\n'
                    'if you found any bug or issue with the bot , please report it here to our support group'
                    ',or if you want to see the testing phase of the bot also can.\n\n'
                    'https://t.me/joinchat/T5T8DXtuPdk4Y2Q1', reply_markup=reply_markup)
    return THIRD
def mc(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('来查看你的卡片或者炫耀\n\n'
                    'to check what cards you have or to flex', reply_markup=reply_markup)
    return THIRD
def dr(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('<b>抽卡机</B>\n'
                    '◊ 请写 /draw 卡池名字'
                    '◊ 每次要等6秒后才可以再使用以避免炸群\n'
                    '◊ 每次抽卡花费 5 魔法石\n'
                    '◊ 要比较顺的抽卡体验请到私聊抽哦\n'
                    '\n'
                    '<b>card slots</b>\n'
                    'please write /draw card slot name\n'
                    'bot have been set to sleep 6 sec after every draw to avoid spam.\n'
                    'every draw cost 5 diamonds\n'
                    'draw in pm if you want smoother experience', reply_markup=reply_markup, parse_mode = ParseMode.HTML)
    return THIRD
def gm(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('回复一个的信息以邀请他来玩游戏\n'
                    '这个游戏类似于猜拳: 水>火>木\n'
                    '游戏以双方3分开始计算，赢者扣0分，输家扣1分\n'
                    '平局双方扣1分，其中一个人分数到零游戏结束\n\n'
                    'Reply to someone to begin the game\n'
                    '- Each player have 3 life point, if one of the player life point drop to 0 the other player wins\n'
                            '- Choose one of the elements water, fire, and earth to attach the player.\n'
                            '- (Water > Fire >Earth)\nYou will get 100 Gold and 100 EXP when you win. The loser get nothing.', reply_markup=reply_markup)
    return THIRD
def ch(update , context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('加入频道以获得机器人最新消息谢谢\n'
                    'Join Channel to be updated with latest news'
                    '\n\nhttps://t.me/botsupportgourp', reply_markup=reply_markup)
    return THIRD
def ck(update , context):
    query = update.callback_query
    query.answer() 
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('查找资讯\n'
                    'find something info\n'
                    '例如：/check 切西亚 \n'
                    'E.g：/check chessia', reply_markup=reply_markup)
    return THIRD

def sex(update , context):
    user = update.message.from_user.first_name
    to = update.message.reply_to_message.from_user.first_name
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton('Join', callback_data='join'),InlineKeyboardButton('Run', callback_data='run')]
    ]
    r = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'{user} invite {to} to have sex', reply_markup = r)
    if query.data == 'join':
        query.edit_text(f'{to} joined')
    if query.data == 'run':
        query.edit_text(f'{to} being forced to joined')

def mycards(update , context):
    cd = context.chat_data 
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    cd["user"] = user
    cd["id"] = user_id
    query = update.callback_query
    cards = DB.get_user_card(user_id, 'card_name')
    cards_en = DB.get_user_card_eng(user_id, 'eng')
    keyboard = [
               [InlineKeyboardButton("Next\n下一页", callback_data ="next"),InlineKeyboardButton("Previous\n前一页", callback_data ="previous")]
            ] 
    reply_markup = InlineKeyboardMarkup(keyboard)
    b = 1
    c = "."
    page = 1
    cd["page"] = page
    finS = []
    cd["cards"] = finS
    for chink, engk in zip(cards, cards_en):
        for chinj, engj in zip(chink, engk):
            finS.append(str(b) + ' ' + str(c) + ' ' + str(chinj) + '\n' + str(engj) + '\n\n')
            b += 1
    #context.bot.send_message(chat_id = update.effective_chat.id, text = f"currently on page {page}") 
    update.message.reply_text(f'<u><b>{user} \'s</b> Bag(背包里的卡)</u>\n\n'
                              f'{"".join(finS[(page-1)*(10-1):page*(10-1)])}'
                              , parse_mode = ParseMode.HTML, reply_markup =reply_markup)
    
    return SHOW
def swap_page(update, context):
    query = update.callback_query
    cd = context.chat_data 
    user = cd["user"]
    user_id = cd["id"] 
    finS = cd["cards"] 
    keyboard = [
               [InlineKeyboardButton("Next\n下一页", callback_data ="next"),InlineKeyboardButton("Previous\n前一页", callback_data ="previous")]
            ] 
    if update.callback_query.from_user.id!= user_id:
     query.answer("Not Authorised", show_alert = True)
    reply_markup = InlineKeyboardMarkup(keyboard)
  
    if query.data == "next":
     if len(finS)>=cd["page"]*10:
      cd["page"]+=1
      #context.bot.send_message(chat_id = update.effective_chat.id, text = f"currently on page {page}") 
      query.message.edit_text(f'<u><b>{user} \'s</b> Bag(背包里的卡)</u>\n\n'
                              f'{"".join(finS[(cd["page"]-1)*(10-1):cd["page"]*(10-1)])}'
                              , parse_mode = ParseMode.HTML, reply_markup =reply_markup)
   
      return SHOW
     if len(finS)<10:
      query.answer("没了\nCan't go furthur", show_alert = True) 
      return None
    if query.data == "previous":
     if cd["page"] <=1:
      query.answer("You're on first page \n现在在第一页好吗", show_alert = True)
      return None
     cd["page"]-=1 
     query.message.edit_text(f'<u><b>{user} \'s</b> Bag(背包里的卡)</u>\n\n'
                              f'{"".join(finS[(cd["page"]-1)*(10-1):cd["page"]*(10-1)])}'
                              , parse_mode = ParseMode.HTML, reply_markup =reply_markup)
     return SHOW

def make_sudo(update, context):
    
    id = update.message.reply_to_message.from_user.id
    toname = update.message.reply_to_message.from_user.first_name
    name = update.effective_user.first_name
    myid = update.effective_user.id
    if myid in owners:
     if id not in owners:
      owners.append(id)
      update.message.reply_text(f"{name} make you sudo user, now you can use\n\n- /add \n- /pop\n -/bigpop \n\n您现在有资格使用 /add , /pop 和 /bigpop") 
      return -1
     if id in owners:
      update.message.reply_text(f"{toname} is already sudo user, {toname} 已经是管理员") 
      return -1
    if myid not in owners:
     update.message.reply_text("Not authorised") 

def remove_sudo(update, context):
    id = update.message.reply_to_message.from_user.id
    toname = update.message.reply_to_message.from_user.first_name
    name = update.effective_user.first_name
    myid = update.effective_user.id
    if myid in owners:
     if id in owners:
      owners.remove(id)
      update.message.reply_text(f"sorry {toname} you're fired\n\n抱歉{toname}，您被取消资格了") 
      return -1
     if id not in owners:
      update.message.reply_text(f"This guy is not sudo \n这位{toname}不是管理要我怎么降级他") 
      return -1
    if myid not in owners:
     update.message.reply_text("Not authorised") 

def sudo_list(update, context):
    b = "" 
    c = 0
    for i in owners:
     b += str(c+1) +"\." + str(i) + "\n"
     c+=1
    context.bot.send_message(chat_id = update.effective_chat.id, text = f"*Sudo of the bot\n管理员*\n\n*{b}*", parse_mode=ParseMode.MARKDOWN_V2) 

def bet(update, context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    from_gold = DB.get_user_value(id, "diamonds")
    Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
     update.message.reply_text("use in pm \n请私聊机器人")
     return -1
    try:
     msg = update.message.text.split(None,1)[1]
     msg = int(msg)
     if from_gold<=0:
        return -1
     if from_gold< int(msg):
        return -1
     if msg <=0:
        return -1
    except TypeError:
        return -1
    except IndexError:
        return -1
    except ValueError:
        return -1
    except AttributeError:
        return -1
    a = random.randint(1,2)
    if a == 1:
     msgs = msg*2
     update.message.reply_text(f"{name}! You bet {msg}💎 and won {msgs}💎\n{name}! 你赌了{msg}💎, 然后赢了{msgs}💎")
     DB.add_diamonds(id,msg)
    else:
     msgs = msg*0
     update.message.reply_text(f"{name}! You bet {msg}💎 and loss {msg}💎\n{name}! 你赌了{msg}💎, 然后输了{msg}💎")
     DB.add_diamonds(id,-msg)
    

def add_column(update , context):
    id = update.effective_user.id
    if id != 163494588:
      update.message.reply_text("Not Authorised")
    else:
      DB.add_column()
      update.message.reply_text("done") 
    
def del_column(update , context):
    id = update.effective_user.id
    if id != 163494588:
      update.message.reply_text("Not Authorised")
    else:
      DB.del_column()
      update.message.reply_text("done") 
      
button_handler = ConversationHandler(
    entry_points=[CommandHandler('button', button)],
    states={
        S_START:
            [
                CallbackQueryHandler(switch, pattern="^s.*$"),
                CallbackQueryHandler(button, pattern="^b.*$")
            ]
    },
    fallbacks=[],
    allow_reentry=True,
    per_user=True,
    persistent=False
)

increase_handler = ConversationHandler(
    entry_points=[CommandHandler('increase', increase)],
    states={
        S_INCREASE:
            [
                CallbackQueryHandler(end_increase, pattern=".")
            ]
    },
    fallbacks=[],
    allow_reentry=True,
    per_user=True,
    persistent=False
)

pop_handler = ConversationHandler(
    entry_points=[CommandHandler('pop', pop)],
    states={
        S_POP:
            [
                CallbackQueryHandler(end_pop, pattern="^claim$")
            ]
    },
    fallbacks=[],
    allow_reentry=True,
    per_user=False

)

bigpop_handler = ConversationHandler(
    entry_points=[CommandHandler('bigpop', bigpop)],
    states={
        SS_POP:
            [
                CallbackQueryHandler(end_bigpop, pattern="^claim$")
            ]
    },
    fallbacks=[],
    allow_reentry=True,
    per_user=False

)

mycards_handler = ConversationHandler(
        entry_points=[CommandHandler('mycards', mycards)],
        states={
            SHOW: [
                CallbackQueryHandler(swap_page, pattern='^' + str('next') + '$'), 
                CallbackQueryHandler(swap_page, pattern='^' + str('previous') + '$')
  
            ]
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
   ) 


help_handler = ConversationHandler(
        entry_points=[CommandHandler('help', help)],
        states={
            THIRD: [
                CallbackQueryHandler(st, pattern='^' + str('start') + '$'),
                CallbackQueryHandler(gi, pattern='^' + str('give') + '$'),
                CallbackQueryHandler(inv, pattern='^' + str('inventory') + '$'),
                CallbackQueryHandler(grp, pattern='^' + str('group') + '$'),
                CallbackQueryHandler(spt, pattern='^' + str('support') + '$'),
                CallbackQueryHandler(mc, pattern='^' + str('mycards') + '$'),
                CallbackQueryHandler(dr, pattern='^' + str('draw') + '$'),
                CallbackQueryHandler(gm, pattern='^' + str('game') + '$'),
                CallbackQueryHandler(bk, pattern='^' + str('back') + '$'),
                CallbackQueryHandler(ch, pattern='^' + str('channel') + '$'), 
                CallbackQueryHandler(inc, pattern='^' + str('increase') + '$'),
                CallbackQueryHandler(cls, pattern='^' + str('close') + '$'), 
                CallbackQueryHandler(ck, pattern='^' + str('check') + '$') 

            ]
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )
shop_handler = ConversationHandler(
        entry_points=[CommandHandler('shop', shop)],
        states={
            FOUR: [
                CallbackQueryHandler(name1, pattern='^' + str('name') + '$'),
CallbackQueryHandler(finname, pattern='^' + str('1') + '$'),
CallbackQueryHandler(finname, pattern='^' + str('2') + '$'),
CallbackQueryHandler(finname, pattern='^' + str('3') + '$'),
CallbackQueryHandler(finname, pattern='^' + str('4') + '$'),
CallbackQueryHandler(finname, pattern='^' + str('5') + '$')
            ]
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )

INVENTORY_HANDLER = CommandHandler('inventory', inventory)
DRAW_HANDLER = CommandHandler('draw', draw, run_async=True)
SLOT_HANDLER = CommandHandler('slot', slot)
START_HANDLER = CommandHandler('starts', starts)
CREDIT_HANDLER = CommandHandler('credit', credit)
ADD_HANDLER = CommandHandler('add', add)
GIVE_HANDLER = CommandHandler('give', give)
sex_HANDLER = CommandHandler('sex', sex)
MAKE_SUDO_HANDLER = CommandHandler('make_sudo', make_sudo)
REMOVE_SUDO_HANDLER = CommandHandler('remove_sudo', remove_sudo)
SUDO_LIST_HANDLER = CommandHandler('sudo_list', sudo_list)
GIFT_HANDLER = CommandHandler('gift', gift)
BET_HANDLER = CommandHandler('bet', bet)
ADD_COLUMN_HANDLER = CommandHandler('add_column', add_column)
DEL_COLUMN_HANDLER = CommandHandler('del_column', del_column)

dispatcher.add_handler(DRAW_HANDLER)
dispatcher.add_handler(INVENTORY_HANDLER)
dispatcher.add_handler(SLOT_HANDLER)
dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(ADD_HANDLER)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(CREDIT_HANDLER)
dispatcher.add_handler(GIVE_HANDLER)
dispatcher.add_handler(mycards_handler)
dispatcher.add_handler(increase_handler)
dispatcher.add_handler(pop_handler)
dispatcher.add_handler(bigpop_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(sex_HANDLER)
dispatcher.add_handler(MAKE_SUDO_HANDLER)
dispatcher.add_handler(REMOVE_SUDO_HANDLER)
dispatcher.add_handler(SUDO_LIST_HANDLER)
dispatcher.add_handler(GIFT_HANDLER)
dispatcher.add_handler(BET_HANDLER)
dispatcher.add_handler(ADD_COLUMN_HANDLER)
dispatcher.add_handler(DEL_COLUMN_HANDLER)
dispatcher.add_handler(shop_handler)



