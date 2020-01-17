#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/3 8:37 PM
# @Author  : Slade
# @File    : Rake.py

import re
import jieba


def separate_sentence(text):
    '''
    :param text: 待切分文本
    :return: list
    '''
    splitter = re.compile("[^\u4e00-\u9fa5a-z0-9,.!?，。？！；;~～……、]")
    words = []
    text = splitter.sub("", str(text))
    for single_word in re.split('[",", ".", "?", "!", "~", ";", "，", "。", "？", "！", "～", "；", "……", "、"]', text):
        current_word = single_word.strip()
        if current_word != '' and not current_word.isdigit():
            words.append(current_word)
    return words


def separate_word(text, min_word_return_size, stop_word):
    text = jieba.lcut(text)
    text = [w for w in text if w not in stop_word]
    words = []
    for single_word in text:
        if len(single_word) >= min_word_return_size and not single_word.isdigit():
            words.append(single_word)
    return words


def calculate_word_scores(phraseList, min_word_return_size=2, max_freq=5):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_word(phrase, min_word_return_size, {})
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1

        # 平衡高频词
        word_list_degree = min(word_list_degree, max_freq)

        for word in word_list:
            # 词频
            word_frequency[word] = word_frequency.get(word, 0) + 1
            # 共现
            word_degree[word] = word_degree.get(word, 0) + word_list_degree

    for item in word_frequency:
        # 度
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  # orig.

    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score, min_word_return_size=2, top_x=1 / 3):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_word(phrase, min_word_return_size, {})
        candidate_score = 0
        if len(word_list) == 0:
            continue
        for word in word_list:
            candidate_score += word_score[word]
        # 平衡长文本的影响
        keyword_candidates[phrase] = candidate_score / len(word_list)
        # keyword_candidates[phrase] = candidate_score

    # 排序前top_x句子
    keyword_candidates = sorted(keyword_candidates.items(), key=lambda x: x[1], reverse=True)[
                         :int(max(top_x, 0.01) * len(keyword_candidates))]
    return keyword_candidates


