import logging
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters

S_START , S_INCREASE ,S_POP , FIRST , SECOND ,THIRD,CHECK, *_ = range(1000)

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
'Both the Leader and Ally are "Beyond Salvation - Satan".'},
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
'chi_lead':'虓虎之勇 ‧ 殺伐\n\n'
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
'以「驍猛狂者 ‧ 呂布」及「月華穹 ‧ 貂蟬」作成員\n'
'(召喚獸等級達 50 或以上)',
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
'There are "Belligerent Mania - Lü Bu" and "Love of Fidelity - Diaochan" in the Team (the Monsters must reach Lv. 50 or above).'},
{'chi_name':'曹操', 
'chif_name':'曹操', 
'eng_name':'caocao',
'chi_act':'星火延展．強 CD6\n\n'
'I. 將 8 個 固定位置 的符石\n'
'⇒ 轉化為火強化符石\n'
'1 回合內\n'
'II. 延長移動符石時間至 10 秒\n'
'III. 消除 ≥4 組火符石時\n'
'⇒ 全隊攻擊力 2 倍',
'eng_act':'Extension of Fiery Stars CD6\n\n'
'I. Turn 8 Runestones at fixed positions into Enchanted Fire Runestones.\n'
'For 1 Round:\n'
'II. Extend Runestone-moving time to 10 seconds.\n'
'III. By dissolving ≥4 groups of Fire Runestones, Team Attack x 2 additionally.',
'chi_lead':'殘妒之熾燄\n\n'
'I. 魔族及「紅軍」成員攻擊力 5 倍，\n'
'生命力及回復力 1.4 倍\n'
'II. 必然延長移動符石時間 1 秒\n'
'III. 消除火符石的組數愈多\n'
'⇒ 火屬性及「紅軍」成員攻擊力提升愈多\n'
'⇒ 4 組可達至最大 3.5 倍',
'eng_lead':'Flames of Brutal Tyrant - EX\n\n'
'I. Attack of Demons & "Red Army" Members x 5; HP & Recovery x 1.4.\n'
'II. Extend Runestone-moving time regardlessly by 1 second.\n'
'III. The more the groups of Fire Runestones dissolved,\n'
'⇒ the higher the Attack of Fire & "Red Army" Members increases additionally,\n'
'⇒ to the max x 3.5 for 4 groups.',
'chi_team':'隊伍技能：\n\n'
'每首批消除 1 粒\n'
'「紅軍」區域內的符石\n'
'⇒ 提升「紅軍」成員攻擊力\n'
'⇒ 首批消除 10 粒可達至最大 3 倍\n\n'
'發動條件：\n'
'以潛能解放「紅軍」角色作隊長，\n'
'且隊伍中有 ≥3 個「紅軍」成員\n\n'
'隊伍技能：\n'
'I. 消除火符石時，\n'
'下回合將 4 個角落共 4 粒符石\n'
'⇒ 轉化為火強化符石\n'
'II. 消除 ≥3 組火符石時\n'
'⇒ 該回合所受傷害不會使你死亡\n'
'III.「燃燒」敵技的傷害減至 1\n\n'
'發動條件：\n'
'以「霸業魔政 ‧ 曹操」作隊長及戰友\n\n'
'隊伍技能：\n'
'火符石兼具其他屬性符石效果\n\n'
'發動條件：\n'
'以「霸業魔政 ‧ 曹操」作隊長及戰友；且隊伍中有 ≥3 個「紅軍」成員\n\n'
'隊伍技能：\n'
'無視「黏腐」敵技\n\n'
'發動條件：\n'
'以潛能解放「紅軍」角色作隊長，且隊伍中有 ≥3 個「紅軍」成員',
'eng_team':'Team Skill:\n\n'
'By dissolving a Runestone in the "Red Army" region in the first batch,\n'
'⇒ Attack of "Red Army" Members increases additionally,\n'
'⇒ to the max x 3 for 10 Runestones dissolved.\n'
'Condition:\n'
'The Leader is a 7* Monster of "Red Army".\n'
'There are 3 or more Members of "Red Army" in the Team.\n\n'
'Team Skill:\n'
'I. By dissolving Fire Runestones, turn 4 Runestones in 4 corners into Enchanted Fire Runestones at the beginning of the next Round.\n\n'
'II. By dissolving ≥3 groups of Fire Runestones, the Damage received in the Round will not lead to your defeat.\n\n'
'III. Reduce the Damage by “Burning” to 1.\n'
'Condition:\n'
'Both the Leader and Ally are "Tyranny of Dominance - Cao Cao".\n\n'
'Team Skill:\n'
'Fire Runestones also possess the effect of other Attributive Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Tyranny of Dominance - Cao Cao".\n'
'There are 3 or more Members of "Red Army" in the Team.\n\n'
'Team Skill:\n'
'Boss Skill "Sticky Runestones" will be nullified.\n'
'Condition:\n'
'The Leader is a 7* Monster of "Red Army".\n'
'There are 3 or more Members of "Red Army" in the Team.'},
     {'chi_name':'关羽', 
'chif_name':'關羽', 
'eng_name':'guanyu',
'chi_act':'三原流水刃 ‧ 強 CD 5\n\n'
'I. 將光符石轉化為水強化符石\n'
'II. 將暗符石轉化為火強化符石\n'
'III. 將心符石轉化為木強化符石\n'
'1 回合內\n'
'IV. 水符石兼具 50% 心符石效果',
'eng_act':'Blade of Tricolor Stream CD 5\n\n'
'I. Turn Light Runestones into Enchanted Water Runestones.\n'
'II. Turn Dark Runestones into Enchanted Fire Runestones.\n'
'III. Turn Heart Runestones into Enchanted Earth Runestones.\n'
'IV. For 1 Round, Water Runestones also possess 50% effect of Heart Runestones.',
'chi_lead':'結義盟誓\n\n'
'隊伍中只有水、火及木屬性成員時：\n'
'I. 水符石兼具 50% 其他屬性符石效果\n'
'II. 火符石兼具 50% 其他屬性符石效果\n'
'III. 木符石兼具 50% 其他屬性符石效果\n'
'IV. 消除 3 種符石時\n'
'⇒ 全隊攻擊力 4 倍\n'
'V. 消除 ≥4 種符石時\n'
'⇒ 全隊攻擊力 5 ',
'eng_lead':'Final Vow of Fraternity\n\n'
'When the Team consists of only Water, Fire and Earth Monsters:\n'
'I. Water Runestones also possess 50% effects of other Attributive Runestones.\n'
'II. Fire Runestones also possess 50% effects of other Attributive Runestones.\n'
'III. Earth Runestones also possess 50% effects of other Attributive Runestones.\n'
'IV. If 3 types of Runestones are dissolved,\n'
'⇒ Team Attack x 4.\n'
'V. If 4 or more types of Runestones are dissolved,\n'
'⇒ Team Attack x 5.',
'chi_team':'隊伍技能:\n\n'
'隊長的隊長技能「結義盟誓」\n'
'⇒ 變為「結義盟誓 ‧ 強」\n\n'
'隊伍中只有水、火及木屬性成員時：\n'
'I. 水符石兼具 50% 其他屬性符石效果\n'
'II. 火符石兼具 50% 其他屬性符石效果\n'
'III. 木符石兼具 50% 其他屬性符石效果\n\n'
'IV. 消除 3 種符石時\n'
'⇒ 全隊攻擊力 4 倍\n'
'V. 消除 ≥4 種符石時\n'
'⇒ 全隊攻擊力 5 倍\n\n'
'VI. 3 粒相連的屬性符石可發動消除\n'
'VII. 2 粒心符石相連可發動消除所有符石掉落率不受其他技能影響\n'
'(包括改變掉落符石屬性的技能)\n\n'
'發動條件：\n'
'以「驍銳武聖 ‧ 關羽」作隊長及戰友\n\n'
'隊伍技能：\n'
'I.全隊生命力、攻擊力、回復力 1.3 倍\n\n'
'II. 最左方的「靈應童將 ‧ 張飛」\n'
'⇒ 技能 CD 減少 3\n\n'
'發動條件：\n'
'以「驍銳武聖 ‧ 關羽」、「革導皇命 ‧ 劉備」及「靈應童將 ‧ 張飛」作成員\n\n'
'隊伍技能：\n'
'每首批消除 1 粒\n'
'「綠軍」區域內的符石\n'
'⇒ 提升「綠軍」成員攻擊力\n'
'⇒ 首批消除 10 粒可達至最大 3 倍\n\n'
'發動條件：\n'
'以潛能解放「綠軍」角色作隊長，且隊伍中有 ≥3 個「綠軍」成員\n\n'
'隊伍技能：\n'
'消除 ≥3 種符石時，\n'
'「綠軍」成員額外追打 50% 攻擊 1 次\n\n'
'發動條件：\n'
'以潛能解放「綠軍」角色作隊長，且隊伍中有 ≥3 個「綠軍」成員\n\n'
'組合技能：三原獵刃 ‧ 結義\n'
'I. 引爆所有符石\n'
'II. 將所有符石轉化為\n'
'⇒ 固定數量及位置的\n'
'水、火、木人族強化符石\n'
'1 回合內\n'
'III. 水、火、木符石兼具50% 心符石效果\n'
'IV. 全隊追打光屬性攻擊 2 次\n\n'
'發動條件：\n'
'以「驍銳武聖 ‧ 關羽」及「革導皇命 ‧ 劉備」作成員\n'
'(召喚獸等級達 50 或以上)\n'
'發動條件：\n'
'以「驍銳武聖 ‧ 關羽」及「靈應童將 ‧ 張飛」作成員\n'
'(召喚獸等級達 50 或以上)\n\n'
'組合技能：三原獵刃 ‧ 結義\n'
'I. 引爆所有符石\n'
'II. 將所有符石轉化為\n'
'⇒ 固定數量及位置的水、火、木人族強化符石\n'
'1 回合內\n'
'III. 水、火、木符石兼具50% 心符石效果\n'
'IV. 全隊追打光屬性攻擊 2 次\n'
'發動條件：\n'
'以「驍銳武聖 ‧ 關羽」及「革導皇命 ‧ 劉備」作成員(召喚獸等級達 50 或以上)',
'eng_team':'Team Skill:\n\n'
'Change the Leader Skill of the Leader from "Final Vow of Fraternity" to "Final Vow of Fraternity - EX".\n\n'
'When the Team consists of only Water, Fire and Earth Monsters:\n'
'I. Water Runestones also possess 50% effects of other Attributive Runestones.\n'
'II. Fire Runestones also possess 50% effects of other Attributive Runestones.\n'
'III. Earth Runestones also possess 50% effects of other Attributive Runestones.\n'
'IV. If 3 types of Runestones are dissolved,\n'
'⇒ Team Attack x 4.\n'
'V. If 4 or more types of Runestones are dissolved,\n'
'⇒ Team Attack x 5.\n\n'
'VI. Attributive Runestones can be dissolved by grouping 3 or more of them.\n'
'VII. Heart Runestones can be dissolved by grouping 2 or more of them.\n'
'Drop rate of all Runestones will not be affected by Amelioration or Skills (including those altering the Attribute of dropping Runestones).\n'
'Condition:\n'
'Both the Leader and Ally are "Valorous Legend - Guan Yu".\n'
'Team Skill:\n\n'
'I. Team HP, Attack & Recovery x 1.3 additionally.\n'
'II. Active Skill CD of the first "Wildlife Affinity - Zhang Fei" from the left -3.\n\n'
'Condition:\n'
'There are "Valorous Legend - Guan Yu", "Fate of Revolution - Liu Bei" and "Wildlife Affinity - Zhang Fei" in the Team.\n\n'
'Team Skill:\n'
'By dissolving a Runestone in the "Green Army" region in the first batch,\n'
'⇒ Attack of "Green Army" Members increases additionally,\n'
'⇒ to the max x 3 for 10 Runestones dissolved.\n'
'Condition:\n'
'The Leader is a 7* Monster of "Green Army".\n'
'There are 3 or more Members of "Green Army" in the Team.\n\n'
'Team Skill:\n'
'By dissolving ≥3 types of Runestones, each "Green Army" Member launches an extra attack as much as 50% of its attack.\n'
'Condition:\n'
'The Leader is a 7* Monster of "Green Army".\n'
'There are 3 or more Members of "Green Army" in the Team.\n\n'
'Combine Skill: Blade of Tricolor Rays - EX\n'
'I. Explode all Runestones.\n'
'II. Turn all Runestones into Enchanted Water Human, Enchanted Fire Human and Enchanted Earth Human Runestones of fixed numbers and fixed positions.\n'
'For 1 Round:\n'
'III. Water, Fire and Earth Runestones also possess 50% effect of Heart Runestones.\n'
'IV. The Team launches 2 extra Light attacks.\n'
'Condition:\n'
'There are "Valorous Legend - Guan Yu" and "Wildlife Affinity - Zhang Fei" in the Team (the Monsters must reach Lv. 50 or above).\n\n'
'Combine Skill: Blade of Tricolor Rays - EX\n'
'I. Explode all Runestones.\n'
'II. Turn all Runestones into Enchanted Water Human, Enchanted Fire Human and Enchanted Earth Human Runestones of fixed numbers and fixed positions.\n\n'
'For 1 Round:\n'
'III. Water, Fire and Earth Runestones also possess 50% effect of Heart Runestones.\n'
'IV. The Team launches 2 extra Light attacks.\n'
'Condition:\n'
'There are "Valorous Legend - Guan Yu" and "Fate of Revolution - Liu Bei" in the Team (the Monsters must reach Lv. 50 or above).'},
     {'chi_name':'月读', 
'chif_name':'月讀', 
'eng_name':'tsukuyomi',
'chi_act':'凝时之念 ‧ 神  CD6\n\n'
'I. 延长移动符石时间至 10 秒\n'
'II. 于移动符石时间内，\n'
'可任意移动符石而不会发动消除\n'
'III. 敌方全体的防御力减至 0\n'
'(效果会在关闭此技能或死亡后消失)\n\n'
'此技能可随时关闭，关闭时：\n'
'⓵ 将所有符石添加为神族符石\n'
'⓶ 将暗符石转化为神族强化符石',
'eng_act':'Time-freezing Notion - EX  CD6\n\n'
'I. Extend Runestone-moving time to 10 seconds.\n'
'II. Unlimited Runestone movement without dissolving within Runestone-moving time.\n'
'III. Enemies\' Defense will be reduced to 0. The Skill stays in play until deactivation or defeated.\n\n'
'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'⓵ Modify all Runestones to become God Runestones.\n'
'⓶ Turn Dark Runestones into Enchanted God Runestones.',
'chi_lead':'魅之花海 ‧ 盛\n\n'
'I. 暗属性攻击力 6 倍，生命力及回复力 1.2 倍\n'
'II. 回合结束时，\n'
'随机将 3 粒暗强化符石四周的符石\n'
'⇒ 转化为暗神族符石\n'
'III. 消除神族符石时\n'
'⇒ 暗属性攻击力额外 2.5 倍',
'eng_lead':'Floral Sea of Shadow - EX\n\n'
'I. Dark Attack x 6; HP & Recovery x 1.2.\n'
'II. At the end of each Round,\n'
'turn Runestones around 3 random Enchanted Dark Runestones into Dark God Runestones.\n'
'III. By dissolving God Runestones,\n'
'⇒ Dark Attack x 2.5 additionally.',
'chi_team':'队伍技能：\n\n'
'消除符石前场上有种族符石\n'
'⇒ 该种族成员攻击力 2.5 倍\n'
'发动条件：\n'
'以相同的潜解“大和”系列角色\n'
'作队长及战友\n\n'
'队伍技能：\n'
'I. 首批消除 1 组暗符石的数量愈多\n'
'⇒ 连击 (Combo) 数量增加愈多\n'
'II. 首批消除 1 组 ≥12 粒暗符石\n'
'⇒ 暗属性成员的攻击\n'
'无视“指定形状盾”敌技\n'
'发动条件：\n'
'以“寂寥偶戏 ‧ 月读“作队长及战友.',
'eng_team':'Team Skill:\n\n'
'When there are Race Runestones before dissolving Runestones, Attack of that Race x 2.5.\n'
'Condition:\n'
'The Leader and Ally are the same Monster of “Yamato - Power Release”.\n\n'
'Team Skill:\n'
'I. The more Dark Runestones dissolved in a group in the first batch, the higher the Combo count.\n'
'II. When a group of ≥12 Dark Runestones is dissolved in the first batch, Damage of Dark Members will be dealt regardless of Puzzle Shield.\n'
'Condition:\n'
'The Leader and Ally are “Lone Puppeteer - Tsukuyomi”.'},
    {'chi_name':'天照',
'chif_name':'天照',
'eng_name':'amaterasu',
'chi_act':'神权八咫镜 ‧ 强 CD10\n\n'
'I. 将所有符石转化为神族强化符石\n'
'2 回合内\n'
'II. 吸收该回合敌人首次攻击伤害\n'
'III. 以所吸收攻击力的 1000 倍\n'
'⇒ 对其进行火属性反击\n'
'(此伤害无视防御力及“强化突破”敌技',
'eng_act':'Mighty Eight Hand Mirror - EX CD10\n\n'
'I. Turn all Runestones into Enchanted God Runestones.\n'
'For 2 Rounds,\n'
'II. Absorb the first Attack of the first attacking enemy in the Round.\n'
'III. Deal a Fire Damage as much as 1000x the absorbed Attack to it, regardless of Defense and Enchanted Runestone Shield.',
'chi_lead':'焰神咒术．强\n\n'
'I. 火属性及神族攻击力 6.5 倍\n'
'II. 神族生命力及回复力 1.5 倍\n'
'III. 火符石兼具 50% 其他符石效果\n'
'IV. 消除 1 种符石 ≥8 粒时\n'
'⇒ 火属性及神族攻击力额外 2.5 倍\n'
'V. 消除 1 种符石 ≥15 粒时\n'
'⇒ 火属性及神族攻击力额外 3 倍',
'eng_lead':'Spell of Flames & Gods - EX\n\n'
'I. Fire Attack and God Attack x 6.5.\n'
'II. God HP & Recovery x 1.5.\n'
'III. Fire Runestones also possess 50% effect of other Runestones.\n'
'IV. If ≥8 Runestones of one type are dissolved, Fire & God Attack x 2.5 additionally.\n'
'V. If ≥15 Runestones of one type are dissolved, Fire & God Attack x 3 additionally.',
'chi_team':'队伍技能：\n\n'
'消除符石前场上有种族符石\n'
'⇒ 该种族成员攻击力 2.5 倍\n'
'发动条件：\n'
'以相同的潜解“大和”系列角色\n'
'作队长及战友\n\n'
'队伍技能：\n'
'I. 队中主动技能 ≥CD 10 的成员\n'
'⇒ 进入关卡后，技能 CD 减少 10\n'
'II. 每次发动龙刻脉动后\n'
'(只适用于首 2 次)\n'
'⇒ 火属性神族成员技能 CD 减少 10\n'
'III. 下回合开始时，\n'
'将火符石转化为神族符石\n'
'发动条件：\n'
'以“馨阳晴爽 ‧ 天照”作队长及战友.',
'eng_team':'Team Skill:\n\n'
'When there are Race Runestones before dissolving Runestones, Attack of that Race x 2.5.\n'
'Condition:\n'
'The Leader and Ally are the same Monster of “Yamato - Power Release”.\n\n'
'Team Skill:\n'
'I. Monsters with Active Skill CD ≥10,\n'
'⇒ Active Skill CD -10 after entering a Stage.\n'
'II. Every time a Dragonic Compulsion is activated (only applicable for the first 2 times),\n'
'⇒ Active Skill CD of Fire Gods -10.\n'
'III. Turn Fire Runestones into God at the beginning of next Round.\n'
'Condition:\n'
'The Leader and Ally are “Radiant Sunshine - Amaterasu”.'},
     {'chi_name':'伊邪那岐',
'chif_name':'伊邪那岐',
'eng_name':'izanagi',
'chi_act':'靈木無量 ‧ 靈動 CD8\n\n'
'I. 將場上所有符石轉化為\n'
'⇒ 固定數量及位置 的\n'
'「心及木神族」強化符石\n'
'1 回合內\n'
'II. 木及心符石\n'
'首批 2 粒相連即可發動消除',
'eng_act':'Immense Power of Earth Spirits - EX CD8\n'
'I. Turn all Runestones into Enchanted Heart Runestones and Enchanted Earth God\n' 'Runestones of fixed numbers and fixed positions.\n'
'For 1 Round,\n'
'II. Earth and Heart Runestones can be dissolved by aligning 2 or more of them in the first batch.',
'chi_lead':'藤木之靈 ‧ 延\n\n'
'I. 木屬性攻擊力 6.5 倍，\n'
' 生命力及回復力 1.2 倍\n'
'II. 心符石兼具 50% 木符石效果\n'
'III. 延長移動符石時間 1.5 秒\n'
'IV. 同時消除木及心符石時\n'
'⇒ 木屬性攻擊力額外 2 倍',
'eng_lead':'Spirits of Vines - EX\n\n'
'I. Earth Attack x 6.5; HP & Recovery x 1.2.\n'
'II. Heart Runestones also possess 50% effect of Earth Runestones.\n'
'III. Extend Runestone-moving time by 1.5 seconds.\n'
'IV. If Earth and Heart Runestones are dissolved in the same Round,\n'
'⇒ Earth Attack x 2 additionally.',
'chi_team':'隊伍技能：\n\n'
'消除符石前場上有種族符石\n'
'⇒ 該種族成員攻擊力 2.5 倍\n'
'發動條件：\n'
'以相同的潛解「大和」系列角色作隊長及戰友\n\n'
'隊伍技能：\n'
'I. 消除木符石時，回合結束時：\n'
'將最底 1 橫行的符石轉化為\n'
'⇒「木及心」神族強化符石各 3 粒\n'
'II. 首批消除 ≥4 組木或心符石時\n'
'⇒ 木屬性攻擊力 2 倍\n'
'發動條件：\n'
'以「顧眄相伴 ‧ 伊邪那岐」作隊長及戰友.',
'eng_team':'Team Skill:\n\n'
'When there are Race Runestones before dissolving Runestones, Attack of that Race x 2.5.\n'
'Condition:\n'
'The Leader and Ally are the same Monster of “Yamato - Power Release”.\n\n'
'Team Skill:\n'
'I. By dissolving Earth Runestones, turn the bottom row into 3 Enchanted Earth God Runestones and 3 Enchanted Heart God Runestones after the Round.\n'
'II. When ≥4 groups of Earth or Heart Runestones are dissolved in the first batch, Earth Attack x 2.\n'
'Condition:\n'
'The Leader and Ally are “Resilient Love - Izanagi”.'},
    {'chi_name':'亚瑟',
'chif_name':'亞瑟',
'eng_name':'arthur',
'chi_act':'王之剑 CD7\n\n'
'1 回合内消除水符石时，减少 60% 所受伤害；消除火符石时，无视全体敌人的防御力；消除木符石时，回复 15000 点生命力。同时消除水、火及木符石时，全队攻击力提升 2 倍',
'eng_act':'Legendary Sword of the King CD7\n\n'
'For 1 Round, by dissolving Water Runestones, Damage received -60%; by dissolving Fire Runestones, Damage will be dealt regardless of enemies\' Defense; by dissolving Earth Runestones, recover 15000 HP. If Water, Fire and Earth Runestones are dissolved in the same Round, Team Attack x 2.',
'chi_lead':'圣剑\n\n'
'队伍中只有光属性人类时：\n'
'I. 全队攻击力 3 倍\n'
'II. 所有符石兼具 15% 光符石效果',
'eng_lead':'Sword in the Lake\n\n'
'When the Team consists of only Light Humans, Team Attack x 3; all Runestones also possess 15% effects of Light Runestones.',
'chi_team':'队伍技能：\n\n'
'消除 4 组或以上符石，回合结束时，将随机 1 个角落的 3 粒符石转化为光符石。\n'
'队长的队长技能“圣剑”变为“圣剑 ‧ 裂光”，当中于每回合移动并消除符石后，引爆所有光符石，直至场上没有光符石，引爆的光符石愈多，攻击力额外提升愈多，引爆 5 粒可达至最大 2 倍 (倍率不可叠加)\n'
'光属性攻击力提升 1.5 倍\n'
'发动条件：\n'
'以高洁骑士．亚瑟作队长及战友\n\n'
'队伍技能：\n'
'最左方的脱兔派对王 ‧ 君士坦丁的主动技能 CD 减少 3\n'
'发动条件：\n'
'队伍中有高洁骑士．亚瑟及脱兔派对王 ‧ 君士坦丁作成员',
'eng_team':'When 4 or more groups of Runestones are dissolved, turn 3 Runestones in 1 random corner into Light Runestones after the Round.\n'
'Change the Leader Skill of the Leader from "Sword in the Lake"to "Sword in the Lake - Light-cracking" Upon the completion of moving and dissolving Runestones each Round, all Light Runestones will explode until there is no more Light Runestone on the screen. The more Light Runestones exploded, the higher the Team Attack, to the max x 2 additionally for 5 Light Runestones (no superimposing).\n'
'Light Attack x 1.5 additionally.\n'
'Conditon:\n'
'Both the Leader and Ally are "Knight of Virtuousness - Arthur".\n\n'
'Team Skill:\n'
'Active Skill CD of the first "Constantine the Master of Celebration" from the left -3.\n'
'Condition:\n'
'There are "Knight of Virtuousness - Arthur" and "Constantine the Master of Celebration" in the Team.'},
    {'chi_name':'兰斯洛特',
'chif_name':'蘭斯洛特',
'eng_name':'lancelot',
'chi_act':'暗黑之劍氣 CD5\n'
'水符石轉化為暗強化符石，下回合開始時，將本回合所消除強化符石的數量等值的符石轉化為暗強化符石 (水及光符石優先轉換)\n\n'
'銳劍出鞘 CD5\n'
'每回合自身攻擊力持續提升，最大 4 倍，直至自身沒有發動攻擊',
'eng_act':'Dark Power of Blade CD5\n'
'Turn Water Runestones into Enchanted Dark Runestones. At the beginning of next Round, turn Runestones into Enchanted Dark Runestones of a number same as that of the Enchanted Runestones dissolved in this Round (Water and Light Runestones rank first in priority).\n\n'
'Sword Unsheathing CD5\n'
'The Monster\'s Attack continues to increase every Round, to the max x 4, until no Attack is launched by the Monster.',
'chi_lead':'騎士之盟\n'
'隊伍中只有火、木及暗屬性成員時：\n'
'I. 全隊攻擊力 4 倍\n'
'II. 消除心符石時\n'
'⇒ 全隊攻擊力有 50% 機率額外 2 倍\n'
'(機率可以疊加)',
'eng_lead':'Alliance of Knights\n\n'
'When the Team consists of only Fire, Earth and Dark Monsters, Team Attack x 4 and if Heart Runestones are dissolved, there will be a 50 chance of gaining an extra of x 2 (the probability can be summed up)',
'chi_team':'沒有隊伍技能',
'eng_team':'None'},
    {'chi_name':'梅林',
'chif_name':'梅林',
'eng_name':'merlin',
'chi_act':'治癒之賦 ‧ 化擊 CD6\n\n'
'1 回合內，隊伍成員的屬性愈多，回復力愈高，最大 3.5 倍；當隊伍中所有成員的回復力基值相同時，所有成員追打 1 次暗屬性傷害，並將全隊對敵方造成傷害的 5% 轉化為生命力 (不計算主動及隊長技傷害)',
'eng_act':'Recovery Talent - Attack Conversion CD6\n\n'
'For 1 Round, the more the Attributes of Monsters in the Team, the higher the Recovery, to the max x 3.5. When all Members have the same Recovery basic value, one extra Dark Attack will be launched by each Member; 5% of Damage dealt to enemies will be converted to HP Recovery (Damage dealt by Active and Leader Skills will not trigger the effect). ',
'chi_lead':'暗黑回復魔法\n\n'
'I. 妖精類攻擊力及回復力 4 倍\n'
'II. 回合結束時，將心符石轉化為心強化符石',
'eng_lead':'Dark Magic of Recovery\n\n'
'Elf Attack & Recovery x 4. Turn Heart Runestones into Enchanted Heart Runestones after each Round.',
'chi_team':'沒有隊伍技能',
'eng_team':'None'},
    {'chi_name':'织田信长',
'chif_name':'織田信長',
'eng_name':'nobunaga',
'chi_act':'森涛尽噬 ‧ 赤火 CD6\n\n'
'1 回合内，全队攻击力 1.3 倍；将火符石转化为火强化符石，并引爆场上所有水、木及心符石，以掉落火、光及暗强化符石',
'eng_act':'Waves & Forests Burnt Down CD6\n\n'
'Team Attack x 1.3 for 1 Round. Turn Fire Runestones into Enchanted Fire Runestones. Explode all Water, Earth and Heart Runestones to generate Enchanted Fire, Enchanted Light and Enchanted Dark Runestones.',
'chi_lead':'焰刃袭\n\n'
'I. 火属性“人类、龙类”攻击力 4.5 倍\n'
'II. 延长移动符石时间 1 秒\n'
'III. 消除 ≥12 粒火符石时\n'
'⇒ 全队攻击力额外 1.5 倍',
'eng_lead':'Raid of Flaming Blade\n\n'
'Fire Human and Fire Dragon Attack x 4.5. Extend Runestone-moving time by 1 second. By dissolving 12 or more Fire Runestones, Team Attack x 1.5 additionally.',
'chi_team':'队伍技能：\n\n'
'光及暗符石兼具火符石效果\n'
'发动条件：\n'
'以烽火武心．织田信长作队长及战友\n\n'
'队伍技能：\n'
'华丝潋滟．浓姬的主动技能 CD 减少 2\n'
'发动条件：\n'
'以烽火武心．织田信长作队长及战友，并以华丝潋滟．浓姬作队员',
'eng_team':'Team Skill:\n\n'
'Light and Dark Runestones also possess the effect of Fire Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Nobunaga the Blazing Fervour".\n\n'
'Team Skill:\n'
'Active Skill CD of "Nohime the Alluring Beauty" -2.\n'
'Condition:\n'
'Both the Leader and Ally are "Nobunaga the Blazing Fervour", with "Nohime the Alluring Beauty" as a Team Member.'},
    {'chi_name':'丰臣秀吉',
'chif_name':'豐臣秀吉',
'eng_name':'hideyoshi',
'chi_act':' 藤棘術 CD3\n\n'
'隨機將 4 至 7 粒符石轉化為木強化符石(光及暗符石優先轉換)',
'eng_act':'Spell of Pricking Thorns CD3\n\n'
'Turn 4 to 7 random Runestones into Enchanted Earth Runestones (Light and Dark Runestones rank first in priority).',
'chi_lead':'木葉之森\n\n'
'I. 消除 6 粒木符石時\n'
'⇒ 木屬性人類攻擊力 3.75 倍\n'
'II. 消除的木符石數量愈多\n'
'⇒ 木屬性人類攻擊力愈高\n'
'⇒ 消除 15 粒木符石可達至最大 6 倍',
'eng_lead':'Leafy Forest\n\n'
'By dissolving 6 Earth Runestones, Earth Human Attack x 3.75; the more Earth Runestones dissolved, the higher the Attack, to the max x 6 for 15 Earth Runestones.',
'chi_team':'隊伍技能：\n\n'
'扇頁浮金．豐臣秀吉及忌心妒者．明智光秀的主動技能 CD 減少 2\n'
'發動條件：\n'
'以扇頁浮金．豐臣秀吉作隊長及戰友',
'eng_team':'Team Skill:\n\n'
'Active Skill CDs of "Hideyoshi the Insatiable Greed" and "Akechi the Bloodthirsty Blade" -2.\n'
'Condition:\n'
'Both the Leader and Ally are "Hideyoshi the Insatiable Greed".'},
    {'chi_name':'本多忠胜',
'chif_name':'本多忠勝',
'eng_name':'honda',
'chi_act':'百戰不摧 CD8\n\n'
'1 回合內，將我方所受傷害直接轉化為我方生命力。若該回合敵人沒有發動攻擊，下回合全隊攻擊力 2 倍',
'eng_act':'Dauntless in Battles CD8\n\n'
'Damage received will be converted to HP Recovery for 1 Round. If no Damage is received upon the Round of Skill activation, Team Attack x 2 in.',
'chi_lead':'巨力之腕\n\n'
'I. 隊伍中只有 2 種屬性成員時\n'
'⇒ 全隊攻擊力 2.5 倍\n'
'II. 若隊伍中有 ≥4 個人類成員\n'
'⇒ 全隊攻擊力額外 2 倍',
'eng_lead':'Fist of Immense Strength\n\n'
'When there are only 2 Attributes in the Team, Team Attack x 2.5. If there are 4 or more Humans in the Team, Team Attack x 2 additionally.',
'chi_team':'隊伍技能：\n\n'
'水符石兼具光符石效果，同時光符石兼具水符石效果\n'
'消除 4 連擊 (Combo) 或以上時，減少 35% 所受傷害\n'
'發動條件：\n'
'以豪拳斷罪．本多忠勝作隊長，並以九天應元 ‧ 聞仲、齊恆天帥‧ 姜子牙、僭逆王徒‧ 孫權、戀眷朝暮‧ 大喬與小喬或豪拳斷罪．本多忠勝作戰友',
'eng_team':'Team Skill:\n\n'
'Water Runestones also possess the effect of Light Runestones; Light Runestones also possess the effect of Water Runestones.\n'
'If 4 or more Combos are made, Damage received -35%.\n'
'Condition:\n'
'The Leader is "Honda the Fist of Savagery", and the Ally is "Wen Zhong the Sagacious Welkinite", "Jiang Ziya, High Marshal of Empyrean", "Sun Quan the Lord of Veiled Ability", Genuine Sentiments - Qiao Sisters" or "Honda the Fist of Savagery".\n'
'The Team consists of only Water and Light Monsters.'},
   {'chi_name':'蛇夫座',
'chif_name':'蛇夫座',
'eng_name':'ophiuchus',
'chi_act':'蛇影灵动 CD8\n\n'
'15 秒内，可任意移动符石而不会发动消除。若队伍中只有神族及妖精类成员时，1 回合内全队攻击力 2 倍',
'eng_act':'Shadows of Snake Spirits CD8\n\n'
'Unlimited Runestone movement in 15 seconds without dissolving. If the Team consists of only Gods and Elves, Team Attack x 2 for 1 Round.',
'chi_lead':'神魅猎杀势\n\n'
'队伍中只有神族及妖精类成员时\n'
'⇒ 全队攻击力 4.5 倍及生命力 1.3 倍',
'eng_lead':'Aggressive Gods & Elves\n\n'
'When the Team consists of only Gods and Elves:\n'
'⇒ Team Attack x 4.5 and HP x 1.3.',
'chi_team':'队伍技能：\n\n'
'I. 队长及战友的队长技“神魅猎杀势”⇒ 变为“神魅猎杀势・突破”：队伍中只有神族及妖精类成员时\n'
'① 全队攻击力 4.5 倍及生命力 1.3 倍\n'
'② 将移动符石时触碰的符石\n'
'⇒ 转化为强化符石\n'
'③ 移动的步数愈多\n'
'⇒ 全队攻击力提升愈多\n'
'⇒ 移动 50 步攻击力可提升至最大 3 倍\n'
'II. 必然延长移动符石时间 1 秒\n'
'III. 队伍中每个妖精类成员\n'
'⇒ 必然增加移动符石时间 2 秒\n'
'发动条件：\n'
'宿命扭转 ‧ 蛇夫座斯克勒作队长及战友',
'eng_team':'Team Skill:\n\n'
'Change the Leader Skill of the Leader and Ally from "Aggressive Gods & Elves" to "Aggressive Gods & Elves - EX". When the Team consists of only Gods and Elves:\n'
'① Team Attack x 4.5 and HP x 1.3.\n'
'② Turn all Runestones touched while moving into Enchanted Runestones.\n'
'③ The more the steps moved while moving Runestones, the higher the Team Attack, to the max x 3 additionally for 50 steps.\n'
'II. Extend Runestone-moving time regardlessly by 1 second.\n'
'III. For every Elf present in the Team, extend Runestone-moving time regardlessly by 2 more seconds.'},
    {'chi_name':'仙女座',
'chif_name':'仙女座',
'eng_name':'andromeda',
'chi_act':'幻影流星 CD5\n\n'
'消除屬性符石時，個人追打與消除符石屬性相同的攻擊各 1 次。效果持續至沒有消除 3 種或以上的屬性符石',
'eng_act':'Shade of Shooting Stars CD5\n\n'
'By dissolving Attributive Runestones, the Monster launches an extra Attack of that Attribute The Skill stays in play until not 3 or more Attributes of Runestones are dissolved in the Round.',
'chi_lead':'流水之誘惑\n\n'
'I. 水屬性攻擊力 2 倍、生命力及回復力 1.3 倍\n'
'II. 妖精攻擊力額外 5 倍\n'
'III. 消除 ≥4 種符石時\n'
'⇒ 該回合減少 25% 所受傷害',
'eng_lead':'Alluring Beauty of the Sea - EX\n\n'
'I. Water Attack x 2; HP & Recovery x 1.3.\n'
'II. Elf Attack x 5 additionally.\n'
'III. By dissolving 4 or more types of Runestones,\n'
'⇒ Damage received -25%.',
'chi_team':'隊伍技能：\n\n'
'連擊 (Combo) 時攻擊力提升 25%\n'
'發動條件：\n'
'以綺香誘惑 ‧ 仙女座安德洛作隊長',
'eng_team':'Team Skill:\n'
'Attack bonus for Combo increases by 25%.\n'
'Condition:\n'
'The Leader is "Sultry Fragrance - Andromeda".'},
    {'chi_name':'夏娃',
'chif_name':'夏娃',
'eng_name':'eve',
'chi_act':'金果诱毒 CD6 \n\n'
'I. 每回合所有“澜漫勾惑 ‧ 夏娃” \n'
'⇒ 增加 1 个金果 \n'
'II. 若队长及战友均为“魔性原罪 · 夏娃”时 \n'
'⇒ 每回合所有“魔性原罪 · 夏娃”增加 1 个禁果 \n'
'III. 必延 1.5 秒 \n'
'IV. 魔族成员伤害 \n'
'⇒ 可克制木属性目标'
'V. 若队中有 ≥2 个魔族成员 \n'
'⇒ 连击 (Ex. Combo、Combo)时攻击力提升 40% (效果会在关闭此技能或死亡后消失) \n\n'
'此技能可随时关闭，关闭时：\n'
'⓵ 自身每有 1 个金果 \n'
'⇒ 该回合 + 3 Combo (最多 + 12 Combo) \n'
'⓶ 若自身有 4 个金果 \n'
'⇒ 该回合所有成员的攻击无视“攻前盾” \n',
'eng_act':'Fruit of Poison CD6 \n\n'
'I. Golden Fruit of All “Innocent Temptation - Eve” +1 each Round. \n'
'II. If the Leader & Ally are “Origin of All Sins - Eve”, \n'
'⇒ Forbidden Fruit of All “Origin of All Sins - Eve” +1 each Round. \n'
'III. Extend Runestone-moving time regardlessly by 1.5 seconds. \n'
'IV. Damage of Demons can overpower Earth enemies. \n'
'V. If there are ≥2 Demons in the Team, \n'
'⇒ Attack bonus +40% for Ex.Combo or Combo made. (the Skill stays in play until deactivation or defeated) \n'
'This Skill can be deactivated anytime. Upon deactivation of the Skill: \n'
'⓵ For every Golden Fruit the Monster has, \n'
'⇒ Combo count +3 this Round (max +12). \n'
'⓶ If the Monster has 4 Golden Fruits, \n'
'⇒ Damage of the Team will be dealt regardless of Initial Shield this Round.',
'chi_lead':'致命的娇媚 \n\n'
'I. 魔族及妖精类攻击力 6 倍 \n'
'II. 其他属性符石兼具 50% 水符石效果 \n'
'III. 每回合回复相等于队中所有“澜漫勾惑 ‧ 夏娃”及“魔性原罪 · 夏娃”攻击力基值总和的生命力(需消除符石)',
'eng_lead':'Deadly Temptation \n\n'
'I. Demon & Elf Attack x 6. \n'
'II. All Attributive Runestones also possess 50% effect of Water Runestones. \n'
'III. Recover HP as much as the total Attack basic value of “Innocent Temptation - Eve” and "Origin of All Sins - Eve" in the Team each Round (dissolving Runestones is necessary).',
'chi_team':'队伍技能： \n\n'
'“炙烈熔岩 ‧ 克鲁非” \n'
'⓵ 生命力及攻击力 2 倍 \n'
'⓶ 技能 CD -1 \n\n'
'发动条件： \n'
'以“炙烈熔岩 ‧ 克鲁非”及；“魔性原罪 · 夏娃”或“澜漫勾惑 ‧ 夏娃”作成员 \n\n'
'I. 每消除 1 组 ≥4 粒符石 \n'
'⇒“澜漫勾惑 ‧ 夏娃”获得 1 个金果 \n'
'⇒ 每回合最多可获 2 个 \n'
'II.“澜漫勾惑 ‧ 夏娃” \n'
'⇒ 最多可同时持有 4 个金果 \n'
'III. 持有 4 个金果的“澜漫勾惑 ‧ 夏娃” \n'
'⇒ 攻击力 1.5 倍 \n'
'IV. 于“澜漫勾惑 ‧ 夏娃”直行首批消除 1 组 ≥5 粒水符石 \n'
'⓵ 根据最左方的“澜漫勾惑 ‧ 夏娃”所持金果数量 \n'
'⇒ 所有“澜漫勾惑 ‧ 夏娃”追打相应次数的水属性攻击 1 次 \n'
'⓶ 消耗所有金果 \n\n'
'发动条件： \n'
'以“澜漫勾惑 ‧ 夏娃”作成员 \n\n'
'I. 进入关卡后 \n'
'⓵ 所有“魔性原罪 · 夏娃” 、\n'
'⇒ 获得 2 个禁果 \n'
'⓶ 所有“澜漫勾惑 ‧ 夏娃” \n'
'⇒ 获得 2 个金果 \n'
'II.“魔性原罪 · 夏娃”及“澜漫勾惑 ‧ 夏娃” \n'
'⇒ 攻击力基值提升 1,500 点\n\n'
'发动条件： \n'
'以“魔性原罪 · 夏娃”作队长及战友，以“澜漫勾惑 ‧ 夏娃”作成员 \n\n'
'组合技能：魔契 \n'
'I. 引爆场上所有符石 \n'
'⇒ 掉落固定版面的魔族符石 \n'
'3 回合内 \n'
'II. 增加 9 连击 (Combo) \n'
'III. 将“魔权在握 ‧ 巴力”及“澜漫勾惑 ‧ 夏娃”直行符石转化为 \n'
'⇒ 魔族符石 \n'
'IV. 若队长为“魔权在握 ‧ 巴力” \n'
'⇒ 刷新护盾 \n\n'
'发动条件： \n'
'以“魔权在握 ‧ 巴力”及“澜漫勾惑 ‧ 夏娃”作成员(召唤兽等级达 50 或以上) ',
     'eng_team':'Team Skill: \n\n'
'“Diabolic Magma - Cherufe“ \n'
'⓵ HP & Attack x 2. \n'
'⓶ Skill CD -1. \n\n'
'Condition: \n'
'There are “Diabolic Magma - Cherufe“ and “Origin of All Sins - Eve“ or “Innocent Temptation - Eve“ in the Team. \n\n'
'I. For every group of ≥4 Runestones dissolved, \n'
'⇒ “Innocent Temptation - Eve“ gets a Golden Fruit, \n'
'⇒ to the max 2 Golden Fruits each Round. \n'
'⇒ to the max 2 Golden Fruits each Round. \n'
'II. “Innocent Temptation - Eve“ can possess at most 4 Golden Fruits at a time. \n'
'III. For “Innocent Temptation - Eve“ who has 4 Golden Fruits, \n'
'⇒ Attack x 1.5. \n'
'IV. By dissolving a group of ≥5 Water Runestones in the column below “Innocent Temptation - Eve“ in the first batch: \n'
'⓵ Based on the number of Golden Fruits held by the first “Innocent Temptation - Eve“ from the left, \n'
'⇒ all “Innocent Temptation - Eve” launches a corresponding extra Water attack(s). \n\n'
'⓶ All Golden Fruits will be consumed. \n\n'
'Condition: \n'
'There is “Innocent Temptation - Eve“ in the Team. \n\n'
'I. After entering a Stage: \n'
'⓵ All “Origin of All Sins - Eve” get 2 Forbidden Fruits. \n'
'⓶ All “Innocent Temptation - Eve” get 2 Golden Fruits. \n'
'II. “Origin of All Sins - Eve” and “Innocent Temptation - Eve“ \n'
'⇒ Attack basic value +1,500. \n'
'The Leader and Ally are “Origin of All Sins - Eve”, with “Innocent Temptation - Eve“ in the Team. \n\n'
'Combine Skill: Pact of Demons \n'
'I. Explode all Runestones \n'
'⇒ to generate Demon Runestones at fixed positions. \n'
'For 3 Rounds, \n'
'II. Combo count +9. \n'
'III. Turn the columns below “Absolute Authoritarian - Baal” and “Innocent Temptation - Eve” into Demon Runestones. \n'
'IV. If the Leader is “Absolute Authoritarian - Baal”, \n'
'⇒ refresh the protective shield.\n\n'
'Condition: \n'
'There are "Absolute Authoritarian - Baal" and "Innocent Temptation - Eve" in the Team (the Monsters must reach Lv. 50 or above). '},
    {'chi_name':'巴力',
'chif_name':'巴力',
'eng_name':'baal',
'chi_act':'魔鬼的代号 CD 7 \n\n'
'I. 对敌方全体造成 \n'
'⇒ 6,666 万无属性伤害(此伤害无视敌人防御力、“强化突破”、“攻前盾”) \n'
'1 回合内 \n'
'II. 自身攻击力提升至 6,666 \n'
'III.“魔权在握 ‧ 巴力”的攻击 \n'
'⇒ 无视“符石连击零化”、“指定连击法印” \n'
'IV. 若队长为“魔权在握 ‧ 巴力” \n'
'⇒ 刷新护盾 \n',
'eng_act':'666 the Demon CD7 \n\n'
'I. Deal 66.66-million non-Attributive Damage to all enemies regardless of Defense, Enchanted Runestone Shield and Initial Shield. \n'
'For 1 Round, \n'
'II. Monster’s Attack increases to 6,666. \n'
'III. Damage of “Absolute Authoritarian - Baal” will be dealt regardless of Runestone Combo Nullifying and Combo Seal. \n'
'IV. If the Leader is “Absolute Authoritarian - Baal”, \n'
'⇒ refresh the protective shield. ',
'chi_lead':'御天之志 \n\n'
'I. 自身属性攻击力 6 倍、生命力及回复力 1.8 倍 \n'
'II. 每经过一层 (Wave) \n'
'⇒ 全队攻击力额外提升 \n'
'⇒ 最多 3 倍 \n'
'III. 每次直行消除 1 组 ≥4 粒符石 \n'
'⇒ 全队攻击力额外 1.2 倍 \n'
'⇒ 最多可提升 4 次 \n',
'eng_lead':'Crowned Power \n\n'
'I. Attack of the Monster\'s Attribute x 6; HP & Recovery x 1.8. \n'
'II. For every Wave passed, \n'
'⇒ Team Attack increases additionally, \n'
'⇒ to the max x 3. \n'
'III. Every time a group of ≥4 Runestones is dissolved in a column, \n'
'⇒ Team Attack x 1.2 additionally, \n'
'⇒ to the max increasing Team Attack for 4 times. \n',
'chi_team':'队伍技能： \n'
'I. 必然延长移动符石时间 2 秒 \n'
'II. 最左方的“全知的恶魔 · 拉普拉斯” \n'
'⇒ 攻击力基值提升 1,000 点 \n\n'
'发动条件： \n'
'以“魔权在握 ‧ 巴力”及“全知的恶魔 · 拉普拉斯”作成员 \n\n'
'队伍技能： \n'
'队中每有 1 个魔族成员 \n'
'⇒ 获得 10,000 点护盾 \n'
'II. 若队中全为魔族成员 \n'
'⇒ 则可获得 66,666 点护盾 \n\n'
'发动条件： \n'
'以“魔权在握 ‧ 巴力”作队长 \n\n'
'队伍技能： \n'
'所有成员的属性转换为 \n'
'⇒ 左方起第 2 位成员的属性 \n\n'
'发动条件： \n'
'以“魔权在握 ‧ 巴力”作队长，且队中有 6 个魔族成员 \n\n'
'队伍技能： \n'
'I. “魔权在握 ‧ 巴力”、“澜漫勾惑 ‧ 夏娃”、“全知的恶魔 · 拉普拉斯” \n'
'⇒ 攻击力基值跟随攻击力基值最高(不包括受主动技能影响的基值)的魔族成员 \n'
'II. 每回合移动符石后，可点选 1 粒符石 \n'
'⇒ 将该符石直行及横行的符石引爆 \n'
'⇒ 掉落所点选的魔族符石 \n'
'III. 消除 ≥5 粒水、火或木符石时 \n'
'⓵ 魔族攻击力 1.5 倍 \n'
'⓶ 魔族成员无视“指定形状盾” \n'
'IV. 消除 ≥5 粒光、暗或心符石时 \n'
'⓵ 魔族攻击力 1.5 倍 \n'
'⓶ 魔族成员无视“固定连击盾” \n'
'V. 减少 25% 所受伤害 \n'
'VI. 受敌人反击伤害减少 85% \n'
'VII. 必然延长移动符石时间 2 秒 \n\n'
'发动条件： \n'
'以“魔权在握 ‧ 巴力”作队长及战友 \n\n'
'组合技能：魔劫 \n\n'
'I. 移除场上所有符石 \n'
'⇒ 掉落固定版面的魔族强化符石 \n'
'3 回合内 \n'
'II.“魔权在握 ‧ 巴力”及“全知的恶魔 · 拉普拉斯” \n'
'⓵ 追打 2 次 \n'
'⓶ 无视五属盾 \n'
'⓷ 不会被封锁主动技能 \n'
'III.若队长为“魔权在握 ‧ 巴力” \n'
'⇒ 刷新护盾 \n\n'
'发动条件：\n'
'以“全知的恶魔 ‧ 拉普拉斯”及“魔权在握 ‧ 巴力”作成员 \n'
'(召唤兽等级达 50 或以上) \n\n'
'组合技能：魔契 \n\n'
'I. 引爆场上所有符石 \n'
'⇒ 掉落固定版面的魔族符石 \n'
'3 回合内 \n'
'II. 增加 9 连击 (Combo) \n'
'III. 将“魔权在握 ‧ 巴力”及“澜漫勾惑 ‧ 夏娃”直行符石转化为 \n'
'⇒ 魔族符石 \n'
'IV. 若队长为“魔权在握 ‧ 巴力” \n'
'⇒ 刷新护盾 \n\n'
'发动条件： \n'
'以“魔权在握 ‧ 巴力”及“澜漫勾惑 ‧ 夏娃”作成员(召唤兽等级达 50 或以上',
'eng_team':'Team Skill: \n'
'I. Extend Runestone-moving time regardlessly by 2 seconds. \n'
'II. Attack basic value of the leftmost "Demon of Omniscience - Laplace" +1,000. \n\n'
'Condition: \n'
'There are “Absolute Authoritarian - Baal“ and “Demon of Omniscience - Laplace" in the Team. \n\n'
'Team Skill: \n'
'I. For each Demon present in the Team, \n'
'⇒ acquire a protective shield of 10,000. \n'
'II. If the Team has all Demons, \n'
'⇒ acquire a protective shield of 66,666. \n\n'
'Condition: \n'
'The Leader is "Absolute Authoritarian - Baal". \n\n'
'Team Skill: \n'
'The Attributes of the Team will be changed into that of the 2nd Member from the left. \n\n'
'Condition: \n'
'The Leader is "Absolute Authoritarian - Baal" and there are 6 Demons in the Team. \n\n'
'Team Skill: \n'
'I. “Absolute Authoritarian - Baal“, “Innocent Temptation - Eve“ and “Demon of Omniscience - Laplace” \n'
'⇒ Attack basic value will synchronize with that of the Demon Member that has the highest Attack (effects of Active Skills are not counted). \n'
'II. Upon the completion of moving Runestones each Round, tap a Runestone \n'
'⇒ to explode the column and row of that Runestone \n'
'⇒ to generate the selected Demon Runestones. \n'
'III. By dissolving ≥5 Water, Fire or Earth Runestones, \n'
'⓵ Demon Attack x 1.5. \n'
'⓶ Damage of Demons will be dealt regardless of Puzzle Shield. \n'
'IV. By dissolving ≥5 Light, Dark or Heart Runestones, \n'
'⓵ Demon Attack x 1.5. \n'
'⓶ Damage of Demons will be dealt regardless of Fixed Combo Shield \n'
'V. Damage received -25%. \n'
'VI. Damage reflected from enemies -85%. \n'
'VII. Extend Runestone-moving time regardlessly by 2 seconds. \n\n'
'Condition: \n'
'The Leader and Ally are “Absolute Authoritarian - Baal“ \n\n'
'Combine Skill: Calamity of Demons \n'
'I. Remove all Runestones  \n'
'⇒ to generate Enchanted Demon Runestones at fixed positions. \n'
'For 3 Rounds, \n'
'II. “Absolute Authoritarian - Baal” & “Demon of Omniscience - Laplace”: \n'
'⓵ Launch 2 extra attacks. \n'
'⓶ Damage will be dealt regardless of Quintet Elemental Shield. \n'
'⓷ Active Skills will not be locked. \n'
'III. If the Leader is “Absolute Authoritarian - Baal”, \n'
'⇒ refresh the protective shield. \n\n'
'Condition: \n'
'There are "Demon of Omniscience - Laplace" and "Absolute Authoritarian - Baal" in the Team (the Monsters must reach Lv. 50 or above). \n\n'
'Combine Skill: Pact of Demons \n'
'I. Explode all Runestones \n'
'⇒ to generate Demon Runestones at fixed positions. \n'
'For 3 Rounds, \n'
'II. Combo count +9. \n'
'III. Turn the columns below “Absolute Authoritarian - Baal” and “Innocent Temptation - Eve” into Demon Runestones. \n'
'IV. If the Leader is “Absolute Authoritarian - Baal”, \n'
'⇒ refresh the protective shield. \n'
'Condition: \n'
'There are "Absolute Authoritarian - Baal" and "Innocent Temptation - Eve" in the Team (the Monsters must reach Lv. 50 or above). '},
    {'chi_name':'虹伶',
'chif_name':'虹伶',
'eng_name':'hongling',
'chi_act':'燃解心锁 CD8 \n\n'
'I. 解除火属性成员被封锁的技能 (此技能无视封锁技能) \n'
'2 回合内 \n'
'II. 心符石的掉落率降至 0，并将原有几率增加至火符石的掉落率 \n'
'III. 所有符石兼具 50% 火符石效果',
'eng_act':'Fiery Heart Unlocked CD8 \n\n'
'I. Release the locked Skills of all Fire Members (this Skill will not be locked). \n'
'For 2 Rounds \n'
'II. Drop rate of Heart Runestones will be transferred to that of Fire Runestones. \n'
'III. All Runestones also possess 50% effect of Fire Runestones. \n',
'chi_lead':'虹女之焰 \n\n'
'I. 全队攻击力 3.2 倍 \n'
'II. 队伍中火属性成员愈多 \n'
'⇒ 火属性攻击力及回复力额外提升愈多\n'
'⇒ 6 个可达至最大 2.8 倍',
'eng_lead':'Rings of Flames \n\n'
'Team Attack x 3.2. The more the Fire Members in the Team, the higher the Fire Attack & Recovery, to the max x 2.8 for 6 Fire Members.',
'chi_team':'队伍技能： \n'
'I. 将移动符石时触碰的火符石转化为火人族强化符石 \n'
'II. 火属性成员的生命力提升 1500 点 \n'
'III. 无视“燃烧”敌技 \n'
'IV. 火符石兼具 50% 心符石效果 \n'
'V. 必然延长移动符石时间 2 秒 \n\n'
'发动条件： \n'
'以喵喵大将军 ‧ 虹伶作队长及战友 \n\n'
'队伍技能： \n'
'I. 于回合结束时，最左方的“罪与责之承诺 ‧ 美狄亚”直行的符石转化为火人族符石 \n'
'II. “罪与责之承诺 ‧ 美狄亚”的主动技能“喋血战意”变为“喋血战意・虹”，移除“受到的伤害提升 1.5 倍”的效果 \n\n'
'发动条件： \n'
'以“喵喵大将军 ‧ 虹伶”作队长及战友，并以“罪与责之承诺 ‧ 美狄亚”作队员 \n',
'eng_team':'Team Skill: \n'
'I. Turn all Fire Runestones touched while moving into Enchanted Human Runestones. \n'
'II. Monster\'s HP of each Fire Member +1500 additionally. \n'
'III. Boss Skill "Burning" will be nullified. \n'
'IV. Fire Runestones also possess 50% effect of Heart Runestones. \n'
'V. Extend Runestone-moving time regardlessly by 2 seconds. \n\n'
'Condition: \n'
'Both the Leader and Ally are "General Meow - Hongling". \n\n'
'Team Skill: \n'
'I. Turn the column of Runestones below the first "Sin Atoner - Medea" from the left into Fire Human Runestones at the end of each Round. \n'
'II. Change the Active Skill of "Sin Atoner - Medea" from "Blood-stained Morale" to "Blood-stained Morale - EX". The effect of Damage received x 1.5 will be removed. \n\n'
'Condition: \n'
'Both the Leader and Ally are "General Meow - Hongling", with "Sin Atoner - Medea" as a Team Member. '},
{'chi_name':'弗丽嘉',
'chif_name':'弗麗嘉',
'eng_name':'frigg',
'chi_act':'天地之掌 CD6 \n\n'
'队长需为神族才可发动此技能： \n'
'1 回合内，敌方全体转为自身克制的属性；效果期间全队攻击力 1.8 倍及必然延长移动符石时间 2 秒。若队长为北欧神系列角色，回合结束时，自身技能 CD 减少 5 ',
'eng_act':'Palm of the World CD6 \n\n' 
'This Skill can be activated only when the Leader is God.  \n'
'For 1 Round, change the Attribute of all enemies into the Monster\'s Counter Attribute; when the effect is in play, Team Attack x 1.8; extend Runestone-moving time regardlessly by 2 seconds. If the Leader is a Monster of "Norse Gods", the Monster\'s current Skill CD -5 at the end of the Round. ',
'chi_lead':'神界之念 \n\n'
'I. 全队攻击力 5 倍 \n'
'II. 队伍中有 5 种属性成员时 \n'
'⇒ 全队攻击力及回复力额外 2 倍 ',
'eng_lead':'The Norse Notion \n\n'
'When the Team consists of only Gods, Team Attack x 5; when there are 5 Attributes in the Team, Team Attack & Recovery x 2 additionally.',
'chi_team':'队伍技能： \n'
'永恒碑纹 ‧ 主神奥丁、众生天命 ‧ 主神奥丁及弗丽嘉转换为队长的属性 \n\n'
'发动条件： \n'
'以相同属性的 8 星究极北欧神系列角色作队长及战友 \n\n'
'队伍技能： \n'
'弗丽嘉自身的生命力提升 2 倍 \n\n'
'发动条件： \n'
'以相同属性的 8 星究极北欧神系列角色作队长及战友，并以弗丽嘉作队员',
'eng_team':'Team Skill: \n'
'Attribute of "Gungnir of Runes - Odin the Allfather", "Odin the Fated Savior of All" and "Frigg" will synchronize with that of the Leader. \n\n'
'Condition: \n'
'The Leader and Ally are 8* Monsters of "Norse Gods" of the same Attribute. \n\n'
'Team Skill: \n'
'HP of "Frigg" x 2 additionally. \n\n'
'Condition: \n'
'The Leader and Ally are 8* Monsters of "Norse Gods" of the same Attribute, with "Frigg" as a Team Member. '},
    {'chi_name':'莎娜',
'chif_name':'莎娜',
'eng_name':'zana',
'chi_act':'元素的音韵 CD7 \n\n',
'I. 12 秒内，可任意移动符石而不会发动消除 \n'
'1 回合内 \n'
'II. 将首次移动符石时触碰的符石 \n'
'⇒ 转化为木妖族强化符石 \n'
'III. 木属性及妖精类成员攻击力 2 倍 \n'
'IV. 木属性及妖精类成员的攻击 \n'
'⇒ 无视“三属盾”及“五属盾”敌技',
'eng_act':'Melodic Tunes of Runes CD7 \n\n'
'I. Unlimited Runestone movement in 12 seconds without dissolving. \n'
'For 1 Round: \n'
'II. Turn the Runestones touched while moving at first into Enchanted Earth Elf Runestones. \n'
'III. Earth Attack & Elf Attack x 2. \n'
'IV. Earth & Elf Damage will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield.',
'chi_lead':'妖灵之音 \n\n'
'I. 全队攻击力 4.5 倍、生命力及回复力 1.3 倍 \n'
'II. 所有属性符石 \n'
'⇒ 兼具 50% 心符石效果 ',
'eng_lead':'Melodies of Elfish Spirits \n\n'
'When the Team consists of only Elves: \n'
'I. Team Attack x 4.5; HP & Recovery x 1.3. \n'
'II. All Attributive Runestones also possess 50% effect of Heart Runestones. ',
'chi_team':'队伍技能： \n\n'
'奏响世界之音 ‧ 莎娜”的生命力、攻击力、回复力增加 1000 点 \n\n'
'发动条件： \n'
'以“奏响世界之音 ‧ 莎娜”作成员，且队中只有妖精类成员',
'eng_team':'Team Skill: \n'
'HP, Attack & Recovery of "Resonance of the World - Zana" +1000. \n\n'
'Condition: \n'
'The Team consists of only Elves, with "Resonance of the World - Zana" as a Team Member. '}
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
