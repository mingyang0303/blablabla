import logging
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB

S_START , S_INCREASE ,S_POP , FIRST , SECOND ,THIRD,CHECK, *_ = range(1000)

def game(update: Update, context: CallbackContext):
    if not update.message.reply_to_message:
             update.message.reply_text('reply to someone')
             return ConversationHandler.END

    cd = context.chat_data
    cd['fighter'] = update.effective_user.first_name
    cd['to'] = update.message.reply_to_message.from_user.first_name
    cd['fighterid'] = update.effective_user.id
    cd['toid'] = update.message.reply_to_message.from_user.id
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']
    cd['round'] = 1
    cd['fromhp'] = 3
    cd['tohp'] = 3

    keyboard = [
        [
            InlineKeyboardButton("接受\naccept", callback_data=str('yes')),
            InlineKeyboardButton("拒绝\ndecline", callback_data=str('no')),
        ],
        [InlineKeyboardButton("取消\ncancel", callback_data=str('cancel'))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if tid == context.bot.id:
       update.message.reply_text('不能和机器人玩啊\n'
                                  'You cant play with me bruh, reply to a human')
       return ConversationHandler.END
    if tid == fid:
       update.message.reply_text('你傻的吗？跟自己玩？\n'
                                      'whats wrong with you wanting to play with yourself??')
       return ConversationHandler.END
    if tid != fid:
       update.message.reply_text(f"*{f}* 邀请 *{t}* 来个游戏\n"
                              f"*{f}* invite *{t}* to a game", reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN_V2)
       return FIRST

def cancel(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']
    if update.callback_query.from_user.id != fid:
        query.answer('不能使用\nCannot use')
        return None
    query.edit_message_text(f'{f}取消了游戏\n'
                            f'{f} cancelled the game')
    return ConversationHandler.END



def accept(update: Update, context: CallbackContext):
    cd = context.chat_data
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("💧水", callback_data=str('water')),
            InlineKeyboardButton("🔥火", callback_data=str('fire')),
            InlineKeyboardButton("🍀木", callback_data=str('wood'))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query.from_user.id != tid:
        query.answer('不能使用\nCannot use')
        return None
    query.edit_message_text(
        text=f"_*Round : {cd['round']}*_\n\n"
             f"{f}❤ : {cd['fromhp']}\n{t}❤ : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性", reply_markup=reply_markup,parse_mode = ParseMode.MARKDOWN_V2
    )
    return FIRST

def decline(update: Update, context: CallbackContext):
    cd = context.chat_data
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']
    query = update.callback_query
    query.answer()
    if update.callback_query.from_user.id != tid:
        query.answer('不能使用\ncannot use')
        return None
    return ConversationHandler.END

def first(update: Update, context: CallbackContext):
    print('entered state 2')
    cd = context.chat_data
    query = update.callback_query
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']


    keyboard = [
        [
            InlineKeyboardButton("水💧", callback_data=str('water')),
            InlineKeyboardButton("火🔥", callback_data=str('fire')),
            InlineKeyboardButton("木🍀", callback_data=str('wood'))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query.from_user.id != fid:
        query.answer('player 2 not ur turn')
        return None
    query.edit_message_text(
        text=f"_*Round : {cd['round']}*_\n\n"
             f"{f}❤ : {cd['fromhp']}\n{t}❤ : {cd['tohp']}\n\n"
             f"*{t}* choose one elemental\n"
             f"*{t}* 选一个攻击属性", reply_markup=reply_markup, parse_mode = ParseMode.MARKDOWN_V2
    )
    cd['round']+=1
    cd['choice1'] = query.data
    if tid == 163494588:
     context.bot.send_message(chat_id=163494588, text = f'{f} choose : {query.data}')
    if tid == 652962567:
     context.bot.send_message(chat_id=652962567, text=f'{f} choose : {query.data}')
    print('player 1 choose : '+str(cd['choice1'])+ ',id : ' + str(update.callback_query.from_user.id))
    return SECOND

def res(update: Update, context: CallbackContext):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    cd['choice2'] = query.data
    print('player 2 choose : '+str(cd['choice2'])+ ',id : ' + str(update.callback_query.from_user.id))
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']
    fchose = cd['choice1']
    tchose = cd['choice2']
    print(cd['fromhp'])
    print(cd['tohp'])
    keyboard = [
        [
            InlineKeyboardButton("水💧", callback_data=str('water')),
            InlineKeyboardButton("火🔥", callback_data=str('fire')),
            InlineKeyboardButton("木🍀", callback_data=str('wood'))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query.from_user.id != tid:
        query.answer('player 2 not ur turn')
        return None
    elements = {
            "water": "💧",
            "wood": "☘️",
             "fire": "🔥"
                        }

    a = elements[cd['choice1']]
    b = elements[cd['choice2']]
    if update.callback_query.from_user.id != tid:
        query.answer('player 1 not ur turn')
        return None
      
      
    if cd['choice1'] == cd['choice2']:
        cd['fromhp'] -= 1
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'*{f}* 使用 {a} 和 *{t}* 使用 {b}\n'
                                f'_its a Draw_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性"
                                f'{t}', parse_mode=ParseMode.MARKDOWN_V2, reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                DB.add_diamonds(fid, 1)
                DB.add_exp(fid , 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
                
          elif cd['tohp'] > cd['fromhp']:
                DB.add_diamonds(tid, 1)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
                
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw !!\n")
                
          return ConversationHandler.END
          
        return FIRST  
     
    elif cd['choice1'] == 'water' and cd['choice2'] == 'fire':
        cd['fromhp'] -= 0
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'*{f}* 使用 水{a}来攻击和 *{t}* 使用火{b}来攻击\n'
                                f'_[{f}](tg://user?id={fid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
            if cd['fromhp'] > cd['tohp']:
                DB.add_diamonds(fid, 1)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
             
            elif cd['tohp'] > cd['fromhp']:
                DB.add_diamonds( tid, 1)
                DB.add_exp( tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            return ConversationHandler.END

        return FIRST

    elif cd['choice1'] == 'fire' and cd['choice2'] == 'water':
        cd['fromhp'] -= 1
        cd['tohp'] -= 0
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'*{f}* 使用 火来攻击{a} 和 *{t}* 使用 水{b}来攻击\n'
                                f'_[{t}](tg://user?id={tid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
            if cd['fromhp'] > cd['tohp']:
                DB.add_diamonds( fid, 1)
                DB.add_exp( fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}魔法石💎diamond + 1\n'
                                        f'EXP + 100')

            elif cd['tohp'] > cd['fromhp']:
                DB.add_diamonds(tid, 1)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            return ConversationHandler.END

        return FIRST

    elif cd['choice1'] == 'water' and cd['choice2'] == 'wood':
        cd['fromhp'] -= 1
        cd['tohp'] -= 0
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'*{f}* 使用 水{a}来攻击 和 *{t}* 使用 木{b}来攻击\n'
                                f'_[{t}](tg://user?id={tid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
            if cd['fromhp'] > cd['tohp']:
                DB.add_diamonds(fid, 1)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_diamonds(tid, 1)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            return ConversationHandler.END

        return FIRST

    elif cd['choice1'] == 'wood' and cd['choice2'] == 'water':
        cd['fromhp'] -= 0
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'*{f}* 使用 木{a}来攻击 和 *{t}* 使用 水{b}来攻击\n'
                                f'_[{f}](tg://user?id={fid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
            if cd['fromhp'] > cd['tohp']:
                DB.add_diamonds(fid, 1)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_diamonds(tid, 1)
                DB.add_exp(tid , 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            return ConversationHandler.END

        return FIRST

    elif cd['choice1'] == 'wood' and cd['choice2'] == 'fire':
        cd['fromhp'] -= 1
        cd['tohp'] -= 0
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'*{f}* 使用 木{a}来攻击 和 *{t}* 使用 火{b}来攻击\n'
                                f'_[{t}](tg://user?id={tid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
            if cd['fromhp'] > cd['tohp']:
                DB.add_diamonds(fid, 1)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!"
                                        f'{f}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold(tid, 100)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!"
                                        f'{t}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            return ConversationHandler.END

        return FIRST

    elif cd['choice1'] == 'fire' and cd['choice2'] == 'wood':
        cd['fromhp'] -= 0
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'*{f}* 使用 火{a}来攻击 和 *{t}* 使用 木{b}来攻击\n'
                                f'_[{f}](tg://user?id={fid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}* choose one elemental\n"
             f"*{f}* 选一个攻击属性"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
            if cd['fromhp'] > cd['tohp']:
                DB.add_diamonds(fid, 1)
                DB.add_exp(fid, 100)
                query.message.edit_text(f'{f}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_diamonds(tid, 1)
                DB.add_exp(tid, 100)
                query.message.edit_text(f'{t}魔法石💎diamond + 1\n'
                                        f'EXP + 100')
            return ConversationHandler.END

        return FIRST
      
game_handler = ConversationHandler(
        entry_points=[CommandHandler('game', game)],
        states={
            FIRST: [
                CallbackQueryHandler(accept, pattern='^' + str('yes') + '$'),
                CallbackQueryHandler(cancel, pattern='^' + str('cancel') + '$'),
                CallbackQueryHandler(decline, pattern='^' + str('no') + '$'),
                CallbackQueryHandler(first, pattern='^' + str('water') + '$'),
                CallbackQueryHandler(first, pattern='^' + str('fire') + '$'),
                CallbackQueryHandler(first, pattern='^' + str('wood') + '$')
            ],
            SECOND: [
                CallbackQueryHandler(res, pattern='^' + str('water') + '$'),
CallbackQueryHandler(res, pattern='^' + str('fire') + '$'),
CallbackQueryHandler(res, pattern='^' + str('wood') + '$')

            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=False,
    run_async=True
    )
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dispatcher.add_handler(game_handler)
