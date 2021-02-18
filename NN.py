#!/usr/bin/env python
# coding: utf-8
import json
import numpy as np
import pandas as pd
import keras
from keras.preprocessing.text import Tokenizer, text_to_word_sequence

del_symbols = '''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n0123456789
😀😃😄😁😆😅😂🤣😇😉😊🙂🙃☺😋😌😍🥰😘😗😙😚🤪😜😝
😛🤑😎🤓🧐🤠🥳🤗🤡😏😶😐😑😒🙄🤨🤔🤫🤭🤥😳😞😟😠😡
🤬😔😕🙁☹😬🥺😣😖😫😩🥱😤😮😱😨😰😯😦😧😢😥😪🤤😓
😭🤩😵🥴😲🤯🤐😷🤕🤒🤮🤢🤧🥵🥶😴💤😈👿👹👺💩👻💀☠
👽🤖🎃😺😸😹😻😼😽🙀😿😾👐🤲🙌👏🙏🤝👍👎👊✊🤛🤜🤞✌
🤘🤟👌🤏👈👉👆👇☝✋🤚🖐🖖👋🤙💪🦾🖕✍🤳💅🦵🦿🦶👄🦷👅👂
🦻👃👁👀🧠🦴👤👥🗣👶👧🧒👦👩🧑👨👩‍🦱🧑‍🦱👨‍🦱👩‍🦰🧑‍🦰👨‍🦰👱‍♀️👱👱‍♂️
👩‍🦳🧑‍🦳👨‍🦳👩‍🦲🧑‍🦲👨‍🦲🧔👵🧓👴👲👳‍♀️👳👳‍♂️🧕👼👸🤴👰🤵‍♀️🤵🤵‍♂️🙇‍♀️
🙇🙇‍♂️💁‍♀️💁💁‍♂️🙅‍♀️🙅🙅‍♂️🙆‍♀️🙆🙆‍♂️🤷‍♀️🤷🤷‍♂️🙋‍♀️🙋🙋‍♂️🤦‍♀️🤦🤦‍♂️🧏‍♀️🧏🧏‍♂️🙎‍♀️🙎🙎‍♂️
🙍‍♀️🙍🙍‍♂️💇‍♀️💇💇‍♂️💆‍♀️💆💆‍♂️🤰🤱🧎‍♀️🧎🧎‍♂️🧍‍♀️🧍🧍‍♂️🚶‍♀️🚶🚶‍♂️👩‍🦯🧑‍🦯👨‍🦯🏃‍♀️🏃🏃‍♂️👩‍🦼🧑‍🦼👨‍🦼
👩‍🦽🧑‍🦽👨‍🦽💃🕺👫🧑‍🤝‍🧑👩‍❤️‍👨💑👩‍❤️‍💋‍👨💏❤🧡💛💚💙💜🤎🖤🤍💔❣💕💞💓💗
💖💘💝💟🐶🐱🐭🐹🐰🐻🧸🐼🐨🐯🦁🐮🐷🐽🐸🐵🙈🙉🙊🐒🦍
🦧🐔🐧🐦🐤🐣🐥🐺🦊🦝🐗🐴🦓🦒🦌🦘🦥🦦🦄🐝🐛🦋🐌🐞🐜🦗
🕷🕸🦂🦟🦠🐢🐍🦎🐙🦑🦞🦀🦐🦪🐠🐟🐡🐬🦈🐳🐋🐊🐆🐅🐃🐂
🐄🐪🐫🦙🐘🦏🦛🐐🐏🐑🐎🐖🦇🐓🦃🕊🦅🦆🦢🦉🦩🦚🦜🐕🦮🐕‍🦺
🐩🐈🐇🐀🐁🐿🦨🦡🦔🐾🐉🐲🦕🦖🌵🎄🌲🌳🌴🌱🌿☘🍀🎍🎋🍃🍂
🍁🌾🌺🌻🌹🥀🌷🌼🌸💐🍄🌰🐚🌎🌍🌏🌕🌖🌗🌘🌑🌒🌓🌔🌙🌚
🌝🌛🌜⭐🌟💫✨☄🪐🌞☀🌤⛅🌥🌦☁🌧⛈🌩⚡🔥💥❄🌨☃⛄🌬💨🌪🌫🌈
☔💧💦🌊🍏🍎🍐🍊🍋🍌🍉🍇🍓🍈🍒🍑🥭🍍🥥🥝🍅🥑🍆🌶🥒🥬🥦
🧄🧅🌽🥕🥗🥔🍠🥜🍯🍞🥐🥖🥨🥯🥞🧇🧀🍗🍖🥩🍤🥚🍳🥓🍔🍟
🌭🍕🍝🥪🌮🌯🥙🧆🍜🥘🍲🥫🧂🧈🍥🍣🍱🍛🍙🍚🍘🥟🍢🍡🍧🍨🍦
🍰🎂🧁🥧🍮🍭🍬🍫🍿🍩🍪🥠🥮☕🍵🥣🍼🥤🧃🧉🥛🍺🍻🍷🥂🥃🍸🍹
🍾🍶🧊🥄🍴🍽🥢🥡⚽🏀🏈⚾🥎🎾🏐🏉🎱🥏🏓🏸🥅🏒🏑🏏🥍🥌
⛳🏹🎣🤿🥊🥋⛸🎿🛷⛷🏂🏋️‍♀️🏋🏋️‍♂️🤺🤼‍♀️🤼🤼‍♂️🤸‍♀️🤸🤸‍♂️⛹️‍♀️⛹⛹️‍♂️🤾‍♀️🤾🤾‍♂️
🧗‍♀️🧗🧗‍♂️🏌️‍♀️🏌🏌️‍♂️🧘‍♀️🧘🧘‍♂️🧖‍♀️🧖🧖‍♂️🏄‍♀️🏄🏄‍♂️🏊‍♀️🏊🏊‍♂️🤽‍♀️🤽🤽‍♂️🚣‍♀️🚣🚣‍♂️🏇🚴‍♀️🚴
🚴‍♂️🚵‍♀️🚵🚵‍♂️🎽🎖🏅🥇🥈🥉🏆🏵🎗🎫🎟🎪🤹‍♀️🤹🤹‍♂️🎭🎨🎬🎤🎧🎼🎹🥁🎷
🎺🎸🪕🎻🎲🧩♟🎯🎳🪀🪁🎮👾🎰👮‍♀️👮👮‍♂️👩‍🚒🧑‍🚒👨‍🚒👷‍♀️👷👷‍♂️👩‍🏭🧑‍🏭👨‍🏭
👩‍🔧🧑‍🔧👨‍🔧👩‍🌾🧑‍🌾👨‍🌾👩‍🍳🧑‍🍳👨‍🍳👩‍🎤🧑‍🎤👨‍🎤👩‍🎨🧑‍🎨👨‍🎨👩‍🏫🧑‍🏫👨‍🏫👩‍🎓🧑‍🎓
👨‍🎓👩‍💼🧑‍💼👨‍💼👩‍💻🧑‍💻👨‍💻👩‍🔬🧑‍🔬👨‍🔬👩‍🚀🧑‍🚀👨‍🚀👩‍⚕️🧑‍⚕️👨‍⚕️👩‍⚖️🧑‍⚖️👨‍⚖️👩‍✈️🧑‍✈️
👨‍✈️💂‍♀️💂💂‍♂️🕵️‍♀️🕵🕵️‍♂️🤶🎅🕴️‍♀️🕴🕴️‍♂️🦸‍♀️🦸🦸‍♂️🦹‍♀️🦹🦹‍♂️🧙‍♀️🧙🧙‍♂️🧝‍♀️🧝🧝‍♂️🧚‍♀️🧚🧚‍♂️🧞‍♀️
🧞🧞‍♂️🧜‍♀️🧜🧜‍♂️🧛‍♀️🧛🧛‍♂️🧟‍♀️🧟🧟‍♂️👯‍♀️👯👯‍♂️👪👨‍👩‍👧👨‍👩‍👧‍👦👨‍👩‍👦‍👦👨‍👩‍👧‍👧👩‍👦👩‍👧👩‍👧‍👦👩‍👦‍👦👩‍👧‍👧👨‍👦👨‍👧
👨‍👧‍👦👨‍👦‍👦👨‍👧‍👧🚗🚙🚕🛺🚌🚎🏎🚓🚑🚒🚐🚚🚛🚜🏍🛵🚲🦼🦽🛴🛹🚨🚔
🚍🚘🚖🚡🚠🚟🚃🚋🚝🚄🚅🚈🚞🚂🚆🚇🚊🚉🚁🛩✈🛫🛬🪂💺🛰🚀
🛸🛶⛵🛥🚤⛴🛳🚢⚓⛽🚧🚏🚦🚥🛑🎡🎢🎠🏗🌁🗼🏭⛲🎑⛰🏔🗻🌋
🗾🏕⛺🏞🛣🛤🌅🌄🏜🏖🏝🌇🌆🏙🌃🌉🌌🌠🎇🎆🏘🏰🏯🏟🗽🏠🏡🏚🏢
🏬🏣🏤🏥🏦🏨🏪🏫🏩💒🏛⛪🕌🛕🕍🕋⛩⌚📱📲💻⌨🖥🖨🖱🖲🕹🗜💽
💾💿📀📼📷📸📹🎥📽🎞📞☎📟📠📺📻🎙🎚🎛⏱⏲⏰🕰⏳⌛🧮📡🔋🔌💡
🔦🕯🧯🗑🛢🛒💸💵💴💶💷💰💳🧾💎⚖🦯🧰🔧🔨⚒🛠⛏🪓🔩⚙⛓🧱🔫🧨
💣🔪🗡⚔🛡🚬⚰⚱🏺🔮📿🧿💈🧲⚗🧪🧫🧬🔭🔬🕳💊💉🩸🩹🩺🌡🏷🔖🚽
🚿🛁🛀🪒🧴🧻🧼🧽🧹🧺🔑🗝🛋🪑🛌🛏🚪🧳🛎🖼🧭🗺⛱🗿🛍🎈🎏🎀🧧
🎁🎊🎉🎎🎐🏮🪔✉📩📨📧💌📮📪📫📬📭📦📯📥📤📜📃📑📊📈📉
📄📅📆🗓📇🗃🗳🗄📋🗒📁📂🗂🗞📰📓📕📗📘📙📔📒📚📖🔗📎🖇✂📐📏📌
📍🧷🧵🧶🔐🔒🔓🔏🖊🖋✒📝✏🖍🖌🔍🔎👚👕🥼🦺🧥👖👔👗👘🥻🩱👙🩲
🩳💄💋👣🧦👠👡👢🥿👞👟🩰🥾🧢👒🎩🎓👑⛑🎒👝👛👜💼👓🕶🥽
🧣🧤💍🌂☂☮✝☪🕉☸✡🔯🕎☯☦🛐⛎♈♉♊♋♌♍♎♏♐♑♒♓🆔
⚛⚕☢☣📴📳🈶🈚🈸🈺🈷✴🆚🉑💮🉐㊙㊗🈴🈵🈹🈲🅰🅱🆎🆑🅾🆘⛔
📛🚫❌⭕💢♨🚷🚯🚳🚱🔞📵🚭❗❕❓❔‼⁉💯🔅🔆🔱⚜〽⚠🚸🔰♻🈯💹
❇✳❎✅💠🌀➿🌐♾Ⓜ🏧🚾♿🅿🈳🈂🛂🛃🛄🛅🚰🚹♂🚺♀⚧🚼🚻🚮🎦
📶🈁🆖🆗🆙🆒🆕🆓0⃣1⃣2⃣3⃣4⃣5⃣6⃣7⃣8⃣9⃣🔟🔢▶⏸⏯⏹⏺⏏⏭⏮
⏩⏪🔀🔁🔂◀🔼🔽⏫⏬➡⬅⬆⬇↗↘↙↖↕↔🔄↪↩🔃⤴⤵#⃣*⃣ℹ🔤🔡🔠🔣
🎵🎶〰➰✔➕➖➗✖💲💱©®™🔚🔙🔛🔝🔜☑🔘🔴🟠🟡🟢🔵🟣🟤⚫
⚪🟥🟧🟨🟩🟦🟪🟫⬛⬜◼◻◾◽▪▫🔸🔹🔶🔷🔺🔻🔲🔳🔈🔉🔊🔇📣
📢🔔🔕🃏🀄♠♣♥♦🎴👁‍🗨🗨💭🗯💬🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕜🕝
🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧'''


