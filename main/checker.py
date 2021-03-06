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
'chi_team':'队伍技能：\n'
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
'chi_team':'队伍技能：\n'
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
'chi_act':'王之剑 ‧ 誅 CD7\n'
'將所有符石分別轉化為直行\n'
'「光、火、木、水、暗、心」 \n'
'強化符石\n\n'
'王之劍 ‧ 弑 CD7\n'
'1 回合内消除水符石时\n'
'I. 消除水符石時\n'
'⇒ 減少 85% 所受傷害\n'
'II. 消除火符石時\n'
'⓵ 全隊無視敵人防禦力\n'
'⓶ 個人追打火屬性攻擊 2 次\n'
'III. 消除木符石時\n'
'⇒ 回復 100,000 點生命力\n'
'IV. 同時消除水、火及木符石\n'
'⓵ 全隊攻擊力 2.5 倍\n'
'⓶ 全隊無視「攻前盾」\n',
'eng_act':'King\'s Sword - Execution CD7\n'
'Turn all Runestones into Enchanted Runestones of "Light, Fire, Wood, Water, Darkness, Heart" running straight. \n\n'
'King\'s Sword - Murder CD7\n'
'For 1 Round \n'
'I. When water runestones are dissolved \n'
'⇒ 85% of damage taken \n'
'II. When fire runestones are dissolved \n'
'⓵ The whole team ignores the enemy\'s defense \n'
'⓶ Individual pursuit fire attack twice \n'
'III. When wood runestones are dissolved \n'
'⇒ 100,000 Point HP \n'
'IV. Dissolve Water, Fire and Wood Runestones at the same time \n'
'⓵ Team Attack Power 2.5 times \n'
'⓶ All team ignores "Attack Front Shield"',
'chi_lead':'聖劍絕殺\n\n'
'隊中只有光屬性人類及【圓桌騎士】成員時：\n'
'I. 全隊攻擊力 7 倍、\n'
'生命力及回復力 1.8 倍\n'
'II. 其他符石分別兼具\n'
'⇒ 50% 光及心符石效果\n'
'III. 每首批全部消除\n'
'場上 1 種符石時\n'
'⇒ 全隊攻擊力額外 1.35 倍\n'
'IV. 每消除 1 組光以外的符石\n'
'⇒ 額外計算多 1 Combo\n'
'⇒ 最多可增加 4 Combo',
'eng_lead':'holy sword lore\n\n'
'When there are only Light Humans and [Knights of the Round Table] in the team: \n'
'I. Team Attack 7 times,HP and Recovery 1.8 times \n'
'II. Other Runestones have both \n'    
'⇒ 50% of Light and Heart Runestones\n'
'III. When all 1 type of Runestones are dissolved on the field \n'
'⇒ the team\'s attack power is increased by 1.35 times \n'
'IV. For each group of Runestones dissolved other than Light \n'
'⇒ 1 extra Combo is calculated \n'
'⇒ Up to 4 Combos can be added',
'chi_team':'队伍技能：\n'
'I. 必然延長移動符石時間 5 秒\n'
'II. 觸碰電擊符石時仍可移動符石\n'
'III. 無視「黏腐」敵技\n'
'IV. 無視「燃燒」敵技\n'
'V.【圓桌騎士】成員\n'
'⓵ 轉換為隊長的屬性\n'
'⓶ 技能 CD -1\n'
'⓷ 以 50% 攻擊力追打\n'
'自身原屬性攻擊 1 次\n'
'VI. 以【十】形\n'
'首批消除 1 組 ≥5 粒符石\n'
'⇒ 暈擊敵方全體，\n'
'使受影響目標無法行動 1 回合\n'
'(每層最多觸發 1 次)\n'
'VII. 回合結束時，\n'
'將 1 個角落的 3 粒符石\n'
'⇒ 轉化為光人族強化符石\n'
'(屬性符石優先轉換)\n'
'VIII. 於移動並消除符石後\n'
'⇒ 引爆所有光符石\n'
'⇒ 直至場上沒有光符石\n'
'IX. 上述若有引爆光符石\n'
'⇒ 全隊攻擊力 2.5 倍\n'
'X. 消除人族符石\n'
'⇒ 全隊攻擊力額外 2.5 倍\n\n'
'發動條件：\n'
'以「榮聲披身 ‧ 亞瑟」作隊長及戰友',
'eng_team':'Team Skills: \n'
'◆ Extend Runestone-moving time regardlessly by 5 seconds.\n'
'◆ Runestone movement will not be stopped when an Electrified Runestone is touched.\n'
'◆ Boss Skills "Sticky" and "Burning" will be nullified.\n'
'◆ Each Member of 【Knights of the Round Table】:\n'
'⓵ Synchronizes its Attribute with that of the Leader.\n'
'⓶ Skill CD -1.\n'
'⓷ Launches an extra attack of its original Attribute as much as 50% of its Attack.\n'
'◆ By dissolving a group of ≥5 Runestones in the shape of【十】 in the first batch,\n'
'⇒ stun all enemies to inactivate them for 1 Round (once only within the Wave).\n'
'◆ At the end of the Round,\n'
'turn 3 Runestones in a corner into Enchanted Light Human Runestones.\n'
'(Attributive Runestones rank first in priority)\n'
'◆ Upon the completion of moving and dissolving Runestones,\n'
'⇒ explode all Light Runestones until there is no more Light Runestone.\n'
'◆ If Light Runestones are exploded,\n'
'⇒ Team Attack x 2.5.\n'
'◆ By dissolving Human Runestones,\n'
'⇒ Team Attack x 2.5 additionally.\n\n'
'Condition:\n'
'Both the Leader and Ally are Illustrious Laurels - Arthur'},

{'chi_name':'兰斯洛特',
 'chif_name':'蘭斯洛特',
 'eng_name':'lancelot',
     
'chi_act':'暗黑之劍氣 ‧ 魔息 CD5\n'
'I. 引爆水符石\n'
'⇒ 掉落暗強化符石\n'
'II. 引爆光符石\n'
'⇒ 掉落心強化符石\n'
'III. 回合結束時，將本回合所消除強化符石的數量等值的符石轉化為\n'
'⇒ 暗魔族強化符石\n'
'(水及光符石優先轉換)\n\n'
'銳劍出鞘 ‧ 破攻  CD5\n'
'I. 每回合自身攻擊力持續提升\n'
'⇒ 最大 5 倍\n'
'II. 自身無視「攻前盾」\n'
'效果持續至自身沒有發動攻擊',
     
'eng_act':'Dark Power of Blade - Ex CD5\n'
'I. Explode Water Runestones to generate Enchanted Dark Runestones. \n'
'II. Explode Light Runestones to generate Enchanted Heart Runestones. \n'
'III. At the end of the Round, \n'
'turn Runestones into Enchanted Dark Demon Runestones of a number same as that of the Enchanted Runestones dissolved in the Round (Water and Light Runestones rank first in priority).\n\n'
'Sword Unsheathing - Ex CD5\n'
'I. The Character\'s Attack continues to increase each Round, to the max x 5. \n'
'II. The Character\'s Damage will be dealt regardless of Initial Shield. \n'
'The Skill stays in play until no attack is launched by the Character.',

'chi_lead':'騎士之盟\n\n'
'隊伍中只有火、木及暗屬性成員時：\n'
'I. 全隊攻擊力 6.5 倍、\n'
'生命力及回復力 1.3 倍\n'
'II. 消除心符石時\n'
'⇒ 全隊攻擊力額外 2.5 倍\n'
'III. 消除強化符石時\n'
'⇒ 自身攻擊力額外 1.5 倍\n',
     
'eng_lead':'League of Knights \n\n'
'When the Team has only Fire, Earth or Dark Members: \n'
'I. Team Attack x 6.5; HP & Recovery x 1.3. \n'
'II. By dissolving Heart Runestones, \n'
'⇒ Team Attack x 2.5 additionally. \n'
'III. By dissolving Enchanted Runestones, \n'
'⇒ the Character’s Attack x 1.5 additionally.',
     
'chi_team':'隊伍技能：\n\n'
'I. 必然延長移動符石時間 3 秒\n'
'II. 火、木、暗符石互相兼具效果\n'
'III. 火、木、暗符石兼具\n'
'⇒ 25% 心符石效果\n'
'IV. 心符石兼具\n'
'⇒ 火、木、暗符石效果\n'
'V. 消除 ≥4 種符石\n'
'⇒ 所有成員追打被克屬性攻擊 1 次\n'
'VI. 將移動符石時觸碰的火、木、暗符石\n'
'⇒ 轉化為強化符石\n'
'VII. 同時消除火、木及暗符石\n'
'⇒「逐光暗徒．蘭斯洛特」\n'
'無視「三屬盾」及「五屬盾」\n\n'
'發動條件：\n'
'以「逐光暗徒．蘭斯洛特」作隊長及戰友',
     
'eng_team':'Team Skill: \n\n'
    '◆ Extend Runestone-moving time regardlessly by 3 seconds. \n'
    '◆ Fire, Earth and Dark Runestones also possess the effect of each other. \n'
    '◆ Fire, Earth and Dark Runestones also possess 25% effect of Heart Runestones. \n'
    '◆ Heart Runestones also possess the effect of Fire, Earth and Dark Runestones. \n'
    '◆ By dissolving ≥4 types of Runestones, each Member launches an extra attack of its Weakness Attribute. \n'
    '◆ Turn the Fire, Earth and Dark Runestones touched while moving into Enchanted Runestones. \n'
    '◆ By dissolving Fire, Earth and Dark Runestones in the same Round, \n'
    '⇒ Damage of “Light Chaser - Lancelot” will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield. \n\n'
    'Condition: \n'
    'Both the Leader and Ally are Light Chaser - Lancelot '},
    
    {'chi_name':'梅林',
'chif_name':'梅林',
'eng_name':'merlin',
     
'chi_act':'	治癒之賦 ‧ 五屬追擊 CD6\n\n'
'1 回合內\n'
'I. 隊伍成員的屬性愈多\n'
'⇒ 全隊攻擊力及回復力愈高\n'
'最大 3.5 倍\n'
'II. 當隊中所有成員的回復力基值相同\n'
'⓵ 個人追打五屬攻擊各 1 次\n'
'⓶ 所有成員追打暗屬性攻擊 1 次\n'
'⓷ 全隊對敵方造成攻擊傷害的 5%\n'
'⇒ 轉化為生命力',
     
'chi_lead':'暗黑回復魔法 ‧ 魅\n\n'
'I. 妖精類攻擊力及回復力 6.5 倍、生命力 1.5 倍\n'
'II. 每直行首批消除 1 組 ≥4 粒符石\n'
'⇒ 該直行產生 1 粒心強化符石\n'
'III. 回合結束時\n'
'⇒ 將心符石轉化為妖族強化符石\n',

'chi_team':'隊伍技能：\n'
'I. 必然延長移動符石時間 3 秒\n'
'II. 心符石兼具 300% 屬性符石效果\n'
'III. 每有 1 直行首批消除\n'
'1 組 ≥4 粒符石\n'
'⇒ 全隊攻擊力提升\n'
'⇒ 6 直行可達至最大 7 倍\n'
'IV. 直行首批消除 1 組 ≥4 粒符石\n'
'⇒ 該直行產生 2 粒心強化符石\n'
'(主動技能 - 結界術 ‧ 玄光、結界術 ‧ 幽冥將不能發動)\n'
'V. 觸碰心符石時\n'
'⇒ 解除其電擊、凍結、弱化、化血、石化符石狀態\n'
'⇒ 添加為妖族符石\n'
'VI. 無視「黏腐」敵技\n'
'VII. 消除心符石時\n'
'⇒ 減少 50% 所受傷害\n\n'
'發動條件：\n'
'以「幻域真我．梅林」作隊長及戰友\n\n'
'隊伍技能：\n'
'所有成員的回復力基值跟隨回復力基值最高的成員\n\n'
'發動條件：\n'
'以「幻域真我．梅林」及 ≥3 個妖精類作成員',
     
     'eng_act':'Recovery Talent - Quintet Attack CD 6 \n'
     'For 1 Round: \n'
     'I. The more Attributes in the Team, \n'
     '⇒ the higher the Team Attack and Recovery, to the max x 3.5. \n'
     'II. When all Members in the Team has the same Recovery basic value: \n'
     '⓵ The Character launches 5 extra attacks (one Attribute each).\n'
     '⓶ Each Member launches an extra Dark attack.\n'
     '⓷ 5% of Attack-damage dealt to enemies by the Team will be converted to HP Recovery.',
     
     'eng_lead':'Dark Magic of Recovery - EX \n\n'
     'I. Elf Attack & Recovery x 6.5; HP x 1.5. \n'
     'II. If a group of ≥4 Runestones is dissolved in a column in the first batch, \n'
     '⇒ 1 Enchanted Heart Runestone will be generated in that column. \n'
     'III. At the end of the Round, \n'
     '⇒ turn Heart Runestones into Enchanted Elf Runestones. ',
     
     'eng_team':'Team Skill: \n'
     '◆ Extend Runestone-moving time regardlessly by 3 seconds. \n'
     '◆ Heart Runestones also possess 300% effect of Attributive Runestones \n'
     '◆ For every group of ≥4 Runestones dissolved in a column in the first batch, \,'
     '⇒ Team Attack increases \n'
     '⇒ to the max x 7 for 6 columns. \n'
     '◆ If a group of ≥4 Runestones is dissolved in a column in the first batch, \n'
     '⇒ 2 Enchanted Heart Runestones will be generated in that column. \n'
     '(Active Skills "Magical Stage - Beam" and "Magical Stage - Gloom" cannot be activated) \n'
     '◆ If Heart Runestones are touched, \n'
     '⇒ clear their negative state of Electrified Runestones, Frozen Runestones, Weakened Runestones, Lock-for-Recovery Runestones and Petrified Runestones, \n'
     '⇒ and modify them to become Elf Runestones. \n'
     '◆ Boss Skill “Sticky” will be nullified. \n'
     '◆ By dissolving Heart Runestones, \n'
     '⇒ Damage received -50%. \n\n'
     'Condition: \n'
     'Both the Leader and Ally are Illusionist\'s Anima - Merlin.'},


    
    
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
'chi_team':'队伍技能：\n'
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
'chi_team':'队伍技能：\n'
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
    
{'chi_name':'天猫座',
'chif_name':'天貓座',
'eng_name':'lynx',

'chi_act':'天降夜露 CD7\n\n'
'1 回合内\n'
'I. 移动符石后首批掉落的符石必定为暗符石\n'
'II. 无视固定连击盾\n'
'III. 若队长及战友均为兽类成员\n'
'⇒ 自身 CD - 2',

'eng_act':'Drops of Daybreak Dew CD7\n\n'
'For 1 Round:\n'
'I. The first batch of Runestones to be dropped will be Dark Runestones.\n'
'II. Damage will be dealt regardless of Fixed Combo Shield.\n'
'III. If the Leader and Ally are Beasts,\n'
'⇒ Skill CD of the Monster -2.',

'chi_lead':'紫魅断魂 ‧ 强\n\n'
'I. 队伍中只有兽类成员时：\n'
'⇒ 全队攻击力 5 倍及生命力 1.2 倍\n'
'II. 每消除 ≥3 种符石时 (不计重复)\n'
'⇒ 掉落 1 粒暗兽族强化符石',

'eng_lead':'Purple Shadow of Assassination - EX\n\n'
'When the Team consists of only Beasts, \n'
'Team Attack x 5 & HP x 1.2. \n'
'By dissolving 3 types of Runestones (each type will be counted once only), \n'
'1 Enchanted Dark Beast Runestone will be generated.',

'chi_team':'队伍技能：\n'
'每掉落 1 粒暗符石，回复 5 %生命力\n'
'发动条件：\n'
'以危命猎杀 ‧ 天猫座琳叩斯作队长及战友\n\n'
'队伍技能：\n'
'进入关卡后，所有成员的主动技能 CD 减少 2\n'
'发动条件：\n'
'以危命猎杀 ‧ 天猫座琳叩斯作队长及战友，且队伍中只有暗属性兽类成员',

'eng_team':'Team Skill:\n\n'
'◆ Recover 5% HP for each Dark Runestone dropped.\n'
'Condition:\n'
'Both the Leader and Ally are Fatal Hunter - Lynx.\n\n'
'Team Skill:\n'
'◆ After entering a stage, Active Skill CDs of all Members -2.\n'
'Condition:\n'
'Both the Leader and Ally are Fatal Hunter - Lynx, with only Dark Beasts in the Team.'},
    
    {'chi_name':'矢车菊',
'chif_name':'矢車菊',
'eng_name':'cornflower',

'chi_act':'逆我尽灭 CD6\n\n'
'1 回合内，全队攻击力 1.3 倍，并引爆场上所有非克制敌人属性的属性符石，以掉落敌人属性以外的符石；若队伍中只有妖精类成员时，1 回合内，连击 (Combo) 数目增加 8',
'eng_act':'Elimination of Opposition CD6\n\n'
'Team Attack x 1.3 for 1 Round. Explode all Runestones which are not of the enemy\'s Weakness Attribute to generate Runestones which are not of the enemy\'s Attribute. If the Team consists of only Elves, Combo count +8 for 1 Round.',

'chi_lead':'妖娆之蓝\n\n'
'I. 水属性及妖精类攻击力 4.5 倍\n'
'II. 消除 ≥2 组水符石时\n'
'⇒ 攻击力提升至 5 倍\n'
'III. 消除心符石时\n'
'⇒ 水属性及妖精类攻击力额外 1.5 倍\n'
'IV. 首批没有消除水符石时\n'
'⇒ 减少 35% 所受伤害',

'eng_lead':'Coils of Elfish Indigo\n\n'
'Elf Attack & Water Attack x 4.5.\n' 
'When 2 or more groups of Water Runestones are dissolved, \n'
'the Attack multiplier increases to x 5. \n'
'When Heart Runestones are dissolved, \n'
'Elf Attack & Water Attack x 1.5 additionally. \n'
'When Water Runestones are not dissolved, \n'
'Damage received -35% (only the first batch of Runestones dissolved will be counted).',

'chi_team':'队伍技能：\n'
'以回血溢出值作全体攻击，最大 10 倍\n'
'发动条件：\n'
'以噩耗元素噬者 ‧ 迪亚布罗作队长，并以 3 个或以上的 5 星或 6 星妖女系列、 6 星或 7 星玩具精灵系列的召唤兽、精灵使 ‧ 乌特博丽公主或 6 星妖娆花梦系列召唤兽作成员 (不可重复)\n\n'
'队伍技能：\n'
'当前生命力全满时，下一次所受伤害不会使你死亡 (同 1 回合只会发动 1 次)\n'
'发动条件：\n'
'以 6 星妖娆花梦系列召唤兽作队长及战友，队伍中有 3 个或以上 6 星的妖娆花梦系列召唤兽及只有妖精类成员\n\n'
'队伍技能：\n'
'将每个成员回复力基值的 2 倍\n'
'⇒ 各自加入自身攻击力基值\n'
'发动条件：\n'
'以绽放荣耀 ‧ 矢车菊作队长及战友',

'eng_team':'Team Skill:\n\n'
'◆ Recovery surplus will become a Full Attack, the largest Damage that could be dealt is 10 times of Recovery\n\n'
'Condition:\n'
'The Leader is Diablo, Nightmare Guttler of Elements, with 3 or more Elfish Perennials series 6 star, Sprites series 5 or 6 star, Toy Pixies series 6 or 7 star, or Elf Summoner - Princess Woodburyin the Team (identical Characters will only be counted as one).\n\n'
'Team Skill:\n'
'◆ When HP is full, the next Damage received will not lead to your defeat (one activation each Round).\n'
'Condition:\n'
'Both the Leader and Ally are Elfish Perennials series 6 star, with only Elves and 3 or more Elfish Perennials series 6 star in the Team.\n\n'
'Team Skill:\n'
'◆ Add 2x Recovery basic value of each Monster into its own Attack basic value.\n'
'Condition:\n'
'Both the Leader and Ally are Rekindled Honor - Cornflower.'},
    
    {'chi_name':'樱',
'chif_name':'櫻',
'eng_name':'sakura',

'chi_act':'幻樱花海 ‧ 魅 CD6\n\n'
'将火及心符石添加为妖族符石。根据本回合的连击 (Combo) 数目，下回合开始时将火及心以外的符石，转化为该数目等值的火强化符石',
'eng_act':'	Floral Sea of Sakura - EX CD6\n\n'
'Modify Fire and Heart Runestones to become Elf Runestones. Upon the Round of activation, the number of Combos made in the Round will be recorded. At the beginning of next Round, turn non-Fire and non-Heart Runestones into Enchanted Fire Runestones of a number same as the recorded number of Combos made.',

'chi_lead':'粉樱花雨\n\n'
'I. 妖精类攻击力 1.8 倍\n'
'II. 火及心符石兼具 25%\n'
'其他属性符石效果 (可叠加)\n'
'III. 2 粒火或心符石相连，即可发动消除\n'
'IV. 所有符石掉落率不受其他技能影响(包括改变掉落符石属性的技能)\n'
'V. 队伍回复力愈高，\n'
'全队攻击力额外提升愈多：\n'
'⇒ 队伍回复力达 3000 额外 2 倍\n'
'⇒ 4000 可达至最大 2.5 倍',

'eng_lead':'Floral Rain of Sakura - EX\n\n'
'I. Elf Attack x 1.8.\n'
'II. Fire and Heart Runestones also possess 25% effect of all Attributive Runestones (effects can be superimposed).\n'
'III. Fire and Heart Runestones can be dissolved by aligning 2 or more of them.\n'
'Drop rate of all Runestones will not be affected by Amelioration or Skills (including those altering the Attribute of dropping Runestones).\n'
'IV. The higher the Team Recovery, the higher the Team Attack,\n'
'⇒ starting from x 2 additionally for 3000 Team Recovery,\n'
'⇒ to the max x 2.5 additionally for 4000 Team Recovery.',

'chi_team':'队伍技能：\n'
'以回血溢出值作全体攻击，最大 10 倍\n'
'发动条件：\n'
'以噩耗元素噬者 ‧ 迪亚布罗作队长，并以 3 个或以上的 5 星或 6 星妖女系列、 6 星或 7 星玩具精灵系列的召唤兽、精灵使 ‧ 乌特博丽公主或 6 星妖娆花梦系列召唤兽作成员 (不可重复)\n\n'
'队伍技能：\n'
'当前生命力全满时，下一次所受伤害不会使你死亡 (同 1 回合只会发动 1 次)\n'
'发动条件：\n'
'以 6 星妖娆花梦系列召唤兽作队长及战友，队伍中有 3 个或以上 6 星的妖娆花梦系列召唤兽及只有妖精类成员\n\n'
'队伍技能：\n'
'每首批消除 1 组水、火或木符石将掉落 4 粒火强化符石；每首批消除 1 组光、暗或心符石，将掉落 4 粒心强化符石；每累计消除 10 粒火或心符石，将掉落 1 粒火妖族强化符石\n'
'发动条件：\n'
'以闭锁心蕾 ‧ 樱作队长及战友',

'eng_team':'Team Skill:\n\n'
'◆ Recovery surplus will become a Full Attack, the largest Damage that could be dealt is 10 times of Recovery\n'
'Condition:\n'
'The Leader is Diablo, Nightmare Guttler of Elements, with 3 or more Elfish Perennials series 6 star, Sprites series 5 or 6 star, Toy Pixies series 6 or 7 star, or Elf Summoner - Princess Woodbury in the Team (identical Characters will only be counted as one).\n\n'
'Team Skill:\n'
'◆ When HP is full, the next Damage received will not lead to your defeat (one activation each Round).\n'
'Condition:\n'
'Both the Leader and Ally are Elfish Perennials series 6 star, with only Elves and 3 or more Elfish Perennials series 6 star in the Team.\n\n'
'Team Skill:\n'
'◆ 4 Enchanted Fire Runestones will be generated for every group of Water, Fire or Earth Runestones dissolved (only the first batch of Runestones dissolved will be counted). 4 Enchanted Heart Runestones will be generated for every group of Light, Dark or Heart Runestones dissolved (only the first batch of Runestones dissolved will be counted). 1 Fire Elf Runestone will be generated for every 10 Fire or Heart Runestones dissolved cumulatively.\n'
'Condition:\n'
'Both the Leader and Ally are Shrunk Petals - Sakura.'},
    
    {'chi_name':'蔷薇',
'chif_name':'薔薇',
'eng_name':'rose',

'chi_act':'如一之灵 CD6\n\n'
'点选 1 横行的符石，并将该横行的符石转化为心强化符石；1 回合内，妖精类攻击力 2 倍',
'eng_act':'Spirits in a Row CD\n\n'
'Tap and turn a row of Runestones into Enchanted Heart Runestones. Elf Attack x 2 for 1 Round.',

'chi_lead':'魅艳之刺\n\n'
'I. 妖精类攻击力 4.5 倍\n'
'II. 心符石兼具 25% 所有属性符石效果(可叠加)',
'eng_lead':'Ornamental Thorns of Elves\n\n'
'Elf Attack x 4.5. Heart Runestones also possess 25% effect of all Attributive Runestones (effects can be superimposed).',

'chi_team':'队伍技能：\n\n'
'以回血溢出值作全体攻击，最大 10 倍\n'
'发动条件：\n'
'以噩耗元素噬者 ‧ 迪亚布罗作队长，并以 3 个或以上的 5 星或 6 星妖女系列、 6 星或 7 星玩具精灵系列的召唤兽、精灵使 ‧ 乌特博丽公主或 6 星妖娆花梦系列召唤兽作成员 (不可重复)\n\n'
'队伍技能：\n'
'当前生命力全满时，下一次所受伤害不会使你死亡 (同 1 回合只会发动 1 次)\n'
'发动条件：\n'
'以 6 星妖娆花梦系列召唤兽作队长及战友，队伍中有 3 个或以上 6 星的妖娆花梦系列召唤兽及只有妖精类成员\n\n'
'队伍技能：\n'
'妖精类成员对最后成功攻击我方的敌人属性的目标攻击力提升 1.5 倍\n\n'
'队长的队长技能“魅艳之刺”变为“魅艳之刺 ‧ 强”：妖精类攻击力 4.5 倍，心符石兼具 75% 所有属性符石效果 (可叠加)；每消除 1 横行内的所有符石时 (只计算首批消除的符石)，必定掉落 5 粒心符石\n'
'发动条件：\n'
'以恋慕弥漫 ‧ 蔷薇作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Recovery surplus will become a Full Attack, the largest Damage that could be dealt is 10 times of Recovery\n'
'Condition:\n'
'The Leader is Diablo, Nightmare Guttler of Elements, with 3 or more Elfish Perennials series 6 star, Sprites series 5 or 6 star, Toy Pixies series 6 or 7 star or Elf Summoner - Princess Woodbury in the Team (identical Characters will only be counted as one).\n\n'
'Team Skill:\n'
'◆ When HP is full, the next Damage received will not lead to your defeat (one activation each Round).\n'
'Condition:\n'
'Both the Leader and Ally are Elfish Perennials (series) ( 6* ), with only Elves and 3 or more Elfish Perennials (series) ( 6* ) in the Team.\n\n'
'Team Skill:\n'
'◆ Elf Attack on enemies of Attribute from which the Summoner received the last Damage x 1.5 additionally.\n'
'◆ Change the Leader Skill of the Leader from "Ornamental Thorns of Elves" to "Ornamental Thorns of Elves - EX": Elf Attack x 4.5. Heart Runestones also possess 75% effect of all Attributive Runestones (effects can be superimposed). By dissolving all Runestones in a row, 5 Heart Runestones will be generated (only the first batch of Runestones dissolved will be counted).\n'
'Condition:\n'
'Both the Leader and Ally are Lovey Dovey Romancist - Rose.'},
    
    {'chi_name':'道罗斯',
'chif_name':'道羅斯',
'eng_name':'daoloth',

'chi_act':'力量之源 CD6\n\n'
'1 回合内，自身攻击力 4 倍，连击 (Combo) 数目增加 6，队伍中每个龙类、兽类或妖精类成员将额外增加 1 连击 (Combo)，最多可额外增加 6 连击 (Combo)',
'eng_act':'	Source of Power CD6\n\n'
'For 1 Round, the Monster\'s Attack x 4, Combo count +6, for each Dragon, Beast or Elf present in the Team, Combo count +1 additionally, to the max +6.',

'chi_lead':'创造之能 ‧ 强\n\n'
'I. 光属性“龙类、兽类及妖精类”\n'
'生命力 1.8 倍及攻击力 6.5 倍\n'
'II. 延长移动符石时间 1 秒\n'
'III. 消除 1 组 5 粒符石攻击力额外 4 倍，\n'
'消除 1 组符石的数目愈多，\n'
'⇒ 攻击力额外提升愈多\n'
'⇒ 消除 1 组 8 粒符石可提升至最大 4.6 倍',
'eng_lead':'Power of Creation - EX\n\n'
'I. Light Dragon, Light Beast & Light Elf Attack x 6.5; HP x 1.8.\n'
'II. Extend Runestone-moving time by 1 second.\n'
'III. If a group of ≥5 Runestones is dissolved, Attack increases additionally and proportionally.\n'
'⇒ Attack x 4 if a group of 5 Runestones are dissolved,\n'
'⇒ to the max x 4.6 for a group of 8 Runestones dissolved.',

'chi_team':'队伍技能：\n\n'
'每回合移动符石时触碰的首 5 粒符石转化为光强化符石\n'
'发动条件：\n'
'以悖论创造 ‧ 道罗斯作队长及战友\n\n'
'队伍技能：\n'
'龙类及兽类成员\n'
'⇒ 增加 600 点回复力基值\n'
'发动条件：\n'
'以悖论创造 ‧ 道罗斯作队长及战友，\n'
'且队中只有光属性龙类\n'
'光属性兽类或光属性妖精类成员',
'eng_team':'Team Skill:\n\n'
'◆ Turn the first 5 Runestones touched while moving into Enchanted Light Runestones each Round.\n'
'Condition:\n'
'Both the Leader and Ally are Demiurge of Antinomy - Daoloth.\n\n'
'Team Skill:\n'
'◆ Dragon & Beast Recovery basic value +600.\n'
'Condition:\n'
'Both the Leader and Ally are Demiurge of Antinomy - Daoloth, with only Light Beasts, Light Elves, or Light Dragons in the Team.'},
    
    {'chi_name':'格赫罗斯',
'chif_name':'格赫羅斯',
'eng_name':'ghroth',

'chi_act':'梦中结界 CD10\n\n'
'1 回合内，2 粒符石相连，即可发动消除，效果持续至消除 1 种符石达 30 粒',
'eng_act':'Dimensions of Dreams CD10\n\n'
'For 1 Round, Runestones can be dissolved by aligning 2 or more of them, until 30 Runestones of one type are dissolved.',

'chi_lead':'吞噬之欲\n\n'
'I. 魔族、龙类及兽类攻击力 4 倍\n'
'II. 心符石兼具 50% 所有属性符石效果 (可叠加)',
'eng_lead':'Ravening Desire\n\n'
'Demon, Dragon & Beast Attack x 4; Heart Runestones also possess 50% effect of all Attributive Runestones (effects can be superimposed).',

'chi_team':'队伍技能：\n\n'
'I. 每消除 1 组符石时\n'
'⇒ 全队攻击力提升 0.15 倍\n'
'⇒ 消除 8 组可提升至最大 2.2 倍\n'
'队中 6 星“宇宙序章”系列成员愈多\n'
'⇒ 所获得的效果愈多：\n\n'
'≥2 只：\n'
'队中最左方的 2 只\n'
'疯癫梦界度 ‧ 格赫罗斯的攻击力基值跟随攻击力基值最高的成员\n\n'
'≥3 只：\n'
'魔族、龙类及兽类成员\n'
'⇒生命力、攻击力及回复力基值 1.5 倍\n\n'
'≥4 只：\n'
'必然延长移动符石时间 2 秒\n'
'发动条件：\n'
'以疯癫梦界度 ‧ 格赫罗斯作队长及战友',
'eng_team':'Team Skill\n\n'
'◆ For each group of Runestones dissolved, Team Attack increases by x 0.15 additionally, to the max x 2.2 for 8 groups of Runestones dissolved.\n'
'◆ The more 6 star Characters of Prologue of the Universe in the Team,\n'
'⇒ the more of the following effects will be triggered:\n\n'
'≥2 Characters:\n'
'⇒Attack basic value of the first two Dream Gobbler - Ghroth from the left will synchronize with that of the Member that has the highest Attack basic value\n\n'
'≥3 Characters:\n'
'⇒Demon, Dragon & Beast HP, Attack & Recovery x 1.5 additionally\n\n'
'≥4 Characters:\n'
'⇒Extend Runestone-moving time regardlessly by 2 seconds.\n'
'Condition:\n'
'Both the Leader and Ally Dream Gobbler - Ghroth.'},
    
    {'chi_name':'阿撒托斯',
'chif_name':'阿撒托斯',
'eng_name':'azathoth',

'chi_act':'灭绝之噬 CD8\n\n'
'引爆场上所有符石，以掉落所属队伍栏直行龙类成员属性的符石，龙类以外成员队伍栏直行的符石则随机掉落',
'eng_act':'Extensive Elimination CD8\n\n'
'Explode all Runestones to generate Enchanted Dragon Runestones of the Attribute of the Dragons in the column(s).\n'
'For columns below non-Dragon, Runestones will be dropped randomly.',

'chi_lead':'暗龙暴 ‧ 强\n\n'
'I. 龙类生命力 1.6 倍及攻击力 7 倍\n'
'II. 每首批消除 1 连击 (Combo)\n'
'⇒ 自身直行掉落 1 粒暗强化符石\n'
'III. 消除 ≥10 粒暗符石时\n'
'⇒ 全队攻击力额外 3.2 倍',
'eng_lead':'Violence of Dark Dragons - EX\n\n'
'I. Dragon HP x 1.6; Dragon Attack x 7.\n'
'II. For each Combo made in the first batch,\n'
'⇒ 1 Enchanted Dark Runestone will be generated in the column below the Monster.\n'
'III. If ≥10 Dark Runestones are dissolved in the Round, Team Attack x 3.2 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后，\n'
'暗属性龙类成员技能 CD -6\n'
'II. 每首批消除 10 粒符石时\n'
'⇒ 于发动攻击前对全体敌人\n'
'造成 100 万暗属性伤害\n'
'⇒ 首批消除 30 粒符石可造成最多 300 万暗属性伤害\n'
'III. 将敌方所受此攻击伤害的 1%\n'
'⇒ 转化为我方生命力(只适用于未被击毙的敌人)。\n'
'IV. 每击毙 1 个敌人\n'
'⇒ 回复自身总生命力 50%\n'
'延长移动符石时间 1 秒，\n'
'队伍成员属性愈多，\n'
'延长移动符石时间愈多，\n'
'最多可延长 3 秒\n'
'发动条件：\n'
'以因果破坏 ‧ 阿撒托斯作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ After entering a Stage, Skill CD of Dark Dragon(s) -6.\n'
'◆ For every 10 Runestones dissolved in the first batch,\n'
'⇒ deal 1,000,000 Dark Damage to all enemies before attacks,\n'
'⇒ to the max 3,000,000 for 30 Runestones dissolved.\n'
'◆ 1% of Damage dealt will be converted to HP Recovery (only Damage dealt to undefeated enemies will be counted).\n'
'◆ Recover 50% HP for each enemy defeated.\n'
'◆ Extend Runestone-moving time by 1 second. The more the Attributes in the Team, the more the Runestone-moving time will be extended, to the max 3 seconds.\n'
'Condition:\n'
'Both the Leader and Ally are Fiend of Destruction - Azathoth.\n'},
    
    {'chi_name':'夏侯惇',
'chif_name':'夏侯惇',
'eng_name':'xiahoudun',

'chi_act':'反杀之狠戾 CD6\n\n'
'I. 自身攻击力 3 倍\n'
'II. 人类及魔族成员\n'
'⇒ 以 50% 自身攻击力追打 1 次\n'
'III. 每当敌人发动攻击\n'
'⇒ 下回合人类及魔族成员额外追打 1 次\n'
'效果持续至首批消除 6 种符石',
'eng_act':'Super Counter Striker CD6\n\n'
'I. The Monster\'s Attack x 3.\n'
'II. Each of Humans and Demons in the Team launches an extra attack as much as 50% of its attack.\n'
'III. When the enemy attacks, Humans and Demons will launch one more extra attack next Round.\n'
'The effects stay in play until Runestones of 6 types are dissolved in the first batch.',

'chi_lead':'酷冷之杀意 ‧ 溢\n\n'
'队伍中只有火、木及暗属性成员时：\n'
'I. 全队攻击力 5 倍\n'
'II. 任意消除火、木或暗符石达 ≥9 粒\n'
'⇒ 全队攻击力额外 2 倍\n'
'III. 同时消除火、木及暗符石\n'
'⇒ 所受伤害减少 40%',
'eng_lead':'Coldness of Combativeness\n\n'
'When the Team includes only Fire, Earth and Dark Members:\n'
'I. Team Attack x 5.\n'
'II. By dissolving ≥9 Fire, Earth or Dark Runestones in total,\n'
'⇒ Team Attack x 2 additionally.\n'
'III. If Fire, Earth and Dark Runestones are dissolved in the same Round,\n'
'⇒ Damage received -40%.',

'chi_team':'队伍技能：\n\n'
'每首批消除 1 粒“红军”区域内的符石\n'
'⇒ 提升“红军”成员攻击力\n'
'⇒ 首批消除 10 粒可达至最大 3 倍\n'
'发动条件：\n'
'以潜能解放“红军”角色作队长，且队伍中有 ≥3 个“红军”成员\n\n'
'火符石兼具其他属性符石效果\n'
'发动条件：\n'
'以“霸业魔政 ‧ 曹操”作队长及战友；且队伍中有 ≥3 个“红军”成员\n\n'
'I. 锁定 9 个固定位置，消除固定位置内的所有符石时：\n'
'⓵ 该回合全队攻击力 1.5 倍\n'
'⓶ 回合结束时，\n'
'将锁定位置的符石转化为\n'
'⇒“火、木、暗”强化符石各 3 粒\n\n'
'II. 火、木、暗符石互相兼具效果\n'
'发动条件：\n'
'以“魔瞳狂枪 ‧ 夏侯惇”作队长及战友\n'
'队伍技能：\n'
'无视“黏腐”敌技\n'
'发动条件：\n'
'以潜能解放“红军”角色作队长，且队伍中有 ≥3 个“红军”成员',
'eng_team':'Team Skill:\n\n'
'◆ By dissolving a Runestone in the "Red Army" region in the first batch,\n'
'⇒ Attack of "Red Army" Members increases additionally,\n'
'⇒ to the max x 3 for 10 Runestones dissolved.\n'
'◆ Boss Skill "Sticky Land" will be nullified.\n'
'Condition:\n'
'The Leader is "Red Army" 7 star, with 3 or more Characters of "Red Army" in the Team.\n\n'
'Team Skill:\n'
'◆ Fire Runestones also possess the effect of other Attributive Runestones.\n'
'Condition:\n'
'The Leader is Tyranny of Dominance - Cao Cao, with 3 or more Characters of "Red Army" in the Team.'},
    
    {'chi_name':'孙策',
'chif_name':'孫策',
'eng_name':'sunce',

'chi_act':'骁雄之攻 ‧ 剿除 CD8\n\n'
'I. 引爆所有风化、电击符石\n'
'II. 将水符石转化为\n'
'⇒ 水人族强化符石\n'
'1 回合内\n'
'III. 可任意移动符石而不会发动消除\n'
'IV. 连击 (Combo) 数目愈高\n'
'⇒ 自身攻击力愈高\n'
'⇒ 10 连击 (Combo) 可达至最大 15 倍',
'eng_act':'Strike of the Warlord - EX CD8\n\n'
'I. Explode all Weathered and Electrified Runestones.\n'
'II. Turn Water Runestones into Enchanted Human Runestones.\n'
'For 1 Round:\n'
'III. Unlimited Runestone movement without dissolving.\n'
'IV. The more Combos made, the higher the Monster\'s Attack, to the max x 15 for 10 Combos.',

'chi_lead':'霸者盛势 ‧ 无上控压\n\n'
'I. 必然延长移动符石时间 1 秒\n'
'II. 队伍中只有水属性人类时：\n'
'全队攻击力 6 倍、生命力及回复力 1.3 倍\n'
'⓵每消除 1 组符石\n'
'⇒ 额外计算多 1 连击 (Combo)\n'
'⓶首批消除 ≥2 组 ≥4 粒符石\n'
'⇒ 全队攻击力额外 2.25 倍\n'
'⓷ 属性符石需 ≥4 粒相连才可发动消除\n'
'⓸心符石 ≥2 粒相连即可发动消除',
'eng_lead':'Greatness of the Warlord - Ultimate\n\n'
'I. Extend Runestone-moving time regardlessly by 1 second.\n'
'II. When the Team consists of only Water Humans:\n'
'⓵ Team Attack x 6; HP & Recovery x 1.3.\n'
'⓶ Total Combo count +1 for every group of Runestones dissolved\n'
'⓷ By dissolving ≥2 groups of ≥4 Runestones in the first batch, Team Attack x 2.25 additionally.\n'
'⓸ Attributive Runestones can only be dissolved by grouping 4 or more of them.\n'
'⓹ Heart Runestones can be dissolved by aligning 2 or more of them.',

'chi_team':'队伍技能：\n\n'
'每首批消除 1 粒“蓝军”区域内的符石\n'
'⇒ 提升“蓝军”成员攻击力\n'
'⇒ 首批消除 10 粒可达至最大 3 倍\n'
'发动条件：\n'
'以潜能解放“蓝军”角色作队长，且队伍中有 ≥3 个“蓝军”成员\n\n'
'队伍技能：\n'
'“蓝军”成员\n'
'⇒“生命力、攻击力及回复力”基值 1.3 倍\n'
'发动条件：\n'
'以潜能解放“蓝军”角色作队长，且队伍中有 ≥3 个“蓝军”成员\n\n'
'队伍技能：\n'
'其他符石兼具 50% 水符石效果\n'
'发动条件：\n'
'以“不屈鸿志 ‧ 孙策”作队长及战友',
'eng_team':'Team Skill:\n'
'◆ By dissolving a Runestone in the "Blue Army" region in the first batch,\n'
'⇒ Attack of "Blue Army" Members increases additionally,\n'
'⇒ to the max x 3 for 10 Runestones dissolved.\n'
'◆ HP, Attack & Recovery basic value of "Blue Army" Members x 1.3 additionally.\n'
'Condition:\n'
'The Leader is "Blue Army" 7 star, with 3 or more Characters of "Blue Army" in the Team.\n\n'
'Team Skill:\n'
'◆ Other Runestones also possess 50% effect of Water Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are Unbending Aspiration - Sun Ce.'},
    
    {'chi_name':'祝融',
'chif_name':'祝融',
'eng_name':'zhurong',

'chi_act':'骁勇之力 ‧ 霸 CD5\n\n'
'I. 每消除 3 种符石\n'
'⇒ 可累积 1 点“蛮力”\n'
'⇒ 最多可累积 10 点\n'
'1 回合内\n'
'II. 根据累积“蛮力”\n'
'⇒ 提升自身攻击力\n'
'⇒ 最多可提升至 10 倍\n'
'III. 每有 1 点“蛮力”\n'
'⇒ 转化 3 粒人族强化符石\n'
'⇒ 最多可转化 30 粒\n'
'IV. 若“蛮力”累积至 10 点\n'
'⓵ 自身攻击无视“指定形状盾”敌技\n'
'⓶ 自身攻击无视敌人防御力\n\n'
'发动技能后蛮力减少一半',
'eng_act':'Force of the Heroine - EX CD5\n\n'
'I. 1 force point can be obtained for every 3 types of Runestones dissolved, to the max 10 force points in accumulation.\n'
'For 1 Round:\n'
'II. The more the force points accumulated, the higher the Monster\'s Attack, to the max x 10.\n'
'III. For each force point, turn 3 Runestones into Enchanted Human Runestones, to the max 30 Runestones.\n'
'IV. When the Monster has 10 force points upon Skill activation, the Monster\'s Damage will be dealt regardless of Puzzle Shield and enemies\' Defense.\n\n'
'Force points -50% after Skill activation.',

'chi_lead':'巾帼之炽焰\n\n'
'I. 队伍中有 ≥3 种属性成员时：\n'
'⓵ 全队攻击力 3.5 倍\n'
'⓶ 火符石兼具 50% 其他符石效果\n'
'II. 队伍中有 ≥3 个人类成员时：\n'
'⓵ 人类攻击力 3.5 倍、\n'
'生命力及回复力 1.3 倍',
'eng_lead':'Flames of the Heroine - EX\n\n'
'I. When there are 3 or more Attributes in the Team:\n'
'⓵ Team Attack x 3.5.\n'
'⓶ Fire Runestones also possess 50% effect of other Runestones.\n'
'II. When there are 3 or more Humans in the Team:\n'
'⓵ Human Attack x 3.5; HP & Recovery x 1.3.',

'chi_team':'队伍技能：\n\n'
'消除 1 组符石的数目愈多\n'
'⇒ 全队攻击力提升愈多\n'
'⇒ 消除 1 组 10 粒可提升至最大 2.5 倍\n'
'发动条件：\n'
'以“义军”角色作队长及战友\n\n'
'I. 进入关卡后，“义军”成员的技能 CD 减少 2\n'
'II. “义军”成员的攻击\n'
'⇒ 无视敌人防御力\n'
'发动条件：\n'
'以潜能解放“义军”角色作队长，且队伍中有 ≥3 个“义军”成员\n'
'队中每有 1 个人类成员，首批消除火符石，于回合结束时\n'
'⇒ 将 1 粒符石转化为火人族强化符石(光及暗符石优先转换)\n'
'⇒ 最多可转化 6 粒\n'
'发动条件：\n'
'以“葬殇修罗 ‧ 祝融”作队长及战友\n\n'
'“崇高炎护 ‧ 孟获”的技能 CD 减少 3\n'
'发动条件：\n'
'以“葬殇修罗 ‧ 祝融”及“崇高炎护 ‧ 孟获”作成员',
'eng_team':'Team Skill:\n\n'
'◆ The more the Runestones dissolved in a group, the higher the Team Attack, to the max x 2.5 additionally for a group of 10 Runestones dissolved.\n'
'Condition:\n'
'The Leader and Ally are "Rebel Army".\n\n'
'◆ Active Skill CDs of "Rebel Army" Members -2 after entering a Stage.\n'
'◆ Damage of "Rebel Army" Members will be dealt regardless of Defense.\n'
'Condition:\n'
'The Leader is "Rebel Army", with 3 or more Characters of "Rebel Army" in the Team.\n\n'
'◆ By dissolving Fire Runestones in the first batch, turn 1 Runestone into Enchanted Fire Human Runestones at the end of the Round for every Human present in the Team, to the max 6 Runestones to be turned (Light and Dark Runestones rank first in priority).\n'
'Condition:\n'
'Both the Leader and Ally are "Reaper of Wrath - Zhurong".\n\n'
'◆ Active Skill CD of "Afire Love - Meng Huo" -3.\n'
'Condition:\n'
'There are "Reaper of Wrath - Zhurong" and "Afire Love - Meng Huo" in the Team.'},
    
    {'chi_name':'吕洞宾',
'chif_name':'呂洞賓',
'eng_name':'ludongbin',

'chi_act':'幽魂八卦阵 CD6\n\n'
'点选元素法阵上的 1 粒符石，并将该种符石引爆，以掉落暗神族强化符石。1 回合内，暗符石兼具 50% 其他属性符石效果',
'eng_act':'Trigram of Gloom CD6\n\n'
'By tapping a Runestone on the Magic Circle of Elements, Runestones of that type will be exploded to generate Enchanted Dark God Runestones. For 1 Round, Dark Runestones also possess 50% effect of other Attributive Runestones.',

'chi_lead':'冥神 ‧ 符箓\n\n'
'I. 暗属性及神族攻击力 3.4 倍\n'
'II. 消除 3 粒符石\n'
'⇒ 暗属性及神族攻击力额外 1.3 倍\n'
'⇒ 消除 15 粒可提升至最大 2.5 倍',
'eng_lead':'Godly Charm of Gloom\n\n'
'Dark Attack & God Attack x 3.4, if 3 Runestones are dissolved, Attack x 1.3 additionally; the more Runestones dissolved, the higher the Attack increases additionally, to the max x 2.5 for 15 Runestones dissolved.',

'chi_team':'队伍技能：\n\n'
'“八仙”系列召唤兽对妖精类及魔族目标攻击力提升 2 倍\n'
'发动条件：\n'
'队伍中有八仙系列召唤兽作成员\n\n'
'必然延长移动符石时间 2 秒。\n'
'每消除 1 组队伍成员属性符石，额外计算多 1 连击 (Ex. Combo)，最多可额外增加 10 连击 (Ex. Combo)\n'
'发动条件：\n'
'以菡萏香销 ‧ 何仙姑及剑气御神 ‧ 吕洞宾作队长或战友',
'eng_team':'Team Skill:\n'
'◆ Damage dealt to Elves and Demons by Monsters of "The Eight Xian" x 2 additionally.\n'
'Condition:\n'
'There is Characters of "The Eight Xian" (series) in the Team.\n\n'
'◆ 1 Ex. Combo count for each group of Runestones of Members\' Attributes dissolved, to the max 10 Ex. Combo count.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'Condition:\n'
'The Leader and Ally are  "Supreme Lotus - He Xian\'gu" and "Mischievous Wit - Lü Dongbin" (interchangeable).'},
    
    {'chi_name':'铁拐李',
'chif_name':'鐵拐李',
'eng_name':'litieguai',

'chi_act':'穿魂之力 ‧ 机械 CD6\n\n'
'木属性及机械族攻击力 1.8 倍，若发动技能时自身行动值达至 100%，攻击力提升至 2.2 倍；队伍中若有 3 个或以上机械族成员，必然延长移动符石时间 3 秒。效果会在进入下一层数 (Wave) 时消失',
'eng_act':'Soul-penetrating Power CD6\n\n'
'Earth Attack & Machina Attack x 1.8, if the Monster\'s Fuel is 100% upon Skill activation, the Attack multiplier increases to x 2.2. If there are 3 or more Machinas in the Team, extend Runestone-moving time regardlessly by 3 seconds. The Skill stays in play within the Wave.',

'chi_lead':'夺魄之森\n\n'
'I. “妖精类及魔族”以外的木属性成员攻击力 4 倍\n'
'II. 消除属性符石时\n'
'⇒ 所有成员对该属性目标攻击力 1.5 倍',
'eng_lead':'Harvester of Soul Pieces\n\n'
'Earth non-Elf & Earth non-Demon Attack x 4. Damage dealt to enemies of the Attributes of Runestones dissolved x 1.5.',

'chi_team':'队伍技能：\n\n'
'“八仙”系列召唤兽对妖精类及魔族目标攻击力提升 2 倍\n'
'发动条件：\n'
'队伍中有八仙系列召唤兽作成员\n\n'
'场上有附加效果时，“血植异足 ‧ 铁拐李”的攻击力提升 2 倍。\n'
'每首批消除 1 组符石，于该回合结束时，将 1 粒符石 (木属性以外多于 3 粒的属性符石优先转换) 转化为木符石，最多可转 6 粒\n'
'发动条件：\n'
'以血植异足 ‧ 铁拐李作队长及战友\n\n'
'【机械动力】\n'
'I. 每首批消除 1 粒自身属性符石\n'
'⇒ 自身行动值提升 2%\n'
'II. 每首批消除 1 粒心符石\n'
'⇒ 自身行动值提升 1%\n'
'III. 行动值愈高\n'
'⇒ 自身攻击力提升愈多\n'
'⇒ 最大提升至 2 倍。\n'
'IV. 当所有机械族成员的行动值达至 50% 或以上时\n'
'⇒ 机械族成员属性的符石效果提升\n'
'⇒ 每个机械族成员可提升 10% 效果\n'
'⇒ 最高 60%\n'
'V. 当所有机械族成员的行动值达至 100% 时\n'
'⇒ 机械族成员每回合\n'
'以 25% 自身攻击力随机追打自身属性或自身克制属性的攻击 1 至 2 次\n'
'发动条件：\n'
'队伍中有 ≥2 个【机械族】成员',
'eng_team':'Team Skill:\n\n'
'◆ Damage dealt to Elves and Demons by Monsters of "The Eight Xian" x 2 additionally.\n'
'Condition:\n'
'There is Characters of "The Eight Xian" (series) in the Team.\n\n'
'◆ When there is an additional effect in play, Attack of "Bionic Immortal - Li Tieguai" x 2. For every group of Runestones dissolved, turn a Runestone into Earth Runestone at the end of the Round, to the max 6 Runestones to be turned (only the first batch of Runestones dissolved will be counted) (non-Earth Attributive Runestones in a number of more than 3 rank first in priority).\n'
'Condition:\n'
'Both the Leader and Ally are "Bionic Immortal - Li Tieguai".\n\n'
'◆ 【Machina Dynamics】\n'
'⓵ For each Runestone of the Character\'s Attribute dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +2%.\n'
'⓶ For each Heart Runestone dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +1%.\n'
'⓷ The higher the Character\'s Fuel,\n'
'⇒ the higher the Character\'s Attack,\n'
'⇒ to the max x 2 additionally.\n'
'⓸ When all Machinas in the Team have ≥ 50% Fuel,\n'
'⇒ effects of Runestones of their Attributes increase,\n'
'⇒ 10% for each Machina present in the Team,\n'
'⇒ to the max 60%.\n'
'⓹ When all Machinas in the Team have 100% Fuel,\n'
'⇒ all Machinas randomly launch 1 to 2 extra attack(s) of its own Attribute or its Counter Attribute as much as 25% of its Attack every Round.\n'
'Condition:\n'
'There are 2 or more 【Machina Dynamics】 Members in the Team.'},

{'chi_name':'何仙姑',
'chif_name':'何仙姑',
'eng_name':'hexiangu',

'chi_act':'	仙荷之力 ‧ 强 CD5\n\n'
'神族攻击力 2 倍；每首批消除 1 组队伍成员属性符石或心符石时，将产生 1 粒神族强化符石，最多可产生 6 粒，效果持续至受到敌人攻击',
'eng_act':'Lotus Power - EX CD5\n\n'
'God Attack x 2, for each group of Heart Runestones or Runestones of Team Members\' Attributes dissolved, 1 Enchanted God Runestone will be generated, to the max 6 Runestones to be generated (only the first batch of Runestones dissolved will be counted). The Skill stays in play until receiving Damage from enemies\' attacks.',

'chi_lead':'八仙阵\n\n'
'队伍中有 3 个或以上八仙系列角色时：\n'
'I. 连击 (Combo) 时攻击力提升 125%\n'
'II. 消除心符石时\n'
'⇒ 全队攻击力额外 1.6 倍',
'eng_lead':'Assembly of the Eight Xian\n\n'
'If there are 3 or more Monsters of "The Eight Xian" in the Team, Attack bonus for each Combo increases by 125%, by dissolving Heart Runestones, Team Attack x 1.6 additionally.',

'chi_team':'队伍技能：\n\n'
'“八仙”系列召唤兽对妖精类及魔族目标攻击力提升 2 倍\n'
'发动条件：\n'
'队伍中有八仙系列召唤兽作成员\n'
'必然延长移动符石时间 2 秒。\n'
'每消除 1 组队伍成员属性符石，额外计算多 1 连击 (Ex. Combo)，最多可额外增加 10 连击 (Ex. Combo)\n'
'发动条件：\n'
'以菡萏香销 ‧ 何仙姑及剑气御神 ‧ 吕洞宾作队长或战友',
'eng_team':'Team Skill:\n\n'
'◆ Damage dealt to Elves and Demons by Monsters of "The Eight Xian" x 2 additionally.\n'
'Condition:\n'
'There is Characters of "The Eight Xian" (series) in the Team.\n\n'
'◆ 1 Ex. Combo count for each group of Runestones of Members\' Attributes dissolved, to the max 10 Ex. Combo count.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'Condition:\n'
'The Leader and Ally are "Supreme Lotus - He Xian gu" and "Mischievous Wit - Lü Dongbin" (interchangeable).'},

    {'chi_name':'梵天',
'chif_name':'梵天',
'eng_name':'brahma',

'chi_act':'力量的肇始 CD6\n\n'
'将黑白符石变回原来色调,1 回合内，必然延长移动符石时间 6 秒，自身攻击力 6 倍，连击 (Combo) 数目增加 6',
'eng_act':'Beginning of Power CD6\n\n'
'Clear the negative effect of "B&W Zone". For 1 Round, extend Runestone-moving time regardlessly by 6 seconds, the Monster\'s Attack x 6, Combo count +6.',

'chi_lead':'元素创念 ‧ 强\n\n'
'队伍中只有神族成员时\n'
'I. 全队攻击力 5 倍、生命力及回复力 1.3 倍\n'
'II. 首批掉落“没有首批消除”的其中 1 种属性符石 (剩余数量最少优先)\n'
'III. 消除 5 种属性符石时\n'
'⇒ 全队攻击力额外 1.5 倍',
'eng_lead':'Creation of Elements - EX\n\n'
'When the Team consists of only Gods:\n'
'I. Team Attack x 5, HP & Recovery x 1.3.\n'
'II. If not Runestones of all 5 Attributes are dissolved, the first batch of Runestones to be dropped will be Runestones of an undissolved Attribute (the Attributive Runestones that are the least in number rank first in priority) (only the first batch of Runestones dissolved will be counted).\n'
'III. If Runestones of all 5 Attributes are dissolved, Team Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 每回合移动符石时触碰的首 6 粒符石\n'
'⇒ 转化为神族强化符石\n'
'II. 每首批消除 1 粒神族符石\n'
'⇒ 产生 2 粒火神族强化符石\n'
'⇒ 最多 15 粒\n'
'III. 每消除 1 粒火强化符石\n'
'⇒ 回复 5% 总生命力\n'
'⇒ 最多可回复 100% (不会溢补)\n'
'IV. 心符石兼具 50% 所有属性符石效果\n'
'发动条件：\n'
'以唯识无境 ‧ 梵天作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Turn the first 6 Runestones touched while moving into Enchanted God Runestones.\n'
'◆ 2 Enchanted Fire God Runestones will be generated for each God Runestone dissolved, to the max 15 Runestones to be generated (only the first batch of Runestones dissolved will be counted).\n'
'◆ 5% of total HP will be recovered for each Enchanted Fire Runestone dissolved, to the max 100% HP (no overhealing).\n'
'◆ Heart Runestones also possess 50% effect of all Attributive Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Chittamatra - Brahma".'},
    
    {'chi_name':'湿婆',
'chif_name':'濕婆',
'eng_name':'shiva',

'chi_act':'混沌再生 CD5\n\n'
'将黑白符石变回原来色调；点选 2 直行的符石并引爆，以掉落水神族强化符石',
'eng_act':'Reform of Chaos\n\n'
'Clear the negative effect of "B&W Zone". Tap and explode 2 columns of Runestones to generate Enchanted Water God Runestones.',

'chi_lead':'神妖灭世 ‧ 强\n\n'
'队伍中只有神族或妖精类成员时\n'
'I. 全队攻击力 6 倍\n'
'II. 必然延长移动符石时间 1 秒\n'
'III. 消除神族或妖族符石时\n'
'⇒ 全队攻击力额外 1.5 倍',
'eng_lead':'Destructive Power of Gods & Elves - EX\n\n'
'When the Team consists of only Gods and Elves:\n'
'I. Team Attack x 6.\n'
'II. Extend Runestone-moving time regardlessly by 1 second.\n'
'III. By dissolving God or Elf Runestones, Team Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'每回合移动符石时触碰的首 5 粒符石转化为神族强化符石，而与神族符石种类相同的符石兼具 50% 水符石效果。每消除 1 粒神族符石，可减少 10% 所受伤害，最多可减少 50%\n\n'
'发动条件：\n'
'以大自在天 ‧ 湿婆作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Turn the first 5 Runestones touched while moving into Enchanted God Runestones each Round. Types of God Runestones also possess 50% effect of Water Runestones. Damage received -10% for each God Runestones dissolved, to the max -50%.\n'
'Condition:\n\n'
'Both the Leader and Ally are "Maheśvara - Shiva".'},

    {'chi_name':'毗湿奴',
'chif_name':'毗濕奴',
'eng_name':'vishnu',

'chi_act':'化厄之念 CD5\n\n'
'将黑白符石变回原来色调,1 回合内，减少 50% 所受伤害,消除神族符石愈多，全队攻击力提升愈多，5 粒可提升至最大 2 倍',
'eng_act':'Notion of Salvation CD5\n\n'
'Clear the negative effect of "B&W Zone". For 1 Round, Damage received -50%; the more the God Runestones dissolved, the higher the Team Attack, to the max x 2 for 5 Runestones.',

'chi_lead':'幻惑护生\n\n'
'队伍中只有神族成员时：\n'
'I. 全队攻击力 4 倍及回复力 1.5 倍\n'
'II. 同时消除光及暗符石时\n'
'⇒ 全队攻击力 1.5 倍\n'
'⇒ 减少 20% 所受伤害\n'
'III. 消除神族符石时\n'
'⇒ 全队攻击力额外 1.5 倍',
'eng_lead':'Supreme Protection\n\n'
'When the Team consists of only Gods:\n'
'I. Team Attack x 4 and Recovery x 1.5.\n'
'II. By dissolving Light and Dark Runestones in the same Round,\n'
'⇒ Team Attack x 1.5 additionally and Damage received -20%.\n'
'III. By dissolving God Runestones,\n'
'⇒ Team Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 每回合移动符石时触碰的首 5 粒符石转化为神族强化符石\n'
'II. 光符石兼具暗符石效果\n'
'III. 暗符石兼具光符石效果\n'
'IV. 每首批消除 1 组水、火或木符石\n'
'⇒ 左方 3 直行将首批掉落共 3 粒暗神族符石\n'
'⇒ 右方 3 直行将首批掉落共 3 粒光神族符石\n'
'⇒ 左右 2 方各可掉落最多 9 粒\n'
'发动条件：\n'
'以持戒苦行 ‧ 毗湿奴作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Turn the first 5 Runestones touched while moving into Enchanted God Runestones.\n'
'◆ Light Runestones also possess the effect of Dark Runestones.\n'
'◆ Dark Runestones also possess the effect of Light Runestones.\n'
'◆ For each group of Water, Fire or Earth Runestones dissolved (only the first batch of Runestones dissolved will be counted),\n'
'⇒ 3 Dark God Runestones will be dropped in the first batch of Runestones in the 3 columns on the left, and 3 Light God Runestones in the 3 columns on the right, to the max 9 Runestones to be dropped for each side.\n'
'Condition:\n'
'Both the Leader and Ally are "Ascetic Mind - Vishnu".'},
    
    {'chi_name':'零',
'chif_name':'零',
'eng_name':'Zero',

'chi_act':'顺势而攻 CD8\n\n'
'I. 15 秒内，可任意移动符石而不会发动消除\n'
'1 回合内\n'
'II. 若队长及战友均为兽类成员时\n'
'⓵ 全队攻击力 2.5 倍\n'
'⓶ 该回合所受伤害不会使你死亡',
'eng_act':'	Control of Situation CD8\n\n'
'I. Unlimited Runestone movement in 15 seconds without dissolving.\n'
'For 1 Round:\n'
'II. If the Leader and Ally are Beasts:\n'
'⓵ Team Attack x 2.5\n'
'⓶ The Damage received in the Round will not lead to your defeat.',

'chi_lead':'异瞳的力量 ‧ 强\n\n'
'I. 兽类生命力及回复力 1.8 倍\n'
'II. 延长移动符石时间 2 秒\n'
'III. 连击 (Combo) 时攻击力提升 200%\n'
'IV. 所有属性符石兼具其他属性符石效果：\n'
'队伍中每多 1 个兽类成员\n'
'⇒ 可提升 20% 兼具效果\n'
'⇒ 最大 100% (可叠加)\n'
'V. 消除兽族符石\n'
'⇒ 兽类攻击力额外 3 倍',
'eng_lead':'Pupils of the Cat - EX\n\n'
'I. Beast HP & Recovery x 1.8.\n'
'II. Extend Runestone-moving time by 2 seconds.\n'
'III. Attack bonus for each Combo increases by 200%.\n'
'IV. All Attributive Runestones also possess the effect of other Attributive Runestones:\n'
'For every extra Beast in the Team, ⇒ the effect +20%,\n'
'⇒ to the max +100% (effects can be superimposed).\n'
'V. By dissolving Beast Runestones,\n'
'⇒ Beast Attack x 3 additionally.',

'chi_team':'队伍技能：\n\n'
'队伍中每多 1 个 6 星“神猫大盗”系列角色，于回合结束时，将 2 粒属性符石转化为兽族强化符石 (木符石优先转换)，最多可转 10 粒\n'
'发动条件：\n'
'以“如烟无迹 ‧ 阿飘”作队长\n'
'I. 兽类成员\n'
'⇒“生命力、攻击力及回复力”基值 1.3 倍\n'
'II. 延长移动符石时间 2 秒\n'
'发动条件：\n'
'以“领风典范 ‧ 蜜儿”作队长，并以“如烟无迹 ‧ 阿飘”或“随缘顺心 ‧ 零”作战友\n\n'
'队伍中每多 1 个 6 星“神猫大盗”系列角色，可使兽类成员进入关卡后的主动技能 CD 减少 1，最多可减少 5 CD\n'
'每回合移动符石时触碰的首 6 粒符石转化为兽族强化符石\m'
'发动条件：\n'
'以“随缘顺心 ‧ 零”作队长',
'eng_team':'Team Skill:\n\n'
'◆ Beast Attack, HP & Recovery basic value x 1.3 additionally.\n'
'◆ Extend Runestone-moving time by 2 seconds.\n'
'Condition:\n'
'The Leader is "Cat of Charisma - Mellow", and the Ally is "Carefree Mindset - Zero".\n'
'◆ For every extra 6 star Monster of "The Master Cathieves" present in the Team, Active Skill CDs of Beasts -1 after entering a Stage, to the max -5 CD.\n'
'◆ Turn the first 6 Runestones touched while moving into Enchanted Beast Runestones each Round.\n'
'Condition:\n'
'The Leader is "Carefree Mindset - Zero".\n\n'
'◆ For every extra 6 star Monster of "The Master Cathieves" present in the Team, turn 2 Attributive Runestones into Enchanted Beast Runestones at the end of each Round, to the max 10 Runestones to be turned (Earth Runestones rank first in priority).\n'
'Condition:\n'
'The Leader is "Untraceable Moves - Ghostie".'},
    
    {'chi_name':'蜜儿',
'chif_name':'蜜兒',
'eng_name':'Mellow',

'chi_act':'伺机而攻 CD8\n\n'
'发动技能时敌方全体生命力需为全满：所有成员进入潜行模式及攻击力提升 3 倍，效果持续至对敌人造成伤害 (效果持续期间技能不会冷却)',
'eng_act':'Spying Feline CD8\n\n'
'This Skill can be activated only when the enemies\' HP is full. All Monsters will be undercover with their Attack x 3. The effect stays in play until the Damage is dealt to the enemy. CD will not drop when the Skill is in play.',

'chi_lead':'女王的力量\n\n'
'队伍中只有兽类成员时：\n'
'I. 全队攻击力 4 倍\n'
'II. 每个成员增加 400 点回复力\n'
'III. 队伍中没有重复成员时：\n'
'每回合消除符石的组数愈多\n'
'⇒ 全队攻击力额外提升愈多\n'
'⇒ 消除 10 组可提升至最大 3 倍',
'eng_lead':'Reign of the Queen\n\n'
'When the Team has only Beasts,\n'
'I. Team Attack x 4.\n'
'II. Recovery basic value of each Member +400.\n'
'III. When there are no identical Members in the Team:\n'
'the more the groups of Runestones dissolved in the Round,\n'
'⇒ the higher the Team Attack increases additionally,\n'
'⇒ to the max x 3 for 10 groups.',

'chi_team':'队伍技能：\n\n'
'队伍中每多 1 个 6 星“神猫大盗”系列角色，于回合结束时，将 2 粒属性符石转化为兽族强化符石 (木符石优先转换)，最多可转 10 粒\n'
'发动条件：\n'
'以“如烟无迹 ‧ 阿飘”作队长\n\n'
'I. 兽类成员\n'
'⇒“生命力、攻击力及回复力”基值 1.3 倍\n'
'II. 延长移动符石时间 2 秒\n'
'发动条件：\n'
'以“领风典范 ‧ 蜜儿”作队长，并以“如烟无迹 ‧ 阿飘”或“随缘顺心 ‧ 零”作战友\n\n'
'队伍中每多 1 个 6 星“神猫大盗”系列角色，可使兽类成员进入关卡后的主动技能 CD 减少 1，最多可减少 5 CD\n'
'每回合移动符石时触碰的首 6 粒符石转化为兽族强化符石\n'
'发动条件：\n'
'以“随缘顺心 ‧ 零”作队长',
'eng_team':'Team Skill:\n\n'
'◆ Beast Attack, HP & Recovery basic value x 1.3 additionally.\n'
'◆ Extend Runestone-moving time by 2 seconds.\n'
'Condition:\n'
'The Leader is "Cat of Charisma - Mellow", and the Ally is "Untraceable Moves - Ghostie".or "Carefree Mindset - Zero".\n\n'
'◆ For every extra 6 star Monster of "The Master Cathieves" present in the Team, Active Skill CDs of Beasts -1 after entering a Stage, to the max -5 CD.\n'
'Condition:\n'
'The Leader is "Carefree Mindset - Zero".\n\n'
'◆ For every extra 6 star Monster of "The Master Cathieves" present in the Team, turn 2 Attributive Runestones into Enchanted Beast Runestones at the end of each Round, to the max 10 Runestones to be turned (Earth Runestones rank first in priority).\n'
'Condition:\n'
'The Leader is "Untraceable Moves - Ghostie".'},
   
{'chi_name':'阿飘',
'chif_name':'阿飄',
'eng_name':'ghostie',

'chi_act':'	惊世爆破 CD10\n\n'
'所有符石转化为兽族强化符石。队伍中只有兽类成员时，1 回合内，首批 1 粒符石即可发动消除',
'eng_act':'	Phenomenal Detonation CD10\n\n'
'Turn all Runestones into Enchanted Beast Runestones. When the Team consists of only Beasts, for 1 Round, Runestones can be dissolved singly or in groups of 2 or more',

'chi_lead':'幽魂的力量\n\n'
'队伍中只有兽类成员时：\n'
'I. 全队生命力 2 倍及攻击力 5.5 倍\n'
'II. 每回合扣除全队总生命力 10%\n'
'III. 每消除 1 粒兽族符石，回复 5% 总生命力',
'eng_lead':'Ability of the Unnoticed\n\n'
'When the Team consists of only Beasts, Team Attack x 5.5, HP x 2, 10% of total HP will be deducted every Round, recover 5% of total HP for each Beast Runestone dissolved.',

'chi_team':'队伍技能：\n\n'
'队伍中每多 1 个 6 星“神猫大盗”系列角色，于回合结束时，将 2 粒属性符石转化为兽族强化符石 (木符石优先转换)，最多可转 10 粒\n'
'发动条件：\n'
'以“如烟无迹 ‧ 阿飘”作队长\n\n'
'I. 兽类成员\n'
'⇒“生命力、攻击力及回复力”基值 1.3 倍\n'
'II. 延长移动符石时间 2 秒\n'
'发动条件：\n'
'以“领风典范 ‧ 蜜儿”作队长，并以“如烟无迹 ‧ 阿飘”或“随缘顺心 ‧ 零”作战友\n\n'
'队伍中每多 1 个 6 星“神猫大盗”系列角色，可使兽类成员进入关卡后的主动技能 CD 减少 1，最多可减少 5 CD\n'
'每回合移动符石时触碰的首 6 粒符石转化为兽族强化符石\n'
'发动条件：\n'
'以“随缘顺心 ‧ 零”作队长',
'eng_team':'Team Skill:\n\n'
'◆ Beast Attack, HP & Recovery basic value x 1.3 additionally.\n'
'◆ Extend Runestone-moving time by 2 seconds.\n'
'Condition:\n'
'The Leader is "Cat of Charisma - Mellow", and the Ally is "Untraceable Moves - Ghostie".\n\n'
'◆ For every extra 6 star Monster of "The Master Cathieves" present in the Team, Active Skill CDs of Beasts -1 after entering a Stage, to the max -5 CD.\n'
'Condition:\n'
'The Leader is "Carefree Mindset - Zero".\n'
'◆ For every extra 6 star Monster of "The Master Cathieves" present in the Team, turn 2 Attributive Runestones into Enchanted Beast Runestones at the end of each Round, to the max 10 Runestones to be turned (Earth Runestones rank first in priority).\n'
'Condition:\n'
'The Leader is "Untraceable Moves - Ghostie".'},
    
    {'chi_name':'爱因斯坦',
'chif_name':'愛因斯坦',
'eng_name':'einstein',

'chi_act':'流水定律 CD6\n\n'
'3 回合内，首批掉落的 8 粒符石必定为水强化符石；技能持续时若所有机械族成员的行动值达至 100%，自身攻击力 3 倍',
'eng_act':'Principle of Water\n\n'
'For 3 Rounds, the first batch of 8 Runestones to be dropped will be Enchanted Water Runestones. When all Machinas in the Team have 100% Fuel when the effect is in play, the Monster\'s Attack x 3.',

'chi_lead':'机械理论\n\n'
'队伍中只有机械族或人类成员时：\n'
'I. 全队攻击力 4.5 倍\n'
'II. 减少 40% 所受伤害\n'
'III. 消除水强化符石时\n'
'⇒ 机械族成员的行动值提升 5%\n'
'IV. 所有机械族成员的行动值达至 100% 时\n'
'⇒ 攻击力额外 1.5 倍',
'eng_lead':'Theory of Machines\n\n'
'When the Team consists of only Machinas and Humans, Team Attack x 4.5; Damage received -40%; by dissolving Enchanted Water Runestones, Fuel of Machinas +5%; when all Machinas in the Team have 100% Fuel, Team Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'若当前回合总伤害大于敌方总生命力 2.5 倍等值，下回合全队攻击力提升 2 倍\n'
'回合结束时，引爆水符石四周的水以外符石\n'
'水符石兼具 50% 心符石效果\n'
'进入关卡后，机械族成员的主动技能 CD 减少 3\n'
'发动条件：\n'
'以时空相对论 ‧ 爱因斯坦作队长及战友\n\n'
'【机械动力】\n'
'I. 每首批消除 1 粒自身属性符石\n'
'⇒ 自身行动值提升 2%\n'
'II. 每首批消除 1 粒心符石\n'
'⇒ 自身行动值提升 1%\n'
'III. 行动值愈高\n'
'⇒ 自身攻击力提升愈多\n'
'⇒ 最大提升至 2 倍。\n'
'IV. 当所有机械族成员的行动值达至 50% 或以上时\n'
'⇒ 机械族成员属性的符石效果提升\n'
'⇒ 每个机械族成员可提升 10% 效果\n'
'⇒ 最高 60%\n'
'V. 当所有机械族成员的行动值达至 100% 时\n'
'⇒ 机械族成员每回合\n'
'以 25% 自身攻击力随机追打自身属性或自身克制属性的攻击 1 至 2 次\n'
'发动条件：\n'
'队伍中有 ≥2 个【机械族】成员',
'eng_team':'Team Skill:\n\n'
'◆ When the total Damage dealt in the Round is more than 2.5x of the enemy\'s total HP, Team Attack x 2 additionally in the next Round.\n'
'◆ Explode non-Water Runestones around Water Runestones at the end of each Round.\n'
'◆ Water Runestones also possess 50% effect of Heart Runestones. After entering a Stage, Active Skill CDs of Machinas -3.\n'
'Condition:\n'
'Both the Leader and Ally are "Relativity of Cosmology - Einstein".\n\n'
'◆ 【Machina Dynamics】\n'
'⓵ For each Runestone of the Character\'s Attribute dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +2%.\n'
'⓶ For each Heart Runestone dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +1%.\n'
'⓷ The higher the Character\'s Fuel,\n'
'⇒ the higher the Character\'s Attack,\n'
'⇒ to the max x 2 additionally.\n'
'⓸ When all Machinas in the Team have ≥ 50% Fuel,\n'
'⇒ effects of Runestones of their Attributes increase,\n'
'⇒ 10% for each Machina present in the Team,\n'
'⇒ to the max 60%.\n'
'⓹ When all Machinas in the Team have 100% Fuel,\n'
'⇒ all Machinas randomly launch 1 to 2 extra attack(s) of its own Attribute or its Counter Attribute as much as 25% of its Attack every Round.\n'
'Condition:\n'
'There are 2 or more 【Machina Dynamics】 Members in the Team.'},
    
    {'chi_name':'伽利略',
'chif_name':'伽利略',
'eng_name':'galileo',

'chi_act':'机械解密 CD6\n\n'
'解除机械族成员被封锁的技能 (此技能无视封锁技能)。3 回合内，机械族成员的攻击力及回复力 1.8 倍；发动技能时若所有机械族成员的行动值达至 100%，延长移动符石时间至 15 秒',
'eng_act':'	Machine Decoder CD6\n\n'
'Release the locked Skills of all Machinas. For 3 Rounds, Machina Attack & Recovery x 1.8; when all Machinas in the Team have 100% Fuel upon Skill activation, extend Runestone-moving time to 15 seconds. This Skill will not be locked.',

'chi_lead':'几何结界\n\n'
'队伍中只有机械族成员时：\n'
'I. 全队攻击力 5 倍\n'
'II. 必然延长移动符石时间 1 秒\n'
'III. 自身的攻击力减至 0 并将原有的攻击力基值的 2 倍\n'
'⇒ 分别加入其他成员的攻击力基值\n'
'IV. 若使用相同的队长及战友\n'
'⇒ 则分别加入所有队员的攻击力基值\n'
'V. 于自身直行首批消除 1 组 ≥4 粒符石时\n'
'⇒ 身旁成员的主动技能 CD 减少 1',
'eng_lead':'Dimension of Geometry\n\n'
'When the Team has only Machinas,\n'
'I. Team Attack x 5.\n'
'II. Extend Runestone-moving time regardlessly by 1 second.\n'
'III. The Character\'s Attack becomes 0, adding 2x the deducted Attack basic value to the Attack basic value of all Members\n'
'IV. If the Leader and Ally are the same, the deducted Attack basic value will be added to the Attack basic value of all Members (Leader and Ally excluded)\n'
'V. By dissolving a group of ≥4 Runestones in the column below the Monster, Active Skill CD of the neighboring Member(s) -1.',

'chi_team':'队伍技能：\n\n'
'每首批消除 1 粒火、木或暗符石，额外提升机械族成员的行动值 1%\n'
'发动条件：\n'
'以生物多样性 ‧ 达尔文或超新星序曲 ‧ 伽利略作队长及战友；或以生物多样性 ‧ 达尔文作队长及战友\n\n'
'【机械动力】\n'
'I. 每首批消除 1 粒自身属性符石\n'
'⇒ 自身行动值提升 2%\n'
'II. 每首批消除 1 粒心符石\n'
'⇒ 自身行动值提升 1%\n'
'III. 行动值愈高\n'
'⇒ 自身攻击力提升愈多\n'
'⇒ 最大提升至 2 倍。\n'
'IV. 当所有机械族成员的行动值达至 50% 或以上时\n'
'⇒ 机械族成员属性的符石效果提升\n'
'⇒ 每个机械族成员可提升 10% 效果\n'
'⇒ 最高 60%\n'
'V. 当所有机械族成员的行动值达至 100% 时\n'
'⇒ 机械族成员每回合\n'
'以 25% 自身攻击力随机追打自身属性或自身克制属性的攻击 1 至 2 次\n'
'发动条件：\n'
'队伍中有 ≥2 个【机械族】成员',
'eng_team':'Team Skill:\n\n'
'◆ Fuel of Machinas +1% for each Fire, Earth or Dark Runestone dissolved (only the first batch of Runestones dissolved will be counted).\n'
'Condition:\n'
'The Leader and Ally are "Mutated Biodiversity - Darwin" or "Prologue of Supernova - Galileo".\n\n'
'◆ 【Machina Dynamics】\n'
'⓵ For each Runestone of the Character\'s Attribute dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +2%.\n'
'⓶ For each Heart Runestone dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +1%.\n'
'⓷ The higher the Character\'s Fuel,\n'
'⇒ the higher the Character\'s Attack,\n'
'⇒ to the max x 2 additionally.\n'
'⓸ When all Machinas in the Team have ≥ 50% Fuel,\n'
'⇒ effects of Runestones of their Attributes increase,\n'
'⇒ 10% for each Machina present in the Team,\n'
'⇒ to the max 60%.\n'
'⓹ When all Machinas in the Team have 100% Fuel,\n'
'⇒ all Machinas randomly launch 1 to 2 extra attack(s) of its own Attribute or its Counter Attribute as much as 25% of its Attack every Round.\n'
'Condition:\n'
'There are 2 or more 【Machina Dynamics】 Members in the Team.'},
    
    {'chi_name':'达尔文',
'chif_name':'達爾文',
'eng_name':'darwin',

'chi_act':'元素探研 CD6\n\n'
'引爆所有符石以掉落强化符石，每引爆 1 种属性符石，1 回合内自身攻击力额外提升 1 倍，最多可提升至 6 倍；消除 5 种属性符石时，自身主动技能 CD 减少 3',
'eng_act':'Experiment of Elements CD6\n\n'
'Explode all Runestones to generate Enchanted Runestones. For 1 Round, the more the Attributes of Runestones exploded, the higher the Monster\'s Attack, to the max x 6. When Runestones of 5 Attributes are dissolved, the Monster\'s current Skill CD -3.',

'chi_lead':'金液流动\n\n'
'队伍中只有机械族成员时：\n'
'I. 全队生命力、攻击力及回复力 2 倍\n'
'II. 消除 ≥3 种符石时\n'
'⇒ 全队攻击力额外 3 倍\n'
'III. 心符石兼具 50% 所有属性符石效果(可叠加)',
'eng_lead':'Flow of Golden Liquid\n\n'
'When the Team consists of only Machinas, Team HP, Attack & Recovery x 2; by dissolving Runestones of 3 or more types, Team Attack x 3 additionally; Heart Runestones also possess 50% effects of all Attributive Runestones (the effects can be superimposed).',

'chi_team':'队伍技能：\n\n'
'每首批消除 1 粒火、木或暗符石，额外提升机械族成员的行动值 1%\n'
'发动条件：\n'
'以生物多样性 ‧ 达尔文或超新星序曲 ‧ 伽利略作队长及战友；或以生物多样性 ‧ 达尔文作队长及战友\n\n'
'【机械动力】\n'
'I. 每首批消除 1 粒自身属性符石\n'
'⇒ 自身行动值提升 2%\n'
'II. 每首批消除 1 粒心符石\n'
'⇒ 自身行动值提升 1%\n'
'III. 行动值愈高\n'
'⇒ 自身攻击力提升愈多\n'
'⇒ 最大提升至 2 倍。\n'
'IV. 当所有机械族成员的行动值达至 50% 或以上时\n'
'⇒ 机械族成员属性的符石效果提升\n'
'⇒ 每个机械族成员可提升 10% 效果\n'
'⇒ 最高 60%\n'
'V. 当所有机械族成员的行动值达至 100% 时\n'
'⇒ 机械族成员每回合\n'
'以 25% 自身攻击力随机追打自身属性或自身克制属性的攻击 1 至 2 次\n'
'发动条件：\n'
'队伍中有 ≥2 个【机械族】成员',
'eng_team':'Team Skill:\n\n'
'◆ Fuel of Machinas +1% for each Fire, Earth or Dark Runestone dissolved (only the first batch of Runestones dissolved will be counted).\n'
'Condition:\n'
'The Leader and Ally are "Mutated Biodiversity - Darwin" or "Prologue of Supernova - Galileo".\n\n'
'◆ 【Machina Dynamics】\n'
'⓵ For each Runestone of the Character\'s Attribute dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +2%.\n'
'⓶ For each Heart Runestone dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +1%.\n'
'⓷ The higher the Character\'s Fuel,\n'
'⇒ the higher the Character\'s Attack,\n'
'⇒ to the max x 2 additionally.\n'
'⓸ When all Machinas in the Team have ≥ 50% Fuel,\n'
'⇒ effects of Runestones of their Attributes increase,\n'
'⇒ 10% for each Machina present in the Team,\n'
'⇒ to the max 60%.\n'
'⓹ When all Machinas in the Team have 100% Fuel,\n'
'⇒ all Machinas randomly launch 1 to 2 extra attack(s) of its own Attribute or its Counter Attribute as much as 25% of its Attack every Round.\n'
'Condition:\n'
'There are 2 or more 【Machina Dynamics】 Members in the Team.'},
    
    {'chi_name':'达尔文',
'chif_name':'達爾文',
'eng_name':'darwin',

'chi_act':'元素探研 CD6\n\n'
'引爆所有符石以掉落强化符石，每引爆 1 种属性符石，1 回合内自身攻击力额外提升 1 倍，最多可提升至 6 倍；消除 5 种属性符石时，自身主动技能 CD 减少 3',
'eng_act':'Experiment of Elements CD6\n\n'
'Explode all Runestones to generate Enchanted Runestones. For 1 Round, the more the Attributes of Runestones exploded, the higher the Monster\'s Attack, to the max x 6. When Runestones of 5 Attributes are dissolved, the Monster\'s current Skill CD -3.',

'chi_lead':'金液流动\n\n'
'队伍中只有机械族成员时：\n'
'I. 全队生命力、攻击力及回复力 2 倍\n'
'II. 消除 ≥3 种符石时\n'
'⇒ 全队攻击力额外 3 倍\n'
'III. 心符石兼具 50% 所有属性符石效果(可叠加)',
'eng_lead':'Flow of Golden Liquid\n\n'
'When the Team consists of only Machinas, Team HP, Attack & Recovery x 2; by dissolving Runestones of 3 or more types, Team Attack x 3 additionally; Heart Runestones also possess 50% effects of all Attributive Runestones (the effects can be superimposed).',

'chi_team':'队伍技能：\n\n'
'每首批消除 1 粒火、木或暗符石，额外提升机械族成员的行动值 1%\n'
'发动条件：\n'
'以生物多样性 ‧ 达尔文或超新星序曲 ‧ 伽利略作队长及战友；或以生物多样性 ‧ 达尔文作队长及战友\n\n'
'【机械动力】\n'
'I. 每首批消除 1 粒自身属性符石\n'
'⇒ 自身行动值提升 2%\n'
'II. 每首批消除 1 粒心符石\n'
'⇒ 自身行动值提升 1%\n'
'III. 行动值愈高\n'
'⇒ 自身攻击力提升愈多\n'
'⇒ 最大提升至 2 倍。\n'
'IV. 当所有机械族成员的行动值达至 50% 或以上时\n'
'⇒ 机械族成员属性的符石效果提升\n'
'⇒ 每个机械族成员可提升 10% 效果\n'
'⇒ 最高 60%\n'
'V. 当所有机械族成员的行动值达至 100% 时\n'
'⇒ 机械族成员每回合\n'
'以 25% 自身攻击力随机追打自身属性或自身克制属性的攻击 1 至 2 次\n'
'发动条件：\n'
'队伍中有 ≥2 个【机械族】成员',
'eng_team':'Team Skill:\n\n'
'◆ Fuel of Machinas +1% for each Fire, Earth or Dark Runestone dissolved (only the first batch of Runestones dissolved will be counted).\n'
'Condition:\n'
'The Leader and Ally are "Mutated Biodiversity - Darwin" or "Prologue of Supernova - Galileo".\n\n'
'◆ 【Machina Dynamics】\n'
'⓵ For each Runestone of the Character\'s Attribute dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +2%.\n'
'⓶ For each Heart Runestone dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +1%.\n'
'⓷ The higher the Character\'s Fuel,\n'
'⇒ the higher the Character\'s Attack,\n'
'⇒ to the max x 2 additionally.\n'
'⓸ When all Machinas in the Team have ≥ 50% Fuel,\n'
'⇒ effects of Runestones of their Attributes increase,\n'
'⇒ 10% for each Machina present in the Team,\n'
'⇒ to the max 60%.\n'
'⓹ When all Machinas in the Team have 100% Fuel,\n'
'⇒ all Machinas randomly launch 1 to 2 extra attack(s) of its own Attribute or its Counter Attribute as much as 25% of its Attack every Round.\n'
'Condition:\n'
'There are 2 or more 【Machina Dynamics】 Members in the Team.'},
    
    {'chi_name':'夏娃',
'chif_name':'夏娃',
'eng_name':'eve',

'chi_act':'禁果之惑 CD3\n'
'火及心符石转化为魔族强化符石，若队长及战友均为“魔性原罪 · 夏娃”时，所有“魔性原罪 · 夏娃”获得 1 个禁果\n\n'
'亲尝禁果 CD3\n'
'若队长及战友均为“魔性原罪 · 夏娃”时，消耗战友的 2 个禁果以发动技能：1 回合内，火属性及魔族攻击力 2.2 倍，“魔性原罪 · 夏娃”的攻击无视敌人防御力',
'eng_act':'The Forbidden Temptation CD3\n'
'Turn Fire and Heart Runestones into Enchanted Demon Runestones. When both the Leader and Ally are "Origin of All Sins - Eve", all "Origin of All Sins - Eve" in the Team gets a Forbidden Fruit.\n\n'
'Taste of Forbidden Fruit CD3\n'
'When both the Leader and Ally are "Origin of All Sins - Eve", the Skill can be activated at the expense of 2 Forbidden Fruits of the Ally. For 1 Round, Fire Attack and Demon Attack x 2.2, Damage of "Origin of All Sins - Eve" in the Team will be dealt regardless of enemies\' Defense.',

'chi_lead':'魔念之罪\n\n'
'队伍中只有魔族或妖精类成员时：\n'
'I. 全队攻击力 6 倍及生命力 2 倍\n'
'II. 所有属性符石兼具25% 其他属性符石效果 (可叠加)\n'
'III. 每回合回复相等于队伍中所有“魔性原罪 · 夏娃”攻击力基值总和的生命力(需消除符石)',
'eng_lead':'The Original Sin\n\n'
'When the Team consists of only Demons and Elves, Team Attack x 6, HP x 2, all Attributive Runestones also possess 25% effects of other Attributive Runestones (effects can be superimposed), recover HP as much as the total Attack basic value of "Origin of All Sins - Eve" in the Team each Round (dissolving Runestones is necessary).',

'chi_team':'队伍技能：\n\n'
'每消除 1 组 5 粒或以上的心或火符石时，1 个魔性原罪 · 夏娃 (最左方优先) 获得 1 个禁果，消除 2 组可获最多 2 个禁果。 魔性原罪 · 夏娃最多可同时持有 4 个禁果,每持有 1 个禁果，于回合结束时，随机转化 1 粒魔族符石，最多 24 粒。\n'
'持有 4 个禁果的魔性原罪 · 夏娃在发动攻击时，额外追打无属性攻击 1 次。\n'
'魔性原罪 · 夏娃持有禁果时，全队攻击力提升 1.3 倍\n'
'发动条件：\n'
'以魔性原罪 · 夏娃作队长及战友\n\n'
'必然延长移动符石时间 2 秒。\n'
'移动符石时触碰的火、光、暗符石转化为魔族强化符石\n'
'发动条件：\n'
'以魔性原罪 · 夏娃或艳后争鸣 · 克丽奥作队长及战友；或以魔性原罪 · 夏娃作队长及战友\n\n'
'I. 进入关卡后，“魔性原罪 · 夏娃”\n'
'⇒ 增加 2,000 点攻击力基值\n'
'II. 队长右旁的魔族成员的攻击力基值跟随队长\n'
'发动条件：\n'
'以魔性原罪 · 夏娃作队长及战友，且队伍中只有妖精类或魔族成员\n\n'
'“炙烈熔岩 ‧ 克鲁非”\n'
'⓵“生命力及攻击力”基值 2 倍\n'
'⓶ 技能 CD -1\n'
'发动条件：\n'
'以“炙烈熔岩 ‧ 克鲁非”及；“魔性原罪 · 夏娃”或“澜漫勾惑 ‧ 夏娃”作成员\n\n'
'I. 进入关卡后\n'
'⓵ 所有“魔性原罪 · 夏娃”\n'
'⇒ 获得 2 个禁果\n'
'⓶ 所有“澜漫勾惑 ‧ 夏娃”\n'
'⇒ 获得 2 个金果\n'
'II.“魔性原罪 · 夏娃”及“澜漫勾惑 ‧ 夏娃”\n'
'⇒ 增加 1,500 点攻击力基值\n'
'发动条件：\n'
'以“魔性原罪 · 夏娃”作队长及战友，以“澜漫勾惑 ‧ 夏娃”作成员',
'eng_team':'Team Skill:\n\n'
'◆ By dissolving a group of 5 or more Heart or Fire Runestones, the first "Origin of All Sins - Eve" from the left gets a Forbidden Fruit, to the max 2 Forbidden Fruits for 2 groups of Runestones dissolved. Each "Origin of All Sins - Eve" in the Team can possess at most 4 Forbidden Fruits at a time. Turn 1 Runestone into Demon Runestone at the end of the Round for each Forbidden Fruit in hand, to the max 24 Runestones to be turned.\n'
'◆ For "Origin of All Sins - Eve" who has 4 Forbidden Fruits, the Monster launches an extra non-Attributive attack.\n'
'◆ When "Origin of All Sins - Eve" is having Forbidden Fruits, Team Attack x 1.3 additionally.\n'
'Condition:\n'
'Both the Leader and Ally are "Origin of All Sins - Eve".\n\n'

'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'◆ Turn all Fire, Light and Dark Runestones touched while moving into Enchanted Demon Runestones.\n'
'Condition:\n'
'The Leader and Ally are "Origin of All Sins - Eve" or "Diva of Obsession - Cleo".\n\n'

'◆ After entering a Stage:\n'
'⓵ All "Origin of All Sins - Eve" get 2 Forbidden Fruits.\n'
'⓶ All "Innocent Temptation - Eve" get 2 Golden Fruits.\n'
'◆ "Origin of All Sins - Eve” and "Innocent Temptation - Eve"\n'
'⇒ Attack basic value +1,500.\n'
'Condition:\n'
'Both the Leader and Ally are "Origin of All Sins - Eve", with "Innocent Temptation - Eve" in the Team.\n\n'

'◆ "Diabolic Magma - Cherufe"\n'
'⓵ HP & Attack basic value x 2.\n'
'⓶ Skill CD -1.\n'
'Condition:\n'
'There are "Diabolic Magma - Cherufe" and "Origin of All Sins - Eve" or "Innocent Temptation - Eve" in the Team.\n'

'◆ Attack basic value of "Origin of All Sins - Eve" +2000 after entering a Stage.\n'
'◆ Attack basic value of the Demon to the right of the Leader will synchronize with that of the first "Origin of All Sins - Eve" from the left.\n'
'Condition:\n'
'Both the Leader and Ally are "Origin of All Sins - Eve", with only Elves or Demons in the Team.'},

    {'chi_name':'武则天',
'chif_name':'武則天',
'eng_name':'wuzetian',

'chi_act':'集权之谋 CD8\n\n'
'引爆队伍成员属性以外的符石，以掉落强化符石。1 回合内，延长移动符石时间至 12 秒；每首批消除 2 组符石，魔族及光属性成员以 30% 自身攻击力追打光属性攻击 1 次，最多可追打 5 次',
'eng_act':'Scheme for Authority CD8\n\n'
'Explode Runestones not of Team Members\' Attributes to generate Enchanted Runestones. For 1 Round, extend Runestone-moving time to 12 seconds. For every 2 groups of Runestones dissolved, each Demon and Light Member in the Team launch an extra Light attack as much as 30% of its own attack, to the max 5 extra attacks to be launched by each Monster (only the first batch of Runestones dissolved will be counted)',

'chi_lead':'魔曌之势\n\n'
'队伍中只有魔族成员时：\n'
'I. 魔族攻击力 4 倍，光属性魔族攻击力则 5 倍\n'
'II. 消除魔族符石时\n'
'⇒ 全队攻击力额外 2 倍',
'eng_lead':'Dominance of the Empress\n\n'
'When the Team consists of only Demons, Demon Attack x 4, Light Demon Attack x 5, by dissolving Demon Runestones, Team Attack x 2 additionally.',

'chi_team':'队伍技能：\n\n'
'队长的队长技能“魔曌之势”变为“魔曌之势 ‧ 强”：队伍中只有魔族成员时：魔族攻击力 4 倍，光属性魔族攻击力则 5 倍；消除魔族符石时，全队攻击力额外提升 2 倍。若转珠结束时放手的符石为属性符石：该种属性符石兼具其他符石效果，移动符石时触碰的首 5 粒符石转化为该属性魔族强化符石。减少 90% 所受伤害，受到 5 次攻击后变为减少 45% 所受伤害\n'
'发动条件：\n'
'以后仪天下 · 武则天作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Change the Leader Skill of the Leader from "Dominance of the Empress" to "Dominance of the Empress - EX".\n'
'When the Team has only Demons, Demon Attack x 4, Light Demon Attack x 5, by dissolving Demon Runestones, Team Attack x 2 additionally. When the last Runestone you let go to end moving is an Attributive Runestone, Runestones of that Attribute also possess the effect of other Runestones, turn the first 5 Runestones touched while moving into Enchanted Demon Runestones of that Attribute. Damage received -90% for the first 5 Damage received. After that, Damage received -45%.\n'
'Condition:\n'
'Both the Leader and Ally are "Militant Heroine - Wu Zetian".'},
    
    {'chi_name':'克丽奥',
'chif_name':'克麗奧',
'eng_name':'cleo',

'chi_act':'翩跹起舞 CD6\n\n'
'点选 2 直行的符石，将之转化为暗魔族强化符石，1 回合内，魔族及妖精类攻击力 2 倍',
'eng_act':'Top of the Pyramid CD6\n\n'
'Tap and turn 2 columns of Runestones into Enchanted Dark Demon Runestones. For 1 Round, Demon and Elf Attack x 2.',

'chi_lead':'倾世魅颜\n\n'
'队伍中只有魔族或妖精类成员时：\n'
'I. 全队生命力、攻击力及回复力 1.5 倍\n'
'II. 每首批消除 1 个角落的符石时\n'
'⇒ 全队攻击力提升 1.25 倍\n'
'⇒ 4 个角落可达至最大 5 倍',
'eng_lead':'Beauty of the World\n\n'
'When the Team consists of only Demons and Elves, Team Attack, HP & Recovery x 1.5, by dissolving a Runestone in a corner, Team Attack x 1.25 additionally, to the max x 5 for dissolving Runestones in 4 corners (only the first batch of Runestones dissolved will be counted).',

'chi_team':'队伍技能：\n\n'
'必然延长移动符石时间 2 秒。\n'
'移动符石时触碰的火、光、暗符石转化为魔族强化符石\n'
'发动条件：\n'
'以魔性原罪 · 夏娃或艳后争鸣 · 克丽奥作队长及战友，或以艳后争鸣 · 克丽奥作队长及战友\n\n'
'下回合开始时，将 4 个角落的符石转化为暗魔族符石。\n'
'每消除 1 粒魔族符石，该回合减少 10% 所受伤害，最多减少 60%\n'
'发动条件：\n'
'以艳后争鸣 · 克丽奥作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'◆ Turn all Fire, Light and Dark Runestones touched while moving into Enchanted Demon Runestones.\n'
'Condition:\n'
'The Leader and Ally are "Origin of All Sins - Eve" or "Diva of Obsession - Cleo".\n\n'
'◆ Turn Runestones in the 4 corners into Dark Demon Runestones at the beginning of each Round.\n'
'◆ Damage received -10% for each Demon Runestone dissolved, to the max -60%.\n'
'Condition:\n'
'Both the Leader and Ally are "Diva of Obsession - Cleo".'},
    
   {'chi_name':'女娲',
'chif_name':'女媧',
'eng_name':'nuwa',

'chi_act':'五色秘术 CD6\n\n'
'1 回合内\n'
'I. 每消除 1 组符石\n'
'⇒ 额外计算多 2 连击 (Ex. Combo)\n'
'⇒ 最多可额外增加 20 连击 (Ex. Combo）\n'
'II. 发动技能时若自身“仙力”达 10 点\n'
'⓵ 效果则持续 2 回合\n'
'⓶ 最多可增加 30 个 Ex. Combo\n'
'III. 若队长或战友为“上古诸神”成员\n'
'⇒ 额外增加 1 回合效果',
'eng_act':'Magic of Five Elements CD6\n\n'
'For 1 Round:\n'
'I. Ex. Combo count +2 for every group of Runestones dissolved, to the max Ex. Combo count +20.\n'
'II. If the Monster\'s Xian Point (XP) is 10 upon Skill activation:\n'
'⓵ The Skill stays in play for 2 Rounds.\n'
'⓶ Ex. Combo count to the max +30.\n'
'III. If the Leader or Ally is a Monster of "Primal Deities", the Skill stays in play for 1 more Round.',

'chi_lead':'补天炼石\n\n'
'队伍中只有神族或兽类成员时：\n'
'I. 全队攻击力 6 倍及回复力 2 倍\n'
'II. 队中每有 1 个 6 星“上古诸神”系列角色\n'
'⇒ 必然延长移动符石时间 1 秒\n'
'III. 消除神族符石时\n'
'⇒ 神族及兽类攻击力额外 2 倍',
'eng_lead':'Repairing the Heaven\n\n'
'When the Team consists of only Gods and Beasts:\n'
'I. Team Attack x 6, Recovery x 2.\n'
'II. Extend Runestone-moving by 1 second for each 6* Monster of "Primal Deities" present in the Team.\n'
'III. By dissolving God Runestones, Team Attack x 2 additionally.',

'chi_team':'队伍技能：\n\n'
'每消除 1 粒木神族符石\n'
'⇒ 自身可累积 1 点“仙力”\n'
'⇒ 最多可累积 20 点。\n'
'每受敌人攻击 1 次\n'
'⇒ 减少 2 点“仙力”\n'
'发动条件：\n'
'以“创世神女 ‧ 女娲”作成员\n\n'

'I. 将移动符石时触碰的队伍成员属性符石\n'
'⇒ 转化为神族强化符石\n'
'II. 光符石兼具 50% 其他属性符石效果\n'
'III. 暗符石兼具 50% 其他属性符石效果\n'
'发动条件：\n'
'以“创世神女 ‧ 女娲”或“太昊八卦 ‧ 伏羲”作队长及战友；或以“创世神女 ‧ 女娲”作队长及战友\n\n'

'每个“上古诸神”系列角色均有几率暴击 2.5 倍：\n'
'其“仙力”愈高\n'
'⇒ 其暴击率愈高\n'
'⇒ 10 点“仙力”可提升至 100%\n'
'发动条件：\n'
'以 6 星“上古诸神”系列角色作队长及战友\n\n'

'“百草药神 ‧ 神农”、“舞干戚 ‧ 刑天”、“开天辟地 ‧ 盘古”跟随队长的暴击率，有几率可暴击 2.5 倍\n'
'发动条件：\n'
'以 6 星“上古诸神”系列角色作队长及战友；且队伍中有 3 个或以上 6 星“上古诸神”系列角色；并以“百草药神 ‧ 神农”、“舞干戚 ‧ 刑天”或“开天辟地 ‧ 盘古”作队员',
'eng_team':'Team Skill:\n\n'
'◆ For each Monster of "Primal Deities" in the Team, there is a chance of Critical Attack x 2.5. The higher the Xian Point (XP), the higher the Critical Rate, to the max 100% for 10 XP.\n'
'Condition:\n'
'The Leader and Ally are 6 star Characters of "Primal Deities" (series).\n\n'

'◆ For 6 star Monsters of "Primal Deities" in the Team, the Monster\'s Xian Point (XP) +1 for every Runestone of its Race and Attribute dissolved, to the max 20 XP in accumulation. XP -2 every time when receiving Damage from an enemy\'s attack.\n'
'Condition:\n'
'There is 6 star Characters of "Primal Deities" (series) in the Team.\n\n'

'◆ Turn Runestones of Members\' Attributes touched while moving into Enchanted God Runestones.\n'
'◆ Light Runestones also possess 50% effect of other Attributive Runestones.\n'
'◆ Dark Runestones also possess 50% effect of other Attributive Runestones.\n'
'Condition:\n'
'The Leader and Ally are "Primal Divinity - Fuxi" or "Ancestral Creation - Nüwa".\n\n'

'◆ Critical Rate of "Mastery of Herbs - Shennong", "Traitor of Goodwill - Xingtian" and "Primitive Creator - Pangu" will synchronize with that of the Leader, with a chance of Critical Attack x 2.5.\n'
'Condition:\n'
'Both the Leader and Ally are 6 star Characters of "Primal Deities" (series), with 3 or more 6 star Characters of "Primal Deities" (series) and "Mastery of Herbs - Shennong", "Traitor of Goodwill - Xingtian", or "Primitive Creator - Pangu" in the Team.'},
    
{'chi_name':'伏羲',
'chif_name':'伏羲',
'eng_name':'fuxi',

'chi_act':'智慧之火 CD7\n\n'
'I. 神族成员直行的符石\n'
'⇒ 添加为神族符石\n'
'II. 兽类成员直行的符石\n'
'⇒ 添加为兽族符石\n'
'III. 15 秒内，可任意移动符石而不会发动消除\n'
'IV. 发动技能时若自身“仙力”达 10 点\n'
'⇒ 1 回合内，全队攻击力及回复力 2 倍',
'eng_act':'Flames of Wisdom CD7\n\n'
'I. Modify the column(s) of Runestones below God(s) to become God Runestones.\n'
'II. Turn the column(s) of Runestones below Beast(s) into Beast Runestones.\n'
'III. Unlimited Runestone movement without dissolving within 15 seconds.\n'
'IV. If the Monster\'s Xian Point (XP) is 10 upon Skill activation, Team Attack & Recovery x 2 for 1 Round.',

'chi_lead':'乾坤太极阵\n\n'
'队伍中只有神族或兽类成员时：\n'
'I. 全队攻击力 4.5 倍、生命力及回复力 1.4 倍\n'
'II. 队伍中有 ≥3 种属性成员时\n'
'⇒ 全队攻击力额外 2 倍\n'
'III. 消除神族符石时\n'
'⇒ 神族及兽类攻击力额外 1.5 倍',
'eng_lead':'Magic Field of Taiji\n\n'
'When the Team consists of only Gods and Beasts:\n'
'I. Team Attack x 4.5, HP & Recovery x 1.4.\n'
'II. When there are 3 or more Attributes in the Team, Team Attack x 2 additionally.\n'
'III. By dissolving God Runestones, Team Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'每消除 1 粒火神族符石\n'
'⇒ 自身可累积 1 点“仙力”\n'
'⇒ 最多可累积 20 点。\n'
'每受敌人攻击 1 次\n'
'⇒ 减少 2 点“仙力”\n'
'发动条件：\n'
'以“太昊八卦 ‧ 伏羲”作成员\n\n'

'I. 将移动符石时触碰的队伍成员属性符石\n'
'⇒ 转化为神族强化符石\n'
'II. 光符石兼具 50% 其他属性符石效果\n'
'III. 暗符石兼具 50% 其他属性符石效果\n'
'发动条件：\n'
'以“创世神女 ‧ 女娲”或“太昊八卦 ‧ 伏羲”作队长及战友\n\n'

'每个“上古诸神”系列角色均有几率暴击 2.5 倍：\n'
'其“仙力”愈高\n'
'⇒ 其暴击率愈高\n'
'⇒ 10 点“仙力”可提升至 100%\n'
'发动条件：\n'
'以 6 星“上古诸神”系列角色作队长及战友\n\n'

'“百草药神 ‧ 神农”、“舞干戚 ‧ 刑天”、“开天辟地 ‧ 盘古”跟随队长的暴击率，有几率可暴击 2.5 倍\n'
'发动条件：\n'
'以 6 星“上古诸神”系列角色作队长及战友，且队伍中有 3 个或以上 6 星“上古诸神”系列角色；并以“百草药神 ‧ 神农”、“舞干戚 ‧ 刑天”或“开天辟地 ‧ 盘古”作队员',
'eng_team':'Team Skill:\n\n'
'◆ For each Monster of "Primal Deities" in the Team, there is a chance of Critical Attack x 2.5. The higher the Xian Point (XP), the higher the Critical Rate, to the max 100% for 10 XP.\n'
'Condition:\n'
'The Leader and Ally are 6 star Characters of "Primal Deities" (series).\n\n'

'◆ For 6 star Monsters of "Primal Deities" in the Team, the Monster\'s Xian Point (XP) +1 for every Runestone of its Race and Attribute dissolved, to the max 20 XP in accumulation. XP -2 every time when receiving Damage from an enemy\'s attack.\n'
'Condition:\n'
'There is 6 star Characters of Primal Deities series in the Team.\n\n'

'◆ Turn Runestones of Members\' Attributes touched while moving into Enchanted God Runestones.\n'
'◆ Light Runestones also possess 50% effect of other Attributive Runestones.\n'
'◆ Dark Runestones also possess 50% effect of other Attributive Runestones.\n'
'Condition:\n'
'The Leader and Ally are "Primal Divinity - Fuxi" or "Ancestral Creation - Nüwa".\n\n'

'◆ Critical Rate of "Mastery of Herbs - Shennong", "Traitor of Goodwill - Xingtian" and "Primitive Creator - Pangu" will synchronize with that of the Leader, with a chance of Critical Attack x 2.5.\n'
'Condition:\n'
'Both the Leader and Ally are 6 star Characters of "Primal Deities" (series), with 3 or more 6 star Characters of "Primal Deities" (series) and "Mastery of Herbs - Shennong", "Traitor of Goodwill - Xingtian", or "Primitive Creator - Pangu" in the Team.'},
    
    {'chi_name':'西王母',
'chif_name':'西王母',
'eng_name':'xiwangmu',

'chi_act':'蟠桃盛宴 CD3\n\n'
'1 回合内\n'
'I. 连击 (Ex. Combo) 数目增加 3\n'
'II. 自身以外“上古诸神”系列角色的“仙力”增加 5 点\n'
'II. 将战友直行的符石\n'
'⇒ 转化为与自身直行相同的符石(包括强化符石、种族符石)\n'
'III. 若自身为战友\n'
'⇒ 则将自身直行的符石添加为神族符石\n'
'IV. 发动技能时若自身“仙力”达 10 点\n'
'⇒ 连击 (Ex. Combo) 数目额外增加 8',
'eng_act':'Peaches of Immortality CD3\n\n'
'For 1 Round\n'
'I. Ex. Combo count +3.\n'
'II. Xian Point (XP) of Monsters of "Primal Deities" (except this Monster) +5.\n'
'II. Turn the column of Runestones below the Ally into the column of Runestones below this Monster (the effects of Enchanted Runestones and Race Runestones apply).\n'
'III. If the Monster is the Ally, modify the column below the Monster to become God Runestones.\n'
'IV. If the Monster\'s XP is 10 upon Skill activation, Ex. Combo count +8.',

'chi_lead':'煞神之罚\n\n'
'队伍中只有神族或兽类成员时：\n'
'I. 全队攻击力 4.5 倍及生命力 1.6 倍\n'
'II. 消除 ≥5 粒神族符石时\n'
'⇒ 神族及兽类攻击力额外 2 倍',
'eng_lead':'Punishment of the Traitor\n\n'
'When the Team consists of only Gods and Beasts:\n'
'I. Team Attack x 4.5, HP x 1.6.\n'
'II. By dissolving 5 or more God Runestones, Team Attack x 2 additionally.',

'chi_team':'队伍技能：\n\n'
'每消除 1 粒光神族符石\n'
'⇒ 自身可累积 1 点“仙力”\n'
'⇒ 最多可累积 20 点。\n'
'每受敌人攻击 1 次\n'
'⇒ 减少 2 点“仙力”\n'
'发动条件：\n'
'以“瑶池婉妗 ‧ 西王母”作成员\n\n'
'于回合结束时，将队长直行的符石转化为光神族符石，若此时生命力全满，则转化为光神族强化符石\n'
'发动条件：\n'
'以“瑶池婉妗 ‧ 西王母”作队长及战友\n\n'
'“逐日旅程 ‧ 夸父”攻击力基值 1.8 倍\n'
'发动条件：\n'
'以“瑶池婉妗 ‧ 西王母”及“逐日旅程 ‧ 夸父”作成员\n\n'
'每个“上古诸神”系列角色均有几率暴击 2.5 倍：\n'
'其“仙力”愈高\n'
'⇒ 其暴击率愈高\n'
'⇒ 10 点“仙力”可提升至 100%\n'
'发动条件：\n'
'以 6 星“上古诸神”系列角色作队长及战友\n\n'
'“百草药神 ‧ 神农”、“舞干戚 ‧ 刑天”、“开天辟地 ‧ 盘古”跟随队长的暴击率，有几率可暴击 2.5 倍\n'
'发动条件：\n'
'以 6 星“上古诸神”系列角色作队长及战友；且队伍中有 3 个或以上 6 星“上古诸神”系列角色；并以“百草药神 ‧ 神农”、“舞干戚 ‧ 刑天”或“开天辟地 ‧ 盘古”作队员',
'eng_team':'Team Skill\n\n'
'◆ At the end of each Round, turn the column of Runestones below the Leader into Light God Runestones; if Team HP is full, the Runestones turned will become Enchanted Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Lady of the Supreme - Xiwangmu".\n\n'
'◆ Attack basic value of "Sun Chaser - Kuafu" x 1.8 additionally.\n'
'Condition:\n'
'There are "Lady of the Supreme - Xiwangmu" and "Sun Chaser - Kuafu" in the Team.\n\n'
'◆ For each Monster of "Primal Deities" in the Team, there is a chance of Critical Attack x 2.5. The higher the Xian Point (XP), the higher the Critical Rate, to the max 100% for 10 XP.\n'
'Condition:\n'
'The Leader and Ally are 6 star Characters of "Primal Deities" (series).\n\n'
'◆ For 6 star Monsters of "Primal Deities" in the Team, the Monster\'s Xian Point (XP) +1 for every Runestone of its Race and Attribute dissolved, to the max 20 XP in accumulation. XP -2 every time when receiving Damage from an enemy\'s attack.\n'
'Condition:\n'
'There is 6 star Characters of "Primal Deities" (series) in the Team.\n\n'
'◆ Critical Rate of "Mastery of Herbs - Shennong", "Traitor of Goodwill - Xingtian" and "Primitive Creator - Pangu" will synchronize with that of the Leader, with a chance of Critical Attack x 2.5.\n'
'Condition:\n'
'Both the Leader and Ally are 6 star Characters of "Primal Deities" (series), with 3 or more 6 star Characters of "Primal Deities" (series) and "Mastery of Herbs - Shennong", "Traitor of Goodwill - Xingtian", or "Primitive Creator - Pangu" in the Team.'},
    
{'chi_name':'钻石',
'chif_name':'鉆石',
'eng_name':'diamond',

'chi_act':'宝石游乐园 CD10\n\n'
'2 回合内\n'
'I. 全队攻击力 2 倍\n'
'II. 延长移动符石时间至 20 秒\n'
'III. 所受伤害减至 0(包括“喋血屠刀”、“一击必杀”等扣除召唤师指定 % 生命力的敌技所造成的伤害)',
'eng_act':'Playground of Diamonds CD10\n\n'
'For 2 Rounds:\n'
'I. Team Attack x 2.\n'
'II. Extend Runestone-moving time to 20 seconds.\n'
'III. Damage received will be lowered to 0.(applicable to Boss Skills deducting a specific % of Summoner\'s HP such as "Bloody Scythe" etc.)',

'chi_lead':'闪钻光华\n\n'
'队伍中有 ≥3 种属性成员时\n'
'I. 妖精类攻击力 6 倍\n'
'II. 心符石兼具 50% 所有属性符石效果\n'
'III. 必然延长移动符石时间 1 秒\n'
'IV. 妖精类成员\n'
'⇒ 对机械族以外目标攻击力 1.8 倍\n'
'⇒ 对人类、神族、魔族、妖精类目标攻击力额外 2.42 倍',
'eng_lead':'Glitter of Diamonds\n\n'
'When there are 3 or more Attributes in the Team:\n'
'I. Elf Attack x 6.\n'
'II. Heart Runestones also possess 50% effect of all Attributive Runestones.\n'
'III. Extend Runestone-moving time regardlessly by 1 second.\n'
'IV. Damage dealt by Elves on non-Machina enemies x 1.8, on Human, God, Demon and Elf enemies x 2.42 additionally.',

'chi_team':'队伍技能：\n\n'

'获得“结晶化”能力：\n'
'1 回合内\n'
'I. 妖精类攻击力 2 倍\n'
'II. 所受伤害减至 0(包括“喋血屠刀”、“一击必杀”等扣除召唤师指定 % 生命力的敌技所造成的伤害)\n'
'于回合开始时点击已储满的龙脉仪\n'
'⇒ 可触发“结晶化”能力(需消耗龙脉仪使用次数 1 次)\n'
'发动条件：\n'
'以“恒久闪耀 ‧ 钻石”作队长及战友\n\n'

'所有成员\n'
'⇒“生命力、攻击力及回复力”基值 2 倍\n'
'发动条件：\n'
'以“恒久闪耀 ‧ 钻石”作队长及战友，且队伍中只有妖精类成员\n\n'

'水及心符石互相兼具效果\n'
'发动条件：\n'
'以“恒久闪耀 ‧ 钻石”作队长及战友，并以“天穹倒影 ‧ 蓝宝石”作队员\n\n'

'火及心符石互相兼具效果\n'
'发动条件：\n'
'以“恒久闪耀 ‧ 钻石”作队长及战友，并以“肆妄火彩 ‧ 红宝石”作队员\n\n'

'木及心符石互相兼具效果\n'
'发动条件：\n'
'以“恒久闪耀 ‧ 钻石”作队长及战友，并以“不菲晶系 ‧ 祖母绿”作队员\n'

'光及心符石互相兼具效果\n'
'发动条件：\n'
'以“恒久闪耀 ‧ 钻石”作队长及战友，并以“织光成梦 ‧ 蛋白石”作队员\n'

'暗及心符石互相兼具效果\n'
'发动条件：\n'
'以“恒久闪耀 ‧ 钻石”作队长及战友，并以“刚刃蚀刻 ‧ 黑曜石”作队员',
'eng_team':'Team Skill:\n\n'
'◆ Acquire ”Crystallization“ Power:\n'
'For 1 Round:\n'
'I. Elf Attack x 2.\n'
'II. Damage received will be lowered to 0.(The Damage-reducing effect is applicable to Boss Skills deducting a specific % of Summoner\'s HP such as "Bloody Scythe" etc.)\n\n'
'◆ The Skill can be activated at the beginning of the Round by tapping the fully charged Craft Apparatus at the expense of one activation of Dragonic Compulsion.\n'
'Condition:\n'
'Both the Leader and Ally are "Paragon of Brilliance - Diamond".\n\n'

'◆ Team HP, Attack & Recovery basic value x 2 additionally.\n'
'Condition:\n'
'Both the Leader and Ally are "Paragon of Brilliance - Diamond", with only Elves in the Team.\n\n'

'◆ Heart and Water Runestones also possess the effects of each other.\n'
'Condition:\n'
'Both the Leader and Ally are "Paragon of Brilliance - Diamond", with "Timid Prodigy - Sapphire" in the Team.\n\n'

'◆ Heart and Fire Runestones also possess the effects of each other.\n'
'Condition:\n'
'Both the Leader and Ally are "Paragon of Brilliance - Diamond", with "Unbridled Ego - Ruby" in the Team.\n\n'

'◆ Heart and Earth Runestones also possess the effects of each other.\n'
'Condition:\n'
'Both the Leader and Ally are "Paragon of Brilliance - Diamond", with "Gem of Vitality - Emerald" in the Team.\n\n'

'◆ Heart and Light Runestones also possess the effects of each other.\n'
'Condition:\n'
'Both the Leader and Ally are "Paragon of Brilliance - Diamond", with "Dorky Dreamer - Opal" in the Team.\n\n'

'◆ Heart and Dark Runestones also possess the effects of each other.\n'
'Condition:\n'
'Both the Leader and Ally are "Paragon of Brilliance - Diamond", with "Volcanic Blade - Obsidian" in the Team.'},
    
    {'chi_name':'翡翠',
'chif_name':'翡翠',
'eng_name':'jade',

'chi_act':'翠碧猎捕 CD6\n\n'
'队长需为妖精类才可发动此技能：\n'
'每个妖精类成员以自身回复力的 3 倍\n'
'⇒ 各自加入自身攻击力(效果会在关闭此技能或死亡后消失)\n\n'
'此技能可随时关闭，关闭时：\n'
'⓵ 引爆所有符石以掉落强化符石\n'
'⓶ 完全回复生命力',
'eng_act':'Jade Green Hunt CD6\n\n'
'The Skill can be activated only when the Leader is an Elf:\n'
'Add 3x the Recovery basic value of each Elf into its own Attack basic value.(The Skill stays in play until deactivation or defeated.)\n\n'
'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'⓵ Explode all Runestones to generate Enchanted Runestones.\n'
'⓶ Fully recover HP.',

'chi_lead':'翠色傲睨\n\n'
'队伍只有妖精类成员时\n'
'I. 全队攻击力 6 倍\n'
'II. 每个成员增加 400 点攻击力及回复力\n'
'III. 木符石兼具 50% 其他属性符石效果\n'
'IV. 心符石兼具 50% 所有属性符石效果\n'
'V. 进入关卡后\n'
'⇒ 所有成员的技能 CD 减少 3 (可叠加)\n'
'VI. 场上有附加效果时\n'
'⇒ 全队攻击力额外 1.65 倍',
'eng_lead':'Jade Green Gaze\n\n'
'When the Team consists of only Elves:\n'
'I. Team Attack x 6.\n'
'II. Attack & Recovery basic value of each Elf +400.\n'
'III. Earth Runestones also possess 50% effect of other Attributive Runestones.\n'
'IV. Heart Runestones also possess 50% effect of all Attributive Runestones.\n'
'V. Skill CDs of all Members -3 after entering a Stage (the effect can be superimposed).\n'
'VI. When there is an additional effect in play,\n'
'⇒ Team Attack x 1.65 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 获得“结晶化”能力：\n'
'⓵ 将场上的符石变回原始模样\n'
'⓶ 1 回合内\n'
'⇒ 无视“燃烧”敌技(不包括“炼狱之火”)\n'
'⇒ 无视“黏腐”敌技\n\n'
'于回合开始时点击已储满的龙脉仪\n'
'⇒ 可触发“结晶化”能力(需消耗龙脉仪使用次数 1 次)\n\n'
'II. 当前生命力全满时\n'
'⇒ 下一次所受伤害不会使你死亡(同 1 回合只会发动 1 次)\n'
'发动条件：\n'
'以“黛心盈透 ‧ 翡翠”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Acquire Crystallization Power:\n'
'⓵ Restore all Runestones to normal state.\n'
'⓶ For 1 Round, Boss Skills "Burning" (excluding "Hellfire") and "Sticky Land" will be nullified.\n'
'◆ The Skill can be activated at the beginning of the Round by tapping the fully charged Craft Apparatus at the expense of one activation of Dragonic Compulsion.\n'
'◆ When HP is full, the next Damage received will not lead to your defeat (one activation each Round).\n'
'Condition:\n'
'Both the Leader and Ally are "Pride of Regalia - Jade".'},
    
    {'chi_name':'琥珀',
'chif_name':'琥珀',
'eng_name':'amber',

'chi_act':'虫璧 CD8\n\n'
'将场上所有符石转化为\n'
'⇒ 固定数量及位置 的“心及火”妖族强化符石',
'eng_act':'Flames of Bug\n\n'
'Turn all Runestones into Enchanted Heart Elf Runestones and Enchanted Fire Elf Runestones of fixed numbers and positions.',

'chi_lead':'慑魄瑰宝\n\n'
'I. 妖精类生命力及攻击力 2.5 倍\n'
'II. 心符石不会发动消除\n'
'III. 每消除 1 组属性符石时\n'
'⇒ 回复“妖精类成员生命力等值”5% 的生命力',
'eng_lead':'Piercing Amber Eyes\n\n'
'I. Elf HP & Attack x 2.5.\n'
'II. Heart Runestones can\'t be dissolved.\n'
'III. For every group of Attributive Runestones dissolved,\n'
'⇒ recover HP as much as 5% of total Elf HP.',

'chi_team':'队伍技能：\n\n'
'获得“结晶化”能力：\n'
'1 回合内，移动符石前场上每有 1 粒心符石\n'
'⇒ 该回合增加 1 连击 (Combo)(需消除符石)\n'
'于回合开始时点击已储满的龙脉仪\n'
'⇒ 可触发“结晶化”能力(需消耗龙脉仪使用次数 1 次)\n'
'发动条件：\n'
'以“虫火浮光 ‧ 琥珀”作队长及战友\n\n'
'I. 受到敌人攻击时，场上每有 1 粒心符石\n'
'⇒ 减少 10% 所受伤害\n'
'⇒ 10 粒可减少最多 100% 伤害\n\n'
'II. 当受到敌人攻击，于所有敌人攻击完结后\n'
'⇒ 将心符石转化为其他属性符石\n'
'⇒ 并以“转化符石粒数”(最多 30 粒)倍化“200 倍队伍攻击力”，对敌方全体造成无属性伤害\n\n'
'III. “虫火浮光 ‧ 琥珀”的主动技能\n'
'⇒“虫璧”变为“虫璧 ‧ 灵动”：\n'
'1 回合内\n'
'⓵ 2 粒心符石相连即可发动消除 (无视队长技能的消心禁令)\n'
'⓶ 将场上所有符石转化为\n'
'⇒ 固定数量及位置的“心及火”妖族强化符石\n\n'
'IV. 消除妖族符石时\n'
'⇒ 妖精类成员的技能 CD 减少 1\n'
'发动条件：\n'
'以“虫火浮光 ‧ 琥珀”作队长及战友，且队伍中只有妖精类成员',
'eng_team':'Team Skill\n\n'
'◆ Acquire Crystallization Power:\n'
'For 1 Round, Combo count +1 for each present Heart Runestone before the start of moving Runestones (dissolving Runestones is necessary).\n'
'◆ The Skill can be activated at the beginning of the Round by tapping the fully charged Craft Apparatus at the expense of one activation of Dragonic Compulsion.\n'
'Condition:\n'
'Both the Leader and Ally are "Heated Fluorescence - Amber".\n\n'

'◆ Upon receiving Damage from the enemy\'s attacks,\n'
'⇒ Damage received -10% for every present Heart Runestone,\n'
'⇒ to the max -100% for 10 Runestones.\n\n'

'◆ After the enemy\'s attacks,\n'
'⇒ Turn Heart Runestones into Attributive Runestones\n'
'⇒ Deal non-Attributive Damage to all enemies as much as 200x Team Attack in proportion to the number of Runestones turned (to the max 30x).\n\n'

'◆ Change the Active Skill of "Heated Fluorescence - Amber" from "Flames of Bug" to "Flames of Bug - EX".\n'
'For 1 Round:\n'
'I. Heart Runestones can be dissolved by aligning 2 or more of them (overriding the Leader Skill).\n'
'II. Turn all Runestones into Enchanted Heart Elf Runestones and Enchanted Fire Elf Runestones of fixed numbers and positions.\n'
'◆ By dissolving Elf Runestones, Skill CD of Elves -1.\n'
'Condition:\n'
'Both the Leader and Ally are "Heated Fluorescence - Amber", with only Elves in the Team.'},
    
    {'chi_name':'苍璧',
'chif_name':'蒼璧',
'eng_name':'cangbi',

'chi_act':'不撓之誌 ‧ 龍 CD6\n\n'
'I. 無視「黏腐」敵技\n'
'II. 每次觸碰「黏腐」位置\n'
'⇒ 回復 5% 生命力 (不會溢補)\n'
'III. 每個成員追打 1 次\n'
'上述效果會在進入下一層數 (Wave) 時消失\n'
'IV. 解除「風化符石」狀態\n'
'V. 將所有符石轉化為強化符石\n'
'VI.「卿雲護庇 ‧ 蒼璧」以外龍類、神族、獸類 CD 減少 1\n\n'
'變身 CD8\n\n'
'需裝備專屬龍刻武裝才可變身及發動此技能：\n'
'I. 引爆水以外的符石\n'
'⇒ 掉落屬性強化符石\n'
'1 回合內\n'
'II. 龍類、神族、獸類\n'
'⇒ 攻擊力 2.5 倍\n'
'III. 發動技能時，若隊長及戰友為「卿雲護庇 ‧ 蒼璧」或「豁達浪息 ‧ 蒼璧」\n'
'⇒「龍鱗值」減至 0 點\n\n'
'若隊長為「緋曦赤霞 ‧ 紅璦」及以「緋曦赤霞 ‧ 紅璦」、「卿雲護庇 ‧ 蒼璧」 或「豁達浪息 ‧ 蒼璧」作戰友，則效果改為：\n'
'I. 引爆「水及火」以外符石\n'
'⇒ 掉落屬性強化符石\n'
'1 回合內\n'
'II. 龍類、人類、妖精類、魔族攻擊力 2.5 倍\n'
'III.「紅鱗值」提升至 100 點\n'
'(變身後技能請查看/check 蒼璧變身)',

'eng_act':'Determination of the Runedragon CD6\n\n'
'I. Boss Skill "Sticky Land" will be nullified.\n'
'II. Recover 5% HP for every time when a sticky position is touched (no overhealing).\n'
'III. Each Monster in the Team launches an extra attack each Round.\n'
'The Skill stays in play within the Wave.\n'
'IV. Restore all Weathered Runestones to normal state.\n'
'V. Turn all Runestones into Enchanted Runestones.\n'
'VI. Skill CDs of all Gods, Beasts and Dragons (except "Auspice of Protection - Cang Bi") -1.\n\n'
'Switching CD8\n\n'
'This Skill can be activated only when the Monster is equipped with the exclusive Dragonware:\n'
'I. Explode non-Water Runestones to generate Enchanted Attributive Runestones.\n'
'For 1 Round\n'
'II. Attack of Dragons, God & Beasts x 2.5.\n'
'III. If the Leader and Ally are "Auspice of Protection - Cang Bi" or "Billows of Freedom - Cang Bi" upon Skill activation,\n'
'⇒ Dragon Point becomes 0.\n'
'If the Leader is 「Crimson Runedragon - Hong Ai」 and the Ally is 「Crimson Runedragon - Hong Ai」, "Auspice of Protection - Cang Bi" or "Billows of Freedom - Cang Bi":\n'
'I. Explode non-Water and non-Fire Runestones to generate Enchanted Attributive Runestones.\n'
'For 1 Round,\n'
'II. Attack of Dragons, Humans, Elves & Demons x 2.5.\n'
'III. Red Dragon Point increases to 100.\n'
'(Active Skill after switching please check /check cangbitrans)',

'chi_lead':'三族戰勢\n\n'
'隊中只有龍類、神族或獸類成員時：\n'
'I. 全隊攻擊力 6.5 倍及生命力 1.4 倍\n'
'II. 每個成員增加 300 點回復力\n'
'III. 龍類、神族、獸類同時發動攻擊時\n'
'⇒ 全隊攻擊力額外 1.8 倍\n'
'IV. 隊中只有龍類成員\n'
'⇒ 全隊攻擊力額外 1.8 倍\n'
'V. 水符石兼具 50% 其他符石效果',
'eng_lead':'Forces of Three Races\n\n'
'When the Team has only Dragons, Gods or Beasts:\n'
'I. Team Attack x 6.5 & HP x 1.4.\n'
'II. Recovery basic value of each Member +300.\n'
'III. When a Dragon, a God and a Beast launch attacks in the same Round,\n'
'⇒ Team Attack x 1.8 additionally.\n'
'IV. When the Team has only Dragons,\n'
'⇒ Team Attack x 1.8 additionally.\n'
'V. Water Runestones also possess 50% effect of other Runestones.',

'chi_team':'隊伍技能：\n\n'
'I. 每消除 1 粒龍族符石\n'
'⇒ 回復 3,000 點生命力\n'
'⇒ 消除 30 粒可回復最多 90,000 點\n'
'II. 必然延長移動符石時間 2 秒\n\n'

'III. 【龍鱗值】\n'
'⓵ 龍鱗值愈高\n'
'⇒ 減少所受傷害愈多\n'
'⇒ 最多可減少 100%\n'
'⓶ 龍鱗值愈低\n'
'⇒ 全隊攻擊力提升愈多\n'
'⇒ 最多可提升至 5 倍\n\n'

'[＊] 進入關卡後，獲得 50 點龍鱗值\n'
'[＊] 每回復 500 點生命力\n'
'⇒ 提升 1 點龍鱗值\n'
'[＊] 每消除 3 粒水符石\n'
'⇒ 減少 10 點龍鱗值\n'
'[＊] 受到敵人攻擊後\n'
'⇒ 該回合減少 30 點龍鱗值\n\n'
'發動條件：\n'
'以「卿雲護庇 ‧ 蒼璧」或「豁達浪息 ‧ 蒼璧」作隊長及戰友\n\n'

'＊此召喚獸於 CD 0 時可以變身，變身後將以消耗能量點的方式發動技能。召喚獸的技能等級愈高，發動技能時所需的能量值愈低。變身時，能量點為全滿狀態 (12 點)，當能量點未滿時，可以於 1 回合內消除 3 粒或以上的水符石，以儲存 1 點能量點。',

'eng_team':'Team Skill:\n\n'
'◆ For each Dragon Runestone dissolved,\n'
'⇒ recover 3,000 HP\n'
'⇒ to the max 90,000 HP for 30 Runestones dissolved.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n\n'

'◆ 【Dragon Point (DP)】\n'
'⓵ The higher the DP, the less the Damage received, to the max -100%.\n'
'⓶ The lower the DP, the higher the Team Attack, to the max x 5 additionally.\n\n'

'◆ [＊] The Team starts with 50 DP after entering a Stage.\n'
'[＊] DP +1 for every 500 HP recovered.\n'
'[＊] DP -10 for every 3 Water Runestones dissolved.\n'
'DP -30 in the Round upon receiving Damage from an enemy\'s attack.\n'
'Condition:\n'
'The Leader and Ally are "Auspice of Protection - Cang Bi" or "Billows of Freedom - Cang Bi".'},
    
    {'chi_name':'苍璧变身',
'chif_name':'蒼璧變身',
'eng_name':'cangbitrans',

'chi_act':'不挠宏志 ‧ 龙 EP6\n\n'
'I. 无视“黏腐”敌技\n'
'II. 每次触碰“黏腐”位置\n'
'⇒ 回复 5% 生命力 (不会溢补)\n'
'III. 每个成员追打 1 次\n'
'上述效果会在进入下一层数 (Wave) 时消失\n'
'IV. 解除“风化符石”状态\n'
'V. 将所有符石转化为强化符石\n'
'VI.“卿云护庇 ‧ 苍璧”以外龙类、神族、兽类 CD 减少 2\n\n'
'碧穹杀机 EP4\n\n'
'1 回合内\n'
'I. 自身攻击力 3 倍\n'
'II. 回合结束时\n'
'⇒ 将心符石转化为水强化符石\n'
'III. 发动技能时，\n'
'若队长及战友为“卿云护庇 ‧ 苍璧”或“豁达浪息 ‧ 苍璧”\n'
'⓵“龙鳞值”减少 50 点\n'
'⓶ 将心符石转化为\n'
'⇒ 水龙族强化符石',

'eng_act':'Determination of the Runedragon - EX\n\n'
'I. Boss Skill "Sticky Land" will be nullified.\n'
'II. Recover 5% HP for each time when a sticky position is touched (no overhealing).\n'
'III. Each Monster in the Team launches an extra attack each Round.\n'
'The above effects stays in play within the Wave.\n'
'IV. Restore all Weathered Runestones to normal state.\n'
'V. Turn all Runestones into Enchanted Runestones.\n'
'VI. Skill CDs of all Gods, Beasts and Dragons (except "Auspice of Protection - Cang Bi") -2.\n\n'
'Assault of the Jade EP4\n\n'
'For 1 Round:\n'
'I. The Monster\'s Attack x 3.\n'
'II. Turn Heart Runestones into Enchanted Water Runestones at the end of the Round.\n'
'III. If the Leader and Ally are "Auspice of Protection - Cang Bi" or "Billows of Freedom - Cang Bi":\n'
'⓵ Dragon Point -50.\n'
'⓶ Turn Heart Runestones into Enchanted Water Dragon Runestones.',

'chi_lead':'三族战势\n\n'
'队中只有龙类、神族或兽类成员时：\n'
'I. 全队攻击力 6.5 倍及生命力 1.4 倍\n'
'II. 每个成员增加 300 点回复力\n'
'III. 龙类、神族、兽类同时发动攻击时\n'
'⇒ 全队攻击力额外 1.8 倍\n'
'IV. 队中只有龙类成员\n'
'⇒ 全队攻击力额外 1.8 倍\n'
'V. 水符石兼具 50% 其他符石效果',
'eng_lead':'Forces of Three Races\n\n'
'When the Team has only Dragons, Gods or Beasts:\n'
'I. Team Attack x 6.5 & HP x 1.4.\n'
'II. Recovery basic value of each Member +300.\n'
'III. When a Dragon, a God and a Beast launch attacks in the same Round,\n'
'⇒ Team Attack x 1.8 additionally.\n'
'IV. When the Team has only Dragons,\n'
'⇒ Team Attack x 1.8 additionally.\n'
'V. Water Runestones also possess 50% effect of other Runestones.',

'chi_team':'队伍技能：\n\n'
'I. 每消除 1 粒龙族符石\n'
'⇒ 回复 3,000 点生命力\n'
'⇒ 消除 30 粒可回复最多 90,000 点\n'
'II. 必然延长移动符石时间 2 秒\n'

'III. 【龙鳞值】\n'
'⓵ 龙鳞值愈高\n'
'⇒ 减少所受伤害愈多\n'
'⇒ 最多可减少 100%\n'
'⓶ 龙鳞值愈低\n'
'⇒ 全队攻击力提升愈多\n'
'⇒ 最多可提升至 5 倍\n\n'

'[＊] 进入关卡后，获得 50 点龙鳞值\n'
'[＊] 每回复 500 点生命力\n'
'⇒ 提升 1 点龙鳞值\n'
'[＊] 每消除 3 粒水符石\n'
'⇒ 减少 10 点龙鳞值\n'
'[＊] 受到敌人攻击后\n'
'⇒ 该回合减少 30 点龙鳞值\n'
'发动条件：\n'
'以“卿云护庇 ‧ 苍璧”或“豁达浪息 ‧ 苍璧”作队长及战友\n'
'＊能量储存条件：1 回合内消除 3 粒或以上的水符石\n'

'“豁达浪息 ‧ 苍璧”的主动技能“碧穹杀机”变为“赤龙杀机”\n'
'I.“红鳞值”提升 50 点\n'
'II. 将心符石转化为\n'
'⇒ 火龙族强化符石\n'
'1 回合内\n'
'III. 自身攻击力 3 倍\n'
'IV. 回合结束时\n'
'⇒ 将心符石转化为火强化符石\n'
'发动条件：\n'
'以“绯曦赤霞 ‧ 红瑷”作队长，并以“豁达浪息 ‧ 苍璧”作成员',
'eng_team':'Team Skill:\n\n'
'◆ For each Dragon Runestone dissolved,\n'
'⇒ recover 3,000 HP\n'
'⇒ to the max 90,000 HP for 30 Runestones dissolved.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n\n'
'◆ 【Dragon Point (DP)】\n'
'⓵ The higher the DP, the less the Damage received, to the max -100%.\n'
'⓶ The lower the DP, the higher the Team Attack, to the max x 5 additionally.\n'
'◆ [＊] The Team starts with 50 DP after entering a Stage.\n'
'[＊] DP +1 for every 500 HP recovered.\n'
'[＊] DP -10 for every 3 Water Runestones dissolved.\n'
'DP -30 in the Round upon receiving Damage from an enemy\'s attack.\n'
'Condition:\n'
'The Leader and Ally are "Auspice of Protection - Cang Bi" or "Billows of Freedom - Cang Bi".\n\n'

'◆ For each Dragon Runestone dissolved,\n'
'⇒ recover 3,000 HP\n'
'⇒ to the max 90,000 HP for 30 Runestones dissolved.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n\n'

'◆ 【Red Dragon Point (RDP)】\n'
'⓵ The higher the RDP,\n'
'⇒ the higher the Team Attack\n'
'⇒ to the max x 5 additionally.\n'
'⓶ When the RDP reaches 100,\n'
'⇒ Attack of “Crimson Runedragon - Hong Ai“ x 3 additionally.\n'
'◆ [＊] The Team starts with 50 RDP after entering a Stage.\n'
'[＊] RDP +10 for every 3 Fire Runestones dissolved.\n'
'[＊] RDP -30 in the Round upon receiving Damage from an enemy\'s attack.\n'
'Condition:\n'
'The Leader is "Crimson Runedragon - Hong Ai", and the Ally is "Crimson Runedragon - Hong Ai", "Auspice of Protection - Cang Bi" or "Billows of Freedom - Cang Bi".\n\n'

'◆ Change the Active Skill “Assault of the Jade” of “Billows of Freedom - Cang Bi” to “Rage of Fire Dragon”.\n'
'I. Red Dragon Point +50.\n'
'II. Turn Heart Runestones into Enchanted Fire Dragon Runestones.\n'
'For 1 Round,\n'
'III. The Monster\'s Attack x 3.\n'
'IV. Turn Heart Runestones into Enchanted Fire Runestones at the end of the Round.\n'
'Condition:\n'
'The Leader is "Crimson Runedragon - Hong Ai", with "Billows of Freedom - Cang Bi" in the Team.\n\n'

'* EP stacking condition:\n'
'Dissolve ≥3 Water Runestones in 1 Round\n'
'⇒ EP +1,\n'
'⇒ to the max +1 each Round.'},
    
 {'chi_name':'维洛妮卡',
'chif_name':'維洛妮卡',
'eng_name':'veronica',

'chi_act':'战甲利刃 ‧ 兽 CD5\n\n'
'I. 消耗现有 20% 生命力(生命力为 1 时无法发动技能)\n'
'II. 将暗符石转化为兽族强化符石\n'
'1 回合内\n'
'III. 自身攻击力 6 倍\n'
'IV. 兽类成员的伤害\n'
'⇒ 无视敌人防御力\n'
'⇒ 无视“指定形状盾”敌技',
'eng_act':'Shield of Purple Blood\n\n'
'At the expense of 20% HP (this Skill cannot be activated when Team HP is 1):\n'
'I. Turn Dark Runestones into Enchanted Beast Runestones.\n'
'For 1 Round:\n'
'II. The Monster\'s Attack x 6.\n'
'III. Damage dealt by Beasts will disregard enemies\' Defense and Puzzle Shield.',

'chi_lead':'战火纷飞\n\n'
'队伍中只有兽类成员：\n'
'I. 全队攻击力 6.5 倍及生命力 1.5 倍\n'
'II. 每个成员增加 500 点回复力\n'
'III. 场上每有 1 个附加效果\n'
'⇒ 全队攻击力额外 1.5 倍\n'
'⇒ 最多计算 4 个附加效果\n'
'IV. 生命力未满时\n'
'⇒ 全队攻击力及回复力额外 2 倍\n'
'V. 首批消除 1 组 ≥5 粒符石时，使敌方全体中毒：\n'
'⇒ 每回合受到自身攻击力的伤害 (此伤害无视防御力及属性并持续至死亡)',
'eng_lead':'Fires of War\n\n'
'When the Team has only Beasts:\n'
'I. Team Attack x 6.5 & HP x 1.5.\n'
'II. Recovery basic value of each Member +500.\n'
'III. For every additional effect in play,\n'
'⇒ Team Attack x 1.5 additionally,\n'
'⇒ to the max for 4 effects.\n'
'IV. When Team HP is not full,\n'
'⇒ Team Attack & Recovery x 2 additionally.\n'
'V. By dissolving a group of ≥5 Runestones in the first batch,\n'
'⇒ poison all enemies with the Monster\'s Attack every Round (regardless of Defense and Attribute until defeated).',

'chi_team':'队伍技能：\n\n'
'I. 将移动符石时所触碰的队伍成员属性符石\n'
'⇒ 转化为兽族强化符石\n'
'II. 必然延长移动符石时间 5 秒\n'
'III. 进入关卡后，兽类成员技能 CD -6\n'
'IV. 所受光属性及暗属性目标伤害\n'
'⇒ 减少 50%\n'
'发动条件：\n'
'以“冥血吞蚀 ‧ 维洛妮卡”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Turn Runestones of Members\' Attributes touched while moving into Enchanted Beast Runestones.\n'
'◆ Extend Runestone-moving time regardlessly by 5 seconds.\n'
'◆ Skill CD of Beasts -6 after entering a Stage.\n'
'◆ Damage received from Light and Dark enemies -50%.\n'
'Condition:\n'
'Both the Leader and Ally are "Blood of Obscurity - Veronica".'},
    
   {'chi_name':'恩莉儿',
'chif_name':'恩莉兒',
'eng_name':'enlil',

'chi_act':'逆水之焰 CD6\n\n'
'I. 火属性伤害可克制水属性目标\n'
'II. 消除种族符石时\n'
'⇒ 个人追打火及木属性攻击 1 次(效果会在关闭此技能或死亡后消失)\n'
'此技能可随时关闭，关闭时：\n'
'⓵ 引爆神族成员直行符石\n'
'⇒ 掉落神族强化符石',
'eng_act':'Unquenchable Flames Cd6\n\n'
'I. Fire Damage can overpower Water enemies.\n'
'II. By dissolving Race Runestones, the Monster launches an extra Fire attack and an extra Earth attack.\n'
'The Skill stays in play until deactivation or defeated.\n'
'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'⇒ Explode the columns of Runestones below Gods to generate Enchanted God Runestones.',

'chi_lead':'神女之柔\n\n'
'队伍中只有神族或人类成员，并需有 ≥4 个神族成员：\n'
'I. 全队攻击力 6.5 倍及生命力 1.2 倍\n'
'II. 必然延长移动符石时间 1 秒\n'
'III. 消除的符石愈多\n'
'⇒ 全队攻击力额外提升愈多\n'
'⇒ 消除 20 粒可达至最大 2.8 倍',
'eng_lead':'Tenderness of the Goddess\n\n'
'When the Team includes only Gods and Humans, and there are ≥4 Gods:\n'
'I. Team Attack x 6.5, HP x 1.2.\n'
'II. Extend Runestone-moving time regardlessly by 1 second.\n'
'III. The more the Runestones dissolved, the higher the Team Attack increases additionally, to the max x 2.8 for 20 Runestones.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后，将龙脉仪储满\n'
'II. 下回合开始时\n'
'⇒ 所有符石随机转换为五属及心符石\n'
'III. 所有属性符石互相兼具 50% 效果\n'
'发动条件：\n'
'以“智火解析 ‧ 恩莉儿”作队长及战友\n\n'

'I. 将移动符石时触碰的首 6 粒符石\n'
'⇒ 转化为人族强化符石\n'
'II. 根据转珠结束时放手的符石\n'
'⇒ 最左方的“编号 6666 ‧ 依贝思”及\n'
'最左方的“智火解析 ‧ 恩莉儿”直行首批掉落该种强化符石\n'
'发动条件：\n'
'以“编号 6666 ‧ 依贝思”作队长及战友\n'

'“源恨复苏 · 恩莉儿”\n'
'⇒ 对神族目标攻击力额外 3 倍\n'
'发动条件：\n'
'以“源恨复苏 · 恩莉儿”及“智火解析 ‧ 恩莉儿”作成员',
'eng_team':'Team Skill:\n\n'
'◆ The Craft Apparatus will be fully charged after entering a Stage.\n'
'◆ Refresh all Runestones into Runestones of all types at the beginning of each Round.\n'
'◆ All Attributive Runestones also possess 50% effect of each other.\n'
'Condition:\n'
'Both the Leader and Ally are "Fire of Sagacity - Enlil".\n\n'
'◆ Damage dealt by "Resentment Awakening - Enlil" on Gods x 3 additionally.\n'
'Condition:\n'
'There are "Fire of Sagacity - Enlil" and "Resentment Awakening - Enlil" in the Team.'}, 
    
    {'chi_name':'依贝思',
'chif_name':'依貝思',
'eng_name':'elpis',

'chi_act':'疾风侵噬 CD2\n\n'
'1 回合内根据累积战斗回合数 (需消除符石)+1 的数量\n'
'⓵“智火解析 ‧ 恩莉儿”及自身\n'
'⇒ 以 50% 攻击力追打\n'
'⇒ 最多可追打 8 次\n'
'⓶ 优先引爆相应粒数的风化、冻结、电击符石，并引爆木以外符石\n'
'⇒ 最多引爆 8 粒符石\n'
'⇒ 掉落木人族符石\n'
'发动技能后累积战斗回合数减半',
'eng_act':'Uncontrollable Winds CD2n\n'
'For 1 Round:\n'
'According to the number of accumulated Rounds +1 (dissolving Runestones is necessary):\n'
'⓵ The Monster and "Fire of Sagacity - Enlil" launch extra attacks as much as 50% of own Attack, to the max 8 extra attacks.\n'
'⓶ Explode Weathered, Frozen, Electrified and non-Earth Runestones to generate Earth Human Runestones, to the max 8 Runestones to be exploded.\n'
'Accumulated Rounds -50% after Skill activation.',

'chi_lead':'藤棘怒号\n\n'
'队伍中只有人类或神族时：\n'
'I. 全队攻击力 6 倍\n'
'II. 木及心符石分别兼具\n'
'⇒ 50% 其他符石效果\n'
'III. 队伍中只有木属性、“代偶规条”成员或“智火解析 ‧ 恩莉儿”\n'
'⇒ 全队攻击力额外 3 倍',
'eng_lead':'Howling Thorns\n\n'
'When the Team includes only Humans and Gods:\n'
'I. Team Attack x 6.\n'
'II. Earth and Heart Runestones also possess 50% effect of other Runestones.\n'
'III. If the Team consists of only Earth Members, Monsters of "Creeds of Earthlings" or "Fire of Sagacity - Enlil", Team Attack x 3 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 将移动符石时触碰的首 6 粒符石\n'
'⇒ 转化为人族强化符石\n'
'II. 根据转珠结束时放手的符石\n'
'⇒ 最左方的“编号 6666 ‧ 依贝思”及最左方的“智火解析 ‧ 恩莉儿”直行首批掉落该种强化符石\n'
'III. 必然延长移动符石时间 2 秒\n'
'发动条件：\n'
'以“编号 6666 ‧ 依贝思”作队长及战友\n\n'

'队长的队长技能“藤棘怒号”\n'
'⇒ 变为“藤棘怒号 ‧ 挡”\n'
'队伍中只有人类或神族时：\n'
'I. 全队攻击力 6 倍\n'
'II. 木及心符石分别兼具\n'
'⇒ 50% 其他符石效果\n'
'III. 队伍中只有木属性、“代偶规条”成员或“智火解析 ‧ 恩莉儿”\n'
'⇒ 全队攻击力额外 3 倍\n'
'IV. 减少 50% 所受伤害\n'
'⇒ 受到 25 次攻击后失去此效果\n'
'发动条件：\n'
'以“编号 6666 ‧ 依贝思”作队长及战友，且队伍中只有人类或神族成员',
'eng_team':'Team Skill:\n\n'
'◆ Turn the first 6 Runestones touched while moving into Enchanted Human Runestones.\n'
'◆ The first batch of Runestones to be dropped in the columns below the first "No. 6666 - Elpis" and "Fire of Sagacity - Enlil" from the left will be Enchanted Runestones of the last Runestone picked to end moving.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'Condition:\n'
'Both the Leader and Ally are "No. 6666 - Elpis".\n'

'◆ Change the Leader Skill of the Leader from "Howling Thorns" to "Howling Thorns - Shield".\n'
'When the Team includes only Humans and Gods:\n'
'I. Team Attack x 6.\n'
'II. Earth and Heart Runestones also possess 50% effect of other Runestones.\n'
'III. If the Team consists of only Earth Members, Monsters of "Creeds of Earthlings" or "Fire of Sagacity - Enlil", Team Attack x 3 additionally.\n'
'IV. Damage received -50% for the first 25 attacks from enemies.\n'
'Condition:\n'
'Both the Leader and Ally are "No. 6666 - Elpis", with only Humans or Gods in the Team.'},
    
    {'chi_name':'因其都',
'chif_name':'因其都',
'eng_name':'enkidu',

'chi_act':'潜能苏醒 CD7\n\n'
'I. 解除所有成员被封锁的技能(此技能无视封锁技能)\n'
'II. 若队伍中齐集 5、6、7、8 星成员\n'
'⇒ 将场上的符石变回原始模样\n'
'III. 引爆所有符石\n'
'⇒ 7 星及 8 星成员直行掉落强化符石\n'
'1 回合内\n'
'IV. 其他符石兼具暗符石效果',
'eng_act':'Awakening Potentials CD7\n\n'
'I. Release the locked Skills of all Members.(This Skill will not be locked.)\n'
'II. When there are 5, 6, 7 and 8 star Monsters in the Team, restore all Runestones to normal state.\n'
'III. Explode all Runestones to generate Enchanted Runestones in the columns below 7 star and 8 star Monsters.\n'
'IV. For 1 Round, other Runestones also possess the effect of Dark Runestones.',

'chi_lead':'筹划之战\n\n'
'队伍中只有暗属性成员时：\n'
'I. 全队攻击力 5 倍\n'
'II. 首批没有消除暗符石时 (需消除符石)\n'
'⇒ 减少 25% 所受伤害\n'
'III. 心符石兼具 50% 暗符石效果\n'
'IV. 队伍中集齐 5、6、7 星成员时\n'
'⓵ 全队生命力、攻击力、回复力 2 倍\n'
'⓶ 必然延长移动符石时间 2.5 秒',
'eng_lead':'Planning for Battles\n\n'
'When the Team consists of only Dark Members:\n'
'I. Team Attack x 5.\n'
'II. If no Dark Runestones are dissolved in the first batch (dissolving Runestones is necessary), Damage received -25%.\n'
'III. Heart Runestones also possess 50% effect of Dark Runestones.\n'
'IV. When there are 5, 6 and 7 star Monsters in the Team:\n'
'⓵ Team Attack, HP & Recovery x 2 additionally.\n'
'⓶ Extend Runestone-moving time regardlessly by 2.5 seconds.',

'chi_team':'队伍技能：\n\n'
'I. 5 星及 8 星成员直行\n'
'⇒ 首批掉落的 5 粒符石必定为暗符石\n'
'II. “无束天赋 ‧ 因其都”直行\n'
'⇒ 首批掉落的 5 粒符石必定为心强化符石\n'
'发动条件：\n'
'以“无束天赋 ‧ 因其都”作队长及战友\n\n'

'暗属性攻击力 3 倍\n'
'发动条件：\n'
'以“无束天赋 ‧ 因其都”作队长及战友；且队伍中有 8 星成员',
'eng_team':'Team Skill:\n\n'
'◆ The first 5 Runestones to be dropped in the first batch in the columns below 5 and 8 star Monsters will be Dark Runestones.\n'
'◆ The first 5 Runestones to be dropped in the first batch in the column below "Liberation of Talent - Enkidu" will be Enchanted Heart Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Liberation of Talent - Enkidu".\n\n'

'◆ Dark Attack x 3 additionally.\n'
'Condition:\n'
'Both the Leader and Ally are "Liberation of Talent - Enkidu", with a 8 star Character in the Team.'},
    
    {'chi_name':'南纳',
'chif_name':'南納',
'eng_name':'leonard',

'chi_act':'水淹木林 CD7\n\n'
'I. 将所有符石转化为强化符石\n'
'1 回合内\n'
'II. 连击 (Combo) 数目增加 6\n'
'III. 水属性伤害可克制木属性目标\n'
'IV. 若队长及战友均为“代偶规条”成员\n'
'⇒ 则连击 (Combo) 数目增加 15',
'eng_act':'Forests in Floods CD7\n\n'
'I. Turn all Runestones into Enchanted Runestones.\n'
'For 1 Round:\n'
'II. Combo count +6.\n'
'III. Water Damage can overpower Earth enemies.\n'
'IV. If the Leader and Ally are "Creeds of Earthlings", Combo count +15.',

'chi_lead':'水月战盾\n\n'
'I. 水属性及“代偶规条”系列成员攻击力 6 倍、生命力及回复力 1.2 倍\n'
'II. 消除水符石时\n'
'⇒ 所受伤害减少 30%\n'
'III. 消除 1 组 ≥5 粒水符石时\n'
'⇒ 水属性及“代偶规条”系列成员攻击力额外 2.8 倍',
'eng_lead':'Shield of Watery Moon\n\n'
'I. Attack of Water Monsters and Monsters of "Creeds of Earthlings" x 6; HP & Recovery x 1.2.\n'
'II. By dissolving Water Runestones, Damage received -30%.\n'
'III. By dissolving a group of ≥5 Water Runestones,\n'
'⇒ Attack of Water Monsters and Monsters of "Creeds of Earthlings" x 2.8 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 将移动符石时触碰的首 6 粒符石\n'
'⇒ 转化为水强化符石\n'
'II. 延长移动符石时间至 15 秒\n'
'III. 水符石兼具其他属性符石效果\n'
'IV. 以不同形状首批消除 1 组 ≥5 粒水符石，获得以下效果：\n\n'

'【一】：水属性及“代偶规条”成员\n'
'⇒ 攻击力 2.2 倍\n'
'【十】：减少 50% 所受伤害\n'
'【不同方向的 ∟】：“代偶规条”系列成员的攻击\n'
'⇒ 无视“三属盾”及“五属盾”\n'
'发动条件：\n'
'以“编号 8299 ‧ 南纳”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Turn the first 6 Runestones touched while moving into Enchanted Water Runestones.\n'
'◆ Extend Runestone-moving time to 15 seconds.\n'
'◆ Water Runestones also possess the effect of other Attributive Runestones.\n'
'◆ By dissolving a group of ≥5 Water Runestones in a specific shape in the first batch, one of the following effects will be triggered:\n'

'◆ 【一】: Attack of Water Monsters and Monsters of "Creeds of Earthlings" x 2.2 additionally.\n'
'◆【十】: Damage received -50%.\n'
'◆【∟(in different forms)】: Damage of Monsters of "Creeds of Earthlings" will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield.\n'
'Condition:\n'
'Both the Leader and Ally are "No. 8299 - Leonard".'},
    
    {'chi_name':'诺索斯',
'chif_name':'諾索斯',
'eng_name':'north',

'chi_act':'畸躯 CD6\n\n'
'I. 将所有强化符石\n'
'⇒ 转化为非强化符石\n'
'II. 12 秒内，可任意移动符石(此移动不会造成任何消除，并不会作 1 回合计算)\n'
'1 回合内\n'
'III. 全队攻击力及回复力 2.6 倍',
'eng_act':'Deformity CD6\n\n'
'Turn all Enchanted Runestones\n'
'⇒ into non-Enchanted Runestones.\n'
'II. Unlimited Runestone movement in 12 seconds without dissolving and this will not be counted as 1 Round.\n'
'For 1 Round,\n'
'III. Team Attack & Recovery x 2.6.',

'chi_lead':'生灵殆尽\n\n'
'I. 自身属性及魔族攻击力 6 倍、生命力及回复力 1.3 倍\n'
'II. 必然延长移动符石时间 2 秒\n'
'III. 木及火符石互相兼具效果\n'
'IV. 消除火符石时\n'
'⇒ 魔族攻击力额外 1.5 倍\n'
'V. 消除木符石时\n'
'⇒ 自身属性及魔族攻击力额外 2 倍',
'eng_lead':'Life Extinction\n\n'
'I. Monster\'s Attribute & Demon Attack x 6; HP & Recovery x 1.3.\n'
'II. Extend Runestone-moving time regardlessly by 2 seconds.\n'
'III. Earth and Fire Runestones also possess the effect of each other.\n'
'IV. By dissolving Fire Runestones, Demon Attack x 1.5 additionally.\n'
'V. By dissolving Earth Runestones,\n'
'⇒ Attack of the Monster\'s Attribute & Demon x 2 additionally.',

'chi_team':'队伍技能：\n\n'
'队长及战友转换为火属性\n'
'发动条件：\n'
'以“命轴剥夺 ‧ 诺索斯”作队长及战友，且队中只有火属性队员\n\n'

'队长的队长技能“生灵殆尽”\n'
'⇒ 变为“生灵殆尽 ‧ 裂心”\n'
'I. 自身属性及魔族攻击力 6 倍、生命力及回复力 1.3 倍\n'
'II. 必然延长移动符石时间 2 秒\n'
'III. 木及火符石互相兼具效果\n'
'IV. 消除火符石时\n'
'⇒ 魔族攻击力额外 1.5 倍\n'
'V. 消除木符石时\n'
'⇒ 自身属性及魔族攻击力额外 2 倍\n'
'VI. 于每回合移动符石后\n'
'⇒ 引爆所有心符石\n'
'⇒ 直至场上没有心符石\n'
'发动条件：\n'
'以“命轴剥夺 ‧ 诺索斯”作队长及战友\n\n'

'I. 火及木符石兼具心符石效果\n'
'II. 魔族成员\n'
'⇒“生命力、攻击力及回复力”基值 1.5 倍',
'eng_team':'Team Skill:\n\n'
'◆ Alter the Attribute of the Leader and Ally into Fire.\n'
'Condition:\n'
'Both the Leader and Ally are "Destructive Deprivation - North", with only Fire Members in the Team.\n\n'

'◆ Change the Leader Skill of the Leader from "Life Extinction" to "Life Extinction - Heart-cracking".\n'
'I. Monster\'s Attribute & Demon Attack x 6; Hp & Recovery x 1.3.\n'
'II. Extend Runestone-moving time regardlessly by 2 seconds.\n'
'III. Earth and Fire Runestones also possess the effect of each other.\n'
'IV. By dissolving Fire Runestones, Demon Attack x 1.5 additionally.\n'
'V. By dissolving Earth Runestones,\n'
'⇒ Attack of the Monster\'s Attribute & Demon x 2 additionally.\n'
'VI. Upon the completion of moving Runestones each Round,\n'
'⇒ all Heart Runestones will explode\n'
'⇒ until there is no more Heart Runestone on the screen.\n\n'

'◆ Fire and Earth Runestones also possess the effect of Heart Runestones.\n'
'◆ Demon HP, Attack & Recovery basic value x 1.5.\n'
'◆ Reduce the Damage of “Burning” to 0.\n'
'◆ Convert the Damage of "Poisoning" to HP Recovery.\n'
'⓵ The Frozen Runestones touched while moving will be restored to normal state and changed into Demon Runestones of the Leader’s Attribute.\n'
'⓶ The Petrified Runestones touched while moving will be restored to normal state and changed into Demon Runestones of the Leader’s Attribute.\n'
'Condition:\n'
'Both the Leader and Ally are "Destructive Deprivation - North".'},
    
    {'chi_name':'苏因',
'chif_name':'蘇因',
'eng_name':'saint',

'chi_act':'星象诠释 CD6\n\n'
'I. 点选元素法阵上的 1 粒符石\n'
'⇒ 引爆该种符石\n'
'⇒ 掉落相同种类的神族强化符石\n'
'1 回合内\n'
'II. 若引爆的符石为水、火或木符石：\n'
'⓵ 光属性及神族攻击力 2 倍\n'
'⓶ “黄道十二宫”、“耀脉星芒”成员\n'
'⇒ 技能 CD 减少 2\n'
'III. 若引爆的符石为光或暗符石：每首批消除 1 组符石\n'
'⇒ 连击 (Combo、Ex. Combo) 数目增加 1\n'
'⇒ 最多可增加 10 连击\n'
'IV. 若引爆的符石为心符石\n'
'⓵ 光属性及神族攻击力 1.6 倍\n'
'⓶ 每首批消除 2 组符石\n'
'⇒ 连击 (Combo、Ex. Combo) 数目增加 1\n'
'⇒ 最多可增加 10 连击\n'
'⓷ “黄道十二宫”、“耀脉星芒”成员\n'
'⇒ 技能 CD 减少 1',
'eng_act':'Astrology Manipulation CD6\n\n'
'I. By tapping a Runestone on the Magic Circle of Elements:\n'
'⇒ Explode Runestones of this type\n'
'⇒ to generate Enchanted God Runestones of the same type.\n'
'For 1 Round,\n'
'II. If Water, Fire or Earth Runestones are exploded:\n'
'⓵ Light & God Attack x 2.\n'
'⓶ "Twelve Zodiacs" & "Star Burst Pulses"\n'
'⇒ Active Skill CD -2.\n'
'III. If Light or Dark Runestones are exploded:\n'
'For every group of Runestones dissolved in the first batch,\n'
'⇒ Combo & Ex. Combo +1\n'
'⇒ to the max +10.\n'
'IV. If Heart Runestones are exploded:\n'
'⓵ Light & God Attack x 1.6.\n'
'⓶ For every 2 groups of Runestones dissolved in the first batch,\n'
'⇒ Combo & Ex. Combo +1\n'
'⇒ to the max +10.\n'
'⓷ "Twelve Zodiacs" & "Star Burst Pulses"\n'
'⇒ Active Skill CD -1.',

'chi_lead':'星宿之掌\n\n'
'队伍中只有神族成员时：\n'
'I. 全队攻击力 6.5 倍、生命力及回复力 1.2 倍\n'
'II. 连击 (Combo) 时攻击力提升 100%\n'
'III. 队伍中有 ≥3 种属性成员\n'
'⓵ 必然延长移动符石时间 2 秒\n'
'⓶ 队伍成员属性符石\n'
'⇒ 互相兼具 50% 效果\n'
'IV. 场上有附加效果时\n'
'⇒ 自身、“黄道十二宫”、“耀脉星芒”成员：\n'
'⓵ 追打 1 次\n'
'⓶ 攻击无视“指定形状盾”敌技',
'eng_lead':'Palm of Astro\n\n'
'When the Team has only Gods:\n'
'I. Team Attack x 6.5, HP & Recovery x 1.2.\n'
'II. Attack bonus for each Combo increases by 100%.\n'
'III. When there are ≥3 Attributes in the Team:\n'
'⓵ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'⓶ Runestones of Team Members\' Attribute also possess 50% effect of each other.\n'
'IV. When there is an additional effect in play,\n'
'⇒ the Monster, "Twelve Zodiacs" & "Star Burst Pulses":\n'
'⓵ Launch an extra attack.\n'
'⓶ Damage will be dealt regardless of Puzzle Shield.',

'chi_team':'队伍技能：\n\n'
'I.“黄道十二宫”、“耀脉星芒”成员\n'
'⓵ 技能 CD -2 (最多减至 CD 1)\n'
'⓶ 进场 CD -8\n'
'⓷“生命力、攻击力及回复力”\n'
'⇒ 基值 2 倍\n'
'II. 连击 (Combo) 时攻击力提升 50%\n'
'发动条件：\n'
'以“星辰之理 ‧ 苏因”作队长，并以“星辰之理 ‧ 苏因”或“蜃楼星火 ‧ 伊斯塔”作战友，且队中有“黄道十二宫”或“耀脉星芒”系列队员\n\n'

'队中“星辰之理 ‧ 苏因”愈多，通过“黄道十二宫上篇”、“黄道十二宫下篇”故事模式内的初级、中级、高级关卡后\n'
'⇒ 额外获得道具愈多\n'
'⇒ 6 个“苏因”可获额外 6 个道具\n'
'发动条件：\n'
'以“星辰之理 ‧ 苏因”作成员',
'eng_team':'Team Skill:\n\n'
'◆ The more “Gospel of Stars - Saint” in the Team,\n'
'⇒ the more extra items obtained in the Basic, Interm. & Advanced stages in the Story Mode “Twelve Zodiacs - Chapter 1 & Chapter 2”,\n'
'⇒ to the max 6 extra items for 6 “Saint”.\n'
'Condition:\n'
'There is "Gospel of Stars - Saint" in the Team.\n\n'

'◆ "Twelve Zodiacs" & "Star Burst Pulses":\n'
'⓵ Active Skill CD -2 (at most to CD 1)\n'
'⓶ Active Skill CD -8 after entering a Stage\n'
'⓷ HP, Attack & Recovery basic value x 2\n'
'◆ Attack bonus for Combo increases by 50%.\n'
'Condition:\n'
'The Leader is "Gospel of Stars - Saint" and the Ally is "Phantom Pride - Ishtar" or "Gospel of Stars - Saint", with a Character of "Twelve Zodiacs" (series) or "Star Burst Pulses" (series) in the Team.\n\n'

'◆ At the end of the Round, turn 9 fixed positions into Enchanted Fire God, Enchanted Light God and Enchanted Heart God Runestones (3 for each).\n'
'◆ By dissolving God Runestones,\n'
'⇒ Active Skill CD of “Phantom Pride - Ishtar” & "Gospel of Stars - Saint" -2.\n'
'◆ Boss Skill "Sticky Land" will be nullified.\n'
'Condition:\n'
'The Leader is "Phantom Pride - Ishtar", and the Ally is "Phantom Pride - Ishtar" or "Gospel of Stars - Saint".'},
    
    {'chi_name':'伊斯塔',
'chif_name':'伊斯塔',
'eng_name':'shtar',

'chi_act':'炮火连天 CD6 \n\n'
'I. 将黑白符石变回原来色调\n'
'II. 身上有附加效果的成员及“星辰之理 ‧ 苏因”攻击力 2.2 倍\n'
'III. 消除神族符石时\n'
'⇒ 神族成员以 50% 攻击力追打 1 次(效果会在关闭此技能或死亡后消失)\n\n'
'此技能可随时关闭，关闭时：\n'
'⓵ 完全回复生命力\n'
'⓶ 将神族成员直行的符石\n'
'⇒ 转化为强化符石',
'eng_act':'Gunfire Blast CD6\n\n'
'I. Clear the negative effect of "B&W Zone".\n'
'II. Attack of Member(s) with additional effect in play and "Gospel of Stars - Saint" x 2.2.\n'
'III. By dissolving God Runestones,\n'
'⇒ God(s) launches an extra attack as much as 50% of own Attack. The Skill stays in play until deactivation or defeated.\n\n'
'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'⓵ Fully recover HP.\n'
'⓶ Turn the column below God\n'
'⇒ into Enchanted Runestones.',

'chi_lead':'战神之焰\n\n'
'队伍中只有神族成员时：\n'
'I. 全队攻击力 6.5 倍及生命力 1.4 倍\n'
'II. 火、光、心符石互相兼具 50% 效果\n'
'III. 同时消除火、光、心符石其中 2 种符石时\n'
'⇒ 全队攻击力额外 3 倍\n'
'IV. 场上有附加效果时\n'
'⇒ 自身及身上有附加效果的成员攻击无视五属盾',
'eng_lead':'Blaze of God\n\n'
'When the Team has only Gods:\n'
'I. Team Attack x 6.5 & HP x 1.4.\n'
'II. Fire, Light & Heart Runestones also possess 50% effect of each other.\n'
'III. If 2 out of 3 types of Runestones (Fire, Light & Heart) are dissolved in the same Round,\n'
'⇒ Team Attack x 3 additionally.\n'
'IV. When there is an additional effect in play,\n'
'⇒ Damage of the Monster and Members with an additional effect in play on their icons will be dealt regardless of "Quintet Elemental Shield".',

'chi_team':'队伍技能：\n\n'
'I. 回合结束时，将指定 9 个位置的符石转化为\n'
'⇒“火、光、心”神族强化符石各 3 粒\n'
'II. 消除神族符石时\n'
'⇒“蜃楼星火 ‧ 伊斯塔”及“星辰之理 ‧ 苏因”技能 CD -2\n'
'III. 无视“黏腐”敌技\n'
'发动条件：\n'
'以“蜃楼星火 ‧ 伊斯塔”作队长，并以“蜃楼星火 ‧ 伊斯塔”或“星辰之理 ‧ 苏因”作战友',
'eng_team':'Team Skill:\n\n'
'◆ "Twelve Zodiacs" & "Star Burst Pulses":\n'
'⓵ Active Skill CD -2 (at most to CD 1)\n'
'⓶ Active Skill CD -8 after entering a Stage\n'
'⓷ HP, Attack & Recovery basic value x 2\n'
'◆ Attack bonus for Combo increases by 50%.\n'
'Condition:\n'
'The Leader is "Gospel of Stars - Saint" and the Ally is "Phantom Pride - Ishtar" or "Gospel of Stars - Saint", with a Character of Twelve Zodiacs series or Star Burst Pulses series in the Team.\n\n'
'◆ At the end of the Round, turn 9 fixed positions into Enchanted Fire God, Enchanted Light God and Enchanted Heart God Runestones (3 for each).\n'
'◆ By dissolving God Runestones,\n'
'⇒ Active Skill CD of “Phantom Pride - Ishtar” & "Gospel of Stars - Saint" -2.\n'
'◆ Boss Skill "Sticky Land" will be nullified.\n'
'Condition:\n'
'The Leader is "Phantom Pride - Ishtar", and the Ally is "Phantom Pride - Ishtar" or "Gospel of Stars - Saint".'},
    
   {'chi_name':'英格丽',
'chif_name':'英格麗',
'eng_name':'ingrid',

'chi_act':'命定的守护 CD8\n\n'
'1 回合内\n'
'I. 心符石兼具\n'
'⇒ 200% 属性符石效果\n'
'II. 2 粒符石即可发动消除，效果持续至消除 1 种符石达 25 粒\n'
'III. 回合结束时\n'
'⇒ 自身进入 2 回合濒死状态',
'eng_act':'Destined Protection\n\n'
'For 1 Round,\n'
'I. Heart Runestones also possess 200% effect of Attributive Runestones.\n'
'II. Runestones can be dissolved by aligning 2 or more of them, until 25 Runestones of one type are dissolved.\n'
'III. The Monster enters a dying state (fatigue state) at the end of the Round for 2 Rounds.',

'chi_lead':'魔女承志\n\n'
'I. 全队攻击力 6 倍\n'
'II. 队中有 ≥3 种族成员时\n'
'⇒ 全队攻击力额外 1.8 倍\n'
'III. 队伍中有 ≥3 种属性成员时\n'
'⇒ 全队攻击力额外 1.5 倍\n'
'IV. 队员、战友的属性及种族均没有重复时\n'
'⇒ 全队生命力、攻击力、回复力额外 1.8 倍',
'eng_lead':'Will of Witch\n\n'
'I. Team Attack x 6.\n'
'II. If there are ≥3 Races in the Team,\n'
'⇒ Team Attack x 1.8 additionally.\n'
'III. If there are ≥3 Attributes in the Team,\n'
'⇒ Team Attack x 1.5 additionally.\n'
'IV. If the Attributes and Races of Team Members and Ally are not repeated,\n'
'⇒ Team HP, Attack & Recovery x 1.8 additionally.',

'chi_team':'队伍技能：\n\n'
'进入关卡后，“梦咏守望 ‧ 英格丽”\n'
'⇒ 技能 CD -2\n'
'发动条件：\n'
'以“梦咏守望 ‧ 英格丽”及“以诺”作成员\n\n'

'进入关卡后，最左方的“天才使魔 ‧ 豹豹”\n'
'⇒ 技能 CD -6\n'
'发动条件：\n'
'以“梦咏守望 ‧ 英格丽”及“天才使魔 ‧ 豹豹”作成员\n\n'

'I. 所有符石兼具\n'
'⇒ 其他属性符石效果\n'
'II. 所有属性符石兼具\n'
'⇒ 50% 心符石效果\n'
'III. 队中有神族及魔族成员时\n'
'⓵ 将移动符石时触碰的符石\n'
'⇒ 转化为强化符石\n'
'⓶ 增加 4 连击 (Combo)\n'
'IV. 队中有龙类、兽类及妖精类其中 2 种族成员时\n'
'⓵ 全队生命力、攻击力、回复力 1.2 倍\n'
'⓶ 无视“燃烧”敌技(不包括“炼狱之火”)\n'
'⓷ 无视“黏腐”敌技\n'
'V. 队中有机械族成员时\n'
'⓵ 所有成员每回合以 50% 攻击力追打自身属性或自身克制属性的攻击 1 次\n'
'⓶ 必然延长移动符石时间 2.5 秒\n'
'发动条件：\n'
'以“梦咏守望 ‧ 英格丽”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ After entering a Stage,\n'
'Skill CD of “Guardian of Reverie - Ingrid“ -2.\n'
'Condition:\n'
'There are "Guardian of Reverie - Ingrid" and "Enoch" in the Team.\n\n'

'◆ After entering a Stage,\n'
'Skill CD of the first “Panther the Ingenious Feline” from the left -6.\n'
'Condition:\n'
'There are "Guardian of Reverie - Ingrid" and "Panther the Ingenious Feline" in the Team.\n\n'

'◆ All Runestones also possess the effect of other Attributive Runestones.\n'
'◆ All Attributive Runestones also possess 50% effect of Heart Runestones.\n'
'◆ When the Team has God(s) and Demon(s):\n'
'⓵ Turn Runestones touched while moving into Enchanted Runestones.\n'
'⓶ Combo count +4 each Round.\n'
'◆ When there are any 2 races of Dragon(s), Beast(s) and Elf(s) in the Team:\n'
'⓵ Team HP, Attack & Recovery x 1.2.\n'
'⓶ Boss Skills "Burning" (excluding "Hellfire") and "Sticky Land" will be nullified.\n'
'◆ When the Team has Machina(s):\n'
'⓵ All Members launch an extra attack of their own Attribute or Counter Attribute as much as 50% of their Attack every Round.\n'
'⓶ Extend Runestone-moving time regardlessly by 2.5 seconds.\n'
'Condition:\n'
'Both the Leader and Ally are "Guardian of Reverie - Ingrid".'},
    
    {'chi_name':'达格',
'chif_name':'達格',
'eng_name':'dagda',

'chi_act':'猛兽列阵 CD7\n\n'
'点选法阵上的动物图像\n'
'⇒ 转换自身形态\n\n'
'【鹿】\n'
'⓵ 引爆所有符石\n'
'3 回合内\n'
'⓶ 全队回复力减至 0\n'
'⓷ 每回合回复\n'
'⇒ 45,000 点生命力\n\n'
'【熊】\n'
'1 回合内\n'
'⓵ 所受伤害减至 0\n\n'
'【狼】\n'
'⓵ 将兽类成员属性符石及心符石转化为强化符石\n'
'1 回合内\n'
'⓶ 兽类攻击力 2 倍\n'
'⓷ 所有成员无视“攻前盾”\n\n'
'【鹰】\n'
'⓵“比拟万象 ‧ 达格”以外兽类成员 CD -1\n'
'1 回合内\n'
'⓶ 所有符石兼具\n'
'⇒ 其他属性符石效果',
'eng_act':'Beast Forces CD7\n\n'
'Tap an animal icon on the Magic Circle to change the Monster\’s form.\n\n'
'【Deer】\n'
'⓵ Explode all Runestones.\n'
'For 3 Rounds,\n'
'⓶ Team Recovery becomes 0.\n'
'⓷ Recover 45,000 HP each Round.\n\n'
'【Bear】\n'
'For 1 Round,\n'
'⓵ Damage received will become 0.\n\n'
'【Wolf】\n'
'⓵ Turn the Attributive Runestones of Beasts and Heart Runestones into Enchanted Runestones.\n'
'For 1 Round,\n'
'⓶ Beast Attack x 2.\n'
'⓷ Damage of the Team will be dealt regardless of Initial Shield.\n\n'
'【Eagle】\n'
'⓵ CD of Beasts other than "Dagda" -1.\n'
'For 1 Round,\n'
'⓶ All Runestones also possess the effect of other Attributive Runestones.',

'chi_lead':'狂兽凶势\n\n'
'队中只有兽类成员：\n'
'I. 全队攻击力 6 倍及生命力 1.3 倍\n'
'II. 达成 ≥5 连击 (Combo) 时\n'
'⓵ 全队攻击力额外 2 倍\n'
'⓶ 所有成员无视“三属盾”\n'
'III. 达成 ≥8 连击 (Combo) 时\n'
'⓵ 全队攻击力额外 2.5 倍\n'
'⓶ 所有成员无视“五属盾”',
'eng_lead':'Beast Berserker\n\n'
'When the Team has only Beasts:\n'
'I. Team Attack x 6 & HP x 1.3.\n'
'II. When ≥5 Combos are made,\n'
'⓵ Team Attack x 2 additionally.\n'
'⓶ Damage of the Team will be dealt regardless of Trio Elemental Shield.\n'
'III. When ≥8 Combos are made,\n'
'⓵ Team Attack x 2.5 additionally.\n'
'⓶ Damage of the Team will be dealt regardless of Quintet Elemental Shield.',

'chi_team':'队伍技能：\n\n'
'每只“比拟万象 ‧ 达格”转换为以下形态时，可获得以下效果：\n'
'【鹿】\n'
'▋每回合回复“所有成员生命力等值”15% 的生命力\n'
'【熊】\n'
'▋所受伤害减少 10%\n'
'【狼】\n'
'▋自身攻击力 2 倍\n'
'▋自身攻击无视敌人防御力\n'
'【鹰】\n'
'▋消除 ≥4 种符石\n'
'⇒ 自身技能 CD -1\n'
'发动条件：\n'
'以“比拟万象 ‧ 达格”作成员\n\n'

'I. 必然延长移动符石时间 2.5 秒\n'
'II. 兽类成员发动技能时\n'
'⓵ 完全回复生命力\n'
'⓶ 兽类攻击力 1.5 倍\n'
'III. 首批消除所有木符石时\n'
'⇒ 于移动并消除符石后引爆单数直行符石\n'
'⇒ 掉落兽族强化符石\n'
'IV. 首批消除所有光符石时\n'
'⇒ 于移动并消除符石后引爆双数直行符石\n'
'⇒ 掉落兽族强化符石\n'
'V. 首批消除所有木或光符石时\n'
'⇒ 增加 5 连击 (Combo)\n'
'VI. 其他符石兼具 50% 木符石效果\n'
'发动条件：\n'
'以“比拟万象 ‧ 达格”作队长及战友\n\n'

'最左方的“凝象境域 ‧ 霍格”\n'
'⇒ 技能 CD -3\n'
'发动条件：\n'
'以“比拟万象 ‧ 达格”及“凝象境域 ‧ 霍格”作成员',
'eng_team':'Team Skill:\n\n'
'◆ “Versatile Shapeshifter - Dagda“ acquires 4 forms of 【Deer】, 【Bear】, 【Wolf】 and 【Eagle】.\n'
'◆ The following effects will be granted when each “Versatile Shapeshifter - Dagda“ turns into the forms below:\n'
'【Deer】\n'
'▋Recover 15% of total HP each Round.\n'
'【Bear】\n'
'▋Damage received -10%.\n'
'【Wolf】\n'
'▋The Character\’s Attack x 2.\n'
'▋The Character\'s Damage can be dealt regardless of Defense.\n'
'【Eagle】\n'
'▋By dissolving ≥4 types of Runestones,\n'
'⇒ the Character\’s Skill CD -1.\n'
'Condition:\n'
'There is "Versatile Shapeshifter - Dagda" in the Team.\n\n'

'◆ Extend Runestone-moving time regardlessly by 2.5 seconds.\n'
'◆ When Beast(s) activates its Skill:\n'
'⓵ Fully recover HP.\n'
'⓶ Beast Attack x 1.5.\n'
'◆ By dissolving all Earth Runestones in the first batch,\n'
'⇒ explode the odd columns upon the completion of moving and dissolving Runestones\n'
'⇒ to generate Enchanted Beast Runestones.\n'
'◆ By dissolving all Light Runestones in the first batch,\n'
'⇒ explode the even columns upon the completion of moving and dissolving Runestones\n'
'⇒ to generate Enchanted Beast Runestones.\n'
'◆ By dissolving all Earth or Light Runestones in the first batch,\n'
'⇒ Combo count +5.\n'
'◆ Other Runestones also possess 50% effect of Earth Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Versatile Shapeshifter - Dagda".\n\n'

'◆ Skill CD of the first “Shapeshifting Mastery - Hogda” from the left -3.\n'
'Condition:\n'
'There are "Versatile Shapeshifter - Dagda" and "Shapeshifting Mastery - Hogda" in the Team.'},
    
    {'chi_name':'红瑷',
'chif_name':'紅璦',
'eng_name':'hongai',

'chi_act':'命运交织 CD8\n\n'
'I. 将场上的符石变回原始模样\n'
'II. 引爆所有符石\n'
'⇒ 掉落 固定数量及位置 的“水及火”龙族强化符石\n'
'1 回合内\n'
'II. 龙类、人类、妖精类、魔族\n'
'⇒ 攻击力 2 倍\n'
'III. 所有成员无视“三属盾”及“五属盾”',
'eng_act':'Intertwined Fate\n\n'
'I. Restore all Runestones to normal state.\n'
'II. Explode all Runestones to generate Enchanted Water Dragon Runestones and Enchanted Fire Dragon Runestones of fixed numbers and fixed positions.\n'
'For 1 Round,\n'
'III. Dragons, Humans, Elves & Demons,\n'
'⇒ Attack x 2.\n'
'IV. Damage of the Team will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield.',

'chi_lead':'赤龙之心\n\n'
'队伍中只有龙类、人类、妖精类或魔族时：\n'
'I. 全队攻击力 6.5 倍\n'
'II. 火符石兼具 50% 其他符石效果\n'
'III. 队中有 ≥3 个龙类成员时\n'
'⓵ 全队生命力 1.8 倍\n'
'⓶ 全队攻击力额外 2.8 倍\n'
'IV. 受到敌人攻击时\n'
'⇒ 随机将 5 粒符石转化为龙族强化符石',
'eng_lead':'Heart of Red Dragon\n\n'
'When the Team has only Dragons, Humans, Elves or Demons:\n'
'I. Team Attack x 6.5.\n'
'II. Fire Runestones also possess 50% effect of other Runestones.\n'
'III. If there are ≥3 Dragons in the Team:\n'
'⓵ Team HP x 1.8.\n'
'⓶ Team Attack x 2.8 additionally.\n'
'IV. Upon receiving Damage from the enemy\'s attack,\n'
'⇒ turn 5 random Runestones into Enchanted Dragon Runestones.',

'chi_team':'队伍技能：\n\n'
'I. 每消除 1 粒龙族符石\n'
'⇒ 回复 3,000 点生命力\n'
'⇒ 消除 30 粒可回复最多 90,000 点\n'
'II. 必然延长移动符石时间 2 秒\n'
'III. 【红鳞值】\n'
'⓵ 红鳞值愈高\n'
'⇒ 全队攻击力提升愈多\n'
'⇒ 最多可提升至 5 倍\n'
'⓶ 红鳞值达至 100 点时\n'
'⇒ “绯曦赤霞 ‧ 红瑷”攻击力额外 3 倍\n\n'

'[＊] 进入关卡后，获得 50 点红鳞值\n'
'[＊] 每消除 3 粒火符石\n'
'⇒ 提升 10 点红鳞值\n'
'[＊] 受到敌人攻击后\n'
'⇒ 该回合减少 30 点红鳞值\n'
'发动条件：\n'
'以“绯曦赤霞 ‧ 红瑷”作队长，并以“绯曦赤霞 ‧ 红瑷”、“卿云护庇 ‧ 苍璧”或“豁达浪息 ‧ 苍璧”作战友\n\n'

'“豁达浪息 ‧ 苍璧”的主动技能\n'
'“碧穹杀机”变为“赤龙杀机”\n'
'I.“红鳞值”提升 50 点\n'
'II. 将心符石转化为\n'
'⇒ 火龙族强化符石\n'
'1 回合内\n'
'III. 自身攻击力 3 倍\n'
'IV. 回合结束时\n'
'⇒ 将心符石转化为火强化符石\n'
'发动条件：\n'
'以“绯曦赤霞 ‧ 红瑷”作队长，并以“豁达浪息 ‧ 苍璧”作成员',
'eng_team':'Team Skill:\n\n'
'◆ For each Dragon Runestone dissolved,\n'
'⇒ recover 3,000 HP\n'
'⇒ to the max 90,000 HP for 30 Runestones dissolved.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'◆ 【Red Dragon Point (RDP)】\n'
'⓵ The higher the RDP,\n'
'⇒ the higher the Team Attack\n'
'⇒ to the max x 5 additionally.\n'
'⓶ When the RDP reaches 100,\n'
'⇒ Attack of “Crimson Runedragon - Hong Ai“ x 3 additionally.\n\n'

'◆ [＊] The Team starts with 50 RDP after entering a Stage.\n'
'◆ [＊] RDP +10 for every 3 Fire Runestones dissolved.\n'
'◆ [＊] RDP -30 in the Round upon receiving Damage from an enemy\'s attack.\n'
'Condition:\n'
'The Leader is "Crimson Runedragon - Hong Ai", and the Ally is "Crimson Runedragon - Hong Ai", "Auspice of Protection - Cang Bi", or "Billows of Freedom - Cang Bi".\n\n'

'◆ Change the Active Skill “Assault of the Jade” of “Billows of Freedom - Cang Bi” to “Rage of Fire Dragon”.\n'
'I. Red Dragon Point +50.\n'
'II. Turn Heart Runestones into Enchanted Fire Dragon Runestones.\n'
'For 1 Round,\n'
'III. The Monster\'s Attack x 3.\n'
'IV. Turn Heart Runestones into Enchanted Fire Runestones at the end of the Round.\n'
'Condition:\n'
'The Leader is "Crimson Runedragon - Hong Ai", with "Billows of Freedom - Cang Bi" in the Team.'},
    
    {'chi_name':'时空菲吕拉',
'chif_name':'時空菲呂拉',
'eng_name':'chronosgatephilyra',

'chi_act':'倍化术 ‧ 连击 CD5\n'
'I. 将《时空之门》角色及神族成员直行的符石\n'
'⇒转化为强化符石\n'
'2 回合内\n'
'II. 额外增加 6 连击(Combo、Ex. Combo)\n'
'III. 首批掉落直行《时空之门》角色的属性种族符石\n\n'
'移除黏涎 CD5\n'
'I. 选择 3 横行的符石\n'
'⇒【左右滑动移除】\n'
'2 回合内\n'
'II. 无视“黏腐”敌技',
'eng_act':'Refinement Multiplier - Combos CD5\n'
'I. Turn the column(s) below "ChronosGate" Monster(s) and God(s) into Enchanted Runestones.\n'
'For 2 Rounds,\n'
'II. Combo count +6 (Combo & Ex. Combo).\n'
'III. The first batch to be dropped will be Race Runestones of the Attribute of "ChronosGate" Monster(s).\n\n'
'Stickiness Removal CD5\n'
'I. Select and swipe to remove 3 rows of Runestones.\n'
'For 2 Rounds,\n'
'II. Boss Skill "Sticky Land" will be nullified.',

'chi_lead':'猛炎之神力\n\n'
'I. “次元英雄”系列及神族攻击力 7 倍\n'
'II. 火、光、暗属性生命力及回复力 1.5 倍\n'
'III. 首批消除任何 1 横行内的所有符石时\n'
'⇒ “次元英雄”系列及神族攻击力额外 2 倍\n'
'IV. 达至 ≥6 连击 (Combo 或 Ex. Combo) 时\n'
'⇒ 全队攻击力额外 2 倍',
'eng_lead':'Act of God\n\n'
'I. Attack of Monsters of “Heroes of Dimension” & Gods x 7.\n'
'II. Fire, Light & Dark HP & Recovery x 1.5.\n'
'III. By dissolving all Runestones in any row in the first batch,\n'
'⇒ Attack of Monsters of “Heroes of Dimension” & Gods x 2 additionally.\n'
'IV. When ≥6 Combos (Combo or Ex. Combo) are made,\n'
'⇒ Team Attack x 2 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 所有符石分别兼具\n'
'⇒ 火、光、暗符石效果\n'
'II. 火符石兼具\n'
'⇒ 50% 心符石效果\n'
'III. 首批 3 粒相连的符石\n'
'⇒ 可发动消除\n'
'IV. 受敌人反击伤害减少 90%\n'
'V. 横行消除 ≥1 组 ≥5 粒符石\n'
'⇒“次元英雄”角色技能 CD -1\n'
'VI. 发动【左右滑动移除】技能\n'
'⇒ 每次向左或向右方滑动，\n'
'触发不同效果：\n\n'

'【向左方滑动】\n'
'⇒1 回合内，延长移动符石时间至 12 秒(可叠加回合数)\n'
'【向右方滑动】\n'
'⇒ 1 回合内\n'
'⓵ 全队攻击力 2.2 倍\n'
'⓶ 无视敌人防御力(可叠加回合数）\n'
'发动条件：\n'
'以“写作之神 ‧ 菲吕拉”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ All Runestones also possess the effect of Fire, Light and Dark Runestones.\n'
'◆ Fire Runestones also possess 50% effect of Heart Runestones.\n'
'◆ Runestones can be dissolved by aligning 3 or more of them in the first batch.\n'
'◆ Damage reflected from enemies -90%.\n'
'◆ By dissolving ≥1 group of ≥5 Runestones in a row, Skill CD of “Heroes of Dimension” -1.\n'
'◆ When activating the Skill of “Swiping left or right to remove Runestones”, different effects will be triggered:\n\n'

'◆ 【Swipe left】\n'
'Extend Runestone-moving time to 12 seconds for 1 Round (the no. of Rounds can be superimposed).\n'
'◆ 【Swipe right】\n'
'For 1 Round:\n'
'⓵ Team Attack x 2.2\n'
'⓶ Damage will be dealt regardless of Defense.(the no. of Rounds can be superimposed).\n'
'Condition:\n'
'Both the Leader and Ally are "Philyra, The Authors\' Muse".'},
    
    {'chi_name':'时空路西法',
'chif_name':'時空路西法',
'eng_name':'chronosgatelucifer',	

'chi_act':'看破 CD8\n'
'发动技能时消耗现有 10% 生命力(生命力为 1 时仍可发动)\n'
'1 回合内\n'
'I. 自身攻击力 8 倍\n'
'II. 自身攻击\n'
'⇒ 无视敌人防御力\n'
'III. 若有击毙敌人时\n'
'⇒ 该回合不会扣减技能持续回合\n\n'

'极热效应 CD6\n'
'I. 选择 2 横行的符石\n'
'⇒【左右滑动移除】\n'
'2 回合内\n'
'II. 无视“燃烧”敌技',

'eng_act':'Ultimate Guard Break CD8\n'
'Deplete 10% of current HP upon Skill activation (activatable when HP is 1).\n'
'For 1 Round:\n'
'I. The Monster\'s Attack x 8.\n'
'II. The Monster\'s Damage will be dealt regardless of Defense.\n'
'III. If an enemy is defeated,\n'
'⇒ the number of Rounds with the Skill staying in play will not reduce.\n\n'

'Burning Effect CD6\n'
'I. Select and swipe to remove 2 rows of Runestones.\n'
'For 2 Rounds,\n'
'II. Boss Skill "Burning" will be nullified.',

'chi_lead':'刺棘之怒\n\n'
'I. 神族、魔族、妖精类攻击力 6 倍、生命力及回复力 1.3 倍\n'
'II. 消除 ≥3 种符石时\n'
'⇒ 神族、魔族、妖精类攻击力额外 2 倍\n'
'III. 生命力未满时\n'
'⇒ 全队攻击力额外 3.5 倍\n'
'IV. 消除暗符石时\n'
'⇒ 全队攻击力额外 1.5 倍',
'eng_lead':'Anger of Thorns\n\n'
'I. God, Demon & Elf Attack x 6; HP & Recovery x 1.3.\n'
'II. By dissolving ≥3 types of Runestones,\n'
'⇒ God, Demon & Elf Attack x 2 additionally.\n'
'III. When HP is not full,\n'
'⇒ Team Attack x 3.5 additionally.\n'
'IV. By dissolving Dark Runestones,\n'
'⇒ Team Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后及每回合结束时\n'
'⇒ 将队长直行的符石转化为“暗及心”神族强化符石\n'
'II. 暗及心符石分别兼具\n'
'⇒ 50% 其他符石效果\n'
'III. 进入关卡后\n'
'⇒ 队长技能 CD -8\n'
'IV. 发动【左右滑动移除】技能\n'
'⇒ 每次向左或向右方滑动，\n'
'触发不同效果：\n\n'

'【向左方滑动】\n'
'⇒ 1 回合内，全体敌人的攻击力弱化 60%(不可叠加回合数)\n'
'【向右方滑动】\n'
'⇒１回合内\n'
'⓵ 全队回复力变 0\n'
'⓶ 全队攻击力 2 倍\n'
'⓷ 队长追打光属性攻击 1 次(可叠加回合数)\n'
'发动条件：\n'
'以“叛逆天使 ‧ 路西法”作队长，并以“叛逆天使 ‧ 路西法”或“扭曲天使 ‧ 亚伯汗”作战友',
'eng_team':'Team Skill:\n\n'
'◆ After entering a Stage and at the end of each Round, turn the column below the Leader into Enchanted Dark God and Enchanted Heart God Runestones.\n'
'◆ Dark and Heart Runestones also possess 50% effect of other Runestones.\n'
'◆ Skill CD of the Leader -8 after entering a Stage.\n'
'◆ When activating the Skill of “Swiping left or right to remove Runestones”, different effects will be triggered:\n\n'

'◆ 【Swipe left】\n'
'Weaken the Attack of all enemies by 60% for 1 Round (the no. of Rounds cannot be superimposed).\n'
'◆ 【Swipe right】\n'
'For 1 Round:\n'
'⓵ Team Recovery becomes 0.\n'
'⓶ Team Attack x 2.\n'
'⓷ The Leader launches an extra Light Attack (the no. of Rounds can be superimposed).\n'
'Condition:\n'
'The Leader is "Angel of Doom Lucifer", and the Ally is "Angel of Distortion Azazel" or "Angel of Doom Lucifer".'},
    
    {'chi_name':'时空亚伯汗',
'chif_name':'時空亞伯汗',
'eng_name':'chronosgateazazel',

'chi_act':'倍化术 ‧ 神族 CD3\n'
'1 回合内\n'
'I. 累积战斗回合数愈多(需消除符石)\n'
'⇒ 转化为神族强化符石愈多\n'
'⇒ 最多可转化 30 粒(队伍成员属性符石及非种族符石优先转换)\n'
'II. 每首批消除 1 粒种族符石\n'
'⇒ 掉落 1 粒光强化符石\n\n'

'回复效应 CD5\n'
'I. 选择 2 横行的符石\n'
'⇒【左右滑动移除】\n'
'II. 回复 60% 生命力\n'
'III. 队长为“次元英雄”系列角色\n'
'⇒ 延迟全体敌人行动 1 回合',
'eng_act':'Refinement Multiplier - Gods CD3\n'
'For 1 Round:\n'
'I. The more the accumulated Rounds (dissolving Runestones is necessary),\n'
'⇒ the more the Enchanted God Runestones to be turned into,\n'
'⇒ to the max 30 Runestones (Runestones of Members\' Attributes and non-Race Runestones rank first in priority).\n'
'II. For every Race Runestone dissolved in the first batch,\n'
'⇒ 1 Enchanted Light Runestone will be generated.\n\n'

'Healing Effect CD5\n'
'I. Select and swipe to remove 2 rows of Runestones.\n'
'II. Recover 60% HP.\n'
'III. If the Leader is a Monster of "Heroes of Dimensions",\n'
'⇒ CDs of all enemies will be delayed for 1 Round.',

'chi_lead':'抗神之力\n\n'
'I. 神族、魔族、妖精类攻击力 6.5 倍、生命力及回复力 1.3 倍\n'
'II. 消除 ≥3 种符石时\n'
'⇒ 神族、魔族、妖精类攻击力额外 2 倍\n'
'III. 消除种族符石时\n'
'⇒ 神族、魔族、妖精类攻击力额外 2 倍\n'
'IV. 消除光符石时\n'
'⇒ 全队攻击力额外 1.5 倍',
'eng_lead':'Overwhelming Power\n\n'
'I. God, Demon & Elf Attack x 6.5; HP & Recovery x 1.3.\n'
'II. By dissolving ≥3 types of Runestones,\n'
'⇒ God, Demon & Elf Attack x 2 additionally.\n'
'III. By dissolving Race Runestones,\n'
'⇒ God, Demon & Elf Attack x 2 additionally.\n'
'IV. By dissolving Light Runestones,\n'
'⇒ Team Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后及每回合结束时\n'
'⇒ 将队长直行的符石转化为“光及心”神族强化符石\n'
'II. 光及心符石分别兼具\n'
'⇒ 50% 其他符石效果\n'
'III. 生命力全满时\n'
'⇒ 减少 70% 所受伤害\n'
'IV. 发动【左右滑动移除】技能\n'
'⇒ 每次向左或向右方滑动，\n'
'触发不同效果：\n\n'

'【向左方滑动】\n'
'⓵ 回复 20,000 点生命力\n'
'⇒ 1 回合内\n'
'⓶ 全队回复力 2.5 倍 (可叠加回合数)\n'
'【向右方滑动】\n'
'⇒ 1 回合内\n'
'⓵ 全队攻击力 2 倍\n'
'⓶ 全队无视“五属盾” (可叠加回合数)\n'
'发动条件：\n'
'以“扭曲天使 ‧ 亚伯汗”作队长，并以“扭曲天使 ‧ 亚伯汗”或“叛逆天使 ‧ 路西法”作战友',
'eng_team':'Team Skill:\n\n'
'◆ After entering a Stage and at the end of each Round, turn the column below the Leader into Enchanted Light God and Enchanted Heart God Runestones.\n'
'◆ Light and Heart Runestones also possess 50% effect of other Runestones.\n'
'◆ When HP is full, Damage received -70%.\n'
'◆ When activating the Skill of “Swiping left or right to remove Runestones”, different effects will be triggered:\n\n'

'◆ 【Swipe left】\n'
'⓵ Recover 20,000 HP.\n'
'⓶ Team Recovery x 2.5 for 1 Round (the no. of Rounds can be superimposed).\n'
'◆ 【Swipe right】\n'
'For 1 Round:\n'
'⓵ Team Attack x 2.\n'
'⓶ Damage of the Team will be dealt regardless of Quintet Elemental Shield (the no. of Rounds can be superimposed).\n'
'Condition:\n'
'The Leader is "Angel of Distortion Azazel", and the Ally is "Angel of Distortion Azazel" or "Angel of Doom Lucifer".'},
    
    {'chi_name':'华曦',
'chif_name':'華曦',
'eng_name':'huaxi',

'chi_act':'龙咒狂暴 CD8\n\n'
'I. 若队长为龙类或兽类\n'
'⇒ 发动技能时自身转换为【龙】形态\n'
'II. 将龙类成员直行符石\n'
'⇒ 转化为龙族强化符石\n'
'1 回合内\n'
'III. 点选元素法阵上的属性符石 2 次\n'
'⓵ 该 2 种属性符石首批 1 粒即可发动消除\n'
'⓶ 个人及身上有附加效果的成员\n'
'⇒ 以 50% 攻击力追打该 2 种属性攻击各 1 次',
'eng_act':'Dragonic Frenzy\n\n'
'I. If the Leader is a Dragon or Beast,\n'
'⇒ the Monster will turn into【Dragon】form upon Skill activation.\n'
'II. Turn the column(s) below Dragon(s) into Enchanted Dragon Runestones.\n'
'For 1 Round:\n'
'III. By tapping an Attributive Runestone on the Magic Circle of Elements twice:\n'
'⓵ Runestones of those 2 types can be dissolved singly or in groups of 2 or more in the first batch.\n'
'⓶ The Monster and Member(s) with an additional effect in play launch an extra attack of each of those 2 Attributes as much as 50% of their own Attack.',

'chi_lead':'龙威震天\n\n'
'I. 龙类及兽类攻击力 7 倍及生命力 1.5 倍\n'
'II. 队中只有龙类及兽类成员时\n'
'⇒ 全队生命力额外 1.5 倍\n'
'III. 首批没有消除心符石时\n'
'⇒ 龙类及兽类攻击力额外 3 倍\n'
'IV. 延长移动符石时间 2.5 秒',
'eng_lead':'Mightiness of Dragons\n\n'
'I. Dragon & Beast Attack x 7 & HP x 1.5.\n'
'II. When the Team has only Dragons and Beasts,\n'
'⇒ Team HP x 1.5 additionally.\n'
'III. If no Heart Runestones are dissolved in the first batch (dissolving Runestones is necessary),\n'
'⇒ Dragon & Beast Attack x 3 additionally.\n'
'IV. Extend Runestone-moving time by 2.5 seconds.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后，“少华钧天 ‧ 华曦”\n'
'⇒ 转换为【龙】形态\n\n'

'II. 当“少华钧天 ‧ 华曦”为【龙】形态时：\n'
'⓵ 自身及身旁龙类或兽类成员获得【邪马台祝福 ‧ 龙】\n'
'⓶ 受到敌人攻击后\n'
'⇒ 转换为【人】形态\n\n'

'III. 当“少华钧天 ‧ 华曦”为【人】形态时：\n'
'⓵ 回合结束时，自身技能 CD -1\n'
'⓶“少华钧天 ‧ 华曦”发动主动技能时\n'
'⇒ 自身转换为【龙】形态\n'
'发动条件：\n'
'队长为龙类或兽类，并以“少华钧天 ‧ 华曦”作成员\n\n'

'身上有【邪马台祝福．龙】的成员\n'
'⇒ 攻击力 1.5 倍\n'
'发动条件：\n'
'队长为龙类或兽类，并以“少华钧天 ‧ 华曦”或“傲志不訾 ‧ 姬臣”作成员\n\n'

'I. 必然延长移动符石时间 3 秒\n'
'II. 进入关卡后，\n'
'⓵ 龙类成员技能 CD -5\n'
'⓶ 兽类成员技能 CD -2\n'
'III. 回合结束时\n'
'⓵ 将心符石转化为属性龙族符石(场上没有的属性符石优先转换)\n'
'⓶ 将木符石转化为龙族强化符石\n'
'IV. 累计消除 30 粒种族符石\n'
'⇒ 每回合回复 50% 生命力\n'
'⇒ 效果持续至下一层数 (Wave) 时消失(累计消除种族符石数目于每一层数 (Wave) 重置)\n'
'V. 发动攻击前我方生命力 ≥ 50%\n'
'⇒ 敌人所受伤害额外 5 倍\n'
'VI. 队中有 ≥3 种属性成员\n'
'⇒ 木符石兼具其他属性符石效果\n'
'发动条件：\n'
'以“少华钧天 ‧ 华曦”作队长，并以“少华钧天 ‧ 华曦”或“琴息濯洗 ‧ 霏音”作战友',

'eng_team':'Team Skill:\n\n'
'◆ “Apex of Fortitude - Huaxi” will turn into【Dragon】form after entering a Stage.\n\n'

'◆ When “Apex of Fortitude - Huaxi” is in【Dragon】form:\n'
'⓵ The Monster and the neighboring Dragon or Beast acquire【Yamatai Blessing - Dragon】\n'
'⓶ The Monster will turn into【Human】form upon receiving Damage from the enemy\'s attack.\n\n'

'◆ When “Apex of Fortitude - Huaxi” is in【Human】form:\n'
'⓵ The Monster\'s Skill CD -1 at the end of each Round.\n'
'⓶ “Apex of Fortitude - Huaxi” will turn into【Dragon】form when its Active Skill is activated.\n'
'Condition:\n'
'The Leader is a Beast or Dragon, with "Apex of Fortitude - Huaxi" in the Team.\n\n'

'◆ Extend Runestone-moving time regardlessly by 3 seconds.\n'
'◆ After entering a Stage:\n'
'⓵ Skill CD of Dragons -5.\n'
'⓶ Skill CD of Beasts -2.\n'
'◆ At the end of the Round:\n'
'⓵ Turn Heart Runestones into Attributive Dragon Runestones (the Attribute that is not on the screen ranks first in priority).\n'
'⓶ Turn Earth Runestones into Enchanted Dragon Runestones.\n'
'◆ When 30 Race Runestones are dissolved cumulatively,\n'
'⇒ recover 50% HP each Round,\n'
'⇒ the Skill stays in play within the Wave (the accumulation resets every Wave).\n'
'◆ When Team HP is ≥50% before attacks,\n'
'⇒ Damage dealt to enemies x 5 additionally.\n'
'◆ When there are ≥3 Attributes of Monsters in the Team,\n'
'⇒ Earth Runestones also possess the effect of other Attributive Runestones.\n'
'Condition:\n'
'The Leader is "Apex of Fortitude - Huaxi", and the Ally is "Apex of Fortitude - Huaxi" or "Harmonic of Purification - Feiyin".'},
    
    {'chi_name':'姬臣',
'chif_name':'姬臣',
'eng_name':'jichen',

'chi_act':'龙息暴发 CD7\n\n'
'I. 若队长为龙类或兽类\n'
'⇒ 发动技能时自身转换为【龙】形态\n'
'II. 点选 2 横行的符石\n'
'⇒ 每横行转化固定位置的“暗及水”龙族强化符石各 3 粒\n'
'1 回合内\n'
'III. 全队攻击力 2 倍\n'
'IV. 下回合所有成员攻击力与此回合相同',
'eng_act':'Dragon Pneuma Burst CD7\n\n'
'I. If the Leader is a Dragon or Beast,\n'
'⇒ the Monster will turn into【Dragon】form upon Skill activation.\n'
'II. Tap 2 rows and turn each of them into 3 Enchanted Dark Dragon and 3 Enchanted Water Dragon Runestones at fixed positions.\n'
'For 1 Round:\n'
'III. Team Attack x 2.\n'
'IV. The Attack of all Members in the next Round will be the same as this Round.',

'chi_lead':'龙威破空\n\n'
'I. 龙类攻击力 6 倍及生命力 2.5 倍\n'
'II. 同时消除水、暗或心符石其中 2 种符石时\n'
'⇒ 龙类攻击力额外 4 倍\n'
'III. 水及暗符石互相兼具 50% 效果\n'
'IV. 延长移动符石时间 2.5 秒',
'eng_lead':'Majesty of Dragons\n\n'
'I. Dragon Attack x 6 & HP x 2.5.\n'
'II. If 2 out of 3 types of Runestones (Water, Dark & Heart) are dissolved in the same Round,\n'
'⇒ Dragon Attack x 4 additionally.\n'
'III. Water and Dark Runestones also possess 50% effect of each other.\n'
'IV. Extend Runestone-moving time by 2.5 seconds.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后，“傲志不訾 ‧ 姬臣”\n'
'⇒ 转换为【龙】形态\n\n'

'II. 当“傲志不訾 ‧ 姬臣”为【龙】形态时：\n'
'⓵ 自身及身旁龙类或兽类成员获得【邪马台祝福 ‧ 龙】\n'
'⓶ 受到敌人攻击后\n'
'⇒ 转换为【人】形态\n\n'

'III. 当“傲志不訾 ‧ 姬臣”为【人】形态时：\n'
'⓵ 回合结束时，自身技能 CD -1\n'
'⓶“傲志不訾 ‧ 姬臣”发动主动技能时\n'
'⇒ 自身转换为【龙】形态\n'
'发动条件：\n'
'队长为龙类或兽类，并以“傲志不訾 ‧ 姬臣”作成员\n\n'

'身上有【邪马台祝福．龙】的成员\n'
'⇒ 攻击力 1.5 倍\n'
'发动条件：\n'
'队长为龙类或兽类，并以“少华钧天 ‧ 华曦”或“傲志不訾 ‧ 姬臣”作成员\n\n'

'I. 进入关卡后，龙类成员技能 CD -5\n'
'II. 将移动符石时触碰的首 10 粒符石\n'
'⇒ 转化为龙族符石\n'
'III. 水及暗符石效果提升 200%\n'
'IV. 每消除 1 粒种族符石\n'
'⇒ 增加 1 连击 (Combo)\n'
'⇒ 最多可增加 30 Combo\n'
'V. 达至 15 连击 (Combo)\n'
'⓵ 所有成员无视“指定形状盾”\n'
'⓶ 回复 50% 生命力\n'
'发动条件：\n'
'以“傲志不訾 ‧ 姬臣”作队长，且队中只有龙类或兽类成员',
'eng_team':'Team Skill\n\n'
'◆ “Soaring Aspiration - Jichen” will turn into【Dragon】form after entering a Stage.\n\n'

'◆ When “Soaring Aspiration - Jichen” is in【Dragon】form:\n'
'⓵ The Monster and the neighboring Dragon or Beast acquire【Yamatai Blessing - Dragon】.\n'
'⓶ The Monster will turn into【Human】form upon receiving Damage from the enemy\'s attack.\n\n'

'◆ When “Soaring Aspiration - Jichen” is in【Human】form:\n'
'⓵ The Monster\'s Skill CD -1 at the end of each Round.\n'
'⓶ “Soaring Aspiration - Jichen” will turn into【Dragon】form when its Active Skill is activated.\n'
'Condition:\n'
'The Leader is a Beast or Dragon, with "Soaring Aspiration - Jichen" in the Team.\n\n'

'◆ Skill CD of Dragons -5 after entering a Stage.\n'
'◆ Turn the first 10 Runestones touched while moving into Dragon Runestones.\n'
'◆ The effect of Water and Dark Runestones increases by 200%.\n'
'◆ For every Race Runestone dissolved,\n'
'⇒ Combo count +1,\n'
'⇒ to the max +30.\n'
'◆ When 15 Combos are made:\n'
'⓵ Damage of the Team will be dealt regardless of Puzzle Shield.\n'
'⓶ Recover 50% HP.\n'
'Condition:\n'
'The Leader is "Soaring Aspiration - Jichen", with only Dragons or Beasts in the Team.\n\n'

'◆ Member(s) with【Yamatai Blessing - Dragon】\n'
'⇒ Attack x 1.5.\n'
'Condition:\n'
'The Leader is a Beast or Dragon, with "Apex of Fortitude - Huaxi" or "Soaring Aspiration - Jichen" in the Team.'},
    
   {'chi_name':'霏音',
'chif_name':'霏音',
'eng_name':'feiyin',

'chi_act':'猛兽极袭 CD7\n\n'
'I. 若队长为龙类或兽类\n'
'⓵ 发动技能时自身转换为【兽】形态\n'
'⓶ 还原所有“碎裂”的位置\n'
'II. 将兽类成员直行的符石\n'
'⇒ 转化为兽族强化符石\n'
'1 回合内\n'
'III. 连击 (Combo) 时攻击力提升 50%\n'
'IV. 受敌人反击伤害减少 100%\n'
'V. 解除“亡命爆击”',
'eng_act':'Assault of Wildness CD7\n\n'
'	I. If the Leader is a Dragon or Beast:\n'
'⓵ The Monster will turn into【Beast】form upon Skill activation.\n'
'⓶ Restore all cracked positions.\n'
'II. Turn the column(s) below Beast(s) into Enchanted Beast Runestones.\n'
'For 1 Round:\n'
'III. Attack bonus +50% for each Combo made.\n'
'IV. Damage reflected from enemies -100%.\n'
'V. Boss Skill “Death Damage” (receiving Damage upon the defeat of the enemy) will be nullified.',

'chi_lead':'兽威撼地\n\n'
'I. 兽类及龙类攻击力 6.5 倍及生命力 1.3 倍\n'
'II. 队伍中只有兽类成员时\n'
'⇒ 兽类生命力及回复力额外 1.3 倍\n'
'III. 达至 ≥6 连击 (Combo) 时\n'
'⇒ 龙类及兽类攻击力额外 2.5 倍\n'
'IV. 延长移动符石时间 2 秒',
'eng_lead':'Predatory Instinct\n\n'
'I. Beast & Dragon Attack x 6.5 & HP x 1.3.\n'
'II. When the Team has only Beasts,\n'
'⇒ Beast HP & Recovery x 1.3 additionally.\n'
'III. When ≥6 Combos are made,\n'
'⇒ Dragon & Beast Attack x 2.5 additionally.\n'
'IV. Extend Runestone-moving time by 2 seconds.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后，“琴息濯洗 ‧ 霏音”\n'
'⇒ 转换为【兽】形态\n\n'

'II. 当“琴息濯洗 ‧ 霏音”为【兽】形态时：\n'
'⓵ 自身攻击力及回复力 2 倍\n'
'⓶ 受到敌人攻击后\n'
'⇒ 转换为【人】形态\n\n'

'III. 当“琴息濯洗 ‧ 霏音”为【人】形态时：\n'
'⓵ 回合结束时，自身技能 CD -1\n'
'⓶“琴息濯洗 ‧ 霏音”发动主动技能时\n'
'⇒ 自身转换为【兽】形态\n'
'发动条件：\n'
'队长为龙类或兽类，并以“琴息濯洗 ‧ 霏音”作成员\n\n'

'I. 首批消除属性符石\n'
'⇒ 该种符石 2 粒相连即可发动消除\n'
'⇒ 效果持续至消除 1 种符石达 15 粒\n'
'II. 将移动符石时触碰的队伍成员属性符石\n'
'⇒ 转化为兽族强化符石\n'
'III. 兽类及龙类成员属性符石\n'
'⇒ 分别兼具 50% 其他符石效果\n'
'IV. 移动符石时间剩余大于或等于 50% \n'
'⇒ 该回合所受伤害减少 50% \n'
'V. 移动符石时间剩余小于50%\n'
'⓵ 所有成员追打 1 次\n'
'⓶ 所有成员无视“固定连击盾”\n'
'发动条件：\n'
'以“琴息濯洗 ‧ 霏音”作队长，并以“琴息濯洗 ‧ 霏音”或“少华钧天 ‧ 华曦”作战友',
'eng_team':'Team Skill:\n\n'
'◆ “Harmonic of Purification - Feiyin” will turn into【Beast】form after entering a Stage.\n'
'◆ When “Harmonic of Purification - Feiyin” is in【Beast】form:\n'
'⓵ The Monster\'s Attack & Recovery x 2.\n'
'⓶ The Monster will turn into【Human】form upon receiving Damage from the enemy\'s attack.\n\n'

'◆ III. When “Harmonic of Purification - Feiyin” is in【Human】form:\n'
'⓵ The Monster\'s Skill CD -1 at the end of each Round.\n'
'⓶ “Harmonic of Purification - Feiyin” will turn into【Beast】form when its Active Skill is activated.\n'
'Condition:\n'
'The Leader is a Beast or Dragon, "Harmonic of Purification - Feiyin" in the Team.\n\n'

'◆ By dissolving Attributive Runestones in the first batch,\n'
'⇒ Runestones of that Attribute can be dissolved by aligning 2 or more of them.\n'
'⇒ The effect stays in play until 15 Runestones of a type are dissolved.\n'
'◆ Turn Runestones of Members\' Attributes touched while moving into Enchanted Beast Runestones.\n'
'◆ Runestones of the Beasts\' and Dragons\' Attributes also possess 50% effect of other Runestones.\n'
'◆ When Runestone-moving time left is higher or equal to 50%,\n'
'⇒ Damage received -50% this Round.\n'
'◆ When Runestone-moving time left is lower than 50%:\n'
'⓵ Each Member launches an extra attack.\n'
'⓶ Damage of the Team will be dealt regardless of Fixed Combo Shield.\n'
'Condition:\n'
'The Leader is "Harmonic of Purification - Feiyin", and the Ally is "Harmonic of Purification - Feiyin" or "Apex of Fortitude - Huaxi.'},
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    {'chi_name':'莉莉丝',
'chif_name':'莉莉絲',
'eng_name':'lilith',

'chi_act':'融魂 ‧ 共鸣 ‧ 模式 CD6\n'
'选择【融魂模式】或【共鸣模式】形态\n'
'⇒ 所有“最初的仿魂 ‧ 莉莉丝”转换为所选择的形态\n'
'【融魂模式】\n'
'▋引爆所有符石\n'
'⇒ 掉落“五属及心”机械族符石各 5 粒\n'
'【共呜模式】\n'
'▋移除所有符石\n'
'⇒ 掉落强化符石\n\n'
'夺命凶器 CD6\n'
'I. 还原所有“碎裂”的位置\n'
'II. 将场上的符石\n'
'⇒ 变回原始模样\n'
'III. 将所有符石\n'
'⇒ 添加为机械族符石\n'
'IV. 对敌方全体造成5000 万的水属性伤害 4 次\n'
'1 回合内\n'
'V. 所有成员无视\n'
'⓵ 敌人防御力\n'
'⓶“连击相等盾”\n'
'⓷“强化突破”\n'
'⓸“固定连击盾”',
'eng_act':'Soul-merging ‧ Resonance ‧ Mode CD6\n'
'Select 【Soul-merging Mode】or 【Resonance Mode】 form:\n'
'⇒ All "The First Synthetic Soul - Lilith" will turn into the selected form.\n'
'【Soul-merging Mode】\n'
'▋Explode all Runestones to generate5 Machina Runestones of each type.\n'
'【Resonance Mode】\n'
'▋Remove all Runestones to generate Enchanted Runestones.\n\n'
'Mortiferous Weapon CD6\n'
'I. Restore all cracked positions.\n'
'II. Restore all Runestones to normal state.\n'
'III. Modify all Runestones to become Machina Runestones.\n'
'IV. Deal 50 million Water Damage to all enemies 4 times.\n'
'For 1 Round:\n'
'V. Damage will be dealt regardless of Defense, Equal-Combo Shield, Enchanted Runestone Shield and Fixed Combo Shield.',

'chi_lead':'仿魂绝杀\n\n'
'I. 全队攻击力 8 倍、生命力及回复力 1.8 倍\n'
'II. 必然延长移动符石时间 2.5 秒\n'
'III. 消除符石的种类愈多\n'
'⇒ 全队攻击力额外提升愈多\n'
'⇒ 最大 4 倍\n'
'IV. 队中有 ≥2 种属性成员时\n'
'⓵ 全队攻击力额外 1.8 倍\n'
'⓶ 每首批消除 6 粒符石\n'
'⇒ 增加 1 连击 (Combo)',
'eng_lead':'Synthetic Soul\'s Knack\n\n'
'I. Team Attack x 8; HP & Recovery x 1.8.\n'
'II. Extend Runestone-moving time regardlessly by 2.5 seconds.\n'
'III. The more the types of Runestones dissolved,\n'
'⇒ the higher the Team Attack increases additionally,\n'
'⇒ to the max x 4.\n'
'IV. When the Team has ≥2 Attributes:\n'
'⓵ Team Attack x 1.8 additionally.\n'
'⓶ For every 6 Runestones dissolved in the first batch,\n'
'⇒ Combo count +1.',

'chi_team':'队伍技能：\n\n'
'◆ 进场时，机械族成员的行动值\n'
'⇒ 提升至 100%\n'
'◆ 吸收每个敌人“首次攻击以外”的‘攻击伤害、“喋血屠刀”等扣除召唤师指定 % 生命力的敌技所造成的伤害\n'
'⇒ 以所吸收攻击力对敌方进行相克属性反击\n'
'◆ 所有符石兼具\n'
'⇒ 机械族成员属性及心符石效果\n'
'◆ 触碰“电击符石”时仍可移动符石\n'
'◆ 无视“燃烧”\n'
'◆ 无视“黏腐”\n'
'◆ 发动角色符石及于“最初的仿魂 ‧ 莉莉丝”直行最后结束转珠\n'
'⇒ 该“最初的仿魂 ‧ 莉莉丝”CD -1\n'
'◆ 根据最后结束转珠时放手的符石种类\n'
'⇒ 首批掉落该种强化符石\n'
'◆ 消除 1 组 ≥10 粒符石\n'
'⇒ 完全回复生命力\n'
'◆ 获得“数据运算”能力：\n'
'▋将所有符石转化为强化符石\n'
'▋将水符石由右下方开始向左排列\n'
'(面对“转化符石技能无效”技能仍可排列)\n'
'于回合开始时点击已储满的龙脉仪\n'
'⇒ 可触发“数据运算”能力 (每回合最多可使用 1 次)\n'
'发动条件：\n'
'以“最初的仿魂 ‧ 莉莉丝”作队长及战友\n\n'

'◆“最初的仿魂 ‧ 莉莉丝”\n'
'⇒ 获得【融魂模式】及【共鸣模式】2 种形态\n'
'发动条件：\n'
'以“最初的仿魂 ‧ 莉莉丝”作成员\n\n'

'◆“最初的仿魂 ‧ 莉莉丝”为以下形态时，可获得以下效果：\n'
'【共鸣模式】\n'
'⓵“幽闭空间”效果只影响 4 个角落的 4 格位置\n'
'⓶“最初的仿魂 ‧ 莉莉丝”的攻击力基值\n'
'⇒ 跟随攻击力基值最高的成员\n'
'【融魂模式】\n'
'⓵ 全队回复力变 0\n'
'⓶ 回合结束时，“最初的仿魂 ‧ 莉莉丝”技能 CD -1\n'
'发动条件：\n'
'以“最初的仿魂 ‧ 莉莉丝”作队长及战友\n\n'

'【机械动力】\n'
'I. 每首批消除 1 粒自身属性符石\n'
'⇒ 自身行动值提升 2%\n'
'II. 每首批消除 1 粒心符石\n'
'⇒ 自身行动值提升 1%\n'
'III. 行动值愈高\n'
'⇒ 自身攻击力提升愈多\n'
'⇒ 最大提升至 2 倍。\n'
'IV. 当所有机械族成员的行动值达至 50% 或以上时\n'
'⇒ 机械族成员属性的符石效果提升\n'
'⇒ 每个机械族成员可提升 10% 效果\n'
'⇒ 最高 60%\n'
'V. 当所有机械族成员的行动值达至 100% 时\n'
'⇒ 机械族成员每回合\n'
'以 25% 自身攻击力随机追打自身属性或自身克制属性的攻击 1 至 2 次\n'
'发动条件：\n'
'队伍中有 ≥2 个【机械族】成员',
'eng_team':'Team Skill:\n\n'
'◆ After entering a Stage, Fuel of all Machinas increases to 100%.\n'
'◆ Absorb the Attack-damage and Damage received from Boss Skills deducting a specific % of Summoner\'s HP such as "Bloody Scythe" etc. of each enemy from the 2nd attack onwards.\n'
'⇒ Launch an Attribute-effective Counterattack as much as the absorbed attack to enemies.\n'
'◆ All Runestones also possess the effect of Heart Runestones and Runestones of the Machinas\' Attributes in the Team.\n'
'◆ Runestone movement will not be stopped when an Electrified Runestone is touched.\n'
'◆ Boss Skills "Burning" and "Sticky" will be nullified.\n'
'◆ When a Character Runestone is triggered and the last Runestone movement ends in the column below "The First Synthetic Soul - Lilith",\n'
'⇒ Skill CD of that "The First Synthetic Soul - Lilith" -1.\n'
'◆ According to the last Runestone picked to end moving,\n'
'⇒ the first batch of Runestones to be dropped will be Enchanted Runestones of that type.\n'
'◆ By dissolving a group of ≥10 Runestones,\n'
'⇒ fully recover HP.\n'
'◆ Aquire "Data Calculation" ability:\n'
'▋Turn all Runestones into Enchanted Runestones.\n'
'▋Arrange Water Runestones from bottom right to left. (This effect will not be affected by Boss Skill "Runestone-turning Skill Nullifying")\n'
'The "Data Calculation" ability can be activated by tapping the fully charged Craft Apparatus at the beginning of the Round.\n'
'(One activation each Round.)\n\n'

'◆ Different effects will be granted when “The First Synthetic Soul - Lilith” is in either form:\n'
'【Resonance Mode】\n'
'⓵ Effect of "B&W Zone" will be limited to 4 corners.\n'
'⓶ Attack basic value of "The First Synthetic Soul - Lilith" will synchronize with that of the Member that has the highest Attack basic value.\n'
'【Soul-merging Mode】\n'
'⓵ Team Recovery becomes 0.\n'
'⓶ At the end of the Round,Skill CD of "The First Synthetic Soul - Lilith" -1.\n'
'Condition:\n'
'Both the Leader and Ally are "The First Synthetic Soul - Lilith".\n\n'

'◆ "The First Synthetic Soul - Lilith" acquires 2 forms: "Soul-merging Mode" and "Resonance Mode".\n'
'Condition:\n'
'There is "The First Synthetic Soul - Lilith" in the Team.\n\n'

'◆ 【Machina Dynamics】\n'
'⓵ For each Runestone of the Character\'s Attribute dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +2%.\n'
'⓶ For each Heart Runestone dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +1%.\n'
'⓷ The higher the Character\'s Fuel,\n'
'⇒ the higher the Character\'s Attack,\n'
'⇒ to the max x 2 additionally.\n'
'⓸ When all Machinas in the Team have ≥ 50% Fuel,\n'
'⇒ effects of Runestones of their Attributes increase,\n'
'⇒ 10% for each Machina present in the Team,\n'
'⇒ to the max 60%.\n'
'⓹ When all Machinas in the Team have 100% Fuel,\n'
'⇒ all Machinas randomly launch 1 to 2 extra attack(s) of its own Attribute or its Counter Attribute as much as 25% of its Attack every Round.\n'
'Condition:\n'
'There are 2 or more 【Machina Dynamics】 Members in the Team.'},
    
    {'chi_name':'刻珲',
'chif_name':'刻琿',
'eng_name':'kehun',

'chi_act':'五重魔导式 CD4\n\n'
'发动五重魔导式法阵，点选获取 1 回合效果：\n'
'【时间静济】\n'
'▋延长移动符石时间 10 秒\n'
'▋无视“燃烧”敌技\n\n'

'【元素欺诈】\n'
'▋引爆所有符石、冻结及石化符石\n'
'▋敌方全体转为木属性\n\n'

'【空间扭曲】\n'
'▋额外增加 3 行符石\n'
'▋将移动符石时触碰的符石\n'
'⇒ 添加为龙族符石\n\n'

'【物质分解】\n'
'▋全队攻击力 2.5 倍\n'
'▋“天道炎旌 ‧ 刻珲”技能 CD-1\n\n'

'【概念覆写】\n'
'▋全队无视“反首消符石盾”\n'
'▋将所有符石转化为强化符石\n\n'

'上述每个魔导式于战斗中只能发动 1 次\n'
'当发动了 3 次“五重魔导式”后，其后每次发动技能时效果改为：\n'
'1 回合内\n'
'I. 将敌方全体转为木属性\n'
'II. 将场上的符石变回原始模样\n'
'III. 额外增加 3 横行符石：\n'
'直行“五属及心”龙族强化符石\n'
'IV. 15 秒内，可任意移动符石而不会发动消除\n'
'V. 全队攻击力及回复力 2.5 倍\n'
'VI. 全队无视“反首消符石盾”\n'
'VII. 无视“燃烧”敌技',
'eng_act':'5-Layered Magic Formula CD4\n\n'
'By activating the 5-Layered Magic Formula, tap to acquire an effect for 1 Round:\n'
'【Time Freeze】\n'
'▋Extend Runestone-moving time by 10 seconds.\n'
'▋Boss Skill "Burning" will be nullified.\n\n'

'【Elemental Deception】\n'
'▋Explode all Runestones,Frozen and Petrified Runestones.\n'
'▋Alter the Attribute of all enemies into Earth.\n\n'

'【Space Distortion】\n'
'▋Add 3 rows of Runestones.\n'
'▋Modify the Runestones touched while movingto become Dragon Runestones.\n\n'

'【Matter Breakdown】\n'
'▋Team Attack x 2.5.\n'
'▋Skill CD of "Flames of Divine Order - Ke Hun" -1.\n\n'

'【Concept Overwriting】\n'
'▋Damage will be dealt regardless of Anti-Runestone Shield (First Batch).\n'
'▋Turn all Runestones into Enchanted Runestones.\n'

'Each layer of the magic formula can be activated once only in a battle.\n'
'After the 3rd activation of "5-Layered Magic Formula", the effect for each Skill activation will change as follows:\n'
'For 1 Round:\n'
'I. Alter the Attribute of all enemies into Earth.\n'
'II. Restore all Runestones to normal state.\n'
'III. Add 3 rows of Enchanted Dragon Runestones of 5 Attributes and Heart. (one type in each column)\n'
'IV. Unlimited Runestone-movement in 15 seconds without dissolving.\n'
'V. Team Attack & Recovery x 2.5.\n'
'VI. Damage will be dealt regardless of Anti-Runestone Shield (First Batch).\n'
'VII. Boss Skill "Burning" will be nullified.',

'chi_lead':'龙裔圣焰\n\n'
'I. 全队攻击力 8 倍及生命力 2 倍\n'
'II. 龙类成员生命力额外 1.6 倍及攻击力额外 4.5 倍\n'
'III. 必然延长移动符石时间 2 秒',
'eng_lead':'Dragonborn Flames\n\n'
'I. Team Attack x 8, HP x 2.\n'
'II. Dragon HP x 1.6 additionally, Attack x 4.5 additionally.\n'
'III. Extend Runestone-moving time regardlessly by 2 seconds.',

'chi_team':'队伍技能：\n\n'
'I. 所有符石兼具其他符石效果\n'
'II.“天道炎旌 ‧ 刻珲”\n'
'⇒ 无视“连击相等盾”\n'
'III. 进场时，随机 5 个位置\n'
'⇒ 出现“暗器”\n'
'IV. 回合结束时\n'
'⓵ 场上每有 1 个“暗器”\n'
'⇒ 回复 10% 生命力 (不会溢补)，\n'
'⓶ 随机 3 个位置\n'
'⇒ 出现“暗器”\,'
'⇒ 场上最多 5 个位置出现“暗器”\n'
'V. 每消除 1 粒“暗器”位置的符石\n'
'⓵ 所有成员追打 1 次\n'
'⓶ 全队无视敌人防御力\n'
'⓷ 该暗器会消失\n'
'VI. 克制敌人属性的伤害额外 3 倍\n'
'发动条件：\n'
'以“天道炎旌 ‧ 刻珲”作队长\n'

'每消除 1 粒龙族符石\n'
'⇒ 回复 3,000 点生命力\n'
'⇒ 消除 30 粒可回复最多 90,000 点\n'
'发动条件：\n'
'以“天道炎旌 ‧ 刻珲”作队长\n'

'“天道炎旌 ‧ 刻珲”及“终身契守 ‧ 和谨”进场 CD -6\n'
'发动条件：\n'
'以“天道炎旌 ‧ 刻珲”及“终身契守 ‧ 和谨”作成员',
'eng_team':'Team Skill:\n\n'
'◆ All Runestones also possess the effect of other Runestones.\n'
'◆ Damage of "Flames of Divine Order - Ke Hun" will be dealt regardless of Equal-Combo Shield.\n'
'◆ A "Hidden Weapon" will appear at 5 random positions after entering a Stage.\n'
'◆ At the end of the Round:\n'
'⓵ For every present "Hidden Weapon",\n'
'⇒ recover 10% HP (no overhealing).\n'
'⓶ "Hidden Weapons" will appear at 3 random positions,\n'
'⇒ to the max 5 "Hidden Weapons" to be present.\n'
'◆ For every Runestone dissolved at a "Hidden Weapon" position:\n'
'⓵ Each Member launches an extra attack.\n'
'⓶ Damage will be dealt regardless of Defense.\n'
'⓷ The "Hidden Weapon" at that position will disappear.\n'
'◆ Damage of the enemy\'s Weakness Attribute x 3 additionally.\n'
'◆ For each Dragon Runestone dissolved,\n'
'⇒ recover 3,000 HP\n'
'⇒ to the max 90,000 HP for 30 Runestones dissolved.\n'
'Condition:\n'
'The Leader is "Flames of Divine Order - Ke Hun".\n\n'

'◆ Skill CDs of "Lifelong Covenant - He Jin" -6 after entering a Stage.\n'
'Condition:\n'
'There are "Flames of Divine Order - Ke Hun" and "Lifelong Covenant - He Jin" in the Team.'},
    
    {'chi_name':'涅索伊',
'chif_name':'涅索伊',
'eng_name':'nesoi',

'chi_act':'绝灵圣枪 CD\n\n'
'I. 心符石的掉落率降至 0\n'
'II. 将原有几率增加至\n'
'⇒ 光符石的掉落率\n'
'III. 掉落的光符石\n'
'⇒ 以光强化符石代替\n'
'IV. 发动技能首回合及每回合结束时\n'
'⇒ 将木符石转为暗强化符石\n'
'V. 首批消除所有符石时\n'
'⇒ 光属性“神族及妖精类”成员 CD -1\n'
'(效果会在关闭此技能或死亡后消失)\n\n'

'此技能可随时关闭，关闭时：\n'
'2 回合内\n'
'⓵ 光属性“神族及妖精类”\n'
'⇒ 进入亢奋状态',
'eng_act':'Spear of Holy Spirits CD6\n\n'
'I. Drop rate of Heart Runestones will be transferred to that of Light Runestones.\n'
'II. Light Runestones to be dropped will be Enchanted Light Runestones.\n'
'III. Upon Skill activation and at the end of each Round,\n'
'⇒ turn Earth Runestones into Enchanted Dark Runestones.\n'
'IV. By dissolving all Runestones in the first batch,\n'
'⇒ Skill CDs of Light Gods & Light Elves -1.\n'
'The Skill stays in play until deactivation or defeat.\n\n'

'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'For 2 Rounds:\n'
'⓵ Turn Earth Runestones into Enchanted Dark Runestones.\n'
'⓶ Light Gods & Light Elves enter a hyper state.',

'chi_lead':'圣神威压\n\n'
'I. 神族及妖精类攻击力 7 倍、生命力及回复力 1.5 倍\n'
'II. 光属性“神族及妖精类”攻击力额外 3 倍、生命力及回复力额外 1.3 倍\n'
'III. 必然延长移动符石时间 3 秒\n'
'IV. 消除 ≥4 组符石时\n'
'⇒ 光属性、神族、妖精类攻击力额外 2 倍',
'eng_lead':'The Holy Intimidation\n\n'
'I. God & Elf Attack x 7; HP & Recovery x 1.5.\n'
'II. Light God & Light Elf Attack x 3 additionally, HP & Recovery x 1.3 additionally.\n'
'III. Extend Runestone-moving time regardlessly by 3 seconds.\n'
'IV. By dissolving ≥4 groups of Runestones\n'
'⇒ Light Attack, God Attack & Elf Attack x 2 additionally.',

'chi_team':'队伍技能：\n\n'
'I.“燃烧”敌技的伤害\n'
'⇒ 转化为我方生命力\n'
'II.“环光圣战 ‧ 涅索伊”\n'
'⇒ 进场 CD -6\n'
'III. 受到拥有“首消粒数盾”敌人的攻击伤害减少 50%\n'
'IV. 水、火、光、暗符石\n'
'⇒ 互相兼具效果\n'
'V. 光及暗符石兼具\n'
'⇒ 50% 心符石效果\n\n'
'VI. 根据场上附加效果的数量\n'
'获得以下效果：\n'
'▋≥1：全队攻击力 1.5 倍\n'
'▋≥2：增加 5 连击 (Combo)\n'
'▋≥3：神族及妖精类成员\n'
'⇒ 无视“固定连击盾”\n'
'▋≥4：神族及妖精类成员\n'
'⇒ 无视“三属盾”及“五属盾”\n'
'▋≥5：增加 8 Ex. Combo\n'
'发动条件：\n'
'以“环光圣战 ‧ 涅索伊”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Damage received from Boss Skill "Burning" will be converted to HP Recovery.\n'
'◆ Skill CD of "Halo Warfare - Nesoi" -6 after entering a Stage.\n'
'◆ Damage received from an enemy with Boss Skill "Runestone Number Shield (First Batch)" -50%.\n'
'◆ Water, Fire, Light and Dark Runestones also possess the effect of each other.\n'
'◆ Light and Dark Runestones also possess 50% effect of Heart Runestones.\n\n'
'◆ With a number of additional effect(s) in play:\n'
'▋≥1：Team Attack x 1.5.\n'
'▋≥2：Combo count +5.\n'
'▋≥3：God & Elf Damage will be dealt regardless of Fixed Combo Shield.\n'
'▋≥4：God & Elf Damage will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield.\n'
'▋≥5：Ex. Combo count +8.\n'
'Condition:\n'
'Both the Leader and Ally are "Halo Warfare - Nesoi".'},
    
    {'chi_name':'卑弥呼',
'chif_name':'卑彌呼',
'eng_name':'himiko',

'chi_act':'诡惑秘术 CD6\n\n'
'I. 解除龙类及兽类成员被封锁的技能\n'
'(此技能无视封锁技能)\n'
'II. 移除所有符石\n'
'⇒ 掉落心强化符石\n'
'1 回合内\n'
'III. 所有符石兼具\n'
'⇒ 200% 其他符石效果\n'
'IV. 若队中有 ≥2 个龙类或兽类成员\n'
'⓵ 全队攻击力及回复力 2.5 倍\n'
'⓶ 全队无视“指定形状盾”',
'eng_act':'Arcane Mystic CD6\n\n'
'I. Release the locked Skill(s) of Dragon(s) and Beast(s).\n'
'(This Skill will not be locked)\n'
'II. Remove all Runestones to generate Enchanted Heart Runestones.\n'
'For 1 Round:\n'
'III. All Runestones also possess 200% effect of other Runestones.\n'
'IV. If there are ≥2 Dragons or Beasts in the Team:\n'
'⓵ Team Attack & Recovery x 2.5.\n'
'⓶ Damage of the Team will be dealt regardless of Puzzle Shield.',

'chi_lead':'元素共生\n\n'
'I. 全队攻击力 7 倍及生命力 1.5 倍\n'
'II. 龙类及兽类成员攻击力则 28 倍、生命力则 3 倍\n'
'III. 火、光、暗、心符石\n'
'⇒ 互相兼具 50% 效果I. 全队攻击力 7 倍及生命力 1.5 倍\n'
'II. 龙类及兽类成员攻击力则 28 倍、生命力则 3 倍\n'
'III. 火、光、暗、心符石\n'
'⇒ 互相兼具 50% 效果',
'eng_lead':'Elemental Symbiosis\n\n'
'I. Team Attack x 7 & HP x 1.5.\n'
'II. Dragon & Beast Attack x 28 & HP x 3.\n'
'III. Fire, Light, Dark and Heart Runestones also possess 50% effect of each other.',

'chi_team':'队伍技能：\n\n'
'获得“秘术土偶”能力：\n'
'I. 所有成员技能 CD -6\n'
'II. 完全回复生命力\n'
'1 回合内\n'
'III. 可任意移动符石而不会发动消除\n'
'于回合开始时点击已储满的龙脉仪\n'
'⇒ 可触发此能力\n'
'(需消耗 100% 龙脉仪能量及消耗龙脉仪使用次数 1 次)\n'
'发动条件：\n'
'以“朔月帝女 ‧ 卑弥呼”作队长及战友\n\n'

'I. 延长移动符石时间至 20 秒\n'
'II. 心符石兼具属性符石效果\n'
'III. 首批只消除 1 种属性符石及没有首批消除心符石\n'
'⇒ 所有成员追打该属性攻击 1 次\n'
'IV. 首批只消除心符石\n'
'⇒ 左方第 2 位成员追打五属攻击各 1 次\n'
'V. 首批只消除 1 组符石\n'
'⇒ 增加 9 连击 (Combo)\n'
'发动条件：\n'
'以“朔月帝女 ‧ 卑弥呼”作队长及战友\n\n'

'I. 龙类及兽类成员\n'
'⇒ 增加 2,500 点攻击力基值\n'
'II. 队中有 ≥2 只龙类或兽类成员：\n'
'⓵ 无视“黏腐”敌技\n'
'⓶ 触碰电击符石时仍可移动符石\n'
'⓷ 触碰暴风时仍可移动符石\n'
'III. 队中有 ≥3 只龙类或兽类成员：\n'
'“朔月帝女 ‧ 卑弥呼”、龙类、兽类成员\n'
'⓵ 无视“固定连击盾”\n'
'⓶ 无视“三属盾”、“五属盾”\n'
'发动条件：\n'
'以“朔月帝女 ‧ 卑弥呼”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Acquire “Arcane Dogū” ability:\n'
'I. Skill CD of all Members -6.\n'
'II. Fully recover HP.\n'
'For 1 Round:\n'
'III. Unlimited Runestone movement without dissolving.\n'
'◆ This ability can be activated at the beginning of the Round by tapping the fully charged Craft Apparatus at the expense of 100% of the power gathered and one activation of Dragonic Compulsion.\n'
'◆ Extend Runestone-moving time to 20 seconds.\n'
'◆ Heart Runestones also possess the effect of Attributive Runestones.\n'
'◆ When Runestones of only 1 Attribute are dissolved and no Heart Runestones are dissolved in the first batch,\n'
'⇒ each Member launches an extra attack of that Attribute.\n'
'◆ When only Heart Runestones are dissolved in the first batch,\n'
'⇒ the 2nd Member from the left launches 5 extra attacks (one Attribute each).\n'
'◆ When only a group of Runestones is dissolved in the first batch,\n'
'⇒ Combo count +9.\n'
'◆ Attack basic value of each Dragon & Beast +2500.\n\n'

'◆ When there are ≥2 Dragons or Beasts in the Team:\n'
'⓵ Boss Skill "Sticky" will be nullified.\n'
'⓶ Runestone movement will not be stopped when an Electrified Runestone is touched.\n'
'⓷ Runestone movement will not be stopped when a tornado is touched.\n\n'

'◆ When there are ≥3 Dragons or Beasts in the Team:\n'
'“Queen of Yamatai - Himiko”, Dragon(s) & Beast(s):\n'
'⓵ Damage will be dealt regardless of Fixed Combo Shield.\n'
'⓶ Damage will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield.\n'
'Condition:\n'
'Both the Leader and Ally are “Queen of Yamatai - Himiko”.'},
    
    {'chi_name':'蚩尤',
'chif_name':'蚩尤',
'eng_name':'chiyou',

'chi_act':'血战山河 CD8\n\n'
'I. 若以九黎战神 ‧ 蚩尤作队长\n'
'⇒ 还原所有“碎裂”的位置\n'
'II. 点选其中 1 个版面\n'
'⓵ 移除所有符石\n'
'⓶ 掉落该固定版面符石\n\n'

'▋ 九战九胜【水、火、木】 \n'
'▋ 制五兵之器【五属及心】 \n'
'▋ 三日三夜雾冥【光、暗、心】\n\n' 

'狂战状态下才可发动\n'
'▋ 八方万邦弭服【终极 ‧ 五属及心】 ',
'eng_act':'Heroic Mettle\n\n'
'I. If the Leader is "Divinity of War - Chiyou",\n'
'⇒ restore all cracked positions.\n'
'II. Tap one of the board setups to:\n'
'⓵ Remove all Runestones.\n'
'⓶ Generate Runestones according to the setup.\n\n'

'▋Setup 1【Water, Fire, Earth】\n'
'▋Setup 2【5-Attribute & Heart】\n'
'▋Setup 3【Light, Dark, Heart】\n\n'

'Available only in the "Berserk" mode:\n'
'▋Setup 4【Ultimate - 5-Attribute & Heart】',

'chi_lead':'战神领军\n\n'
'I. 全队攻击力 7 倍及生命力 1.5 倍\n'
'II. 必然延长移动符石时间 2.5 秒\n'
'III. 减少 20% 所受伤害，\n'
'IV. 所受火属性伤害则减少 40%\n'
'V. 若队中只有火属性成员时\n'
'⇒ 全队攻击力额外 1.2 倍\n'
'VI. 若队中有 ≥2 种属性成员\n'
'⇒ 全队攻击力额外 1.5 倍\n'
'VII. 消除的符石愈多\n'
'⇒ 攻击力额外提升愈多\n'
'⇒ 消除 30 粒可达至最大 4 倍',
'eng_lead':'God of War\n\n'
'I. Team Attack x 7 & HP x 1.5.\n'
'II. Extend Runestone-moving time regardlessly by 2.5 seconds.\n'
'III. Damage received -20%.\n'
'IV. Fire Damage received -40%.\n'
'V. When the Team has only Fire Attribute,\n'
'⇒ Team Attack x 1.2 additionally.\n'
'VI. When the Team has ≥2 Attributes,\n'
'⇒ Team Attack x 1.5 additionally.\n'
'VII. The more the Runestones dissolved,\n'
'⇒ the higher the Attack increases additionally,\n'
'⇒ to the max x 4 for 30 Runestones.',

'chi_team':'队伍技能：\n\n'
'I. 将移动符石时触碰的电击、冻结、弱化、化血、石化符石状态解除\n'
'⇒ 并转化为神族符石\n'
'II.“燃烧”敌技伤害减至 1\n'
'III. 记录“移动符石时间完结一刻”场上的符石分布\n'
'⇒ 首批掉落所记录的符石\n'
'(并加强为神族强化符石)\n'
'IV. 火符石兼具其他符石效果\n'
'V. 其他符石兼具火符石效果\n'
'VI.“九黎战神 ‧ 蚩尤”的攻击\n'
'⇒ 无视指定减伤抗性敌技\n'
'VII.“九黎战神 ‧ 蚩尤”\n'
'⇒ 技能 CD -2\n'
'VIII. 于“九黎战神 ‧ 蚩尤”直行位置结束转珠\n'
'(需消除符石)\n'
'⇒ 完全回复生命力\n'
'发动条件：\n'
'以“九黎战神 ‧ 蚩尤”作队长及战友\n\n'

'I. 触碰“燃烧”位置或累积消除 ≥30 粒火符石后\n'
'⇒“九黎战神 ‧ 蚩尤”进入狂战状态\n'
'* 召唤师死亡后结束狂战状态及重置累积火符石数量\n'
'II. 狂战状态的“九黎战神 ‧ 蚩尤”\n'
'⓵ 攻击力 2.5 倍\n'
'⓶ 攻击克制水属性目标\n'
'⓷ 无视敌人防御力\n'
'发动条件：\n'
'以“九黎战神 ‧ 蚩尤”作成员',
'eng_team':'Team Skill:\n\n'
'◆ All Electrified, Frozen, Weakened, Lock-for-Recovery and Petrified Runestones touched while moving will be restored to normal state and turned into God Runestones.\n'
'◆ Reduce the Damage by “Burning” to 1.\n'
'◆ Record the distribution of Runestones upon the completion of moving Runestones.\n'
'⇒ The first batch of Runestones to be dropped will be Enchanted God Runestones of the recorded distribution.\n'
'◆ Fire Runestones also possess the effect of other Runestones.\n'
'Other Runestones also possess the effect of Fire Runestones.\n'
'◆ Damage of “Divinity of War - Chiyou” will be dealt regardless of enemies\' specific damage-reducing resistance.\n'
'◆ Skill CD of “Divinity of War - Chiyou” -2.\n'
'◆ When Summoner stops moving Runestones in the column below “Divinity of War - Chiyou” (dissolving Runestones is necessary),\n'
'⇒ fully recover HP.\n'
'Condition:\n'
'Both the Leader and Ally are "Divinity of War - Chiyou".\n\n'

'◆ By touching a “Burning” position or dissolving ≥30 Fire Runestones cumulatively,\n'
'⇒ “Divinity of War - Chiyou” enters the "Berserk" mode.\n'
'* "Berserk" mode will be ended and the number of accumulated Fire Runestones will be reset upon defeat.\n'
'◆ When “Divinity of War - Chiyou” is in the “Berserk” mode:\n'
'⓵ Its Attack x 2.5.\n'
'⓶ Its Damage can overpower Water enemies.\n'
'⓷ Its Damage will be dealt regardless of Defense.\n'
'Condition:\n'
'There is "Divinity of War - Chiyou" in the Team.'},
    
    {'chi_name':'项羽',
'chif_name':'項羽',
'eng_name':'xiangyu',

'chi_act':'力拔山河 CD8\n\n'
'I. 将场上的符石变回原始模样\n'
'1 回合内\n'
'II. 点选元素法阵上的 1 粒符石\n'
'⇒ 该种符石以外的符石\n'
'首批 1 粒即可发动消除\n'
'III. 可任意移动符石而不会发动消除',
'eng_act':'Over the Mountains and Rivers CD8\n\n'
'I. Restore all Runestones to normal state.\n'
'For 1 Round:\n'
'II. By tapping a Runestone on the Magic Circle of Elements, Runestones not of that type can be dissolved singly or in groups of 2 or more.\n'
'III. Unlimited Runestone movement without dissolving.',

'chi_lead':'无双之霸\n\n'
'I. 光属性攻击力 7.5 倍、生命力及回复力 1.8 倍\n'
'II. 必然延长移动符石时间 2 秒\n'
'III. 消除 ≥3 组符石时\n'
'⇒ 全队攻击力额外 3.5 倍\n'
'IV. 首批消除所有光符石时\n'
'⇒ 光属性攻击力额外 1.5 倍',
'eng_lead':'Fight of the Hegemon\n\n'
'I. Light Attack x 7.5, HP & Recovery x 1.8.\n'
'II. Extend Runestone-moving time regardlessly by 2 seconds.\n'
'III. By dissolving ≥3 groups of Runestones,\n'
'⇒ Team Attack x 3.5 additionally.\n'
'IV. By dissolving all present Light Runestones in the first batch,\n'
'⇒ Light Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'◆ 移动符石时每触碰 1 粒光符石\n'
'⇒ 回复 2000 点生命力\n'
'⇒ 直至生命力全满\n'
'◆ 无视“黏腐”敌技\n'
'◆ 触碰电击符石时仍可移动符石\n'
'发动条件：\n'
'以“破阵无双 ‧ 项羽”作队长及战友\n\n'

'◆ 所有符石兼具光符石效果\n'
'◆ 每消除 1 组符石\n'
'⇒ 额外计算多 1 连击 (Combo)\n'
'发动条件：\n'
'以“破阵无双 ‧ 项羽”作队长及战友；且队中只有光属性成员\n\n'

'◆ 队伍成员属性符石\n'
'⇒ 互相兼具效果\n'
'◆ 队长及战友的队长技能“无双之霸”变为“盖世之气”\n'
'发动条件：\n'
'以“破阵无双 ‧ 项羽”作队长及战友；且队中有 ≥4 种属性成员\n\n'

'◆ 若“楚颜杀姬 ‧ 虞姬”为左方起第 2 位成员\n'
'⇒“楚颜杀姬 ‧ 虞姬”转换为“破阵无双 ‧ 项羽”的属性\n'
'◆“破阵无双 ‧ 项羽”及“楚颜杀姬 ‧ 虞姬”\n'
'⓵ 技能 CD -3\n'
'⓶“生命力及攻击力”基值 2 倍\n'
'发动条件\n'
'以“破阵无双 ‧ 项羽”作队长，以“楚颜杀姬 ‧ 虞姬”作成员',
'eng_team':'Team Skill:\n\n'
'◆ For every Light Runestone touched while moving,\n'
'⇒ Recover 2000 HP,\n'
'⇒ until Team HP is full.\n'
'◆ Boss Skill "Sticky" will be nullified.\n'
'◆ Runestone movement will not be stopped when an Electrified Runestone is touched.\n'
'Condition:\n'
'Both the Leader and Ally are "Hegemon of the Empire - Xiang Yu".\n\n'

'◆ All Runestones also possess the effect of Light Runestones.\n'
'For every group of Runestones dissolved,\n'
'⇒ Combo count +1.\n'
'Condition:\n'
'Both the Leader and Ally are "Hegemon of the Empire - Xiang Yu", with only Light Members in the Team.\n\n'

'◆ Runestones of Team Members\' Attributes also possess the effect of each other.\n'
'◆ Change the Leader Skill "Fight of the Hegemon" of the Leader and Ally to "Might of the Hegemon".\n'
'I. Team Attack x 9, HP & Recovery x 1.6.\n'
'II. Extend Runestone-moving time regardlessly by 2 seconds.\n'
'III. By dissolving ≥3 types of Runestones,\n'
'⇒ Team Attack x 2 additionally.\n'
'IV. The first batch of Runestones to be dropped will be Enchanted Runestones of the Member\'s Attribute in that column.\n'
'* Runestones to be dropped later will be arranged in proper order.\n'
'Condition:\n'
'Both the Leader and Ally are "Hegemon of the Empire - Xiang Yu", with 4 or more Attributes in the Team.\n\n'

'◆ If "Beguiling Death - Yu Miaoyi" is the 2nd Member from the left,\n'
'⇒ the Attribute of "Beguiling Death - Yu Miaoyi" will synchronize with that of "Hegemon of the Empire - Xiang Yu".\n'
'◆ "Hegemon of the Empire - Xiang Yu" and "Beguiling Death - Yu Miaoyi":\n'
'⓵ Skill CDs -3.\n'
'⓶ HP & Attack basic value x 2.\n'
'Condition:\n'
'The Leader is "Hegemon of the Empire - Xiang Yu", with "Beguiling Death - Yu Miaoyi" in the Team.'},
    
    {'chi_name':'青圭变身',
'chif_name':'青圭變身',
'eng_name':'qingguitrans',

'chi_act':'苍璧诱敌 CD5\n'
'点选元素法阵上的 1 粒符石\n'
'I. 将该种属性符石转化为龙族强化符石\n'
'II. 并将敌方全体转为该属性持续 5 回合\n'
'III. 1 回合内，自身攻击力 5 倍\n\n'
'原璧之固 CD6\n'
'3 回合内\n'
'I. 心符石的掉落率降至 0并将原有几率增加至\n'
'⇒ 其他符石的掉落率\n'
'II. 队伍不受中毒技能影响\n'
'III. 木属性及龙类攻击力 2 倍',
'eng_act':'	Allure of the Jade CD5\n'
'I. By tapping a Runestone on the Magic Circle of Elements, Runestones of that type will be turned into Enchanted Dragon Runestones.\n'
'II. Turn all enemies\' into that Attribute for 5 Rounds.\n'
'III. The Monster\'s Attack x 5 for 1 Round.\n\n'
'Solidity of the Jade CD6\n'
'For 3 Rounds:\n'
'I. Drop rate of Heart Runestones will be transferred to that of other Runestones.\n'
'II. The Team will not be poisoned.\n'
'III. Earth and Dragon Attack x 2.',

'chi_lead':'绝世奇玉\n\n'
'I. 龙类攻击力 6 倍及生命力 1.4 倍队伍中只有龙类成员时：\n'
'II. 水、木、暗符石分别兼具\n'
'⇒ 50% 其他属性符石效果\n'
'III. 首批消除的连击 (Combo) 数目\n'
'⇒ 会加入下回合的连击 (Combo) 数目\n'
'⇒ 下回合随机转化相应粒数的龙族强化符石',
'eng_lead':'Jade of Supremacy\n\n'
'I. Dragon Attack x 6 & HP x 1.4.\n'
'When the Team has only Dragons:\n'
'II. Water, Earth and Dark Runestones also possess 50% effect of other Attributive Runestones.\n'
'III. For Combos made in the first batch:\n'
'⇒ Combos will be added to the next Round.\n'
'⇒ Runestones of the same number will be turned into Enchanted Dragon Runestones in the next Round',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后\n'
'⇒ 龙类成员的主动技能 CD 变 0\n'
'II. 龙类成员每 1 次发动主动技能\n'
'⇒ 永久提升全队攻击力\n'
'⇒ 发动 20 次可提升至最大 6 倍\n'
'III. 连击 (Combo) 数目愈多\n'
'⇒ 攻击力提升愈多\n'
'⇒ 15 连击可达至最大 2.5 倍\n'
'IV. 延长移动符石时间 3 秒\n'
'V. 每消除 1 粒龙族符石\n'
'⇒ 回复 3,000 点生命力\n'
'⇒ 消除 30 粒可回复最多 90,000 点\n'
'发动条件：\n'
'以“和氏之璧 ‧ 青圭”或 “纹龙啸息 ‧ 青圭”作队长及战友\n\n'
'能量储存条件：1 回合内消除 3 粒或以上的木符石',
'eng_team':'Team Skill:\n\n'
'◆ After entering a stage, Active Skill CDs of Dragons become 0.\n'
'◆ Every time a Dragon activating its Skill, Team Attack increases onwards, to the max x 6 for 20 times.\n'
'◆ The more the Combos made, the higher the Team Attack increases additionally, to the max x 2.5 for 15 Combos.\n'
'◆ Extend Runestone-moving time by 3 seconds.\n'
'◆ For each Dragon Runestone dissolved,\n'
'⇒ recover 3,000 HP\n'
'⇒ to the max 90,000 HP for 30 Runestones dissolved.\n'
'Condition:\n'
'The Leader and Ally are "Jade of Prestige - Qing Gui" or "Howl of Rune Dragon - Qing Gui".\n\n'

'* EP stacking condition: \n'
'Dissolve ≥3 Earth Runestones in 1 Round\n'
'⇒ EP +1,\n'
'⇒ to the max +1 each Round.'},
    
    {'chi_name':'青圭',
'chif_name':'青圭',
'eng_name':'qinggui',

'chi_act':'苍璧诱敌 CD5\n'
'点选元素法阵上的 1 粒符石\n'
'I. 将该种属性符石转化为龙族强化符石\n'
'II. 并将敌方全体转为该属性持续 5 回合\n'
'III. 1 回合内，自身攻击力 5 倍\n\n'
'变身 CD8\n'
'变身,\n'
'所有符石转化为龙族符石\n'
'（变身后技能请查看/check 青圭变身）',
'eng_act':'Allure of the Jade\n'
'I. By tapping a Runestone on the Magic Circle of Elements, Runestones of that type will be turned into Enchanted Dragon Runestones.\n'
'II. Turn all enemies\' into that Attribute for 5 Rounds.\n'
'III. The Monster\'s Attack x 5 for 1 Round.\n\n'
'Switching CD8\n'
'Switch. Modify all Runestones to become Dragon Runestones.\n'
'(Active Skill after switching please check /check qingguitrans)',

'chi_lead':'惊世璞玉\n\n'
'I. 龙类攻击力 5 倍及生命力 1.8 倍\n'
'II. 消除龙族符石时\n'
'⇒ 自身攻击力 2.5 倍\n'
'III. ≥3 个龙类成员发动攻击时\n'
'⇒ 全队攻击力额外 2.4 倍\n'
'IV. 队伍中只有龙类成员时\n'
'⇒ 木符石兼具 25% 其他属性符石效果',
'eng_lead':'Jade of Superiority\n\n'
'I. Dragon Attack x 5 & HP x 1.8.\n'
'II. By dissolving Dragon Runestones,\n'
'⇒ the Monster\'s Attack x 2.5.\n'
'III. When ≥3 Dragons launch attacks in the same Round,\n'
'⇒ Team Attack x 2.4 additionally.\n'
'IV. When the Team has only Dragons,\n'
'⇒ Earth Runestones also possess 25% effect of other Attributive Runestones.',

'chi_team':'队伍技能：\n\n'
'I. 进入关卡后\n'
'⇒ 龙类成员的主动技能 CD 变 0\n'
'II. 龙类成员每 1 次发动主动技能\n'
'⇒ 永久提升全队攻击力\n'
'⇒ 发动 20 次可提升至最大 6 倍\n'
'III. 连击 (Combo) 数目愈多\n'
'⇒ 攻击力提升愈多\n'
'⇒ 15 连击可达至最大 2.5 倍\n'
'IV. 延长移动符石时间 3 秒\n'
'V. 每消除 1 粒龙族符石\n'
'⇒ 回复 3,000 点生命力\n'
'⇒ 消除 30 粒可回复最多 90,000 点\n'
'发动条件：\n'
'以“和氏之璧 ‧ 青圭”或 “纹龙啸息 ‧ 青圭”作队长及战友\n'
'＊此召唤兽于 CD 0 时可以变身，变身后将以消耗能量点的方式发动技能。召唤兽的技能等级愈高，发动技能时所需的能量值愈低。变身时，能量点为全满状态 (12 点)；当能量点未满时，可以于 1 回合内消除 3 粒或以上的木符石，以储存 1 点能量点。',
'eng_team':'Team Skill:\n\n'
'◆ After entering a stage, Active Skill CDs of Dragons become 0.\n'
'◆ Every time a Dragon activating its Skill, Team Attack increases onwards, to the max x 6 for 20 times.\n'
'◆ The more the Combos made, the higher the Team Attack increases additionally, to the max x 2.5 for 15 Combos.\n'
'◆ Extend Runestone-moving time by 3 seconds.\n'
'◆ For each Dragon Runestone dissolved,\n'
'⇒ recover 3,000 HP\n'
'⇒ to the max 90,000 HP for 30 Runestones dissolved.\n'
'Condition:\n'
'The Leader and Ally are "Jade of Prestige - Qing Gui" or "Howl of Rune Dragon - Qing Gui".\n\n'

'【Switch】\n'
'I. This Character can Switch to another form when its Skill CD reaches 0.\n'
'⇒ After Switching, Skills can be activated through consuming Energy Points (EPs).\n'
'II. The higher the Character\'s Skill Level,\n'
'⇒ the fewer EPs it needs to activate its Skills.\n'
'III. Character\'s EPs will be at maximum (12 EPs) after Switching.\n'
'IV. If EPs are consumed, Summoner can restack them:\n'
'Dissolve ≥3 Earth Runestones in 1 Round\n'
'⇒ EP +1,\n'
'⇒ to the max +1 each Round.'},
    
    {'chi_name':'艾莉亚',
'chif_name':'艾莉亞',
'eng_name':'aria',

'chi_act':'魔幻之秘 CD6\n\n'
'所有符石转化为固定数量的水人族强化、火人族强化及木人族强化符石。1 回合内，同时消除水强化、火强化及木强化符石时，全队攻击力 2 倍及无视五属盾',
'eng_act':'The Mystery of Magic CD6\n\n'
'Turn all Runestones into Enchanted Water Human, Enchanted Fire Human and Enchanted Earth Human Runestones of fixed numbers. For 1 Round, by dissolving Enchanted Water, Enchanted Fire and Enchanted Earth Runestones, Team Attack x 2 and Damage will be dealt regardless of "Quintet Elemental Shield".',

'chi_lead':'稀世力量\n\n'
'I. 水属性及人类攻击力 6.5 倍\n'
'II. 必然延长移动符石时间 1 秒\n'
'III. 水、火、木符石兼具\n'
'⇒ 50% 心符石效果\n'
'IV. 同时消除水、火、木符石其中 2 种符石时\n'
'⇒ 水属性及人类攻击力额外 3 倍\n'
'V. 同时消除水、火、木符石时\n'
'⇒ 个人追打水、火、木属性攻击各 1 次',
'eng_lead':'Power of the Holy Grail\n\n'
'I. Water & Human Attack x 6.5.\n'
'II. Extend Runestone-moving time regardlessly by 1 second.\n'
'III. Water, Fire and Earth Runestones also possess 50% effect of Heart Runestones.\n'
'IV. If 2 out of 3 types of Runestones (Water, Fire & Earth) are dissolved in the same Round,\n'
'⇒ Water & Human Attack x 3 additionally.\n'
'V. By dissolving Water, Fire and Earth Runestones in the same Round, the Monster launches 3 extra attacks (Water, Fire and Earth each).',

'chi_team':'队伍技能：\n\n'
'火符石兼具水及木符石效果\n'
'发动条件：\n'
'以圣杯之永息 · 艾莉亚作队长及战友，且队伍中有火属性成员\n\n'

'木符石兼具水及火符石效果\n'
'发动条件：\n'
'以圣杯之永息 · 艾莉亚作队长及战友，且队伍中有木属性成员\n\n'

'根据队伍成员发动攻击的次数及属性 (包括全体攻击)，于回合结束时转化相应数量及属性的人族符石，每种属性符石最多转化 6 粒。\n'
'消除人族符石时，全队攻击力提升 2.5 倍\n'
'发动条件：\n'
'以圣杯之永息 · 艾莉亚作队长及战友\n\n'

'当前生命力全满时，下一次所受伤害不会使你死亡 (同 1 回合只会发动 1 次)\n'
'发动条件：\n'
'以圣杯之永息 · 艾莉亚作队长及战友，且队伍中只有水属性或人类成员',
'eng_team':'Team Skill:\n\n'
'◆ When HP is full, the next Damage received will not lead to your defeat (one activation each Round).\n'
'Condition:\n'
'Both the Leader and Ally are "Chalice of Eternity - Aria", with only Humans or Water Members in the Team.\n\n'

'◆ Fire Runestones also possess the effects of Water and Earth Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Chalice of Eternity - Aria", with 1 or more Fire Member in the Team.\n\n'

'◆ Earth Runestones also possess the effects of Water and Fire Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Chalice of Eternity - Aria", with 1 or more Earth Member in the Team.\n\n'

'◆ Turn Runestones into Human Runestones according to Team Members\' number of attacks and Attributes at the end of the Round (including Full Attack), to the max 6 Runestones to be turned for each Attribute.\n'
'◆ By dissolving Human Runestones, Team Attack x 2.5 additionally.\n'
'Condition:\n'
'Both the Leader and Ally are "Chalice of Eternity - Aria".'},
    
    {'chi_name':'潘朵拉',
'chif_name':'潘朵拉',
'eng_name':'pandora',

'chi_act':'绝望的诅咒 CD6\n\n'
'I. 引爆所有风化、冻结、弱化、电击、石化符石\n'
'II. 点选元素法阵上的 1 种属性\n'
'⇒ 所有成员追打该属性攻击 1 次\n'
'III. 若队伍中只有妖精类成员\n'
'⇒ 将所有符石转化为妖族强化符石',
'eng_act':'Imprecation of Desperation CD6\n\n'
'I. Explode all Weathered, Frozen, Weakened, Electrified and Petrified Runestones.\n'
'II. By tapping an Attribute on the Magic Circle of Elements, each Member launches an extra attack of that Attribute.\n'
'III. If the Team consists of only Elves, turn all Runestones into Enchanted Elf Runestones.',

'chi_lead':'万恶之源\n\n'
'I. 妖精类生命力、攻击力、回复力 1.6 倍\n'
'II. 达至 ≥5 连击 (Combo)\n'
'⓵ 全队攻击力额外 2 倍\n'
'⓶ 妖精类攻击力则额外 5 倍\n'
'III. 必然延长移动符石时间 1.5 秒\n'
'IV. 所有符石兼具 300% 其他符石效果',
'eng_lead':'Source of Sins\n\n'
'I. Elf HP, Attack & Recovery x 1.6.\n'
'II. When ≥5 Combos are made,\n'
'⓵ Team Attack x 2 additionally,\n'
'⓶ Elf Attack x 5 additionally.\n'
'III. Extend Runestone-moving time regardlessly by 1.5 seconds.\n'
'IV. All Runestones also possess 300% effect of other Runestones.',

'chi_team':'队伍技能：\n\n'
'所有成员的回复力跟随回复力最高的成员\n'
'发动条件：\n'
'以“希望之盒 ‧ 潘朵拉”作成员，且队中只有妖精类成员\n\n'

'I. 进入关卡后，将龙脉仪储满\n'
'II. 获得“潘朵拉盒子”能力：\n'
'3 回合内\n'
'I. 最左方及最右方直行的符石\n'
'⇒ 不能消除及引爆\n'
'II. 当前生命力全满时\n'
'⇒ 所受伤害不会使你死亡\n'
'III. 每消除 1 连击 (Combo)\n'
'⇒ 额外计算多 4 连击 (Combo)\n'
'于回合开始时点击已储满的龙脉仪\n'
'⇒ 可触发“潘朵拉盒子”能力\n'
'发动条件：\n'
'以“希望之盒 ‧ 潘朵拉”作队长及战友\n\n'

'将每个成员回复力基值的 5 倍\n'
'⇒ 各自加入自身攻击力基值\n'
'发动条件：\n'
'以“希望之盒 ‧ 潘朵拉”作队长及战友，且队伍中只有妖精类成员',
'eng_team':'Team Skill:\n\n'
'◆ Change the Craft Apparatus into the "Pandora\'s Box" with the following Skills:\n'
'◆ For 3 Rounds:\n'
'I. The columns of Runestones on the far left and far right sides cannot be dissolved or exploded.\n'
'II. When HP is full, the Damage received will not lead to your defeat.\n'
'III. Combo count +4 for every Combo made.\n'
'◆ The "Pandora\'s Box" can be activated at the beginning of the Round by tapping the fully charged Craft Apparatus.\n'
'◆ The Craft Apparatus will be fully charged after entering a Stage.\n'
'Condition:\n'
'Both the Leader and Ally are "The Box of Hope - Pandora".\n\n'

'◆ Recovery basic value of all Members will synchronize with that of the Member that has the highest Recovery.\n'
'Condition:\n'
'The Team has only Elves, with "The Box of Hope - Pandora" in the Team.\n\n'

'◆ Add 5x Recovery basic value of each Monster into its own Attack.\n'
'Condition:\n'
'Both the Leader and Ally are "The Box of Hope - Pandora", with only Elves in the Team.'},
    
    {'chi_name':'拉普拉斯',
'chif_name':'拉普拉斯',
'eng_name':'laplace',

'chi_act':'恶魔的幻象 CD4\n'
'I. 完全回复生命力\n'
'II. 队中所有“全知的恶魔 · 拉普拉斯”\n'
'⇒ 转化为“幻象”形态\n\n'
'恶魔的真象 CD6\n'
'I. 点击元素法阵上的符石 2 次\n'
'⓵ 移除首次点选的符石\n'
'⓶ 掉落第 2 次点选的符石\n'
'II. 将所有符石转化为\n'
'⇒ 魔族强化符石\n'
'1 回合内\n'
'III. 可任意移动符石而不会发动消除\n'
'IV. 魔族成员追打 1 次\n'
'V. 魔族成员\n'
'⇒ 无视“三属盾”及“五属盾”敌技\n'
'VI. 队中所有“全知的恶魔 · 拉普拉斯”\n'
'⇒ 转化为“真实”形态',
'eng_act':'Phantom of Demon CD4\n'
'I. Fully recover HP.\n'
'II. Turn all "Demon of Omniscience - Laplace" into 【Phantom】 form.\n\n'
'Truth of Demon CD6\n'
'I. By tapping a Runestone on the Magic Circle of Elements twice:\n'
'⓵ Remove the Runestones tapped for the first time.\n'
'⓶ Generate the Runestones tapped for the second time.\n'
'II. Turn all Runestones into Enchanted Demon Runestones.\n'
'For 1 Round,\n'
'III. Unlimited Runestone movement without dissolving.\n'
'IV. Each Demon launches an extra attack.\n'
'V. Demon Damage will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield.\n'
'VI. Turn all "Demon of Omniscience - Laplace" into 【True】 form.',

'chi_lead':'宇宙之掌\n\n'
'I. 魔族攻击力 7.5 倍及生命力 1.4 倍\n'
'II. 只能消除首批符石\n'
'III. ≥3 粒相同种类的符石相连\n'
'⇒ 即可发动消除\n'
'IV. 必然延长移动符石时间 3 秒\n'
'V. 首批消除 ≥15 粒符石\n'
'⇒ 魔族攻击力额外 2 倍\n'
'⇒ 魔族成员无视“指定形状盾”',
'eng_lead':'Palm of Cosmos\n\n'
'I. Demon Attack x 7.5, HP x 1.4.\n'
'II. Only the first batch of Runestones can be dissolved.\n'
'III. Runestones can be dissolved by grouping ≥3 of them.\n'
'IV. Extend Runestone-moving time regardlessly by 3 seconds.\n'
'V. By dissolving ≥15 Runestones in the first batch,\n'
'⇒ Demon Attack x 2 additionally.\n'
'⇒ Damage of Demons will be dealt regardless of Puzzle Shield.',

'chi_team':'队伍技能：\n\n'
'I.“全知的恶魔 · 拉普拉斯”\n'
'⇒ 获得“幻象”及“真实”2 种形态\n'
'II. 当“全知的恶魔 · 拉普拉斯”为“幻象”形态时\n'
'⇒ 自身攻击力减少 50%\n'
'III. 当“全知的恶魔 · 拉普拉斯”为“真实”形态时\n'
'⇒ 自身攻击力 1.5 倍\n'
'发动条件：\n'
'以“全知的恶魔 · 拉普拉斯”作成员\n\n'

'I. 进入关卡后，“全知的恶魔 · 拉普拉斯”\n'
'⇒ 转换为“幻象”形态\n'
'II. 当“全知的恶魔 · 拉普拉斯”为“幻象”形态时\n'
'⓵ 于移动符石后获得以下效果：\n'
'1 回合内，回避敌人首次攻击\n'
'⓶ 回合结束时，\n'
'“全知的恶魔 · 拉普拉斯”\n'
'⇒ 转换为“真实”形态\n'
'III. 当“全知的恶魔 · 拉普拉斯”为“真实”形态时\n'
'⓵ 每消除 1 组符石，连击 (Combo) 数目增加 2\n'
'⓶“全知的恶魔 · 拉普拉斯”攻击力 4 倍\n'
'⓷ 击毙敌人后，“全知的恶魔 · 拉普拉斯”\n'
'⇒ 转换为“幻象”形态\n'
'发动条件：\n'
'以“全知的恶魔 · 拉普拉斯”作队长及战友\n\n'

'I. 所有符石兼具\n'
'⇒ 其他符石效果\n'
'II. 首批消除 ≤3 种符石\n'
'⇒ 减少 80% 所受伤害\n'
'III. 首批消除场上所有符石时\n'
'⓵ 全队攻击力额外 2 倍\n'
'⓶ 首批掉落五属魔族强化符石各 6 粒\n'
'发动条件：\n'
'以“全知的恶魔 · 拉普拉斯”作队长及战友\n\n'

'“矛盾螺旋 ‧ 沃瓦道”\n'
'⇒ 技能 CD 减少 2\n'
'发动条件：\n'
'以“全知的恶魔 · 拉普拉斯”及“矛盾螺旋 ‧ 沃瓦道”作成员\n\n'

'I. 必然延长移动符石时间 2 秒\n'
'II. 最左方的“全知的恶魔 · 拉普拉斯”\n'
'⇒ 增加 1,000 点攻击力基值\n'
'发动条件：\n'
'以“魔权在握 ‧ 巴力”及“全知的恶魔 · 拉普拉斯”作成员\n\n'

'组合技能：魔劫\n'
'I. 移除场上所有符石\n'
'⇒ 掉落固定版面的魔族强化符石\n'
'3 回合内\n'
'II.“魔权在握 ‧ 巴力”及“全知的恶魔 · 拉普拉斯”\n'
'⓵ 追打 2 次\n'
'⓶ 无视五属盾\n'
'⓷ 不会被封锁主动技能\n'
'III.若队长为“魔权在握 ‧ 巴力”\n'
'⇒ 刷新护盾\n'
'发动条件：\n'
'以“全知的恶魔 ‧ 拉普拉斯”及“魔权在握 ‧ 巴力”作成员\n\n'
'(召唤兽等级达 50 或以上)',
'eng_team':'Team Skill:\n\n'
'◆ “Demon of Omniscience - Laplace” acquires “Phantom” and “True” forms.\n'
'◆ The following effects will be granted when “Demon of Omniscience - Laplace” turns into the forms below:\n'
'【Phantom】\n'
'▋The Character\'s Attack -50%\n'
'【True】\n'
'▋The Character\'s Attack x 1.5.\n'
'Condition:\n'
'There is "Demon of Omniscience - Laplace" in the Team.\n\n'

'◆ “Demon of Omniscience - Laplace” will turn into “Phantom” form after entering a Stage.\n'
'The following effects will be granted when “Demon of Omniscience - Laplace” turns into the forms below:\n'
'【Phantom】\n'
'⓵ The following effects will be granted upon the completion of moving Runestones:\n'
'Dodge the 1st attack of the 1st attacking enemy for 1 Round.\n'
'⓶ At the end of the Round,\n'
'“Demon of Omniscience - Laplace” will be changed into 【True】 form.\n'
'【True】\n'
'⓵ Combo count +2 for every group of Runestones dissolved.\n'
'⓶ Attack of “Demon of Omniscience - Laplace” x 4.\n'
'⓷ After an enemy is defeated,\n'
'“Demon of Omniscience - Laplace” will be changed into 【Phantom】 form.\n'
'◆ All Runestones also possess the effect of other Runestones.\n'
'◆ If ≤3 types of Runestones are dissolved in the first batch,\n'
'⇒ Damage received -80%.\n'
'◆ If all Runestones are dissolved in the first batch,\n'
'⓵ Team Attack x 2 additionally.\n'
'⓶ The first batch of Runestones to be dropped will be Enchanted Demon Runestones of 5 Attributes (6 for each).\n'
'Condition:\n'
'Both the Leader and Ally are "Demon of Omniscience - Laplace".\n\n'

'◆ “Helix of Contradictory - Vorvadoss”\n'
'⇒ Active Skill CD -2.\n'
'Condition:\n'
'There are "Demon of Omniscience - Laplace" and "Helix of Contradictory - Vorvadoss" in the Team.\n\n'

'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'◆ Attack basic value of the leftmost "Demon of Omniscience - Laplace" +1,000.\n'
'Condition:\n'
'There are "Absolute Authoritarian - Baal" and “Demon of Omniscience - Laplace” in the Team.\n\n'

'Combine Skill - Calamity of Demons\n'
'I. Remove all Runestones\n'
'⇒ to generate Enchanted Demon Runestones at fixed positions.\n'
'For 3 Rounds,\n'
'II. “Absolute Authoritarian - Baal” & “Demon of Omniscience - Laplace”:\n'
'⓵ Launch 2 extra attacks.\n'
'⓶ Damage will be dealt regardless of Quintet Elemental Shield.\n'
'⓷ Active Skills will not be locked.\n'
'III. If the Leader is “Absolute Authoritarian - Baal”,\n'
'⇒ refresh the protective shield.\n'
'Condition:\n'
'There are "Absolute Authoritarian - Baal" and “Demon of Omniscience - Laplace” in the Team.'},
    
    {'chi_name':'贾比尔',
'chif_name':'賈比爾',
'eng_name':'jabir',

'chi_act':'惊世之步、炼丹术 CD6\n\n'
'每次只能选取 1 个效果。\n'
'效果1：1 回合内\n'
'I. 移动的步数愈多，全队攻击力提升愈多\n'
'⇒ 移动 20 步攻击力可提升至最大 3 倍\n\n'

'若队伍中只有兽类成员：\n'
'1 回合内\n'
'II. 兽类成员的攻击伤害可克制敌人\n'
'III. 无视“燃烧”(不包括“炼狱之火”)\n'
'IV. 无视“黏腐”敌技\n'
'V. 触碰电击符石时仍可移动符石\n\n'

'效果2：I. 回复相当于兽类成员 2 倍的生命力\n'
'II. 1 回合内，延长移动符石时间至 12 秒',
'eng_act':'Phenomenal Power of Steps & Mystery of Alchemy CD6\n\n'
'Only one effect can be selected for 1 Round.\n'
'Effect One:\n'
'I. The more the steps moved while moving Runestones, the higher the Team Attack, to the max x 3 for 20 steps moved.\n\n'

'When the Team consists of only Beasts:\n'
'II. Damage dealt by Beasts can overpower the enemies.\n'
'II. Boss Skills "Burning" (excluding "Hellfire") and "Sticky Land" will be nullified.\n'
'III. Runestone movement will not be stopped when an Electrified Runestone is touched.\n\n'

'Effect Two:\n'
'I. Recover HP as much as 2x HP of Beasts in the Team.\n'
'II. For 1 Round, extend Runestone-moving time to 12 seconds.',

'chi_lead':'元素之核\n\n'
'队中只有兽类成员时：\n'
'I. 全队攻击力 8 倍、生命力及回复力 1.5 倍\n'
'II. 所有符石兼具\n'
'⇒ 50% 其他符石效果\n'
'III. 消除兽族符石\n'
'⇒ 全队攻击力额外 2.5 倍',
'eng_lead':'Core of Elements\n\n'
'When the Team has only Beasts:\n'
'I. Team Attack x 8, HP & Recovery x 1.5.\n'
'II. All Runestones also possess 50% effect of other Runestones.\n'
'III. By dissolving Beast Runestones,\n'
'⇒ Team Attack x 2.5 additionally.',

'chi_team':'队伍技能：\n\n'
'I. 必然延长移动符石时间 3 秒\n'
'II. 移动符石时间每过 0.5 秒\n'
'⇒ 即时扣除自身总生命力 6.25%\n'
'(最多扣至 1 血)\n'
'III. 根据此队伍技能所扣除的总生命力\n'
'⇒ 提升兽类攻击力\n'
'⇒ 最多可提升至 4 倍\n'
'发动条件：\n'
'以“贤者之石 ‧ 元兽贾比尔”作队长及战友\n\n'

'将移动符石时触碰的符石\n'
'⇒ 添加为兽族符石\n'
'发动条件：\n'
'以“贤者之石 ‧ 元兽贾比尔”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Extend Runestone-moving time regardlessly by 3 seconds.\n'
'◆ For every 0.5 seconds of Runestone-moving time used, deduct HP by 6.25% of total HP (bottom out at 1).\n'
'◆ Beast Attack increases additionally in proportion to total HP deducted, to the max x 4 additionally.\n'
'◆ Modify all Runestones touched while moving to become Beast Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Philosopher\'s Legend - Jabir".'},
    
    {'chi_name':'罗刹女',
'chif_name':'羅剎女',
'eng_name':'rakshasa',

'chi_act':'逆焰之一扇天涯 CD6\n\n'
'I. 木属性伤害可克制火及木属性目标\n'
'II. 每消除 2 粒木符石\n'
'⇒ 个人追打木属性攻击 1 次，最多 10 次\n'
'(效果会在关闭此技能或死亡后消失)\n'

'此技能可随时关闭，关闭时：\n'
'⇒ 当前技能 CD 减少 2\n'
'⇒ 将所有符石转化为木强化符石',
'eng_act':'Flame-quenching Fan - EX CD6\n\n'
'I. Earth Damages can overpower Fire and Earth enemies.\n'
'II. For every 2 Earth Runestones dissolved, the Monster launches an extra Earth attack, to the max 10 extra attacks (the Skill stays in play until deactivation or defeated).\n'
'This Skill can be deactivated anytime.\n'

'Upon deactivation of the Skill:\n'
'⇒ Current Skill CD -2.\n'
'⇒Turn all Runestones into Enchanted Earth Runestones.',

'chi_lead':'神魔之森 ‧ 狂风\n\n'
'队伍中只有木属性魔族或木属性神族成员时：\n'
'I. 全队攻击力 4 倍\n'
'II. 每消除 4 组符石时\n'
'⇒ 必定掉落 4 粒木强化符石',
'eng_lead':'Forest of Gods & Demons - EX\n\n'
'When the Team includes only Earth Demons and Earth Gods, Team Attack x 4; for every 4 groups of Runestones dissolved, 4 Enchanted Earth Runestones will be generated.',

'chi_team':'队伍技能：\n\n'
'“迅杀芭扇 ‧ 罗刹女”、异空转生“中国神”及“究极中国神”系列成员\n'
'⇒“生命力、攻击力及回复力”基值 1.5 倍\n'
'发动条件：\n'
'以“迅杀芭扇 ‧ 罗刹女”及 ≥ 1 个异空转生“中国神”或“究极中国神”系列角色作成员',
'eng_team':'Team Skill:\n\n'
'◆ HP, Attack & Recovery basic value of "Devastating Tornado - Rakshasa" and Monsters of "Chinese Gods Reborn" and "Chinese Gods - Supreme Reckoning" x 1.5 additionally.\n'
'Condition:\n'
'There are "Devastating Tornado - Rakshasa", and Chinese Gods Reborn - Refinement series, Chinese Gods Reborn - Divergence series, or Chinese Gods - Supreme Reckoning series in the Team.'},

    {'chi_name':'唐三藏',
'chif_name':'唐三藏',
'eng_name':'tangsanzang',

'chi_act':'弘扬大义 ‧ 除障 CD5\n\n'
'I. 移除所有电击、风化、冻结、石化符石\n'
'⇒ 掉落随机种族符石\n'
'1 回合内\n'
'II. 光属性攻击力及回复力 2.2 倍\n'
'III. 队中所有成员的攻击力基值相同时\n'
'⇒ 所有符石兼具其他符石效果',
'eng_act':'Tripitaka of Light Divinity CD5\n\n'
'I. Remove all Electrified, Weathered, Frozen and Petrified Runestones to generate random Race Runestones.\n'
'For 1 Round:\n'
'II. Light Attack and Recovery x 2.2.\n'
'III. When all Members have the same Attack basic value,\n'
'⇒ all Runestones also possess the effect of other Runestones.',

'chi_lead':'种族凝汇 ‧ 光之暴\n\n'
'队伍中有 ≥3 种族成员时：\n'
'I. 光属性攻击力 6 倍\n'
'II. 每消除 1 种“种族符石”\n'
'⇒ 光属性攻击力额外 1.5 倍',
'eng_lead':'Convergence of Races - Beam\n\n'
'If there are 3 or more Races in the Team:\n'
'I. Light Attack x 6.\n'
'II. For each Race of Race Runestones dissolved, Light Attack x 1.5 additionally.',

'chi_team':'队伍技能：\n\n'
'队长的队长技能“种族凝汇 ‧ 光之暴”变为“种族凝汇 ‧ 极光之暴”，当中所有成员的生命力基值、攻击力基值及回复力基值分别跟随生命力基值、攻击力基值及回复力基值最高的成员，光符石的掉落率提升，必然延长移动符石时间 2 秒\n'
'发动条件：\n'
'以大乘儆恶 ‧ 唐三藏作队长及战友\n\n'

'流沙河魔将 ‧ 沙僧转换为光属性\n'
'发动条件：\n'
'以大乘儆恶 ‧ 唐三藏作队长及战友，并以流沙河魔将 ‧ 沙僧作队员\n\n'

'天蓬使者・猪八戒转换为光属性\n'
'发动条件：\n'
'以大乘儆恶 ‧ 唐三藏作队长及战友，并以天蓬使者・猪八戒作队员\n\n'

'“化戾金仙 ‧ 孙悟空”发动攻击时\n'
'⇒ 额外追打五属攻击各 1 次\n'
'发动条件：\n'
'以“大乘儆恶 ‧ 唐三藏”作队长及战友并以“化戾金仙 ‧ 孙悟空”作队员\n\n'

'I. 每回合随机将 5 粒非种族符石\n'
'⇒ 添加为队中成员种族符石\n'
'II. 消除种族符石时\n'
'⇒ 全队攻击力额外 5 倍\n'
'III. 队长增加 5,000 点生命力基值\n'
'发动条件：\n'
'以“大乘儆恶 ‧ 唐三藏”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ Drop rate of Light Runestones increases.\n'
'◆ Extend Runestone-moving time regardlessly by 2 seconds.\n'
'◆ Change the Leader Skill of the Leader from "Convergence of Races - Beam" to "Convergence of Races - Beam EX".\n'
'If there are 3 or more Races in the Team:\n'
'I. Light Attack x 6.\n'
'II. For each Race of Race Runestones dissolved, Light Attack x 1.5 additionally.\n'
'III. HP, Attack & Recovery basic value of all Members will synchronize with that of the Member that has the highest HP, Attack & Recovery.\n\n'

'◆ Modify 5 random non-Race Runestones to become Runestones of Members\' Races each Round.\n'
'◆ By dissolving Race Runestones,\n'
'⇒ Team Attack x 5 additionally.\n'
'◆ Leader\'s HP basic value +5,000.\n'
'Condition:\n'
'Both the Leader and Ally are "Mahayana Punisher - Tang Sanzang".\n\n'

'◆ Change the Attribute of Sha Seng the Sand Fiend into Light.\n'
'Condition:\n'
'Both the Leader and Ally are "Mahayana Punisher - Tang Sanzang", with "Sha Seng the Sand Fiend" in the Team.\n\n'

'◆ Change the Attribute of Zhu Bajie the Heavenly Marshal into Light.\n'
'Condition:\n'
'Both the Leader and Ally are "Mahayana Punisher - Tang Sanzang", with "Zhu Bajie the Heavenly Marshal" in the Team.\n\n'

'◆ 5 extra attacks (one Attribute each) will be launched by "Tranquil Transcendence - Sun Wukong" when it attacks.\n'
'Condition:\n'
'Both the Leader and Ally are "Mahayana Punisher - Tang Sanzang", with "Tranquil Transcendence - Sun Wukong" in the Team.'},
    
    {'chi_name':'庞贝',
'chif_name':'龐貝',
'eng_name':'pompeii',

'chi_act':'傲倪万物．三原结界 CD8\n\n'
'I. 解除机械族成员被封锁的技能\n'
'(此技能无视封锁技能)\n'
'II. 移除所有符石\n'
'⇒ 掉落固定数量及位置的“水、火、木”强化符石\n'
'1 回合内\n'
'III. 无视“指定形状盾”及“攻前盾”\n'
'IV.“炙焰城主 ‧ 庞贝”的攻击\n'
'⇒ 无视“五属盾”',
'eng_act':'Breakthrough of Tricolor Siege CD8\n\n'
'I. Release the locked Skills of Machinas.\n'
'(This Skill will not be locked)\n'
'II. Remove all Runestones to generate Enchanted Water, Enchanted Fire and Enchanted Earth Runestones of fixed numbers and fixed positions.\n'
'For 1 Round,\n'
'III. Damage will be dealt regardless of Puzzle Shield and Initial Shield.\n'
'IV. Damage of “Ruler of Scorching Flames - Pompeii” will be dealt regardless of Quintet Elemental Shield.',

'chi_lead':'灭族之焰．追击\n\n'
'I. 火属性及机械族攻击力 6.5 倍\n'
'II.“炙焰城主 ‧ 庞贝”的攻击\n'
'⇒ 无视敌人防御力\n'
'III. 消除水、火或木符石时\n'
'⇒ 机械族成员追打相应属性攻击 1 次\n'
'IV. 每首批消除 1 种符石\n'
'⇒ 于回合结束时将 5 粒该种符石添加为机械族符石 (非种族符石优先转换)',
'eng_lead':'Fire of Extermination - EX\n\n'
'I. Fire Attack & Machina Attack x 6.5.\n'
'II. Damage of "Ruler of Scorching Flames - Pompeii" will be dealt regardless of Defense.\n'
'III. By dissolving Water, Fire or Earth Runestones,\n'
'⇒ each Machina launches an extra attack of the corresponding Attribute(s) dissolved.\n'
'IV. For each type of Runestones dissolved in the first batch,\n'
'⇒ modify 5 random Runestones of that type to become Machina Runestones at the end of the Round\n'
'(non-Race Runestones rank first in priority).',

'chi_team':'队伍技能：\n\n'
'I. 队伍中最小冷却回合为 8且技能等级已满的机械族成员\n'
'⇒ 技能 CD -2\n'
'II. 水、木、心符石\n'
'⇒ 兼具火符石效果\n'
'III. 水、火、木符石\n'
'⇒ 兼具心符石效果\n\n'

'IV. 每回合随机锁定 8 个位置，每消除 1 个锁定位置 (不计重复) 内的符石时\n'
'⓵ 火属性及机械族攻击力提升\n'
'⇒ 最多可提升 3 倍\n'
'⓶“炙焰城主 ‧ 庞贝”以 50% 攻击力追打火属性攻击 1 次\n'
'V. 必然延长移动符石时间 3 秒\n'
'VI. 将移动符石时触碰的水、火、木符石\n'
'⇒ 转化为机械族符石\n'
'发动条件：\n'
'以“炙焰城主 ‧ 庞贝”作队长及战友\n\n'

'I. 机械族成员\n'
'⇒“生命力、攻击力及回复力”基值 2 倍\n'
'II. 进入关卡后，机械族成员的行动值提升 50%\n'
'发动条件：\n'
'以“炙焰城主 ‧ 庞贝”作队长及战友，且队中有 ≥3 个机械族成员\n\n'

'【机械动力】\n'
'I. 每首批消除 1 粒自身属性符石\n'
'⇒ 自身行动值提升 2%\n'
'II. 每首批消除 1 粒心符石\n'
'⇒ 自身行动值提升 1%\n'
'III. 行动值愈高\n'
'⇒ 自身攻击力提升愈多\n'
'⇒ 最大提升至 2 倍。\n'
'IV. 当所有机械族成员的行动值达至 50% 或以上时\n'
'⇒ 机械族成员属性的符石效果提升\n'
'⇒ 每个机械族成员可提升 10% 效果\n'
'⇒ 最高 60%\n'
'V. 当所有机械族成员的行动值达至 100% 时\n'
'⇒ 机械族成员每回合\n'
'以 25% 自身攻击力随机追打自身属性或自身克制属性的攻击 1 至 2 次\n'
'发动条件：\n'
'队伍中有 ≥2 个【机械族】成员',
'eng_team':'Team Skill:\n\n'
'◆ For Machinas with Active Skills that have reached the maximum Lv. of which CD is 8, Skill CD -2.\n'
'◆ Water, Earth and Heart Runestones also possess the effect of Fire Runestones.\n'
'◆ Water, Fire and Earth Runestones also possess the effect of Heart Runestones.\n\n'

'◆ Lock 8 random positions every Round.\n'
'If the Runestone at a locked position is dissolved (each position will be counted once only):\n'
'⓵ Fire Attack & Machina Attack increases, to the max x 3.\n'
'⓶ "Ruler of Scorching Flames - Pompeii" launches an extra Fire attack as much as 50% of its attack.\n'
'◆ Extend Runestone-moving time regardlessly by 3 seconds.\n'
'◆ Turn Water, Fire and Earth Runestones touched while moving into Machina Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Ruler of Scorching Flames - Pompeii".\n\n'

'◆ Machina HP, Attack & Recovery basic value x 2.\n'
'◆ Fuel of Machinas +50% after entering a Stage.\n'
'Condition:\n'
'Both the Leader and Ally are "Ruler of Scorching Flames - Pompeii", with 3 or more Machina in the Team.\n\n'

'◆ 【Machina Dynamics】\n'
'⓵ For each Runestone of the Character\'s Attribute dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +2%.\n'
'⓶ For each Heart Runestone dissolved in the first batch,\n'
'⇒ the Character\'s Fuel +1%.\n'
'⓷ The higher the Character\'s Fuel,\n'
'⇒ the higher the Character\'s Attack,\n'
'⇒ to the max x 2 additionally.\n'
'⓸ When all Machinas in the Team have ≥ 50% Fuel,\n'
'⇒ effects of Runestones of their Attributes increase,\n'
'⇒ 10% for each Machina present in the Team,\n'
'⇒ to the max 60%.\n'
'⓹ When all Machinas in the Team have 100% Fuel,\n'
'⇒ all Machinas randomly launch 1 to 2 extra attack(s) of its own Attribute or its Counter Attribute as much as 25% of its Attack every Round.\n'
'Condition:\n'
'There are 2 or more 【Machina Dynamics】 Members in the Team.'},
    
    {'chi_name':'美索不达米亚',
'chif_name':'美索不達米亞',
'eng_name':'mesopotamia',

'chi_act':'强悍之志 ‧ 勇往 CD5\n\n'
'I. 达成 ≥4 连击 (Combo)\n'
'⇒ 个人追打光及暗属性攻击 1 次\n'
'II. 达成 ≥6 连击\n'
'⓵ 自身攻击力 3 倍\n'
'⓶ 自身无视“三属盾”及“五属盾”\n'
'III. 达成 ≥8 连击 (Combo)\n'
'⓵ 个人以 25% 攻击力\n'
'⇒ 追打水及火属性攻击 1 次\n'
'⓶ 自身无视“固定连击盾”\n'
'(效果会在关闭此技能或死亡后消失)\n\n'

'此技能可随时关闭，关闭时：\n'
'⓵ 点选元素法阵上的 1 粒符石\n'
'⇒ 引爆所有符石\n'
'⇒ 掉落该种符石以外的人族符石',
'eng_act':'Indomitable Will - Ex CD5\n\n'
'I. When ≥4 Combos are made,\n'
'⇒ the Character launches an extra Light attack and an extra Dark attack.\n'
'II. When ≥6 Combos are made:\n'
'⓵ The Character\'s Attack x 3.\n'
'⓶ The Character\'s Damage will be dealt regardless of Trio Elemental Shield and Quintet Elemental Shield.\n'
'III. When ≥8 Combos are made:\n'
'⓵ The Character launches an extra Water attack and an extra Fire attack as much as 25% of its Attack.\n'
'⓶ The Character\'s Damage will be dealt regardless of Fixed Combo Shield.\n'
'(The effect stays in play until deactivation or defeat.)\n\n'

'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'⓵ By tapping a Runestone on the Magic Circle of Elements,\n'
'⇒ Explode all Runestones to generate Human Runestones not of that type.',

'chi_lead':'千秋的传承 ‧ 使命\n\n'
'I. 木属性攻击力 6.5 倍、生命力及回复力 1.6 倍\n'
'II. 木属性人类攻击力则 8 倍\n'
'III. 必然延长移动符石时间 3 秒\n'
'IV. 消除种族符石时\n'
'⇒ 木属性攻击力额外 4 倍\n'
'V. 每消除 1 组光或暗符石\n'
'⇒ 回合结束时将 3 粒符石转化为人族强化符石\n'
'(木及心符石优先转换)\n'
'⇒ 最多可转化 30 粒',
'eng_lead':'Selfless Heiress - EX\n\n'
'I. Earth Attack x 6.5; HP & Recovery x 1.6.\n'
'II. Earth Human Attack x 8.\n'
'III. Extend Runestone-moving time regardlessly by 3 seconds.\n'
'IV. By dissolving Race Runestones,\n'
'⇒ Earth Attack x 4 additionally.\n'
'V. For every group of Light or Dark Runestones dissolved,\n'
'⇒ turn 3 Runestones into Enchanted Human Runestones at the end of the Round (Earth and Heart Runestones rank first in priority),\n'
'⇒ to the max 30 Runestones to be turned.',

'chi_team':'队伍技能：\n\n'
'I. 2 粒光或暗符石相连\n'
'⇒ 即可发动消除\n'
'(所有符石掉落不受其他技能影响，包括改变掉落符石属性的技能)\n'
'II. 光、暗符石兼具\n'
'⇒ 木及心符石效果\n'
'III. 队长及战友进场及首回合结束时 CD-5\n'
'发动条件：\n'
'以“女帝的铭誓 ‧ 美索不达米亚”作队长及战友\n\n'

'I. “千变真个 ‧ 切西亚”\n'
'⇒ 转换为队长的属性\n'
'II.“千变真个 ‧ 切西亚”的主动技能变为“三原灵冕化阵 ‧ 神森”\n'
'1 回合内\n'
'I. 队长及战友进入亢奋状态\n'
'II. 将所有符石转化为\n'
'⇒ “光、暗、木、心”强化符石：\n'
'⓵ 木符石出现率上升\n'
'⓶ 木符石以木神族强化符石代替\n\n'

'III.“千变真个 ‧ 切西亚”\n'
'⇒ 技能 CD -1\n'
'IV.“千变真个 ‧ 切西亚”\n'
'⇒ 攻击力 1.6 倍\n'
'V. 心符石首批 2 粒相连\n'
'⇒ 即可发动消除\n'
'发动条件：\n'
'以“女帝的铭誓 ‧ 美索不达米亚”作队长及战友，并以“千变真个 ‧ 切西亚”作队员',
'eng_team':'Team Skill:\n\n'
'◆ Light and Dark Runestones can be dissolved by grouping 2 or more of them (Drop rate of all Runestones will not be affected by Amelioration or Skills, including those altering the Attribute of dropping Runestones).\n'
'◆ Light and Dark Runestones also possess the effect of Earth and Heart Runestones.\n'
'◆ Skill CDs of the Leader and Ally -5 after entering a stage and at the end of the first Round.\n'
'Condition:\n'
'Both the Leader and Ally are "Fealty of the Amazon - Mesopotamia".\n\n'

'◆ The Attribute of “Disguised Self - Chessia” will synchronize with that of the Leader.\n'
'◆ Change the Active Skill of “Disguised Self - Chessia” into “Tricolor Circle - Deific Woods”.\n'
'For 1 Round:\n'
'I. The Leader and Ally enter a hyper state.\n'
'II. Turn all Runestones into Enchanted Light, Enchanted Dark, Enchanted Earth and Enchanted Heart Runestones:\n'
'⓵ Increase the Occurrence rate of Earth Runestones.\n'
'⓶ Earth Runestones will become Enchanted Earth God Runestones.\n\n'

'◆ Skill CD of “Disguised Self - Chessia” -1.\n'
'◆ Attack of “Disguised Self - Chessia” x 1.6.\n'
'◆ Heart Runestones can be dissolved by aligning 2 or more of them in the first batch.\n'
'Condition:\n'
'Both the Leader and Ally are "Fealty of the Amazon - Mesopotamia", with “Disguised Self - Chessia” in the Team.'},
    
{'chi_name':'阿努比斯',
'chif_name':'阿努比斯',
'eng_name':'anubis',

'chi_act':'断魂冥渊 CD5\n\n'
'I. 全队攻击力 1.5 倍\n'
'II. 自身属性符石掉落率提升\n'
'III. 自身属性符石\n'
'⇒ 兼具 50% 心符石效果\n'
'IV. 发动此技能及回合结束时\n'
'⇒ 将自身属性符石转化为神族强化符石\n'
'(效果会在关闭此技能或死亡后消失)\n\n'

'此技能可随时关闭，关闭时：\n'
'⓵ 引爆自身及身旁神族成员直行符石\n'
'⇒ 掉落强化符石\n'
'1 回合内\n'
'⓶ 神族攻击力及回复力 2 倍\n'
'⓷“冥魂判守 ‧ 阿努比斯”的技能 CD - 2',
'eng_act':'Flow of Soul-reaping Shadow - EX CD5\n\n'
'I. Team Attack x 1.5.\n'
'II. Increase the drop rate of Runestones of the Character\'s Attribute.\n'
'III. Runestones of the Character\'s Attribute also possess 50% effect of Heart Runestones.\n'
'IV. Upon Skill activation and at the end of the Round,\n'
'⇒ turn Runestones of the Character\'s Attribute into Enchanted God Runestones.\n'
'(The Skill stays in play until deactivation or defeat.)\n\n'

'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'⓵ Explode the columns below the Character and neighboring God(s) to generate Enchanted Runestones.\n'
'For 1 Round:\n'
'⓶ God Attack & Recovery x 2.\n'
'⓷ Skill CD of “Shackles of Souls - Anubis” -2.',

'chi_lead':'无上神权 ‧ 制裁\n\n'
'I. 神族攻击力 7 倍\n'
'II. 消除属性强化符石\n'
'⇒ 该属性攻击力额外 2 倍\n'
'III. 自身发动技能时\n'
'⇒ 神族攻击力额外 2 倍',
'eng_lead':'Omnipotence of Gods - EX\n\n'
'I. God Attack x7.\n'
'II. By dissolving Enchanted Attributive Runestones,\n'
'⇒ Attack of that Attribute x 2 additionally.\n'
'III. Upon activation of the Character\'s Skill,\n'
'⇒ God Attack x 2 additionally.',

'chi_team':'队伍技能：\n\n'
'最左方的“冥魂判守 ‧ 阿努比斯”及最左方的各属“埃及皇权”系列成员\n'
'⇒“生命力、攻击力、回复力”基值 1.5 倍\n'
'发动条件：\n'
'以“冥魂判守 ‧ 阿努比斯”及“埃及皇权”系列角色作成员\n\n'

'“冥魂判守 ‧ 阿努比斯”转换为“埃及皇权”系列角色的属性\n'
'发动条件：\n'
'队伍中有“冥魂判守 ‧ 阿努比斯”及“埃及皇权”系列角色，并只有相同属性的神族成员\n'
'(“冥魂判守 ‧ 阿努比斯”除外)',
'eng_team':'Team Skill:\n\n'
'◆ HP, Attack & Recovery basic value of the first "Shackles of Souls - Anubis" and the first Monster of "Imperiality of Egypt" of each Attribute from the left x 1.5 additionally.\n'
'Condition:\n'
'There are "Shackles of Souls - Anubis" and Character(s) of Imperiality of Egypt series in the Team.\n\n'

'◆ Alter the Attribute of "Shackles of Souls - Anubis" into Water.\n'
'Condition:\n'
'The Team has only "Shackles of Souls - Anubis", "Solemn Commitment - Sobek" and Water Gods.\n\n'

'◆ Alter the Attribute of "Shackles of Souls - Anubis" into Fire.\n'
'Condition:\n'
'The Team has only "Shackles of Souls - Anubis", "Twisted Obsession - Khepri" and Fire Gods.\n\n'

'◆ Alter the Attribute of "Shackles of Souls - Anubis" into Earth.\n'
'Condition:\n'
'The Team has only "Shackles of Souls - Anubis", "Honourable Dedication - Serket" and Earth Gods.\n\n'

'◆ Alter the Attribute of "Shackles of Souls - Anubis" into Light.\n'
'Condition:\n'
'The Team has only "Shackles of Souls - Anubis", "Soaring Sacredness - Horus" and Light Gods.'},
    
    {'chi_name':'玛雅',
'chif_name':'瑪雅',
'eng_name':'maya',

'chi_act':'突破之结界 ‧ 强 CD6\n\n'
'I. 将所有符石转化为强化符石\n'
'1 回合内\n'
'II. 光属性、神族、魔族攻击力 2 倍\n'
'III. 光属性“神族及魔族”\n'
'⓵ 则攻击力 2.5 倍\n'
'⓶ 无视“固定连击盾”\n'
'IV. 光、暗、心符石互相兼具效果',
'eng_act':'Magic Field of Enchantment - EX CD6\n\n'
'I. Turn all Runestones into Enchanted Runestones.\n'
'For 1 Round:\n'
'II. Attack of Light Members, Gods and Demons x 2.\n'
'III. For Light Gods and Light Demons,\n'
'⓵ Attack x 2.5.\n'
'⓶ Damage will be dealt regardless of Fixed Combo Shield.\n'
'IV. Light, Dark and Heart Runestones also possess the effect of each other.',

'chi_lead':'玄华独尊 ‧ 崇\n\n'
'I. 光属性生命力、攻击力、回复力 1.5 倍\n'
'II. 光及暗符石兼具\n'
'⇒ 50% 心符石效果\n'
'III. 暗符石兼具 50% 光符石效果\n'
'IV. 心符石兼具光符石效果\n'
'V. 消除光、暗、心符石其中 2 种符石\n'
'⇒ 光属性攻击力额外 7 倍',
'eng_lead':'Total Supremacy of Illumination\n\n'
'I. Light HP, Attack & Recovery x 1.5.\n'
'II. Light and Dark Runestones also possess 50% effect of Heart Runestones.\n'
'III. Dark Runestones also possess 50% effect of Light Runestones.\n'
'IV. Heart Runestones also possess the effect of Light Runestones.\n'
'V. If 2 out of 3 types of Runestones (Light, Dark & Heart) are dissolved in the same Round, Light Attack x 7 additionally.',

'chi_team':'队伍技能：\n\n'
'每合计消除 3 粒光、暗或心符石时\n'
'⇒ 光属性攻击力提升\n'
'⇒ 消除 30 粒可提升至最大 5 倍\n'
'发动条件：\n'
'以“开世的文明 ‧ 玛雅”作队长及战友\n\n'

'队长的队长技能“玄华独尊 ‧ 崇”\n'
'⇒ 变为“玄华独尊 ‧ 崇极”\n'
'I. 光属性生命力、攻击力、回复力 1.6 倍\n'
'II. 延长移动符石时间至 10 秒\n'
'III. 光及暗符石兼具\n'
'⇒ 50% 心符石效果\n'
'IV. 暗及心符石兼具光符石效果\n'
'V. 水、火、木符石兼具\n'
'⇒ 50% 光符石效果\n\n'

'VI. 消除光、暗、心符石其中 2 种符石时\n'
'⇒ 光属性攻击力额外 7 倍\n'
'VII. ≥3 粒相同种类的符石相连，即可发动消除\n'
'VIII. 所有符石掉落率不受其他技能影响\n'
'(包括改变掉落符石属性的技能)\n'
'IX. 回合结束时，可点选“X 型”\n'
'⇒ 引爆 10 个固定位置的符石\n'
'X. 没有点选时，将“X 型”位置的符石\n'
'⇒ 转化为光强化符石\n'
'发动条件：\n'
'以“开世的文明 ‧ 玛雅”作队长',
'eng_team':'Team Skill:\n\n'
'◆ For every 3 Light, Dark or Heart Runestones dissolved, Light Attack increases additionally, to the max x 5 for 30 Runestones dissolved.\n'
'◆ Change the Leader Skill of the Leader from "Total Supremacy of Illumination" to "Total Supremacy of Illumination - EX".\n'
'I. Light HP, Attack & Recovery x 1.6.\n'
'II. Extend Runestone-moving time to 10 seconds.\n'
'III. Light and Dark Runestones also possess 50% effect of Heart Runestones.\n'
'IV. Dark and Heart Runestones also possess the effect of Light Runestones.\n'
'V. Water, Fire and Earth Runestones also possess 50% effect of Light Runestones.\n\n'

'VI. If 2 out of 3 types of Runestones (Light, Dark & Heart) are dissolved in the same Round, Light Attack x 7 additionally.\n'
'VII. Runestones can be dissolved by grouping ≥3 of them.\n'
'VIII. Drop rate of all Runestones will not be affected by Amelioration or Skills (including those altering the Attribute of dropping Runestones).\n'
'IX. At the end of the Round, Summoner can choose whether to explode 10 Runestones at fixed positions (in the shape of "X") or not.\n'
'X. If Runestones are not exploded, turn Runestones at fixed positions into Enchanted Light Runestones.\n'
'Condition:\n'
'Both the Leader and Ally are "Dawn of Civilization - Maya".'},
    
    {'chi_name':'亚特兰堤斯',
'chif_name':'亞特蘭堤斯',
'eng_name':'atlantis',

'chi_act':'自由激涛 ‧ 涌 CD8\n'
'I. 15 秒内，可任意移动符石而不会发动消除\n'
'1 回合内\n'
'II. 全队攻击力 2.2 倍\n'
'III. 若队中只有水属性成员\n'
'⇒ 水符石 1 粒即可发动消除\n'
'⇒ 效果持续至消除 30 粒水符石\n\n'
'睿智急流 CD3\n'
'将 5 至 8 粒符石\n'
'⇒ 转化为水强化符石 (心符石优先转换)',
'eng_act':'Tide of Freedom CD8\n'
'I. Unlimited Runestone movement without dissolving in 15 seconds.\n'
'For 1 Round,\n'
'II. Team Attack x 2.2.\n'
'III. If the Team has only Water Monsters,\n'
'⇒ Water Runestones can be dissolved singly or in groups of 2 or more.\n'
'⇒ The effect stays in play until 30 Water Runestones are dissolved.\n\n'
'Stream of Wisdom CD3\n'
'Turn 5 to 8 Runestones into Enchanted Water Runestones (Heart Runestones rank first in priority).',

'chi_lead':'海渊凝念 ‧ 强\n\n'
'队中只有水属性成员时：\n'
'I. 全队攻击力 6.5 倍及生命力 1.5 倍\n'
'II. 每消除 1 粒水符石\n'
'⇒ 回复 3% 总生命力 (受连击 (Combo) 加乘影响)\n'
'III. 若首批消除的连击 (Combo) 数为单数时\n'
'⓵ 减少 40% 所受伤害\n'
'⓶ 所有成员的攻击无视五属盾\n'
'IV. 若首批消除的连击 (Combo) 数为双数时\n'
'⇒ 全队攻击力额外 2.5 倍\n'
'V. 若首批消除的连击 (Combo) 数 ≥6\n'
'⇒ 可以同时获得 III, IV 效果',
'eng_lead':'Deep Notion of the Ocean - EX\n\n'
'When the Team has only Water Monsters:\n'
'I. Team Attack x 6.5 & HP x 1.5.\n'
'II. Recover 3% of total HP for each Water Runestone dissolved (affected by Combo bonus).\n'
'III. When Combos of odd numbers are made in the first batch,\n'
'⓵ Damage received -40%.\n'
'⓶ Damage of the Team will be dealt regardless of "Quintet Elemental Shield".\n'
'IV. When Combos of even numbers are made in the first batch,\n'
'⇒ Team Attack x 2.5 additionally.\n'
'V. When ≥6 Combos are dissolved in the first batch,\n'
'⇒ Effects III & IV will be triggered.',

'chi_team':'队伍技能：\n\n'
'I. 队中成员每 1 次发动主动技能\n'
'⇒“明悟睿涛 ‧ 亚特兰堤斯”的技能 CD -1 (技能发动者除外)\n'
'II.“明悟睿涛 ‧ 亚特兰堤斯”\n'
'发动技能的回合\n'
'⇒“明悟睿涛 ‧ 亚特兰堤斯”攻击力 2 倍\n'
'发动条件：\n'
'以“明悟睿涛 ‧ 亚特兰堤斯”作成员\n\n'

'I. 水符石的掉落率提升至 40%\n'
'II. 掉落的水符石\n'
'⇒ 以水强化符石代替\n'
'III. 必然延长移动符石时间 3 秒\n'
'IV. 无视“黏腐”敌技\n'
'V. 触碰电击符石时仍可移动符石\n'
'VI. 首批消除所有水符石时\n'
'⇒ 全队攻击力 4 倍\n'
'发动条件：\n'
'以“明悟睿涛 ‧ 亚特兰堤斯”作队长及战友',
'eng_team':'Team Skill:\n\n'
'◆ I. Every time a Monster activates its Skill,\n'
'⇒ Skill CD of “Tide of Wisdom - Atlantis” -1 (except the one activating its Skill).\n'
'◆ II. Upon the Round of activation of the Skill of "Tide of Wisdom - Atlantis”,\n'
'⇒ Attack of "Tide of Wisdom - Atlantis” x 2.\n'
'Condition:\n'
'There is "Tide of Wisdom - Atlantis" in the Team.\n\n'

'◆ Drop rate of Water Runestones increases to 40%.\n'
'◆ All Water Runestones to be dropped will be Enchanted Water Runestones.\n'
'◆ Extend Runestone-moving time regardlessly by 3 seconds.\n'
'◆ Boss Skill "Sticky Land" will be nullified.\n'
'◆ Runestone movement will not be stopped when an Electrified Runestone is touched.\n'
'◆ By dissolving all Water Runestones in the first batch,\n'
'⇒ Team Attack x 4.\n'
'Condition:\n'
'Both the Leader and Ally are "Tide of Wisdom - Atlantis".'},
    
    {'chi_name':'希1',
'chif_name':'希1',
'eng_name':'xi1',

'chi_act':'誓約的泉源 ‧ 神之加冕 CD 6\n\n'
'I. 移除暗及心符石\n'
'⇒ 掉落水神族強化符石\n'
'2 回合內\n'
'II. 全隊攻擊力 2.25 倍\n'
'III. 延長移動符石時間至 20 秒\n'
'IV. 將移動符石時觸碰的凍結符石狀態解除',
'chi_lead':'水元素暴濤 ‧ 強 \n\n'
'I. 水屬性攻擊力 7 倍，消除水符石的組數愈多\n'
'⇒ 水屬性攻擊力愈高\n'
'⇒ 消除 3 組可達至最大 10 倍\n'
'II. 水屬性生命力及回復力 1.6 倍\n'
'III. 每回合結束時，\n'
'隨機將 2 粒符石轉化為\n'
'⇒ 水神族強化符石',
'chi_team':'隊伍技能： \n\n'
'水符石兼具心符石效果發動條件：\n'
'以清絮綺羅 ‧ 希作戰友及隊長 \n\n'
'隊伍技能：\n'
'I. 必然延長移動符石時間 3 秒 \n'
'II. 消除 1 組 ≥10 粒水符石\n'
'⇒ 水屬性成員無視「固定連擊盾」 \n\n'
'發動條件： \n'
'以「清絮綺羅 ‧ 希」作戰友及隊長',

'eng_act':'Watery Promise - God\'s Enchantment CD 6 \n\n'
'I. Remove Dark and Heart Runestones to generate Enchanted Water God Runestones. \n'
'For 2 Rounds:\n'
'II. Team Attack x 2.25.\n'
'III. Extend Runestone-moving time to 20 seconds.\n'
'IV. Clear the negative state of Frozen Runestones touched while moving.',
'eng_lead':'Giant Elemental Waves - EX \n\n'
'I. Water Attack x 7; HP & Recovery x 1.6.\n'
'II. The more the groups of Water Runestones dissolved,\n'
'⇒ the higher the Water Attack,\n'
'⇒ to the max x 10 for 3 groups.\n'
'III. Turn 2 random Runestones into Enchanted Water God Runestones at the end of each Round.',
'eng_team':'Team Skill: \n'
'Water Runestones also have the effect of Heart Runestones Activating \n\n'
'Conditions: \n'
'With Qingxu Qiluo·Xi, a comrade and leader \n\n'
'Team Skills: \n'
'I. The time for moving Runestones must be extended by 3 seconds\n'
'II. Dissolve ≥10 Water Runestones from a group\n'
'⇒ Water-type members ignore the\n'
'activation conditions of "Fixed Combo Shield":\n'
'Combat comrades and captains with "Qingxu Kira·Xi" '},
    
    {'chi_name':'希2',
'chif_name':'希2',
'eng_name':'Xi2',

'chi_act':'疾速巨浪 CD6\n\n'
'I. 水符石掉落率提升至 20%\n'
'II. 发动技能及每回合结束时\n'
'⇒ 将水符石转化为水神族符石\n'
'III. 消除水符石愈多\n'
'⇒ 水属性攻击力愈高\n'
'⇒ 消除 10 粒可达至最大 3 倍\n'
'效果持续至没有消除神族符石',
'eng_act':'Enormous Waves - EX CD6\n\n'
'I. Increase the drop rate of Water Runestones to 20%.\n'
'II. Upon Skill activation and at the end of each Round,\n'
'⇒ turn Water Runestones into Water God Runestones.\n'
'III. The more the Water Runestones dissolved,\n'
'⇒ the higher the Water Attack,\n'
'⇒ to the max x 3 for 10 Runestones dissolved.\n'
'The Skill stays in play until no God Runestones are dissolved.',

'chi_lead':'水元素之力 ‧ 强韧之壁\n\n'
'I. 水属性攻击力 7 倍\n'
'II. 减少 50% 所受伤害',
'eng_lead':'Protective Shield of Water Elements\n\n'
'I. Water Attack x 7.\n'
'II. Damage received -50%.',

'chi_team':'没有队伍技能',
'eng_team':'None'},
    
    {'chi_name':'妍1',
'chif_name':'妍1',
'eng_name':'yan1',

'chi_act':'炽热的约定 ‧ 神之加冕 CD6\n\n'
'I. 将移动符石时触碰的首 8 粒符石添加为神族符石\n'
'II. 达成 ≥4 连击 (Combo)\n'
'⓵ 全队攻击力 2 倍\n'
'⓶ 神族无视敌人防御力\n'
'(效果会在关闭此技能或死亡后消失)\n\n'

'此技能可随时关闭，关闭时：\n'
'⓵ 自身技能 CD -2\n'
'⓶ 将自身、队长、战友直行符石\n'
'⇒ 转化为心神族强化符石',
'eng_act':'Fiery Pact - God\'s Enchantment CD6\n\n'
'I. Modify the first 8 Runestones touched while moving to become God Runestones.\n'
'II. When ≥4 Combos are made:\n'
'⓵ Team Attack x 2.\n'
'⓶ God Damage will be dealt regardless of the enemy\'s Defense.\n'
'The Skill stays in play until deactivation or defeated.\n\n'

'This Skill can be deactivated anytime. Upon deactivation of the Skill:\n'
'⓵ The Character\'s Skill CD -2.\n'
'⓶ Turn the columns below the Character, Leader and Ally into Enchanted Heart God Runestones.',

'chi_lead':'熊熊之火 ‧ 烈\n\n'
'I. 火属性攻击力 7 倍、生命力及回复力 1.6 倍\n'
'II. 每回合结束时，将火符石转化为\n'
'⇒ 火神族强化符石',
'eng_lead':'Inextinguishable Fire - EX\n\n'
'I. Fire Attack x 7 ; HP & Recovery x 1.6.\n'
'II. Turn Fire Runestones into Enchanted Fire God Runestones at the end of each Round.',

'chi_team':'队伍技能：\n\n'
'I. 触碰“燃烧”位置\n'
'⇒ 减少 70% 所受伤害\n'
'II. 光、暗、心符石分别兼具\n'
'⇒ 火符石效果\n'
'III. 消除火神族符石时\n'
'⇒ 火属性成员无视“三属盾”、“四属性”、“五属盾”\n'
'发动条件：\n'
'以“烈焰染暮 ‧ 妍”作战友及队长',
'eng_team':'Team Skill:\n\n'
'◆ Damage received from "Burning" -70%.\n'
'◆ Light, Dark and Heart Runestones also possess the effect of Fire Runestones.\n'
'◆ By dissolving Fire God Runestones,\n'
'⇒ Damage of Fire Members will be dealt regardless of Trio Elemental Shield, Quartet Elemental Shield and Quintet Elemental Shield.\n'
'Condition:\n'
'Both the Leader and Ally are "Rhythm of Blazing Flames - Yan".'},
    
    {'chi_name':'妍2',
'chif_name':'妍2',
'eng_name':'yan2',

'chi_act':'绽放之热焰 CD6\n\n'
'I. 木符石掉落率降至 0\n'
'II. 将原有几率增加至\n'
'⇒ 火符石的掉落率\n'
'III. 掉落的火符石\n'
'⇒ 以火神族强化符石代替\n'
'IV. 消除神族符石时\n'
'⇒ 火符石掉落率提升至 40%\n'
'(效果会在再次发动此技能或死亡后消失)\n\n'

'V. 技能关闭时\n'
'⓵ 移除所有符石\n'
'⇒ 掉落神族强化符石',
'eng_act':'Flames of Blossoms - EX CD6\n\n'
'I. Drop rate of Earth Runestones will be transferred to that of Fire Runestones.\n'
'II. Fire Runestones to be dropped will be Enchanted Fire God Runestones.\n'
'III. By dissolving God Runestones,\n'
'⇒ drop rate of Fire Runestones increases to 40%.\n'
'The Skill stays in play until reactivation of the Skill or defeated.\n\n'

'IV. Upon reactivation of the Skill:\n'
'⇒ Remove all Runestones to generate Enchanted God Runestones.',

'chi_lead':'心中的炽焰\n\n'
'I. 火属性攻击力 7 倍\n'
'II. 消除心符石时\n'
'⇒ 火属性攻击力额外 2 倍',
'eng_lead':'Tongues of Flames - EX\n\n'
'I. Fire Attack x 7.\n'
'II. By dissolving Heart Runestones,\n'
'⇒ Fire Attack x 2 additionally.',

'chi_team':'没有队伍技能',
'eng_team':'None'},
    
    {'chi_name':'暗妍希',
     'chif_name':'暗妍希',
     'eng_name':'darkyanxi',
     'chi_act':'神之幻術  CD 5 \n\n'
     'I. 將水符石轉化為光神族強化符石 \n'
     'II. 將火符石轉化為暗神族強化符石 \n'
     'III. 將木符石轉化為心神族強化符石 \n'
     'IV. 1 回合內，神族成員的攻擊 \n'
     '⇒ 無視「攻前盾」 \n'
     '⇒ 無視敵人的防禦力 \n',
     'chi_lead':'夜月之魅 \n\n'
     'I. 神族攻擊力 4.5 倍 \n'
     'II. 隊伍中只有光及暗屬性成員時 \n'
     '⇒ 全隊攻擊力額外 2.5 倍 \n'
     '⇒ 暗及心符石兼具暗符石效果 \n'
     '⇒ 消除強化符石時，減少 20% 所受傷害 \n',
     'chi_team':'隊伍技能 \n'
     'I. 神族成員 \n'
     '⇒「生命力及回復力」基值 1.3 倍 \n'
     'II. 隊長及戰友進場 CD -5 \n'
     'III. 每回合隨機將 1 粒水、火、木、光及暗符石 \n'
     '⇒ 轉化為強化符石 \n\n'
     '發動條件： \n'
     '以「流光祈護 ‧ 妍希」及「瀟灑雅學 ‧ 妍希」作隊長及戰友',
     'eng_act':'God\'s Illusion  CD 5 \n\n'
     'I. Turn Water Runestones into Enchanted Light God Runestones \n'
     'II. Turn Fire Runestones into Enchanted Dark God Runestones \n'
     'III. Turn Wood Runestones into Enchanted Heart God Runestones  \n'
     'IV. For 1 Round, God member\'s attack \n'
     '⇒ Ignore "Front Shield" \n'
     '⇒ Ignore the enemy\'s defense  \n',
     'eng_lead':'Charm of the Night Moon\n\n'
     'I. God Attack x 4.5 \n'
     'II. When there are only Light and Dark attribute members in the team \n'
     '⇒ Team Attack x 2.5 \n'
     '⇒ Dark and Heart Runestones also have the effect of Dark Runestones \n'
     '⇒ When dissolving Enchanted Runestones, the damage suffered is reduced by 20% harm',
     'eng_team':'Team Skills:\n'
     'I. Protoss members \n'
     '⇒ 1.3 times the base value of "Vitality and Recovery" \n'
     'II. Leaders and comrades enter the battlefield CD -5 \n'
     'III. Randomly turn 1Water, Fire, Wood, Light and Dark Runestones\n'
     '⇒ into Enhancing Runestones \n\n'
     'Conditions: \n'
     '"Prayer of Light - Yenxi" and "Nice and Elegant Learning - Yenxi" as the leader and comrade-in-arms \n'},
    
    {'chi_name':'光妍希',
     'chif_name':'光妍希',
     'eng_name':'lightyanxi',
     'chi_act':'神之弓  CD 8 \n\n'
     'I. 神族攻擊力及回復力 1.6 倍 \n'
     'II. 每回合開始時，將光及暗符石 \n'
     '⇒ 轉化為神族強化符石 \n'
     '(效果會在關閉此技能或死亡後消失) \n'
     '技能關閉時 \n'
     'III. 消除所有附加效果 \n'
     '⇒ 每消除 1 個效果 \n'
     '⇒ 神族成員的技能 CD 減少 2 \n'
     'IV. 引爆場上所有符石',
     'chi_lead':'夜月之輝 \n\n'
     'I. 神族攻擊力 4.5 倍 \n'
     'II. 隊伍中只有光及暗屬性成員時 \n'
     '⇒ 全隊攻擊力額外 2.5 倍 \n'
     '⇒ 光及心符石兼具暗符石效果 \n'
     '⇒ 消除強化符石時，減少 20% 所受傷害 \n',
     'chi_team':'隊伍技能 \n'
     'I. 神族成員 \n'
     '⇒「生命力及回復力」基值 1.3 倍 \n'
     'II. 隊長及戰友進場 CD -5 \n'
     'III. 每回合隨機將 1 粒水、火、木、光及暗符石 \n'
     '⇒ 轉化為強化符石 \n\n'
     '發動條件： \n'
     '以「流光祈護 ‧ 妍希」及「瀟灑雅學 ‧ 妍希」作隊長及戰友',
     'eng_act':'God\'s Bow  CD 8 \n\n'
     'I. God\'s attack power and recovery power 1.6 times \n'
     'II. At the beginning of each round, turn Light and Dark Runestones \n'
     '⇒ into God\'s Enchanted Runestones  \n'
     '(the effect will disappear when the skill is turned offor after death) . \n'
     ' III. When the skill is turned off, all additional Effect \n'
     '⇒ For every effect dispelled  \n'
     '⇒ God member\'s skill CD is reduced by 2 IV. Detonate all runestones on the field',
     'eng_lead':'Brightness of the Night Moon\n\n'
     'I. God Attack x 4.5 \n'
     'II. When there are only Light and Dark attribute members in the team \n'
     '⇒ Team Attack x 2.5 \n'
     '⇒ Light and Heart Runestones also have the effect of Dark Runestones \n'
     '⇒ When dissolving Enchanted Runestones, the damage suffered is reduced by 20% harm',
     'eng_team':'Team Skills:\n'
     'I. Protoss members \n'
     '⇒ 1.3 times the base value of "Vitality and Recovery" \n'
     'II. Leaders and comrades enter the battlefield CD -5 \n'
     'III. Randomly turn 1Water, Fire, Wood, Light and Dark Runestones\n'
     '⇒ into Enhancing Runestones \n\n'
     'Conditions: \n'
     '"Prayer of Light - Yenxi" and "Nice and Elegant Learning - Yenxi" as the leader and comrade-in-arms \n'},
    
{'chi_name':'水夏娃',
'chif_name':'水夏娃',
'eng_name':'watereve',
'chi_act':'金果誘毒  CD 6 \n'
'I. 每回合所有“澜漫勾惑 ‧ 夏娃” \n'
'⇒ 增加 1 个金果\n'
'II. 若队长及战友均为“魔性原罪 · 夏娃”时\n'
'⇒ 每回合所有“魔性原罪 · 夏娃”\n'
'增加 1 个禁果\n'
'III. 必延 2 秒\n'
'IV. 魔族成员伤害\n'
'⇒ 可克制水及木属性目标\n'
'V. 若队中有 ≥2 个魔族或水属性成员\n'
'⓵ 连击 (Ex. Combo、Combo)时攻击力提升 40%\n'
'⓶ 回合结束时，将最底 1 横行符石\n'
'⇒ 添加为魔族符石\n'
'(效果会在关闭此技能或死亡后消失)\n\n'
'此技能可随时关闭，关闭时：\n'
'⓵ 自身每有 1 个金果\n'
'⇒ 该回合 + 3 Combo\n'
'(最多 + 12 Combo)\n'
'⓶ 若自身有 4 个金果\n'
'⇒ 该回合所有成员\n'
'⇒ 无视“攻前盾”\n'
'⇒当前技能 CD -2',
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
'chi_act':'元素的音韵 CD7 \n\n'
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
'chi_team':'队伍技能： \n'
'奏响世界之音 ‧ 莎娜”的生命力、攻击力、回复力增加 1000 点 \n\n'
'发动条件： \n'
'以“奏响世界之音 ‧ 莎娜”作成员，且队中只有妖精类成员',
'eng_team':'Team Skill: \n'
'HP, Attack & Recovery of "Resonance of the World - Zana" +1000. \n\n'
'Condition: \n'
'The Team consists of only Elves, with "Resonance of the World - Zana" as a Team Member. '},
    {'chi_name':'巴哈姆特',
'chif_name':'巴哈姆特',
'eng_name':'bahamut',
'chi_act':'龙之逆鳞 CD6 \n\n'
'I. 解除龙类成员被封锁的技能 \n'
'(此技能无视封锁技能) \n'
'1 回合内 \n'
'II. 龙类攻击力 2.5 倍 \n'
'III.“燃烧”敌技的伤害 \n'
'⇒ 转化为我方生命力 \n'
'IV. 消除龙族符石时 \n'
'⇒ 龙类成员的攻击无视“固定连击盾” \n',
'eng_act':'Reverse of Dragon Scales CD6 \n\n'
'I. Release the locked Skills of all Dragons. \n'
'(This Skill will not be locked.) \n'
'For 1 Round: \n'
'II. Dragon Attack x 2.5. \n'
'III. Damage received from Boss Skill "Burning" will be converted to HP. \n'
'IV. By dissolving Dragon Runestones, \n'
'⇒ Damage of Dragons will be dealt regardless of Fixed Combo Shield \n',
'chi_lead':'龙之怒 \n\n'
'龙类攻击力 2 倍 ',
'eng_lead':'Anger of Dragons \n\n'
'Dragon Attack x 2 ',
'chi_team':'队伍技能： \n'
'I. “迷失者的圣炎 ‧ 巴哈姆特” \n'
'⇒ 生命力及攻击力 2 倍 \n'
'⇒ 进入关卡后，技能 CD 减少 6 \n'
'II. “巴哈姆特”以外的龙类成员 \n'
'⇒ 进入关卡后，技能 CD 减少 1 \n\n'
'发动条件： \n'
'以“迷失者的圣炎 ‧ 巴哈姆特”作成员及队伍中只有龙类成员 ',
'eng_team':'Team Skill: \n'
'I. For "Noble Fire of the Lost - Bahamut", \n'
'⇒ HP & Attack x 2 additionally. \n'
'⇒ Active Skill CD -6 after entering a Stage. \n'
'II. For other Dragons, \n'
'⇒ Active Skill CD -1 after entering a Stage. \n\n'
'Condition: \n'
'The Team consists of only Dragons, with "Noble Fire of the Lost - Bahamut" in the Team. '},
    {'chi_name':'贝西摩斯',
'chif_name':'貝西摩斯',
'eng_name':'behemoth',
'chi_act':'深淵領域 CD6 \n\n'
'I. 1 回合內，獸類攻擊力及回復力 2.3 倍 \n'
'II. 隨機將 23 粒符石轉化為 \n'
'⇒「水、火、木」非強化符石各 5 粒 \n'
'⇒「光、暗」非強化符石各 4 粒 \n'
'III. 消除 23 粒或以上符石時 \n'
'⇒ 自身主動技能 CD 減少 5 \n',
'eng_act':'Regions of Pilgrimage CD6 \n\n'
'For 1 Round: \n'
'I. Beast Attack & Recovery x 2.3.\n'
'II. Turn 23 random Runestones into non-Enchanted Runestones of 5 Attributes \n'
'(5 for Water, Fire and Earth; 4 for Light and Dark). \n'
'III. By dissolving ≥23 Runestones, the Character\'s Skill CD -5.',
'chi_lead':'野獸之怒 \n\n'
'獸類攻擊力 2 倍',
'eng_lead':'Anger of Beasts \n\n'
'Beast Attack x 2 ',
'chi_team':'队伍技能： \n'
'I. 「墜落殺戮 ‧ 貝西摩斯」的生命力、攻擊力、回復力 1.5 倍 \n'
'II. 進入關卡後，獸類成員的主動技能 CD 減少 2 \n\n'
'发动条件： \n'
'以「墜落殺戮 ‧ 貝西摩斯」作成員，且隊伍中只有獸類成員',
'extra': 'test only',
'eng_team':'Team Skill: \n'
'I. HP, Attack & Recovery of "Fallen Massacre - Behemoth" x 1.5 additionally.", \n'
'II. After entering a stage, Active Skill CD(s) of Beast(s) -2. \n\n'
'Condition: \n'
'There is "Fallen Massacre - Behemoth" in the Team.\n'
'The Team consists of only Beasts. '}
]


def biodata_extra(x):
 for dict in checker:
  for key in dict:
   if dict[key] == x:
       return dict['extra']
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
    try:
     extra = cd['extra'] = biodata_extra(msg)
    except KeyError:
     pass
    keyboard = [
        [InlineKeyboardButton(' 主动技能', callback_data='chi_act'),
         InlineKeyboardButton('队伍技能', callback_data='chi_lead'),
         InlineKeyboardButton('Translate\nEN', callback_data='translate_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    keyboard2 = [
        [InlineKeyboardButton(' 主动技能', callback_data='chi_act'),
         InlineKeyboardButton('队伍技能', callback_data='chi_lead'),
         InlineKeyboardButton('更多资料', callback_data='extra'),
         InlineKeyboardButton('Translate\nEN', callback_data='translate_en')]
    ]
    reply_markup2 = InlineKeyboardMarkup(keyboard2)

    if extra != None:
       update.message.reply_text(f'<b>{ch_lead}</b>', reply_markup=reply_markup2, parse_mode = ParseMode.HTML)
    return CHECK

    if ch_name == None:
        update.message.reply_text('failed : 角色还没加入资料库')
        return ConversationHandler.END
    if chf_name == None:
        update.message.reply_text('failed : 角色还没加入资料库')
        return ConversationHandler.END
    if en_name == None:
        update.message.reply_text('failed : 角色还没加入资料库')
        return ConversationHandler.END
    if extra == None:
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
