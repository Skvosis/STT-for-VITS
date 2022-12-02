import json


pinyin_dict = {}
symbol = '\u8352'

pinyin_dict['a']=[]
for i in range(5):
    pinyin_dict['a'].append(symbol)
    symbol+=1


print(pinyin_dict)