with open(r'save_models\input_word_index.json', 'r') as f:
    input_word_index = json.load(f)
input_index_word = dict(zip(input_word_index.values(), input_word_index.keys()))
    
with open(r'save_models\output_word_index.json', 'r') as f:
    output_word_index = json.load(f)
output_index_word = dict(zip(output_word_index.values(), output_word_index.keys()))

input_vocabulary = np.load(r'save_models\input_vocab.npy')
output_vocabulary = np.load(r'save_models\output_vocab.npy')

input_model = keras.models.load_model(r'save_models\input_model.h5')
encoder_model = keras.models.load_model(r'save_models\encoder_model.h5', compile=False)
decoder_model = keras.models.load_model(r'save_models\decoder_model.h5', compile=False)

input_vocab_size = len(input_vocabulary)
output_vocab_size = len(output_vocabulary)

start_token = '\t'
stop_token = '\n'

max_encoder_seq_lenght = 11
max_decoder_seq_lenght = 13

def decode_sequence(input_seq):
    thought = encoder_model.predict(input_seq)#генерируем вектор идеи(входной сигнал)
    
    output_seq = np.zeros((1, 1, output_vocab_size))
    output_seq[0, 0, output_word_index[start_token]] = 1# задаем начала для декодировщика
    
    stop_condition = False
    generated_sequence = ''
    
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
        [output_seq] + thought)
        
        generated_token_idx = np.argmax(output_tokens[0, -1, :])
        generated_word = output_index_word[generated_token_idx]
        generated_sequence += generated_word + ' '
        
        if(generated_word == stop_token or 
           len(generated_sequence) > max_decoder_seq_lenght):
            stop_condition = True
 
        output_seq = np.zeros((1,1, output_vocab_size))
        output_seq[0, 0,  generated_token_idx] += 1
        thought = [h, c]
    return generated_sequence

def word_find(word, dictionary):
    """поиск максимально похожего слова"""
    g = []
    for word_true in dictionary:
        word_table = np.zeros((len(word_true), len(word)))
        for num_i, i in enumerate(word_true):
            for num_j, j in enumerate (word):
                if i==j:
                    word_table[num_i][num_j] = 1+ word_table[num_i-1][num_j-1]
        time = np.sum(word_table)/((len(word_true)+len(word))/2)
        g.append(time)
        arg = np.argmax(g)
        
    return input_vocabulary[arg], arg 

def response(input_text):
    input_seq = np.zeros((1, max_encoder_seq_lenght, input_vocab_size), dtype=np.float32)
    text = text_to_word_sequence(input_text, filters = del_symbols)

    for t, word in enumerate(text):
        try:
            input_seq[0, t, input_word_index[word]] += 1
        except KeyError:
            o, num = word_find(word, input_word_index)
            print(o, num, input_word_index[o])
            input_seq[0, t, num] += 1
            
    decoded_sentence = decode_sequence(input_seq)
    return decoded_sentence

if __name__ == '__main__':
    response('привет')