if __name__ == '__main__':
    article = "醒来的时候，眼前是一片雪白的，凭借眼前那盏熟悉的灰白色的吊灯，我才反应过来，原来我在房间里。盖在身上的被子虽然厚重，但是还是感觉身体凉丝丝的。 轻轻一闻枕头上淡淡的薰衣草香，便想起他的发香，我将脸埋进枕头里，用力地呼吸着。 “阳，阳？阿阳……” 我感觉异常的口渴，喉咙干涩，难以发声，我轻声叫着他的名字，房间的门却迟迟没有被打开。 我掀开被子下了床，脚触及地面的那一刻我感觉骨头和肌肉有些疼痛，我身上仅有的一丝暖意瞬间被冰冷的地板抽走。低下头一看，我穿着蓝白色条纹相间病号服，左胸口还有红十字标志的刺绣。我皱了皱眉头，“哪来的病号服，阿阳可不喜欢我穿这身衣服去见他呢。” 我打开衣柜，找到了第一次和阿阳见面时的那件白色连衣裙，用木质衣架挂着，上面还有透明的防尘罩，它被挂在衣柜安静的角落里。裙身拼接着网纱，领口还有一圈蕾丝当点缀。记得他说过我穿着这身连衣裙的时候，特别像上帝派至人间的天使。 我脱下那身讨厌的病号服，换上了这件白色连衣裙，心情也好了五分，等会见到阿阳，便会有十分的好心情了。 2 打开房间门的一瞬间，我被照进来的阳光晃到眼睛，愣了几秒才回过神。 “阳，阳？阿阳……” 他不在客厅，也不在厨房。我在餐桌上找着和阿阳的情侣杯，准备倒口水喝，发现那对杯子上都是裂痕，有些部分被强制地用胶水沾在一起，而有些部分缺少，留下空白。 我有些疑惑，猜测着也许是阿阳洗杯子的时候不小心打碎了杯子，等会他出现的时候还会带有一个赔礼呢，然后我装作很生气，他就会哄着我求我原谅。想到他脑袋埋在我胸口的委屈撒娇的样子，我捂着嘴都笑出了声。 我找了一只玻璃杯，倒入凉白开，举头一饮而尽。搁下杯子的时候，我看到我和阳两个人做饭时用的围裙，它们被挂在椅背上。我想到周末在家时，我们时常一起做饭，他厨艺精湛，会煎牛排，还会做刺身拼盘。而我在旁边切水果，用榨汁机准备果汁，烤箱里正烤着美味的戚风蛋糕，甜丝丝的气味融入这幸福的空气里，缠绵在我与阳的唇边。 这些时光如同影片般在我脑海中慢慢放映，身体一下子放松下来，陷入沙发里，软绵绵的。 3 观望着外面的天有些阴沉，3月的天总是这样，阴晴不定。我提上伞。锁了门。 其实我很讨厌下雨天，从小便如此。雨天总会让我心情烦躁，有时更加是控制不住自己的情绪，想要发泄。雨点打在身上，衣服会变得湿漉漉的，还和皮肤黏在一起；走路稍微快一点，脚底的雨水便会夹杂着泥土侵蚀我的小腿，把身上都溅满大大小小的泥点；如果再倒霉一些，踩到路边不平整的地砖，地砖下的积水会瞬间以最快的速度扑到裤子上……这些不都是很讨厌的事情吗，所以，我才不喜欢雨天。 可是今天，我很想见到阳。 一路的小心翼翼，就怕雨水和泥弄脏了我的裙子。我来到他公司楼下，抬头看到大摆钟上已经六点过十分钟，我猜测着，阳已经在搭乘电梯的途中，出公司门时肯定提着他深灰色的公文包，拖着沉重的身子去开车。但是见到了我，阳的心情一定会瞬间变好，他一定会奔向我，将我抱起旋转几圈。 想着想着，就看到了稀疏人群里的他。果然不出我所料，阳提着他深灰色的公文包，撑着黑色的伞。因为疲惫，步伐显得沉重。只是……我怎么感觉阳的双眼那么无神呢，眼眶还有些红肿。他也没有抬头寻我，径直进了车，我慌忙追上去，“阳，阳，阿阳！” 4 也许他没注意听，在他发车时，我赶忙坐上了副驾驶。 车子里压抑的气息，让我呼吸困难。也许阳遇到了不顺心的事，比如上司对他的策划提出了意见，然而阳就是那么一个高傲但是又优秀的人，他不允许有谁对他辛劳很久的策划提出异议，也许这也是公司大老板青睐他的地方。 雨点用力地打在车玻璃上，雨刮器以最快的速度将它们刮去。我侧过脸望向他，他不说话，手握着方向盘，望着前方。 他的头发有些凌乱，领结也没有打正，衬衫的袖扣也没有扣上。阳这是怎么了，我很想问问他，但是这阴雨天和车内的压抑扼制着我的声带。 下车后，我随于他身后，进入房子。他丢下公文包和外套，也将自己丢在沙发上，他闭上双眼，劳累已经将他的精神抽走了。我倒了一杯温水放在大理石的茶几上。再看他时，他微闭着双眼，无神的看向天花板。 突然他嘴角上扬了一点弧度，然后起身走向厨房。打开冰箱门取出了一些蔬菜和两包速冻牛排。我眼睛一亮，看来阳想做好吃的给我啊！他围上了那条挂在椅背上的围裙，我偷笑。站在他身后，看着他宽阔的肩膀却虚弱的背影，我上前想环抱住他的腰，手臂却使不上力气。 留他在厨房熟练地操作，我就坐在餐桌边等候了。这种等待的时刻是幸福的。 5 餐桌两头摆好了刀叉，一份牛排也以最精致的造型呈现在我眼前，甚至还有高脚杯和蜡烛。他取出一瓶昂贵的未开封的红酒，倒入我和他的杯中，看来今天的晚餐很独特啊。 夜幕降临，房间里没有开灯，蜡烛已经点上，小火焰轻盈地跃动。 再见他时，他换上了干净的西装，整理好了衬衫和领结，坐于我对面的椅子上。 他举起高脚杯，轻轻晃动，朝我举杯。我笑着回敬，抿了一口放下。其实我和阳都不常喝酒，不喜欢酒精刺激喉咙和胃的感觉，却偏爱以红酒助兴。 烛光的映衬下，他脸上的轮廓更加鲜明，望向我的眼神越发宠溺。 “思思，今天的你，好美。” “思思，你等这一天，已经等很久了吧？” “什么？” 我有些紧张，紧张地猜测接下来可能会发生的事情，也许是我一直期待的。我感觉自己的脸颊发烫。 阳从西装口袋里取出了一个黑色盒子，这黒缎子的盒子在他的手心里安静地躺着。我不是在做梦吧，我一直期待的事情，真的要发生了么。 6 他用另一只手轻轻地打开了首饰盒，一枚精致的戒指摆在里面。戒指上的钻石十分符合阳的品味，他不喜欢太过张扬，也不爱平淡无奇。钻石在烛光下左右闪烁，这跳动的光如同黑暗里的希望，如同森林中的精灵。 他将戒指取出，望向我，满眸深情，“思思……嫁给我吧。” 我激动地抹去眼眶里的泪水，回答道：“阳，我愿意！”我伸出左手，期待阳为我戴上。 而我再望向他时……他是我从未见过的阳。他眼中充盈了泪水，眼眶红肿，肩膀因抽噎着抖动，泪珠滚落在桌布上，晕成一朵花…… “阳，你怎么了，阿阳！” 我慌张地伸出手想拭去他的泪水，然而我怎么都无法触碰到他的脸。我也跟着流泪。“阳，不要哭了，我心好痛。” “思思，如果你还在该多好……今天……是3月4日，我们在一起十年的日子，你应该戴上它的日子啊。”他哽咽着，手中紧紧地攥着那枚戒指，仿佛这戒指要陷入他的皮肤里。 “我？‘我还在’？”我扭头望向墙壁，烛光映衬，却没有我的影子。墙壁上只有阿阳的影子，形单影只。 7 额，头好痛。我扶住脑袋，感觉一阵眩晕。 …… “苏亦阳！你就是不把我的事放心上，天天处理你那公司的破事，知道明天是什么日子吗！” “不知道，但是你能不能冷静一点，我很讨厌你这个样子。”苏亦阳目不转睛地看着电脑的文件，拖动着鼠标。 “好，不知道是吧？”夏可思将电脑强制关机，推掉了桌上的键盘和鼠标。苏亦阳拽过夏可思的手臂，她用力地挣脱开，跑向厨房。 明天，也就是3月4日，是夏可思和苏亦阳在一起十年的日子，因为苏亦阳的回答，加上3月的阴晴不定的天气，夏可思失去了原本的理智，她感觉失望和心痛。十年啊，不是一天两天的时光，怎么能说不记得就不记得。 等苏亦阳赶到厨房，地上桌上一片狼藉，那对情侣杯也被摔的面目全非。夏可思蹲在墙角，抱住腿，脸埋入臂弯中，肩膀随着她的抽泣抖动着。 “思思，我们各自冷静一下吧。” “好啊，那就各自冷静冷静。”充满讽刺的语气，说完，夏可思起身出门。 因为苏亦阳接到公司大项目的任务，他期待将它做的完美。而他怎么可能不知道明天是什么日子，每次夏可思一生气，就喜欢摔东西，那对用了好久的情侣杯今日也没能幸免。他蹲下身小心地将碎片拾起。他突然意识到，外面可能下着雨，思思最讨厌雨天了。他带着伞追出门。 夏可思一路狂奔，她不知道她要去哪，她的希望落空，得到更多的是绝望。雨水和泪水淹没了她的视线，“好讨厌啊，还下着雨呢。”夏可思苦笑着用手臂拭去眼泪。 8 “思思！” 她听到了苏亦阳的声音，她不回头，加快速度往前跑。在十字路口，绿灯已经在闪烁，夏可思想以最快的速度跑到人行横道的另一头，顾不上背后的被泥水溅脏的衣服。 就在夏可思跑到人行横道中间，绿灯停止闪烁，红灯亮起。一辆货车没有减速地开过来，货车的雨刮器处于罢工状态，夏可思就这样藏在了司机的视线死角里。 那一刻，夏可思脑袋一片空白，她看见一朵血红色的花在她胸口绽开。她还看到了苏亦阳，他在奔向自己，他嘴里好像在喊着自己的名字，她已经听不到了。夏可思闭上眼睛，剩下那朵绚烂的红花在继续绽放。 …… “我，已经死了吗，为什么我还在这。我成了缚地灵吗，因生前还有未完成的心愿而无法升天……” “思思，如果那天我不那么在意工作，如果那天在你跑出门前就抱住你与你和好，如果那天……如果那天……”他自言自语着，我从未见过阳这般撕心裂肺痛哭的模样。 “我明白，阳，十年余一日，来世再补还予你。” 那枚戒指默默地闪烁着，我看着我逐渐透明的手指，感受到身体开始变得轻盈…… 第二天，苏亦阳艰难地睁开他那红肿的双眼，他看到枕边卧着一只白猫，那是不带一丝杂色的纯白色，如同天使翅膀的纯白，如同夏可思穿上那件白色连衣裙一样的纯白。他注意到白猫的脖子上挂着的，是那枚应该戴在夏可思手指上的戒指。"
    phrase_list = separate_sentence(article)
    word_score = calculate_word_scores(phrase_list)
    keywords = generate_candidate_keyword_scores(phrase_list, word_score)
    print(keywords)