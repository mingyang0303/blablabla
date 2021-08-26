import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters

S_START , S_INCREASE ,S_POP , FIRST , SECOND ,THIRD,CHECK, *_ = range(1000)
owners = [163494588,652962567,1027794428,801509492,935241907]

updater = Updater(token='1736686159:AAFG0jC4qEHE5ahhc_F7kZY-LMH5UR1lxAM', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

checker = [
    {'chi_name' : '切西亚',
     'chif_name': '切西亞',
     'eng_name': 'chessia',
     'chi_lead': '透幻烈燄 \n\nI. 火屬性攻擊力 4.8 倍, 生命力及回復力 1.3 倍 '
                '\nII. 消除符石的種類愈多，火屬性攻擊力額外提升愈多：\n⇒ 消除 2 種 1.5 倍\n⇒ 消除 4 種可達至最大 2.1 倍',
     'eng_lead': 'Illusory Blaze\n\nI. Fire Attack x 4.8; HP & Recovery x 1.3.\n'
                'II. The more types of Runestones dissolved, the higher the Fire Attack increases additionally:'
                '\nFire Attack x 1.5 for 2 types of Runestones dissolved, to the max x 2.1 for 4 types',
     'chi_act': '三原靈冕化陣 ‧ 神燄 CD6\n\n將所有符石隨機轉化為⇒ 「水、火、木及心」強化符石\n⓵ 同時火符石出現率上升\n⓶ 將火符石以火神族強化符石代替',
     'eng_act':'Tricolor Circle - Blood & Blaze EX CD6\n\nRandomly turn all Runestones into Enchanted Water, Enchanted Fire, Enchanted Earth and Enchanted Heart Runestones.'
               '\n⓵ Increase the Occurrence rate of Fire Runestones.'
               '\n⓶ Fire Runestones will become Enchanted God Runestones.',
     'chi_team':'隊伍技能 : \n\nI隊長的隊長技能「透幻烈燄」變為「透幻烈燄 ‧ 裂心」於每回合移動符石後，引爆所有心符石，直至場上沒有心符石\n'
                'II. 火符石兼具心符石效果'
                '\nIII. 7 星「墮天」系列角色對敵人發動攻擊 (需消除符石) 及沒有首批消除心符石時，該敵人於下回合被附上「墮天印記」，'
                '持續 3 回合。每擊斃 1 隻附有「墮天印記」的敵人 (需消除符石)，7 星「墮天」系列角色的主動技能 CD 減少 1發動條件：以「千變真箇 ‧ 切西亞」作隊長及戰友',
     'eng_team':'Team Skill: \n\nI. Change the Leader Skill of the Leader from "Illusory Blaze" to "Illusory Blaze - '
                'Heart-cracking". Upon the completion of moving and dissolving Runestones each Round, all Heart Runestones '
                'will explode until there is no more Heart Runestone on the screen.\nII. Fire Runestones also possess the eff'
                'ect of Heart Runestones.\nIII. When 7* Monster of "The Fallen Halos - '
                'Power Release" attacks and Heart Runestones are not dissolved, impose a Mark on an enemy for 3 Rounds '
                '(only the first batch of Runestones dissolved will be counted) (dissovling Runestones is necessary).'
                'For each enemy with the Mark defeated, Active Skill CD(s) of 7* Monsters of "The Fallen Halos -'
                ' Power Release" -1.\nCondition:Both the Leader and Ally are "Disguised Self - Chessia".'
     },
    {'chi_name':'亚伯汗',
'chif_name': '亞伯汗',
'eng_name':'abraham',
'chi_act': '深海连环 CD6\n\n'
'1 回合内\n'
'I. 延长移动符石时间至 12 秒\n'
'II. 消除符石的组数愈多时，全队攻击力愈高\n'
'⇒ 消除 10 组可达至最大 2.5 倍',
'eng_act': 'Chains of Deep Sea CD6\n\n'
'For 1 Round:\n'
'I. Extend Runestone-moving time to 12 seconds\n'
'II. The more the groups of Runestones dissolved, the higher the Team Attack\n'
'⇒ to the max x 2.5 for 10 groups\n',
'chi_lead': '浪屠杀 \n\n'
'I. 水属性攻击力 5.25 倍，生命力及回复力 1.3 倍\n'
'II. 每消除 1 组符石均有 50% 几率\n'
'⇒ 额外计算多 1 连击 (Ex. Combo)\n'
'⇒ 最多可额外增加 15 连击 (Ex. Combo)\n'
'(几率及连击数目可以叠加)',
'eng_lead': 'Billows of Fatality\n\n'
'I. Water Attack x 5.25; HP & Recovery x 1.3.\n'
'II. Summoner has a 50% chance to gain 1 Ex. Combo count for each group of Runestones dissolved, to the max 15 Ex. Combos\n'
'(effects and Combo count can be superimposed)',
'chi_team': '隊伍技能: \n\n'
'I. 队长的队长技能“浪屠杀”变为“浪屠杀 ‧ 裂心”，于每回合移动并消除符石后，引爆所有心符石，直至场上没有心符石\n'
'II. 每消除 1 组水符石，(队长技能以外) 将额外计算多 1 连击 (Ex. Combo)。其他计算首批消除符石的技能不受此额外的连击 (Ex. Combo) 影响\n'
'III. 水符石兼具心符石效果\n'
'IV. 7 星“堕天”系列角色对敌人发动攻击 (需消除符石) 及没有首批消除心符石时，该敌人于下回合被附上“堕天印记”，持续 3 回合。'
'每击毙 1 只附有“堕天印记”的敌人 (需消除符石)，7 星“堕天”系列角色的主动技能 CD 减少 1'
'V. 达成 4 连击 (Combo) 或以上时\n'
'⇒ 全队攻击力 2.4 倍\n'
'发动条件：\n'
'以“境界扭曲 ‧ 亚伯汗”作队长及战友',
'eng_team': 'Team Skill: \n\n'
'I. Change the Leader Skill of the Leader from "Billows of Fatality" to "Billows of Fatality - Heart-cracking". Upon the completion of moving and dissolving Runestones each Round, all Heart Runestones will explode until there is no more Heart Runestone on the screen.\n'
'II. 1 Ex. Combo count for every group of Water Runestones dissolved (Ex. Combos are not subjected to Leader Skill\'s quota). Ex. Combos will not be counted for Skills conditioned by the first batch of Runestones dissolved.\n'
'III. Water Runestones also possess the effect of Heart Runestones.\n'
'IV. When 7* Monster of "The Fallen Halos - Power Release" attacks and Heart Runestones are not dissolved, impose a Mark on an enemy for 3 Rounds (only the first batch of Runestones dissolved will be counted) (dissovling Runestones is necessary). For each enemy with the Mark defeated, Active Skill CD(s) of 7* Monsters of "The Fallen Halos - Power Release" -1.\n'
'V. When 4 or more Combos are made, Team Attack x 2.4 additionally.\n'
'Condition:\n'
'Both the Leader and Ally are "Spacial Distortion - Abraham".',
    },
  {'chi_name':'撒旦',
'chif_name':'撒旦',
'eng_name':'satan',
'chi_act':'追魂之幽 ‧ 魔暴 CD8\n\n'
'  I.引爆場上所有風化符石及凍結符石\n'
' II.將所有符石添加為魔族符石\n'
'III. 1 回合內，暗屬性攻擊力 2 倍，自身攻擊力額外提升 3 倍',
'eng_act':'Soul-hunting Gloominess - EX CD8\n\n'
'  I. Explode all Weathered Runestones and Frozen Runestones.\n'
' II. Modify all Runestones to become Demon Runestones.\n'
'III. For 1 Round, Dark Attack x 2; the Monster\'s Attack x 3 additionally.',
'chi_lead':'血祭斷魂劍\n\n'
' I. 暗屬性攻擊力 6 倍、生命力及回復力 1.3 倍\n'
'II. 消除 ≥3 種符石及自身發動攻擊時\n'
'⇒ 個人追打自身攻擊力 5 倍的暗屬性攻擊 1 次',
'eng_lead':'Sword in Blood\n\n'
' I. Dark Attack x 6; HP & Recovery x 1.3.\n'
'II. By dissolving 3 or more types of Runestones, an extra Dark Attack as much as 5x the Monster\'s Attack will be launched when the Monster attacks',
'chi_team':'隊伍技能：\n\n'
'7 星「墮天」系列角色對敵人發動攻擊 (需消除符石) 及沒有首批消除心符石時，該敵人於下回合被附上「墮天印記」，持續 3 回合。\n\n'
'每擊斃 1 隻附有「墮天印記」的敵人 (需消除符石)，7 星「墮天」系列角色的主動技能 CD 減少 1\n\n'
'隊長的隊長技能「血祭斷魂劍」變為「血祭斷魂劍 ‧ 裂心」，當中於每回合移動並消除符石後，引爆所有心符石，直至場上沒有心符石\n\n'
'暗符石兼具心符石效果\n\n'
'消除暗符石時，下回合將暗符石轉化為魔族符石\n\n'
'發動條件：\n'
'以至高罪咎 ‧ 撒旦作隊長及戰友',
'eng_team':'Team Skill:\n\n'
'When 7* Monster of "The Fallen Halos - Power Release" attacks and Heart Runestones are not dissolved, impose a Mark on an enemy for 3 Rounds (only the first batch of Runestones dissolved will be counted) (dissovling Runestones is necessary).\n\n'
'For each enemy with the Mark defeated, Active Skill CD(s) of 7* Monsters of "The Fallen Halos - Power Release" -1.\n\n'
'Change the Leader Skill of the Leader from "Sword in Blood" to "Sword in Blood - Heart-cracking". Upon the completion of moving and dissolving Runestones each Round, all Heart Runestones will explode until there is no more Heart Runestone on the screen.\n\n'
'Dark Runestones also possess the effect of Heart Runestones.\n\n'
'By dissolving Dark Runestones, turn Dark Runestones into Demon Runestones in the next Round.\n\n'
'Condition:\n'
'Both the Leader and Ally are "Beyond Salvation - Satan".'}
]

def biodata_ch_name(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['chi_name']
def biodata_chf_name(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['chif_name']
def biodata_en_name(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['eng_name']
def biodata_ch_lead(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['chi_lead']
def biodata_en_lead(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['eng_lead']
def biodata_ch_act(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['chi_act']
def biodata_en_act(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['eng_act']
def biodata_ch_team(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['chi_team']
def biodata_en_team(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['eng_team']
def check(update , context):
    bot = context.bot
    cd = context.chat_data
    msg = update.message.text.split()[1]
    msg = msg.lower()
    query = update.callback_query
    user = update.effective_user.name
    ch_name = cd['chi_name'] = biodata_ch_name(msg)
    chf_name = cd['chif_name'] = biodata_chf_name(msg)
    en_name = cd['en_name'] = biodata_en_name(msg)
    ch_lead = cd['chi_lead'] = biodata_ch_lead(msg)
    ch_act = cd['chi_act'] = biodata_ch_act(msg)
    ch_team = cd['chi_team'] = biodata_ch_team(msg)
    en_lead = cd['eng_lead'] = biodata_en_lead(msg)
    en_act = cd['eng_act'] = biodata_en_act(msg)
    en_team = cd['eng_team'] = biodata_en_team(msg)
    keyboard = [
        [InlineKeyboardButton(' 主动技能', callback_data='chi_act'),
         InlineKeyboardButton('队伍技能', callback_data='chi_lead'),
         InlineKeyboardButton('Translate\nEN', callback_data='translate_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if ch_name == None:
        update.message.reply_text('failed : 角色还没加入资料库')
        return ConversationHandler.END
    if chf_name == None:
        update.message.reply_text('failed : 角色还没加入资料库')
        return ConversationHandler.END
    if en_name == None:
        update.message.reply_text('failed : 角色还没加入资料库')
        return ConversationHandler.END
    update.message.reply_text(f'<b>{ch_lead}</b>', reply_markup=reply_markup, parse_mode = ParseMode.HTML)
    return CHECK

def chi_act(update , context):
    cd = context.chat_data
    query = update.callback_query
    ch_act = cd['chi_act']
    keyboard = [
        [InlineKeyboardButton(' 队长技能', callback_data='chi_lead'),
         InlineKeyboardButton('队伍技能', callback_data='chi_team'),
         InlineKeyboardButton('Translate\nEN', callback_data='translate_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'<b>{ch_act}</b>', reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    return CHECK
def chi_lead(update , context):
    cd = context.chat_data
    query = update.callback_query
    ch_lead = cd['chi_lead']
    keyboard = [
        [InlineKeyboardButton('主动技能', callback_data='chi_act'),
         InlineKeyboardButton('队伍技能', callback_data='chi_team'),
         InlineKeyboardButton('Translate\nEN', callback_data='translate_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'<b>{ch_lead}</b>', reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    return CHECK
def chi_team(update , context):
    cd = context.chat_data
    query = update.callback_query
    ch_team = cd['chi_team']
    keyboard = [
        [InlineKeyboardButton('主动技能', callback_data='chi_act'),
         InlineKeyboardButton('队长技能', callback_data='chi_lead'),
         InlineKeyboardButton('Translate\nEN', callback_data='translate_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'<b>{ch_team}</b>', reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    return CHECK
def tr_en(update , context):
    cd = context.chat_data
    query = update.callback_query
    en_lead = cd['eng_lead']
    keyboard = [
        [InlineKeyboardButton('Ability', callback_data='eng_act'),
         InlineKeyboardButton('Team', callback_data='eng_team'),
         InlineKeyboardButton('Translate\nCH', callback_data='translate_ch')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'<b>{en_lead}</b>', reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    return CHECK
def eng_act(update , context):
    cd = context.chat_data
    query = update.callback_query
    en_act = cd['eng_act']
    keyboard = [
        [InlineKeyboardButton('Leader', callback_data='eng_lead'),
         InlineKeyboardButton('Team', callback_data='eng_team'),
         InlineKeyboardButton('Translate\nCH', callback_data='translate_ch')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'<b>{en_act}</b>', reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    return CHECK
def eng_team(update , context):
    cd = context.chat_data
    query = update.callback_query
    en_team = cd['eng_team']
    keyboard = [
        [InlineKeyboardButton('Ability', callback_data='eng_act'),
         InlineKeyboardButton('Leader', callback_data='eng_lead'),
         InlineKeyboardButton('Translate\nCH', callback_data='translate_ch')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'<b>{en_team}</b>', reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
def tr_ch(update , context):
    cd = context.chat_data
    query = update.callback_query
    chi_lead = cd['chi_lead']
    keyboard = [
        [InlineKeyboardButton(' 主动技能', callback_data='chi_act'),
         InlineKeyboardButton('队伍技能', callback_data='chi_lead'),
         InlineKeyboardButton('Translate\nEN', callback_data='translate_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(f'<b>{chi_lead}</b>', reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    return CHECK
check_handler = ConversationHandler(
        entry_points=[CommandHandler('check', check)],
        states={
            CHECK: [
                CallbackQueryHandler(chi_act, pattern='^' + str('chi_act') + '$'),
                CallbackQueryHandler(chi_lead, pattern='^' + str('chi_lead') + '$'),
                CallbackQueryHandler(chi_team, pattern='^' + str('chi_team') + '$'),
                CallbackQueryHandler(tr_en, pattern='^' + str('translate_en') + '$'),
                CallbackQueryHandler(tr_ch, pattern='^' + str('translate_ch') + '$'),
                CallbackQueryHandler(eng_act, pattern='^' + str('eng_act') + '$'),
                CallbackQueryHandler(eng_team, pattern='^' + str('eng_team') + '$'), 
                CallbackQueryHandler(tr_en, pattern='^' + str('eng_lead') + '$')


            ]
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )
  
dispatcher.add_handler(check_handler)
  
logger = logging.getLogger()
updater.start_polling()
