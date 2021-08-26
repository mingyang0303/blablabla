import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
import random
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
ONE , TWO , THREE , FIRST , SECOND,  *_ = range(50)
#callback data


S_START , S_INCREASE ,S_POP , FIRST , SECOND ,THIRD,CHECK, *_ = range(1000)
owners = [163494588,652962567,1027794428,801509492,935241907]

updater = Updater(token='1736686159:AAFG0jC4qEHE5ahhc_F7kZY-LMH5UR1lxAM', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ancts = [{'name': '德王顯仁・敖廣',
  'eng': 'Valor of the East Sea - Ao Guang',
  'link': 'https://telegra.ph/file/9c4fd13aded44c1176bea.jpg',
  'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆',
},
{'name': '火輪天王・哪吒',
'eng': 'Heavenly Fire Wheels - Nezha',
'link': 'https://telegra.ph/file/a9247d5c8f43440bcf92d.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},
{
'name': '風馳於世・牛魔王',
'eng': 'Smite of Warhammer - Bull King',
'link': 'https://telegra.ph/file/952857700c91e9763afff.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},
{
'name': '化戾金仙・孫悟空',
'eng': 'Tranquil Transcendence - Sun Wukong',
'link': 'https://telegra.ph/file/646c5d1f52f8f15ee1d00.jpg',
'star' : '★ ★ ★ ★ ★ ★ ★ ★ ☆'},
{'name': '情深狐思・蘇妲己',
'eng': 'Unbreakable Fondness - Su Daji',
'link': 'https://telegra.ph/file/d9b9ba671111f16948c4e.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'},
{
'name': '至高罪咎・撒旦',
'eng': 'Beyond Salvation - Satan',
'link': 'https://telegra.ph/file/96d11091f0c257bfaa100.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},

{'name': '境界扭曲・亞伯汗',
'eng': 'Spacial Distortion - Abraham',
'link': 'https://telegra.ph/file/193651e825fdbf1173a31.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '千變真箇・切西亞',
'eng': 'Tainted Glamor - Queen Chessia',
'link': 'https://telegra.ph/file/e4f2edaa596a70ebc74d4.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '驍銳武聖 ‧ 關羽',
'eng': 'Valorous Legend - Guan Yu',
'link': 'https://telegra.ph/file/a9d89fb6ac4813dc962b8.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '霸業魔政 ‧ 曹操',
'eng': 'Tyranny of Dominance - Cao Cao',
'link': 'https://telegra.ph/file/a15c0d2a520d5908c2d34.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{
'name': '驍猛狂者 ‧ 呂布',
'eng': 'Belligerent Mania - Lü Bu',
'link': 'https://telegra.ph/file/31a4d9ad9ceac96cd7f5c.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},

{'name': '馨陽晴爽 • 天照',
'eng': 'Radiant Sunshine - Amaterasu',
'link': 'https://telegra.ph/file/0145bee9eed6fe840edf3.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '顧眄相伴 • 伊邪那岐',
'eng': 'Resilient Love - Izanagi',
'link': 'https://telegra.ph/file/53f5af0735a0a605dde91.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '寂寥偶戲 • 月讀',
'eng': 'Lone Puppeteer - Tsukuyomi',
'link': 'https://telegra.ph/file/f2fe60aefce81b37ff96a.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '高潔騎士 • 亞瑟',
'eng': 'Knight of Virtuousness - Arthur',
'link': 'https://telegra.ph/file/b282bc6fda729945903fa.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '千刃騎士 • 蘭斯洛特',
'eng': 'Knight of Swordmaster - Lancelot',
'link': 'https://telegra.ph/file/8292d7fead0d4bb81d02a.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '幻變術師 • 梅林',
'eng': 'Merlin the Illusional - Sorceress',
'link': 'https://telegra.ph/file/6cf7005a9612437a8f3b6.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '烽火武心 • 織田信長',
'eng': 'Nobunaga the Blazing Fervour',
'link': 'https://telegra.ph/file/ba1766abadd038072b75a.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '扇頁浮金 • 豐臣秀吉',
'eng': 'Hideyoshi the Insatiable Greed',
'link': 'https://telegra.ph/file/fed203f621eb0470fbc08.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '豪拳斷罪 • 本多忠勝',
'eng': 'Honda the Fist of Savagery',
'link': 'https://telegra.ph/file/2539b2186095bf53b8cc0.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '宿命扭轉 ‧ 蛇夫座斯克勒',
'eng': 'Twisted Fate - Ophiuchus',
'link': 'https://telegra.ph/file/c8c4dde432f780d23e1d3.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '綺香誘惑 ‧ 仙女座安德洛',
'eng': 'Sultry Fragrance - Andromeda',
'link': 'https://telegra.ph/file/9fe7878033dfda4666906.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '危命獵殺 ‧ 天貓座琳叩斯',
'eng': 'Fatal Hunter - Lynx',
'link': 'https://telegra.ph/file/f585b6a136b902b1a30d1.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '綻放榮耀 ‧ 矢車菊',
'eng': 'Rekindled Honor - Cornflower',
'link': 'https://telegra.ph/file/e5d6129f9be5edd9e88ce.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '閉鎖心蕾 ‧ 櫻',
'eng': 'Shrunk Petals - Sakura',
'link': 'https://telegra.ph/file/141ba82040baa5388fce1.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '戀慕瀰漫 ‧ 薔薇',
'eng': 'Lovey Dovey Romancist - Rose',
'link': 'https://telegra.ph/file/84592788925f99b0c99d5.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '因果破壞 ‧ 阿撒托斯',
'eng': 'Fiend of Destruction - Azathoth',
'link': 'https://telegra.ph/file/6acfdf04566f872f62966.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '悖論創造 ‧ 道羅斯',
'eng': 'Demiurge of Antinomy - Daoloth',
'link': 'https://telegra.ph/file/35fa78463bd6bd21df627.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '瘋癲夢界度 ‧ 格赫羅斯',
'eng': 'Dream Gobbler - Ghroth',
'link': 'https://telegra.ph/file/159dcf2b225287534ec57.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '葬殤修羅 ‧ 祝融',
'eng': 'Reaper of Wrath - Zhurong',
'link': 'https://telegra.ph/file/036b7e4495e60092f1ccd.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{
'name': '不屈鴻志 ‧ 孫策',
'eng': 'Unbending Aspiration - Sun Ce',
'link': 'https://telegra.ph/file/7d6afb81698c8367aae1a.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},

{'name': '魔瞳狂槍 ‧ 夏侯惇',
'eng': 'Devil Eye Seal - Xiahou Dun',
'link': 'https://telegra.ph/file/d94684e42fae0239be17f.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '劍氣御神 ‧ 呂洞賓',
'eng': 'Mischievous Wit - Lü Dongbin',
'link': 'https://telegra.ph/file/233f68ef9d004d9cf392a.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '菡萏香銷 ‧ 何仙姑',
'eng': 'Supreme Lotus - He Xian\'gu',
'link': 'https://telegra.ph/file/612dc2831b7b52cc10040.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '血植異足 ‧ 鐵拐李',
'eng': 'Bionic Immortal - Li Tieguai',
'link': 'https://telegra.ph/file/34554fc8eca62cf0d078b.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '唯識無境 ‧ 梵天',
'eng': 'Chittamatra - Brahma',
'link': 'https://telegra.ph/file/4ec0e43c8df5bc18c467a.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '持戒苦行 ‧ 毗濕奴',
'eng': 'Ascetic Mind - Vishnu',
'link': 'https://telegra.ph/file/06acc987ea636b3421c76.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '大自在天 ‧ 濕婆',
'eng': 'Maheśvara - Shiva',
'link': 'https://telegra.ph/file/769c1077fed1584d63e3f.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '隨緣順心 ‧ 零',
'eng': 'Carefree Mindset - Zero',
'link': 'https://telegra.ph/file/55c9556dd17f51cb3a9d9.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '領風典範 ‧ 蜜兒',
'eng': 'Cat of Charisma - Mellow',
'link': 'https://telegra.ph/file/1d80415acccd057e9fa46.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '如煙無跡 ‧ 阿飄',
'eng': 'Untraceable Moves - Ghostie',
'link': 'https://telegra.ph/file/1cd41d9a5c05e4609a219.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '時空相對論 ‧ 愛因斯坦',
'eng': 'Relativity of Cosmology - Einstein',
'link': 'https://telegra.ph/file/1dce7c194f5e21e59b230.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '生物多樣性 ‧ 達爾文',
'eng': 'Mutated Biodiversity - Darwin',
'link': 'https://telegra.ph/file/f1c3e8eb939109a28d54a.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '超新星序曲 ‧ 伽利略',
'eng': 'Prologue of Supernova - Galileo',
'link': 'https://telegra.ph/file/b7a39c2e55fe7b8d75d1b.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '魔性原罪 · 夏娃',
'eng': 'Origin of All Sins - Eve',
'link': 'https://telegra.ph/file/80bfcb0ba9886be0327df.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '后儀天下 · 武則天',
'eng': 'Militant Heroine - Wu Zetian',
'link': 'https://telegra.ph/file/f3fafeb103490e1004e1c.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '艷后爭鳴 · 克麗奧',
'eng': 'Diva of Obsession - Cleo',
'link': 'https://telegra.ph/file/38deaabb7ad3a3648bba1.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '創世神女 ‧ 女媧',
'eng': 'Ancestral Creation - Nüwa',
'link': 'https://telegra.ph/file/c59ab8cd91ee806cf0337.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '太昊八卦 ‧ 伏羲',
'eng': 'Primal Divinity - Fuxi',
'link': 'https://telegra.ph/file/8730faee56e0ef98cbc1e.jpg',
'star' : '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'name': '瑤池婉妗 ‧ 西王母',
'eng': 'Lady of the Supreme - Xiwangmu',
'link': 'https://telegra.ph/file/f0b91cd618e67f47182aa.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '恆久閃耀 ‧ 鑽石',
'eng': 'Paragon of Brilliance - Diamond',
'link': 'https://telegra.ph/file/98ae6caf392efac465677.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '黛心盈透 ‧ 翡翠',
'eng': 'Pride of Regalia - Jade',
'link': 'https://telegra.ph/file/97289d462720f3b8abd8d.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '蟲火浮光 ‧ 琥珀',
'eng': 'Heated Fluorescence - Amber',
'link': 'https://telegra.ph/file/c84a2855b9d5daf63c963.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '卿雲護庇 ‧ 蒼璧',
'eng': 'Billows of Freedom - Cang Bi',
'link': 'https://telegra.ph/file/749893d0f4af78dba3179.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '智火解析 ‧ 恩莉兒',
'eng': 'Fire of Sagacity - Enlil',
'link': 'https://telegra.ph/file/dabc7930739a2c0a0cd0c.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '冥血吞蝕 ‧ 維洛妮卡',
'eng': 'Blood of Obscurity - Veronica',
'link': 'https://telegra.ph/file/21ceacaa79f9389868203.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '編號 6666 ‧ 依貝思',
'eng': 'No. 6666 - Elpis',
'link': 'https://telegra.ph/file/da97b9834f71ee1fe791d.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '無束天賦 ‧ 因其都',
'eng': 'Liberation of Talent - Enkidu',
'link': 'https://telegra.ph/file/a635e525b21cf3bf7c1b9.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '編號 8299 ‧ 南納',
'eng': 'No. 8299 - Leonard',
'link': 'https://telegra.ph/file/0b1faeb765e9c0c59568d.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '命軸剝奪 ‧ 諾索斯',
'eng': 'Destruction Deprivation - North',
'link': 'https://telegra.ph/file/bfb26476ca45df914c99e.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '星辰之理 ‧ 蘇因',
'eng': 'Gospel of Stars - Saint',
'link': 'https://telegra.ph/file/45142cb0598f228f88983.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '蜃樓星火 ‧ 伊斯塔',
'eng': 'Phantom Pride - Ishtar',
'link': 'https://telegra.ph/file/02ddf2fd068de4d87679d.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '梦咏守望 ‧ 英格丽',
'eng': 'Guardian of Reverie - Ingrid',
'link': 'https://telegra.ph/file/14cdfee0be6fc5f2621e0.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '绯曦赤霞 ‧ 红瑷',
'eng': 'Crimson Runedragon - Hong Ai',
'link': 'https://telegra.ph/file/d949242aeb89b7b2736f5.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '比拟万象 ‧ 达格',
'eng': 'Versatile Shapeshifter - Dagda',
'link': 'https://telegra.ph/file/dcfe9dd177f5f4e103dc3.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '写作之神．菲吕拉',
'eng': 'Philyra, The Authors’ Muse',
'link': 'https://telegra.ph/file/4d93a9a2b10f34a509780.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '叛逆天使．路西法',
'eng': 'Angel of Doom Lucifer',
'link': 'https://telegra.ph/file/e0dc13ae939ea48c9f30b.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '扭曲天使．亚伯汗',
'eng': 'Angel of Distortion Azazel',
'link': 'https://telegra.ph/file/a4de4b7d07f4862f82950.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},
{
'name': '少华钧天 ‧ 华曦',
'eng': 'Apex of Fortitude - Huaxi',
'link': 'https://telegra.ph/file/05ff9ac364c46052d9b5e.jpg',
'star' : '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{'name': '傲志不訾 ‧ 姬臣',
'eng': 'Soaring Aspiration - Jichen',
'link': 'https://telegra.ph/file/6157b702362723633d3cc.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'},
{
'name': '琴息濯洗 ‧ 霏音',
'eng': 'Harmonic of Purification - Feiyin',
'link': 'https://telegra.ph/file/809192f984c96a5c3e844.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '幻影如水 • 希',
'eng': 'Sapphire Phantom - Xi',
'link': 'https://telegra.ph/file/3f8c6f7ccadfb82e8494e.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '芍花愛戀 • 妍',
'eng': 'Peony of Romance - Yan',
'link': 'https://telegra.ph/file/8bbc40c3aa3f1626b813a.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '流光祈护 • 妍希',
'eng': 'Halos of Blessing - Yanxi',
'link': 'https://telegra.ph/file/d0533183c0169f02963cd.jpg',
'star' : '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{'name': '瀟灑雅學 • 妍希',
'eng': 'Chic Charisma - Yanxi',
'link': 'https://telegra.ph/file/cb60dbce0d46a016aefc9.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{
'name': '迅殺芭扇 • 羅剎女',
'eng': 'Devastating Tornado - Rakshasa',
'link': 'https://telegra.ph/file/ce3452af1487720fa9ef1.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},

{'name': '大乘儆惡 • 唐三藏',
'eng': 'Mahayana Punisher - Tang Sanzang',
'link': 'https://telegra.ph/file/a4f0a11541ef932baa464.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},
{
'name': '明悟睿濤 • 亞特蘭堤斯',
'eng': 'Tide of Wisdom - Atlantis',
'link': 'https://telegra.ph/file/6ebbb3e9812082b685852.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},
{
'name': '炙焰城主 • 龐貝',
'eng': 'Ruler of Scorching Flames - Pompeii',
'link': 'https://telegra.ph/file/14df626c15dd8e4e222ee.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},
{
'name': '煌耀女帝 • 美索不達米亞',
'eng': 'Glorious Amazon - Mesopotamia',
'link': 'https://telegra.ph/file/d520fe903b618e8090146.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{
'name': '開世的文明 • 瑪雅',
'eng': 'Dawn of Civilization - Maya',
'link': 'https://telegra.ph/file/dc02fe55b3cd573850fbb.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},

{'name': '冥魂判守 • 阿努比斯',
'eng': 'Shackles of Souls - Anubis',
'link': 'https://telegra.ph/file/5f0f8b290e7905e786689.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ★ ☆'
},
{
'name': '千古一帝 • 秦始皇',
'eng': 'Majesty of Millennium - Ying Zheng',
'link': 'https://telegra.ph/file/6262fa8722d9444cfb422.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '聖杯之永息 • 艾麗亞',
'eng': 'Charlice of Eternity - Aria',
'link': 'https://telegra.ph/file/cf6ccef37168f0eb8a625.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '賢者之石 • 元獸賈比爾',
'eng': 'Philosopher’s Legend - Jabir',
'link': 'https://telegra.ph/file/680c768cc79ee3f531fbd.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{
'name': '和氏之璧 • 青圭',
'eng': 'Jade of Prestige - Qing Gui',
'link': 'https://telegra.ph/file/43470b76cf23a98a4b608.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},

{'name': '希望之盒 • 潘朵拉',
'eng': 'The Box of Hope - Pandora',
'link': 'https://telegra.ph/file/6797435f1b27a51ebe42b.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '全知的惡魔 • 拉普拉斯',
'eng': 'Demon of Omniscience - Laplace',
'link': 'https://telegra.ph/file/89376f4e719bf9691d4d0.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '破陣無雙 • 項羽',
'eng': 'Hegemon of the Empire - Xiang Yu',
'link': 'https://telegra.ph/file/6f86538941c8218c61a31.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '九黎戰神 • 蚩尤',
'eng': 'Divinity of War - Chiyou',
'link': 'https://telegra.ph/file/0a70c16de74c8ae6050d0.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{
'name': '朔月帝女 • 卑彌呼',
'eng': 'Queen of Yamatai - Himiko',
'link': 'https://telegra.ph/file/0db95efaab525e6b615c0.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},

{'name': '迷失者的圣炎 • 巴哈姆特',
'eng': 'Noble Fire of the Lost - Bahamut',
'link': 'https://telegra.ph/file/0573d488cfb1519a70bb7.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '墜落殺戮 • 貝西摩斯',
'eng': 'Fallen Massacre - Behemoth',
'link': 'https://telegra.ph/file/f78ca64adc86a87070194.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '奏響世界之音 • 莎娜',
'eng': 'Resonance of the World - Zana',
'link': 'https://telegra.ph/file/440ec44ffcbbc42d3a227.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '弗麗嘉',
'eng': 'Frigg',
'link': 'https://telegra.ph/file/6c414efa1e437de878f48.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'},
{
'name': '喵喵大將軍 • 虹伶',
'eng': 'General Meow - Hongling',
'link': 'https://telegra.ph/file/935eeb099a169155be503.jpg',
'star': '★ ★ ★ ★ ★ ★ ☆ ☆ ☆'
},

{'name': '魔权在握 • 巴力',
'eng': 'Absolute Authoritarian - Baal',
'link': 'https://telegra.ph/file/fa8427a9caceb13d65068.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
},
{
'name': '澜漫勾惑 • 夏娃',
'eng': 'Innocent Temptation - Eve',
'link': 'https://telegra.ph/file/40f7bdbe3cc5fd5a765b3.jpg',
'star': '★ ★ ★ ★ ★ ★ ★ ☆ ☆'
}]

'''checker = [
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
'Both the Leader and Ally are "Spacial Distortion - Abraham".'
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
'Both the Leader and Ally are "Beyond Salvation - Satan".'
},
{'chi_name':'吕布',
'chif_name':'呂布',
'eng_name':'lubu',
'chi_act':'玄靈滅絕 ‧ 暗流之擊 CD5 \n\n'
' i.將光及心符石\n'
'⇒ 轉化為暗人族強化符石 \n'
'1 回合內\n'
'II. 首批消除 1 組暗符石的數量愈多\n'
'⇒ 連擊 (Combo) 數目增加愈多\n'
'⇒ 消除 1 組 10 粒暗符石\n'
'可增加最多 10 連擊 (Combo)',
'eng_act':'Overwhelming Flow of Darkness CD5 \n\n'
'I. Turn Light and Heart Runestones into Enchanted Dark Human Runestones.\n'
'II. For 1 Round, the more the Dark Runestones dissolved in a group in the first batch, the more the Combo count increases, to the max Combo count +10 for a group of 10 Dark Runestones dissolved.',
'chi_lead':'队长技能名字\n\n'
'虓虎之勇 ‧ 殺伐\n'
'I. 暗屬性攻擊力 5 倍\n'
'II. 暗屬性人類生命力及回復力 1.4 倍\n'
'III. 單體攻擊轉化為全體攻擊\n'
'IV. 必然延長移動符石時間 1 秒\n'
'V. 每消除 1 組 ≥5 粒符石時\n'
'⇒ 暗屬性攻擊力提升\n'
'⇒ 消除 3 組可達至最大 2.8 倍',
'eng_lead':'Slaughter of Roaring Tiger\n\n'
'I. Dark Attack x 5.\n'
'II. Dark Human HP & Recovery x 1.4.\n'
'III. Single Attack becomes Full Attack.\n'
'IV. Extend Runestone-moving time regardlessly by 1 second.\n'
'V. By dissolving a group of 5 or more Runestones,\n'
'⇒ Dark Attack increases additionally, to the max x 2.8 for 3 groups.',
'chi_team':'队伍技能：\n\n'
'I. 進入關卡後，\n'
'「義軍」成員的技能 CD 減少 2\n'
'II. 「義軍」成員的攻擊\n'
'⇒ 無視敵人防禦力\n\n'
'發動條件：\n'
'以潛能解放「義軍」角色作隊長，\n'
'且隊伍中有 ≥3 個「義軍」成員\n\n'
'組合技能：懾魂魅靈 ‧ 屠殺流\n\n'
'I. 將場上的符石轉化為\n'
'⇒ 固定數量及位置的\n'
'「暗及心」人族強化符石\n'
'1 回合內\n'
'II. 全隊攻擊力 3 倍\n'
'III. 首批消除 1 組暗符石的數量愈多\n'
'⇒ 連擊 (Combo) 數目增加愈多\n'
'⇒ 消除 1 組 15 粒暗符石\n'
'可增加最多 15 連擊 (Combo)\n'
'IV. 發動技能的「月華穹 ‧ 貂蟬」\n'
'⇒ 其當前技能 CD 減少 4\n'
'發動條件：\n'
'以「驍猛狂者 ‧ 呂布」及「月華穹 ‧ 貂蟬」作成員
'(召喚獸等級達 50 或以上)\n',
'eng_team':'Team Skill:\n'
'The more the Runestones dissolved in a group, the higher the Team Attack, to the max x 2.5 additionally for a group of 10 Runestones dissolved.\n'
'Condition:\n'
'Both the Leader and Ally are Monsters of "Rebels".\n\n'
'Team Skill:\n'
'Turn the bottom row of Runestones into Dark Runestones at the end of each Round (Dissolving Runestones is necessary).\n'
'Condition:\n'
'Both the Leader and Ally are "Belligerent Mania - Lü Bu", with "Love of Fidelity - Diaochan" as a Team Member.\n\n'
'Team Skill:\n\n'
'I.Active Skill CDs of "Rebel Army" Members -2 after entering a Stage.\n'
'II. Damage of "Rebel Army" Members will be dealt regardless of Defense.\n'
'Condition:\n'
'The Leader is a 7* Monster of "Rebel Army".\n'
'There are 3 or more Members of "Rebel Army" in the Team.\n\n'
'Combine Skill: Captivating Beauty - Massacre\n'
'I. Turn Runestones into Enchanted Dark Human Runestones and Enchanted Heart Human\n' 'Runestones of fixed numbers and fixed positions.\n'
'For 1 Round:\n'
'II. Team Attack x 3.\n'
'III. The more the Dark Runestones dissolved in a group in the first batch, the more the Combo count increases, to the max Combo count +15 for a group of 15 Dark Runestones dissolved.\n'
'IV. Love of Fidelity - Diaochan\'s current Skill CD -4 upon the activation of its Active Skill.\n'
'Condition:\n'
'There are "Belligerent Mania - Lü Bu" and "Love of Fidelity - Diaochan" in the Team (the Monsters must reach Lv. 50 or above).\n'}
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
    return CHECK'''

def draw(update ,context):
    msg = update.message.text.split()[-1]
    user = update.effective_user.name
    user_id = update.effective_user.id
    #random.choice(list, weights=(20, 50, 30, 10), k=1)
    #aa = random.choice(ancts)
    aa = random.choices(ancts, (0.008,0.008,0.008,0.008,0.008,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.0125,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,), k=1)
    '''bb = aa['name']
    pic = aa['link']
    star = aa['star']
    eng = aa['eng']'''
    bb = aa[0]['name']
    pic = aa[0]['link']
    star = aa[0]['star']
    eng = aa[0]['eng']
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
         context.bot.send_message(chat_id=update.effective_chat.id, text=f'{user} 升级到了 level : {user_level + 1}\n 魔法石 +5 \nDiamonds +5\n\n type /inventory again to refresh'
                                                                         f'\n再按一次 /inventory 刷新')


     time.sleep(6)
    #elif msg == '古币' and id == 163494588:
     #update.message.reply_text(f'{user} 全部卡有了还要抽？？', parse_mode=ParseMode.HTML)
    # context.bot.send_animation(chat_id=update.message.chat.id,
                    #        animation='CgACAgQAAx0CTuGbpwACA9hhCkV8obuHVsjS-egdaF6Vu5FXRAACUwIAAh5AxFJLupgMIprTjyAE',)

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


def inventory(update , context):
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    user_diamonds = DB.get_user_value(user_id, "diamonds")
    user_bagslot = DB.get_user_value(user_id, "bagslot")
    user_maxbagslot = DB.get_user_value(user_id, "maxbagslot")
    user_gold = DB.get_user_value(user_id, "gold")
    user_exp = DB.get_user_value(user_id, "exp")
    user_level = DB.get_user_value(user_id, "level")
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

def mycards(update , context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    query = update.callback_query
    cards = DB.get_user_card(user_id, 'card_name')
    cards_en = DB.get_user_card_eng(user_id, 'eng')
    b = 1
    c = "."
    finS = ''
    for chink, engk in zip(cards, cards_en):
        for chinj, engj in zip(chink, engk):
            finS += str(b) + ' ' + str(c) + ' ' + str(chinj) + '\n' + str(engj) + '\n\n'
            b += 1
    update.message.reply_text(f'<u><b>{user} \'s</b> Bag(背包里的卡)</u>\n\n'
                              f'{finS}'
                              , parse_mode = ParseMode.HTML)

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
    user_id = update.effective_user.id
    query = update.callback_query
    cd = context.chat_data
    random.seed(time.time())
    b = cd['a'] = random.randint(1,5)
    # query.answer()
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
    else:
      update.message.reply_text('not authorized')
    return S_POP

def end_pop(update , context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    query = update.callback_query
    user_exp = DB.get_user_value(user_id, "exp")
    user_level = DB.get_user_value(user_id, "level")
    # query.answer()
    cd = context.chat_data
    name = update.callback_query.from_user.first_name
    user_id = update.callback_query.from_user.id
    b = cd['a']

    if query.data =='claim':
        query.message.edit_text(f'*{name}*成功领取*{b}*粒魔法石\n'
                                f'*{name}* claimed *{b}* diamonds\n'
                                f'EXP : 250\n\n'
                                f'其他人哈哈哈哈垃圾', parse_mode = ParseMode.MARKDOWN_V2)
        if user_exp >= user_level * 500:
            DB.add_exp(user_id, -user_exp)
            DB.add_level(user_id)
            context.bot.send_message(chat_id = update.effective_chat.id  , text = f'{name} 升级到了 level : {user_level+1}\n type /inventory again to refresh'
                                                                         f'\n再按一次 /inventory 刷新')
        DB.add_diamonds(user_id, b)
        DB.add_exp(user_id , 250)

    return S_POP

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
    a = ''
    b = ''
    if cd['choice1'] == 'water':
        a = '💧'
    if cd['choice1'] == 'fire':
        a = '🔥'
    if cd['choice1'] == 'wood':
        a = '🍀'
    if cd['choice2'] == 'water':
        b = '💧'
    if cd['choice2'] == 'fire':
        b = '🔥'
    if cd['choice2'] == 'wood':
        b = '🍀'
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
                DB.add_gold(fid, 100)
                DB.add_exp(fid , 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold(tid, 100)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] == cd['fromhp']:
                DB.add_gold(tid, 100)
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
                DB.add_gold(fid, 100)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold( tid, 100)
                DB.add_exp( tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}金币🟡Gold + 100\n'
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
                DB.add_gold( fid, 100)
                DB.add_exp( fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold(tid, 100)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}金币🟡Gold + 100\n'
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
                DB.add_gold(fid, 100)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold(tid, 100)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}金币🟡Gold + 100\n'
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
                DB.add_gold(fid, 100)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold(tid, 100)
                DB.add_exp(tid , 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t}金币🟡Gold + 100\n'
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
                DB.add_gold(fid, 100)
                DB.add_exp(fid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!"
                                        f'{f}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold(tid, 100)
                DB.add_exp(tid, 100)
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!"
                                        f'{t}金币🟡Gold + 100\n'
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
                DB.add_gold(fid, 100)
                DB.add_exp(fid, 100)
                query.message.edit_text(f'{f}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            elif cd['tohp'] > cd['fromhp']:
                DB.add_gold(tid, 100)
                DB.add_exp(tid, 100)
                query.message.edit_text(f'{t}金币🟡Gold + 100\n'
                                        f'EXP + 100')
            return ConversationHandler.END

        return FIRST
      
def help(update , context):
    cd = context.chat_data
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton('Give', callback_data='give'),InlineKeyboardButton('Draw', callback_data='draw')],
        [InlineKeyboardButton('Increase', callback_data='increase'), InlineKeyboardButton('Inventory', callback_data='inventory')],
        [InlineKeyboardButton('Mycards', callback_data='mycards'), InlineKeyboardButton('Game', callback_data='game')],
        [InlineKeyboardButton('Support', callback_data='support'), InlineKeyboardButton('Group', callback_data='group'),InlineKeyboardButton('Channel', callback_data='channel')],
        [InlineKeyboardButton('Close', callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    cd['message'] = update.message.reply_text('以下是可以帮到你的信息，请在使用前阅读，谢谢合作\n\n'
                              'Below are explantion of the bot , please take a momment to read , thank you.',reply_markup=reply_markup)
    return THIRD
  
def cls(update , context):
    cd = context.chat_data
    context.bot.delete_message(chat_id = update.effective_chat.id, message_id = cd['message'].message_id)
    return THIRD
    
def bk(update , context):
    cd = context.chat_data
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton('Give', callback_data='give'),InlineKeyboardButton('Draw', callback_data='draw')],
        [InlineKeyboardButton('Increase', callback_data='increase'), InlineKeyboardButton('Inventory', callback_data='inventory')],
        [InlineKeyboardButton('Mycards', callback_data='mycards'), InlineKeyboardButton('Game', callback_data='game')],
        [InlineKeyboardButton('Support', callback_data='support'), InlineKeyboardButton('Group', callback_data='group'),InlineKeyboardButton('Channel', callback_data='channel')],
        [InlineKeyboardButton('Close', callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    cd['message'] = query.edit_message_text('以下是可以帮到你的信息，请在使用前阅读，谢谢合作\n\n'
                              'Below are explantion of the bot , please take a moment to read , thank you.',reply_markup=reply_markup)
    return THIRD
def st(update , context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('先启动机器人 /starts 后你的数据才会被记录\n'
                    'start the bot first with /starts so that your data will be recorded', reply_markup=reply_markup)
    return THIRD
def inc(update , context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('花费5个魔法石增加5个背包空间\n'
                    'spend 5 diamonds to increase 5 bag space', reply_markup=reply_markup)
    return THIRD

def gi(update , context):
    query = update.callback_query
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
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('查看你的个人信息\n\n'
                    'check your personal statistics', reply_markup=reply_markup)
    return THIRD
def grp(update , context):
    query = update.callback_query
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
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('来查看你的卡片或者炫耀\n\n'
                    'to check what cards you have or to flex', reply_markup=reply_markup)
    return THIRD
def dr(update , context):
    query = update.callback_query
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
    keyboard = [
        [InlineKeyboardButton('Back\n回去', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('加入频道以获得机器人最新消息谢谢\n'
                    'Join Channel to be updated with latest news'
                    '\n\nhttps://t.me/botsupportgourp', reply_markup=reply_markup)
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
                CallbackQueryHandler(end_pop, pattern=".")
            ]
    },
    fallbacks=[],
    allow_reentry=True,
    per_user=False

)
'''check_handler = ConversationHandler(
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
    )'''

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
    per_user=False
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
                CallbackQueryHandler(cls, pattern='^' + str('close') + '$')

            ]
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )

ver_chats = [] # Fetch a list of aproved group IDs from the database
approved_chat_filter = Filters.chat(chat_id = ver_chats)
def verify(update, context):
    obtained_id = update.message.chat.id

    # IMPORTANT STEP, Re-Fetch!
    verchats = []  # ReFetch a list of aproved group IDs from the database instead of using the previously fetched results (from line 7)

    if obtained_id not in verchats:
        # Update the Filters
        obtained_idSet = {obtained_id}
        approved_chat_filter.add_chat_ids(chat_id=obtained_idSet)

        # Update the Database
        # Database.VerChats.add(obtained_id) or something like this, whatever...

        update.message.reply_text("Chat approved!")
    else:
        update.message.reply_markdown("This chat is already approved!")


verify_handler = CommandHandler('approve', verify, filters=Filters.user(user_id=owners))
dispatcher.add_handler(verify_handler)


# ========= UN-APPROVE COMMAND =========
def refute(update, context):
    obtained_id = update.message.chat.id

    # IMPORTANT STEP, Re-Fetch!
    verchats = []  # ReFetch a list of aproved group IDs from the database instead of using the previously fetched results (from line 7)

    if obtained_id in verchats:
        # Update the Filters
        obtained_idSet = {obtained_id}
        approved_chat_filter.remove_chat_ids(chat_id=obtained_idSet)

        # Update the Database
        # Database.VerChats.remove(obtained_id) or something like this, whatever...

        update.message.reply_text("Chat un-approved!")
    else:
        update.message.reply_markdown("This chat is not approved yet, can't un-approve!")




refute_handler = CommandHandler('unapprove', refute, filters=Filters.user(user_id=owners))
INVENTORY_HANDLER = CommandHandler('inventory', inventory)
DRAW_HANDLER = CommandHandler('draw', draw)
SLOT_HANDLER = CommandHandler('slot', slot)
START_HANDLER = CommandHandler('starts', starts)
CREDIT_HANDLER = CommandHandler('credit', credit)
ADD_HANDLER = CommandHandler('add', add)
GIVE_HANDLER = CommandHandler('give', give)
MYCARDS_HANDLER = CommandHandler('mycards', mycards)
sex_HANDLER = CommandHandler('sex', sex)

dispatcher.add_handler(refute_handler)

dispatcher.add_handler(DRAW_HANDLER)
dispatcher.add_handler(INVENTORY_HANDLER)
dispatcher.add_handler(SLOT_HANDLER)
dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(ADD_HANDLER)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(CREDIT_HANDLER)
dispatcher.add_handler(GIVE_HANDLER)
dispatcher.add_handler(MYCARDS_HANDLER)
dispatcher.add_handler(increase_handler)
dispatcher.add_handler(pop_handler)
dispatcher.add_handler(game_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(sex_HANDLER)


cmdStrings = ['inventory','slot', 'draw', 'starts','credit','give','add','mycards','sex','game','button','pop','increase']
cmdFuncs = [inventory, slot, draw, starts , credit , give , add , mycards , sex, game , button , pop , increase]
for x, y in zip(cmdStrings, cmdFuncs):
    dispatcher.add_handler(CommandHandler(x, y, filters = approved_chat_filter))

logger = logging.getLogger()

updater.start_polling(clean = True)

