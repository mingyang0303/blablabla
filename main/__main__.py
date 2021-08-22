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


S_START , S_INCREASE ,S_POP , FIRST , SECOND , *_ = range(1000)
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

def filter(x):
     for i in list:
         if i['name'] == x:
             return i['ID']
def text(x):
    for i in list:
        if i['name'] == x:
            return i['name']

list = [
{'ID':  'AgACAgUAAx0CTuGbpwADmWEKCgABF8hOHQ1vFRC6xKrLr5IMkAACVq0xGyYKUFTOb-Y6BY4LMQEAAwIAA3MAAyAE',
'name' : '英格丽' },

{'ID':
'AgACAgUAAx0CTuGbpwADHGEKA9aw3sJu4WBTURW9CpuLpnipAAJIrTEbJgpQVPuzcpBXJ8cTAQADAgADcwADIAQ',
'name' : '蚩尤'},

{'ID':
'AgACAgUAAx0CTuGbpwADVGEKB1OjZ3tE-TA2VezvHhnThX_rAAJMrTEbJgpQVBtS5-8WRB_VAQADAgADcwADIAQ',
'name' : '姬臣'}
]

char = ['蚩尤', '英格丽','姬臣']

def check(update , context):

    msg = update.message.text
    msg = msg.split()[-1]
    user = update.effective_user.name
    bot = context.bot
    pic = filter(msg)
    des = text(msg)
    '''if msg == "蚩尤":
     bot.send_photo(
        chat_id=update.message.chat.id,
        photo='AgACAgUAAx0CTuGbpwADHGEKA9aw3sJu4WBTURW9CpuLpnipAAJIrTEbJgpQVPuzcpBXJ8cTAQADAgADcwADIAQ',
        caption=f'白痴油', parse_mode=ParseMode.HTML
    )
    elif msg == '姬臣':
        bot.send_photo(
            chat_id=update.message.chat.id,
            photo='AgACAgUAAx0CTuGbpwADVGEKB1OjZ3tE-TA2VezvHhnThX_rAAJMrTEbJgpQVBtS5-8WRB_VAQADAgADcwADIAQ',
            caption=f'<b>name : 姬臣</b>\n'
                    f'<b>HP : 5624</b>\n'
                    f'<b>DMG : 1987</b>\n'
                    f'<b>HEAL : 246</b>\n', parse_mode=ParseMode.HTML)
    elif msg == '英格丽':
        bot.send_photo(
            chat_id=update.message.chat.id,
            photo='AgACAgUAAx0CTuGbpwADmWEKCgABF8hOHQ1vFRC6xKrLr5IMkAACVq0xGyYKUFTOb-Y6BY4LMQEAAwIAA3MAAyAE',
            caption=f'<b>name : 英格丽</b>\n'
                    f'<b>HP : 3034</b>\n'
                    f'<b>DMG : 1907</b>\n'
                    f'<b>HEAL : 450</b>\n', parse_mode=ParseMode.HTML)'''
    if msg in char:
        bot.send_photo(
            chat_id=update.message.chat.id,
            photo=f'{pic}',
            caption=f'{user}的:\n\n{des}', parse_mode=ParseMode.HTML
        )

    else:
     update.message.reply_text('failed : 角色还没加入资料库')

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


    if msg == '古币' or msg == 'gubi':
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
     context.bot.send_message(chat_id=update.message.chat.id, text = f"[点击这里，推荐来这里抽卡/Click here](https://t.me/Game_Gamez)", parse_mode =ParseMode.MARKDOWN_V2) 
     DB.add_user_card(user_id,bb,eng)
     DB.add_exp(user_id, 500)
     if user_exp >= user_level*500:
         DB.add_exp(user_id,-user_exp)
         DB.add_level(user_id)
         context.bot.send_message(chat_id=update.effective_chat.id, text=f'{user} 升级到了 level : {user_level + 1}\n type /inventory again to refresh'
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
CHECK_HANDLER = CommandHandler('check', check)
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
dispatcher.add_handler(CHECK_HANDLER)
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
dispatcher.add_handler(sex_HANDLER)


cmdStrings = ['check','inventory','slot', 'draw', 'start','credit','give','add','mycards','sex','game','button','pop','increase']
cmdFuncs = [check, inventory, slot, draw, start , credit , give , add , mycards , sex, game , button , pop , increase]
for x, y in zip(cmdStrings, cmdFuncs):
    dispatcher.add_handler(CommandHandler(x, y, filters = approved_chat_filter))

logger = logging.getLogger()

updater.start_polling()

